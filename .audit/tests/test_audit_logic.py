"""Unit tests for logic extracted from .audit/ processing scripts.

These tests cover the core pure-logic branches in classify.py, gen_trailer.py,
parse_sarif.py, and summarize_al.py — none of which had prior test coverage.
No production files are modified; the functions under test are inlined here
to enable isolated testing without file I/O.
"""

import hashlib
import os
import pytest


# ── classify.py ── our_severity() ─────────────────────────────────────────────

def our_severity(f):
    """Verbatim copy of our_severity() from classify.py."""
    level = f["level"]
    conf = f.get("confidence", "").lower()
    if level == "error" and conf == "high":
        return "Critical"
    if level == "error":
        return "High"
    if level == "warning" and conf == "high":
        return "High"
    if level == "warning":
        return "Medium"
    return "Low"


class TestOurSeverity:
    def test_error_high_confidence_is_critical(self):
        assert our_severity({"level": "error", "confidence": "high"}) == "Critical"

    def test_error_medium_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": "medium"}) == "High"

    def test_error_low_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": "low"}) == "High"

    def test_error_empty_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": ""}) == "High"

    def test_error_missing_confidence_key_is_high(self):
        assert our_severity({"level": "error"}) == "High"

    def test_warning_high_confidence_is_high(self):
        assert our_severity({"level": "warning", "confidence": "high"}) == "High"

    def test_warning_low_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": "low"}) == "Medium"

    def test_warning_empty_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": ""}) == "Medium"

    def test_warning_missing_confidence_key_is_medium(self):
        assert our_severity({"level": "warning"}) == "Medium"

    def test_note_level_is_low(self):
        assert our_severity({"level": "note"}) == "Low"

    def test_unknown_level_is_low(self):
        assert our_severity({"level": "none"}) == "Low"

    def test_confidence_comparison_is_case_insensitive(self):
        # Stored in all-caps from some zizmor versions
        assert our_severity({"level": "error", "confidence": "HIGH"}) == "Critical"
        assert our_severity({"level": "warning", "confidence": "HIGH"}) == "High"


# ── gen_trailer.py ── fp() fingerprint generation ─────────────────────────────

def fp(rule, fname, step):
    """Verbatim copy of fp() from gen_trailer.py."""
    def base(p):
        return os.path.basename(p)
    s = f"{rule}|{base(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestFingerprint:
    def test_returns_16_hex_chars(self):
        result = fp("unpinned-uses", "aeon.yml", "Setup Node")
        assert len(result) == 16
        assert all(c in "0123456789abcdef" for c in result)

    def test_deterministic(self):
        a = fp("template-injection", ".github/workflows/aeon.yml", "Run step")
        b = fp("template-injection", ".github/workflows/aeon.yml", "Run step")
        assert a == b

    def test_spaces_in_step_become_underscores(self):
        with_spaces = fp("rule", "file.yml", "Setup Node")
        with_underscores = fp("rule", "file.yml", "Setup_Node")
        assert with_spaces == with_underscores

    def test_only_basename_of_fname_used(self):
        short = fp("rule", "aeon.yml", "step")
        long_path = fp("rule", ".github/workflows/aeon.yml", "step")
        assert short == long_path

    def test_different_rules_produce_different_fps(self):
        a = fp("rule-a", "aeon.yml", "step")
        b = fp("rule-b", "aeon.yml", "step")
        assert a != b

    def test_different_files_produce_different_fps(self):
        a = fp("rule", "aeon.yml", "step")
        b = fp("rule", "other.yml", "step")
        assert a != b

    def test_different_steps_produce_different_fps(self):
        a = fp("rule", "aeon.yml", "Step A")
        b = fp("rule", "aeon.yml", "Step B")
        assert a != b


# ── parse_sarif.py ── SARIF parsing logic ─────────────────────────────────────

def parse_sarif_finding(result, rules=None):
    """Core extraction logic from parse_sarif.py for a single SARIF result."""
    rules = rules or {}
    rule_id = result.get("ruleId", "?")
    level = result.get("level", "note")
    message = result.get("message", {}).get("text", "")
    props = result.get("properties", {})
    sev = (
        props.get("problem.severity")
        or props.get("zizmor/severity")
        or props.get("security-severity", "")
    )
    conf = props.get("zizmor/confidence", "")
    locs = result.get("locations", [])
    if locs:
        phys = locs[0].get("physicalLocation", {})
        uri = phys.get("artifactLocation", {}).get("uri", "")
        region = phys.get("region", {})
        line = region.get("startLine", 0)
        snippet = region.get("snippet", {}).get("text", "")
    else:
        uri = ""
        line = 0
        snippet = ""
    return {
        "rule_id": rule_id,
        "level": level,
        "severity_zizmor": sev,
        "confidence": conf,
        "message": message,
        "file": uri,
        "line": line,
        "snippet": snippet[:200],
    }


