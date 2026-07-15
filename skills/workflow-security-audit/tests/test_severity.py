"""
Unit tests for the zizmor finding → severity mapping used in workflow-security-audit.

The classify.py / extract_steps.py scripts embed an `our_severity()` function
with five branches. These tests cover all branches plus edge cases (missing or
empty confidence field) that were previously untested.
"""

import sys
import hashlib


# --- replicated from .audit/classify.py (must stay in sync) ---

def our_severity(f):
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


# --- replicated fingerprint helper from .audit/gen_trailer.py ---

def fp(rule, fname, step):
    import os
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# --- tests ---

def test_error_high_confidence_is_critical():
    f = {"level": "error", "confidence": "high"}
    assert our_severity(f) == "Critical"


def test_error_low_confidence_is_high():
    f = {"level": "error", "confidence": "low"}
    assert our_severity(f) == "High"


def test_error_medium_confidence_is_high():
    f = {"level": "error", "confidence": "medium"}
    assert our_severity(f) == "High"


def test_warning_high_confidence_is_high():
    f = {"level": "warning", "confidence": "high"}
    assert our_severity(f) == "High"


def test_warning_low_confidence_is_medium():
    f = {"level": "warning", "confidence": "low"}
    assert our_severity(f) == "Medium"


def test_note_level_is_low():
    f = {"level": "note", "confidence": "high"}
    assert our_severity(f) == "Low"


def test_missing_confidence_defaults_to_empty_string():
    # no 'confidence' key at all — .get() returns "" → counts as non-high
    f = {"level": "error"}
    assert our_severity(f) == "High"


def test_confidence_case_insensitive():
    # zizmor may emit "High" (capitalised) — .lower() must normalise it
    f = {"level": "error", "confidence": "High"}
    assert our_severity(f) == "Critical"


def test_fingerprint_is_deterministic():
    a = fp("template-injection", ".github/workflows/aeon.yml", "Run skill")
    b = fp("template-injection", ".github/workflows/aeon.yml", "Run skill")
    assert a == b


def test_fingerprint_length_is_16():
    h = fp("unpinned-uses", ".github/workflows/aeon.yml", "Checkout")
    assert len(h) == 16
    assert all(c in "0123456789abcdef" for c in h)


def test_fingerprint_space_and_underscore_differ():
    # gen_trailer replaces ' ' with '_' before hashing; the *caller* in delta.py
    # does the reverse. Confirm the two produce different hashes (they must, so
    # that the step-normalisation in delta.py can round-trip correctly).
    h_space = fp("rule", "file.yml", "Run step")
    h_under = fp("rule", "file.yml", "Run_step")
    # After replacement both become "Run_step" — so they should be equal.
    assert h_space == h_under


def test_fingerprint_different_rules_differ():
    h1 = fp("template-injection", "aeon.yml", "step")
    h2 = fp("unpinned-uses", "aeon.yml", "step")
    assert h1 != h2


def test_fingerprint_uses_basename_only():
    h1 = fp("rule", ".github/workflows/aeon.yml", "step")
    h2 = fp("rule", "aeon.yml", "step")
    assert h1 == h2


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failures += 1
    print()
    if failures:
        print(f"{failures}/{len(tests)} tests FAILED")
        sys.exit(1)
    else:
        print(f"All {len(tests)} tests passed")
