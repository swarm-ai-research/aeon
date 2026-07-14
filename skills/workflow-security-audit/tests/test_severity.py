"""
Unit tests for the zizmor SARIF → audit severity mapping.

The our_severity() function (defined inline in .audit/classify.py) maps
zizmor's (level, confidence) pairs to Critical / High / Medium / Low.
These tests cover the branches and edge cases that the nightly audit run
does not exercise deterministically.

Run with:  python3 -m pytest skills/workflow-security-audit/tests/test_severity.py -v
       or:  python3 skills/workflow-security-audit/tests/test_severity.py
"""

import sys


# ── inline copy of the function under test ───────────────────────────────────
# Kept in sync with .audit/classify.py:our_severity().
# If you change the mapping there, update it here too.

def our_severity(f: dict) -> str:
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


# ── helpers ───────────────────────────────────────────────────────────────────

def finding(level: str, confidence: str = "") -> dict:
    return {"level": level, "confidence": confidence}


# ── test cases ────────────────────────────────────────────────────────────────

def test_error_high_confidence_is_critical():
    assert our_severity(finding("error", "high")) == "Critical"


def test_error_high_confidence_case_insensitive():
    # SARIF sources may emit 'High' rather than 'high'; .lower() must normalise.
    assert our_severity(finding("error", "High")) == "Critical"
    assert our_severity(finding("error", "HIGH")) == "Critical"


def test_error_medium_confidence_is_high():
    # Second branch: level=error, conf != 'high' → High
    assert our_severity(finding("error", "medium")) == "High"


def test_error_low_confidence_is_high():
    assert our_severity(finding("error", "low")) == "High"


def test_error_empty_confidence_is_high():
    # Missing confidence key falls back to '' → second 'error' branch → High
    f = {"level": "error"}          # no 'confidence' key at all
    assert our_severity(f) == "High"
    assert our_severity(finding("error", "")) == "High"


def test_warning_high_confidence_is_high():
    assert our_severity(finding("warning", "high")) == "High"


def test_warning_medium_confidence_is_medium():
    assert our_severity(finding("warning", "medium")) == "Medium"


def test_warning_low_confidence_is_medium():
    assert our_severity(finding("warning", "low")) == "Medium"


def test_warning_no_confidence_is_medium():
    f = {"level": "warning"}
    assert our_severity(f) == "Medium"


def test_note_is_low():
    # 'note' falls through all ifs → Low
    assert our_severity(finding("note")) == "Low"
    assert our_severity(finding("note", "high")) == "Low"


def test_unknown_level_is_low():
    # Defensive: unexpected level values (e.g. 'open', 'info') → Low, not an error
    assert our_severity(finding("info")) == "Low"
    assert our_severity(finding("open")) == "Low"
    assert our_severity(finding("")) == "Low"


# ── standalone runner ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"OK  {t.__name__}")
        except AssertionError as e:
            print(f"FAIL {t.__name__}: {e}")
            failed += 1
    print()
    if failed:
        print(f"{failed} test(s) FAILED")
        sys.exit(1)
    print(f"All {len(tests)} tests passed.")