class TestParseSarifFinding:
    def test_empty_locations_yields_zero_line_and_empty_uri(self):
        result = {"ruleId": "some-rule", "level": "warning", "locations": []}
        parsed = parse_sarif_finding(result)
        assert parsed["file"] == ""
        assert parsed["line"] == 0
        assert parsed["snippet"] == ""

    def test_missing_locations_key_yields_defaults(self):
        result = {"ruleId": "some-rule", "level": "error"}
        parsed = parse_sarif_finding(result)
        assert parsed["file"] == ""
        assert parsed["line"] == 0

    def test_location_extracts_uri_and_line(self):
        result = {
            "ruleId": "template-injection",
            "level": "error",
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": ".github/workflows/aeon.yml"},
                    "region": {"startLine": 42, "snippet": {"text": "run: echo ${{ inputs.name }}"}},
                }
            }],
        }
        parsed = parse_sarif_finding(result)
        assert parsed["file"] == ".github/workflows/aeon.yml"
        assert parsed["line"] == 42
        assert parsed["snippet"] == "run: echo ${{ inputs.name }}"

    def test_snippet_truncated_to_200_chars(self):
        long_text = "x" * 300
        result = {
            "ruleId": "r",
            "level": "note",
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": "f.yml"},
                    "region": {"startLine": 1, "snippet": {"text": long_text}},
                }
            }],
        }
        parsed = parse_sarif_finding(result)
        assert len(parsed["snippet"]) == 200

    def test_severity_property_priority_problem_dot_severity_wins(self):
        result = {
            "ruleId": "r",
            "level": "warning",
            "properties": {
                "problem.severity": "high",
                "zizmor/severity": "medium",
                "security-severity": "low",
            },
        }
        parsed = parse_sarif_finding(result)
        assert parsed["severity_zizmor"] == "high"

    def test_severity_falls_back_to_zizmor_severity(self):
        result = {
            "ruleId": "r",
            "level": "warning",
            "properties": {
                "zizmor/severity": "medium",
                "security-severity": "low",
            },
        }
        parsed = parse_sarif_finding(result)
        assert parsed["severity_zizmor"] == "medium"

    def test_severity_falls_back_to_security_severity(self):
        result = {
            "ruleId": "r",
            "level": "warning",
            "properties": {"security-severity": "low"},
        }
        parsed = parse_sarif_finding(result)
        assert parsed["severity_zizmor"] == "low"

    def test_missing_rule_id_defaults_to_question_mark(self):
        result = {"level": "note"}
        parsed = parse_sarif_finding(result)
        assert parsed["rule_id"] == "?"

    def test_missing_level_defaults_to_note(self):
        result = {"ruleId": "r"}
        parsed = parse_sarif_finding(result)
        assert parsed["level"] == "note"


# ── summarize_al.py ── ShellCheck code extraction ─────────────────────────────

KNOWN_CODES = ["SC2086", "SC2046", "SC2129", "SC2153", "SC2155", "SC2034"]


def classify_actionlint_message(msg):
    """Logic from summarize_al.py: first matching code wins; else 'other'."""
    for code in KNOWN_CODES:
        if code in msg:
            return code
    return "other"


def is_high_candidate(finding):
    """Logic from summarize_al.py HIGH-CANDIDATE detection."""
    msg = finding.get("message", "")
    return ("SC2086" in msg or "SC2046" in msg) and "github." in msg.lower()


class TestClassifyActionlintMessage:
    def test_sc2086_detected(self):
        assert classify_actionlint_message("SC2086: Double-quote $VAR") == "SC2086"

    def test_sc2046_detected(self):
        assert classify_actionlint_message("SC2046: quote expansion") == "SC2046"

    def test_first_match_wins_over_later_code(self):
        # SC2086 appears before SC2046 in KNOWN_CODES
        assert classify_actionlint_message("SC2086 and SC2046 both here") == "SC2086"

    def test_unknown_code_becomes_other(self):
        assert classify_actionlint_message("SC9999: unknown warning") == "other"

    def test_empty_message_becomes_other(self):
        assert classify_actionlint_message("") == "other"

    def test_sc2034_detected(self):
        assert classify_actionlint_message("SC2034: unused variable") == "SC2034"


class TestHighCandidateDetection:
    def test_sc2086_with_github_ref_is_high_candidate(self):
        f = {"message": "SC2086: variable ${{ github.event.inputs.ref }} unquoted"}
        assert is_high_candidate(f) is True

    def test_sc2046_with_github_ref_is_high_candidate(self):
        f = {"message": "SC2046: $(github.run_id) word-splitting risk"}
        assert is_high_candidate(f) is True

    def test_sc2086_without_github_is_not_high_candidate(self):
        f = {"message": "SC2086: Double-quote $VAR to prevent globbing"}
        assert is_high_candidate(f) is False

    def test_github_without_injection_code_is_not_high_candidate(self):
        f = {"message": "github.token used in env block"}
        assert is_high_candidate(f) is False

    def test_empty_message_is_not_high_candidate(self):
        assert is_high_candidate({}) is False

    def test_github_detection_is_case_insensitive(self):
        f = {"message": "SC2086: GITHUB.event.inputs.name unquoted"}
        assert is_high_candidate(f) is True
