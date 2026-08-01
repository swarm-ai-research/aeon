"""
Unit tests for audit pipeline pure functions.

Run with: python -m pytest .audit/test_audit.py  or  python .audit/test_audit.py

These tests do NOT require any SARIF / JSON files — they exercise the logic
extracted from classify.py, delta.py, and parse_sarif.py directly.
"""

import hashlib
import os
import re
import unittest


# ---------------------------------------------------------------------------
# Logic extracted from classify.py
# ---------------------------------------------------------------------------

def our_severity(f):
    """Severity mapping from classify.py."""
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


def make_fingerprint(short_rule, file_uri, snippet):
    """Fingerprint logic from classify.py."""
    snip_key = re.sub(r"\s+", " ", snippet)[:60]
    file_short = os.path.basename(file_uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Logic extracted from delta.py
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    """Fingerprint for delta matching from delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def is_individual_fp(key):
    """Return True if key looks like a 16-char hex fingerprint, not an aggregate rule name."""
    return len(key) == 16 and all(c in "0123456789abcdef" for c in key)


# ---------------------------------------------------------------------------
# Logic extracted from parse_sarif.py (finding extraction)
# ---------------------------------------------------------------------------

def extract_findings(sarif_data):
    """Extract findings list from a SARIF dict (mirrors parse_sarif.py logic)."""
    runs = sarif_data.get("runs", [])
    all_findings = []
    for run in runs:
        for r in run.get("results", []):
            rule_id = r.get("ruleId", "?")
            level = r.get("level", "note")
            message = r.get("message", {}).get("text", "")
            props = r.get("properties", {})
            sev = (
                props.get("problem.severity")
                or props.get("zizmor/severity")
                or props.get("security-severity", "")
            )
            conf = props.get("zizmor/confidence", "")
            locs = r.get("locations", [])
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
            all_findings.append(
                {
                    "rule_id": rule_id,
                    "level": level,
                    "severity_zizmor": sev,
                    "confidence": conf,
                    "message": message,
                    "file": uri,
                    "line": line,
                    "snippet": snippet[:200],
                }
            )
    return all_findings


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestOurSeverity(unittest.TestCase):
    """All branches of our_severity()."""

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "high"}), "Critical")

    def test_error_high_conf_case_insensitive(self):
        # confidence stored with mixed case should still map to Critical
        self.assertEqual(our_severity({"level": "error", "confidence": "HIGH"}), "Critical")
        self.assertEqual(our_severity({"level": "error", "confidence": "High"}), "Critical")

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "medium"}), "High")

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": ""}), "High")

    def test_error_no_conf_key_is_high(self):
        self.assertEqual(our_severity({"level": "error"}), "High")

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "high"}), "High")

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "medium"}), "Medium")

    def test_warning_empty_conf_is_medium(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": ""}), "Medium")

    def test_warning_no_conf_key_is_medium(self):
        self.assertEqual(our_severity({"level": "warning"}), "Medium")

    def test_note_level_is_low(self):
        self.assertEqual(our_severity({"level": "note"}), "Low")

    def test_unknown_level_is_low(self):
        # Any level other than error/warning falls through to Low
        self.assertEqual(our_severity({"level": "info"}), "Low")
        self.assertEqual(our_severity({"level": ""}), "Low")


class TestFingerprintClassify(unittest.TestCase):
    """Fingerprint generation in classify.py."""

    def test_deterministic(self):
        fp1 = make_fingerprint("unpinned-uses", ".github/workflows/ci.yml", "uses: actions/checkout@v3")
        fp2 = make_fingerprint("unpinned-uses", ".github/workflows/ci.yml", "uses: actions/checkout@v3")
        self.assertEqual(fp1, fp2)

    def test_length_is_16(self):
        fp = make_fingerprint("rule", "file.yml", "snippet")
        self.assertEqual(len(fp), 16)

    def test_uses_basename_not_full_path(self):
        fp_full = make_fingerprint("rule", ".github/workflows/ci.yml", "x")
        fp_base = make_fingerprint("rule", "ci.yml", "x")
        self.assertEqual(fp_full, fp_base)

    def test_snippet_truncated_to_60_chars(self):
        long_snip = "a" * 100
        fp_long = make_fingerprint("rule", "f.yml", long_snip)
        fp_truncated = make_fingerprint("rule", "f.yml", "a" * 60)
        self.assertEqual(fp_long, fp_truncated)

    def test_snippet_whitespace_normalised(self):
        fp_spaces = make_fingerprint("rule", "f.yml", "foo  bar\tbaz")
        fp_single = make_fingerprint("rule", "f.yml", "foo bar baz")
        self.assertEqual(fp_spaces, fp_single)

    def test_different_rules_give_different_fps(self):
        fp1 = make_fingerprint("rule-a", "f.yml", "x")
        fp2 = make_fingerprint("rule-b", "f.yml", "x")
        self.assertNotEqual(fp1, fp2)


class TestFpForDelta(unittest.TestCase):
    """fp_for() from delta.py and the underscore/space step normalisation."""

    def test_deterministic(self):
        fp1 = fp_for("unpinned-uses", "deploy.yml", "Setup Node")
        fp2 = fp_for("unpinned-uses", "deploy.yml", "Setup Node")
        self.assertEqual(fp1, fp2)

    def test_length_is_16(self):
        self.assertEqual(len(fp_for("r", "f.yml", "step")), 16)

    def test_uses_basename(self):
        a = fp_for("rule", ".github/workflows/ci.yml", "step")
        b = fp_for("rule", "ci.yml", "step")
        self.assertEqual(a, b)

    def test_underscore_and_space_in_step_are_different(self):
        # delta.py tries both variants explicitly — they are NOT equal
        fp_space = fp_for("rule", "ci.yml", "Setup Node")
        fp_under = fp_for("rule", "ci.yml", "Setup_Node")
        self.assertNotEqual(fp_space, fp_under)

    def test_empty_step_does_not_crash(self):
        fp = fp_for("rule", "ci.yml", "")
        self.assertEqual(len(fp), 16)


class TestIsIndividualFp(unittest.TestCase):
    """Key discriminator: 16-char hex string vs aggregate rule name."""

    def test_valid_hex_fp(self):
        self.assertTrue(is_individual_fp("abcdef1234567890"))

    def test_aggregate_rule_name(self):
        self.assertFalse(is_individual_fp("secrets-outside-env"))
        self.assertFalse(is_individual_fp("unpinned-uses"))

    def test_too_short(self):
        self.assertFalse(is_individual_fp("abcdef"))

    def test_too_long(self):
        self.assertFalse(is_individual_fp("abcdef1234567890ab"))

    def test_non_hex_chars(self):
        self.assertFalse(is_individual_fp("abcdefg234567890"))


class TestExtractFindings(unittest.TestCase):
    """SARIF extraction from parse_sarif.py — covers missing-locations branch."""

    def _minimal_sarif(self, result):
        return {"runs": [{"tool": {"driver": {"rules": []}}, "results": [result]}]}

    def test_full_result_with_location(self):
        sarif = self._minimal_sarif(
            {
                "ruleId": "zizmor/unpinned-uses",
                "level": "error",
                "message": {"text": "action not pinned"},
                "properties": {"zizmor/confidence": "high"},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": ".github/workflows/ci.yml"},
                            "region": {"startLine": 42, "snippet": {"text": "uses: foo/bar@v1"}},
                        }
                    }
                ],
            }
        )
        findings = extract_findings(sarif)
        self.assertEqual(len(findings), 1)
        f = findings[0]
        self.assertEqual(f["rule_id"], "zizmor/unpinned-uses")
        self.assertEqual(f["level"], "error")
        self.assertEqual(f["file"], ".github/workflows/ci.yml")
        self.assertEqual(f["line"], 42)
        self.assertEqual(f["snippet"], "uses: foo/bar@v1")
        self.assertEqual(f["confidence"], "high")

    def test_missing_locations_gives_empty_fields(self):
        # The else-branch: no locations key at all
        sarif = self._minimal_sarif(
            {
                "ruleId": "zizmor/some-rule",
                "level": "warning",
                "message": {"text": "msg"},
            }
        )
        findings = extract_findings(sarif)
        self.assertEqual(len(findings), 1)
        f = findings[0]
        self.assertEqual(f["file"], "")
        self.assertEqual(f["line"], 0)
        self.assertEqual(f["snippet"], "")

    def test_empty_locations_list_gives_empty_fields(self):
        # locations present but empty — same else-branch path
        sarif = self._minimal_sarif(
            {"ruleId": "r", "level": "note", "message": {"text": ""}, "locations": []}
        )
        findings = extract_findings(sarif)
        f = findings[0]
        self.assertEqual(f["file"], "")
        self.assertEqual(f["line"], 0)

    def test_missing_region_defaults(self):
        sarif = self._minimal_sarif(
            {
                "ruleId": "r",
                "level": "note",
                "message": {"text": ""},
                "locations": [
                    {"physicalLocation": {"artifactLocation": {"uri": "ci.yml"}}}
                ],
            }
        )
        findings = extract_findings(sarif)
        f = findings[0]
        self.assertEqual(f["file"], "ci.yml")
        self.assertEqual(f["line"], 0)
        self.assertEqual(f["snippet"], "")

    def test_multiple_runs_aggregated(self):
        sarif = {
            "runs": [
                {
                    "tool": {"driver": {"rules": []}},
                    "results": [{"ruleId": "r1", "level": "error", "message": {"text": ""}}],
                },
                {
                    "tool": {"driver": {"rules": []}},
                    "results": [{"ruleId": "r2", "level": "warning", "message": {"text": ""}}],
                },
            ]
        }
        findings = extract_findings(sarif)
        self.assertEqual(len(findings), 2)
        rule_ids = {f["rule_id"] for f in findings}
        self.assertIn("r1", rule_ids)
        self.assertIn("r2", rule_ids)

    def test_snippet_truncated_to_200(self):
        long_text = "x" * 300
        sarif = self._minimal_sarif(
            {
                "ruleId": "r",
                "level": "note",
                "message": {"text": ""},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": "f.yml"},
                            "region": {"startLine": 1, "snippet": {"text": long_text}},
                        }
                    }
                ],
            }
        )
        findings = extract_findings(sarif)
        self.assertEqual(len(findings[0]["snippet"]), 200)

    def test_empty_sarif_gives_no_findings(self):
        self.assertEqual(extract_findings({}), [])
        self.assertEqual(extract_findings({"runs": []}), [])


if __name__ == "__main__":
    unittest.main()
