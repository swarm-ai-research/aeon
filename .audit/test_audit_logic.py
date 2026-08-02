"""
Unit tests for pure functions extracted from the .audit/ processing scripts.
Run with: python -m pytest .audit/test_audit_logic.py

These tests cover logic in classify.py, parse_sarif.py, and summarize_al.py
without triggering any file I/O from those scripts.
"""

import hashlib
import os


# ---------------------------------------------------------------------------
# Logic under test (inlined from classify.py — no file I/O needed)
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


def make_fingerprint(short_rule, file_path, snippet):
    """Fingerprint logic from classify.py."""
    import re
    snip_key = re.sub(r"\s+", " ", snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Logic under test (inlined from delta.py)
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    """Fingerprint function from delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Logic under test (inlined from parse_sarif.py)
# ---------------------------------------------------------------------------

def resolve_severity(props):
    """Priority chain for zizmor severity from parse_sarif.py."""
    return (
        props.get("problem.severity")
        or props.get("zizmor/severity")
        or props.get("security-severity", "")
    )


# ---------------------------------------------------------------------------
# Logic under test (inlined from summarize_al.py)
# ---------------------------------------------------------------------------

SHELLCHECK_CODES = ["SC2086", "SC2046", "SC2129", "SC2153", "SC2155", "SC2034"]


def classify_actionlint_message(msg):
    """Return the first matching SC code, or 'other'."""
    for code in SHELLCHECK_CODES:
        if code in msg:
            return code
    return "other"


def is_high_candidate(msg):
    """HIGH-CANDIDATE detection from summarize_al.py."""
    return ("SC2086" in msg or "SC2046" in msg) and "github." in msg.lower()


# ===========================================================================
# Tests: our_severity
# ===========================================================================

class TestOurSeverity:
    def test_error_high_confidence_is_critical(self):
        assert our_severity({"level": "error", "confidence": "high"}) == "Critical"

    def test_error_high_confidence_case_insensitive(self):
        assert our_severity({"level": "error", "confidence": "HIGH"}) == "Critical"
        assert our_severity({"level": "error", "confidence": "High"}) == "Critical"

    def test_error_medium_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": "medium"}) == "High"

    def test_error_empty_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": ""}) == "High"

    def test_error_missing_confidence_key_is_high(self):
        assert our_severity({"level": "error"}) == "High"

    def test_warning_high_confidence_is_high(self):
        assert our_severity({"level": "warning", "confidence": "high"}) == "High"

    def test_warning_medium_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": "medium"}) == "Medium"

    def test_warning_low_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": "low"}) == "Medium"

    def test_warning_missing_confidence_is_medium(self):
        assert our_severity({"level": "warning"}) == "Medium"

    def test_note_level_is_low(self):
        assert our_severity({"level": "note", "confidence": "high"}) == "Low"
        assert our_severity({"level": "note", "confidence": ""}) == "Low"

    def test_unknown_level_is_low(self):
        assert our_severity({"level": "none", "confidence": "high"}) == "Low"
        assert our_severity({"level": "", "confidence": "high"}) == "Low"


# ===========================================================================
# Tests: make_fingerprint
# ===========================================================================

class TestMakeFingerprint:
    def test_returns_16_hex_chars(self):
        fp = make_fingerprint("unpinned-uses", "some/path/deploy.yml", "uses: actions/checkout@v3")
        assert len(fp) == 16
        assert all(c in "0123456789abcdef" for c in fp)

    def test_deterministic(self):
        fp1 = make_fingerprint("unpinned-uses", "deploy.yml", "uses: actions/checkout@v3")
        fp2 = make_fingerprint("unpinned-uses", "deploy.yml", "uses: actions/checkout@v3")
        assert fp1 == fp2

    def test_uses_basename_not_full_path(self):
        fp_full = make_fingerprint("rule", "/long/path/to/workflow.yml", "snippet")
        fp_base = make_fingerprint("rule", "workflow.yml", "snippet")
        assert fp_full == fp_base

    def test_different_snippets_produce_different_fps(self):
        fp1 = make_fingerprint("rule", "file.yml", "snippet-a")
        fp2 = make_fingerprint("rule", "file.yml", "snippet-b")
        assert fp1 != fp2

    def test_snippet_truncated_at_60_chars(self):
        long_snip = "x" * 100
        fp1 = make_fingerprint("rule", "file.yml", long_snip)
        fp2 = make_fingerprint("rule", "file.yml", "x" * 60)
        assert fp1 == fp2

    def test_whitespace_collapsed_in_snippet(self):
        fp1 = make_fingerprint("rule", "file.yml", "uses:  actions/checkout")
        fp2 = make_fingerprint("rule", "file.yml", "uses: actions/checkout")
        assert fp1 == fp2


# ===========================================================================
# Tests: fp_for (delta.py)
# ===========================================================================

class TestFpFor:
    def test_returns_16_hex_chars(self):
        fp = fp_for("unpinned-uses", "deploy.yml", "Checkout repo")
        assert len(fp) == 16
        assert all(c in "0123456789abcdef" for c in fp)

    def test_uses_basename(self):
        fp_full = fp_for("rule", "/path/to/workflow.yml", "step")
        fp_base = fp_for("rule", "workflow.yml", "step")
        assert fp_full == fp_base

    def test_underscore_vs_space_differs(self):
        """delta.py tries both to handle step name refactoring."""
        fp_space = fp_for("rule", "file.yml", "Setup Node")
        fp_under = fp_for("rule", "file.yml", "Setup_Node")
        assert fp_space != fp_under

    def test_deterministic(self):
        assert fp_for("r", "f.yml", "s") == fp_for("r", "f.yml", "s")


# ===========================================================================
# Tests: resolve_severity (parse_sarif.py)
# ===========================================================================

class TestResolveSeverity:
    def test_problem_severity_wins(self):
        props = {"problem.severity": "high", "zizmor/severity": "medium", "security-severity": "low"}
        assert resolve_severity(props) == "high"

    def test_falls_back_to_zizmor_severity(self):
        props = {"zizmor/severity": "medium", "security-severity": "low"}
        assert resolve_severity(props) == "medium"

    def test_falls_back_to_security_severity(self):
        props = {"security-severity": "low"}
        assert resolve_severity(props) == "low"

    def test_all_absent_returns_empty_string(self):
        assert resolve_severity({}) == ""

    def test_empty_string_problem_severity_falls_through(self):
        """An empty string is falsy; should fall to next key."""
        props = {"problem.severity": "", "zizmor/severity": "medium"}
        assert resolve_severity(props) == "medium"

    def test_none_problem_severity_falls_through(self):
        props = {"problem.severity": None, "zizmor/severity": "high"}
        assert resolve_severity(props) == "high"


# ===========================================================================
# Tests: classify_actionlint_message (summarize_al.py)
# ===========================================================================

class TestClassifyActionlintMessage:
    def test_sc2086_detected(self):
        assert classify_actionlint_message("shellcheck: SC2086: Double quote to prevent globbing") == "SC2086"

    def test_sc2046_detected(self):
        assert classify_actionlint_message("error: SC2046 found in step") == "SC2046"

    def test_sc2129_detected(self):
        assert classify_actionlint_message("note: SC2129 applies here") == "SC2129"

    def test_sc2153_detected(self):
        assert classify_actionlint_message("warning: SC2153 in expression") == "SC2153"

    def test_sc2155_detected(self):
        assert classify_actionlint_message("SC2155: Declare and assign separately") == "SC2155"

    def test_sc2034_detected(self):
        assert classify_actionlint_message("SC2034 appears unused") == "SC2034"

    def test_first_code_wins_when_multiple_present(self):
        """SC2086 appears before SC2046 in the list."""
        assert classify_actionlint_message("SC2086 and SC2046 both here") == "SC2086"

    def test_no_code_returns_other(self):
        assert classify_actionlint_message("some unrecognized shellcheck error") == "other"

    def test_empty_message_returns_other(self):
        assert classify_actionlint_message("") == "other"


# ===========================================================================
# Tests: is_high_candidate (summarize_al.py)
# ===========================================================================

class TestIsHighCandidate:
    def test_sc2086_with_github_context(self):
        assert is_high_candidate("SC2086: unquoted ${{ github.event.inputs.foo }}")

    def test_sc2046_with_github_context(self):
        assert is_high_candidate("SC2046 found in $github.ref expression")

    def test_github_uppercase_is_detected(self):
        """msg.lower() is used so 'GITHUB.' should still match."""
        assert is_high_candidate("SC2086 uses $GITHUB.ref")

    def test_sc2086_without_github_is_not_high(self):
        assert not is_high_candidate("SC2086: unquoted $MY_VAR")

    def test_sc2046_without_github_is_not_high(self):
        assert not is_high_candidate("SC2046 found in loop")

    def test_other_sc_code_with_github_is_not_high(self):
        assert not is_high_candidate("SC2153 github.ref is unset")

    def test_empty_message_is_not_high(self):
        assert not is_high_candidate("")
