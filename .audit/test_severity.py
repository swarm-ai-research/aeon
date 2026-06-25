"""
Tests for the severity mapping and fingerprint helpers used across .audit/ scripts.

The our_severity() function is defined in both classify.py and extract_steps.py
(same logic). Tests are written against the canonical implementation here so they
don't require importing scripts with top-level file I/O.
"""

import hashlib
import os
import re
import unittest


def our_severity(f):
    """Canonical implementation from classify.py / extract_steps.py."""
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


def short_rule(rule_id):
    return rule_id.split("/")[-1]


def fingerprint(rule, fname, step):
    """extract_steps.py fingerprint scheme: rule|file|step (spaces kept)."""
    s = f"{rule}|{fname}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def fingerprint_trailer(rule, fname, step):
    """gen_trailer.py fingerprint scheme: rule|basename(fname)|step (spaces→underscores)."""
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestOurSeverity(unittest.TestCase):

    # --- error level ---

    def test_error_high_confidence_is_critical(self):
        assert our_severity({"level": "error", "confidence": "high"}) == "Critical"

    def test_error_medium_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": "medium"}) == "High"

    def test_error_low_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": "low"}) == "High"

    def test_error_empty_confidence_is_high_not_critical(self):
        # Missing confidence key must not accidentally map to Critical.
        assert our_severity({"level": "error", "confidence": ""}) == "High"
        assert our_severity({"level": "error"}) == "High"

    def test_error_high_confidence_case_insensitive(self):
        # confidence is normalised with .lower(); uppercase input must still map to Critical.
        assert our_severity({"level": "error", "confidence": "HIGH"}) == "Critical"
        assert our_severity({"level": "error", "confidence": "High"}) == "Critical"

    # --- warning level ---

    def test_warning_high_confidence_is_high(self):
        assert our_severity({"level": "warning", "confidence": "high"}) == "High"

    def test_warning_medium_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": "medium"}) == "Medium"

    def test_warning_empty_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": ""}) == "Medium"
        assert our_severity({"level": "warning"}) == "Medium"

    # --- note / other levels ---

    def test_note_is_low(self):
        assert our_severity({"level": "note"}) == "Low"

    def test_note_high_confidence_is_still_low(self):
        # note-level findings are always Low even with high confidence; the
        # guard branches for "error" and "warning" both appear before the fallthrough.
        assert our_severity({"level": "note", "confidence": "high"}) == "Low"

    def test_unknown_level_falls_through_to_low(self):
        assert our_severity({"level": "info"}) == "Low"
        assert our_severity({"level": ""}) == "Low"


class TestShortRule(unittest.TestCase):

    def test_strips_namespace_prefix(self):
        assert short_rule("zizmor/template-injection") == "template-injection"
        assert short_rule("zizmor/unpinned-uses") == "unpinned-uses"

    def test_no_prefix_returns_rule_as_is(self):
        assert short_rule("template-injection") == "template-injection"

    def test_multiple_slashes_returns_last_segment(self):
        assert short_rule("org/category/rule-name") == "rule-name"


class TestFingerprint(unittest.TestCase):

    def test_fingerprint_is_16_hex_chars(self):
        fp = fingerprint("template-injection", "deploy.yml", "Run step")
        assert len(fp) == 16
        assert all(c in "0123456789abcdef" for c in fp)

    def test_fingerprint_is_stable(self):
        fp1 = fingerprint("template-injection", "deploy.yml", "Run step")
        fp2 = fingerprint("template-injection", "deploy.yml", "Run step")
        assert fp1 == fp2

    def test_different_inputs_produce_different_fingerprints(self):
        fp1 = fingerprint("template-injection", "deploy.yml", "Run step")
        fp2 = fingerprint("unpinned-uses", "deploy.yml", "Run step")
        fp3 = fingerprint("template-injection", "other.yml", "Run step")
        fp4 = fingerprint("template-injection", "deploy.yml", "Other step")
        assert len({fp1, fp2, fp3, fp4}) == 4

    def test_trailer_scheme_differs_from_extract_steps_scheme(self):
        # gen_trailer.py replaces spaces with underscores in step name;
        # extract_steps.py does not.  These intentionally diverge — steps with
        # spaces will get different fingerprints under each scheme.
        step_with_space = "Setup Node"
        fp_steps = fingerprint("unpinned-uses", "ci.yml", step_with_space)
        fp_trail = fingerprint_trailer("unpinned-uses", "ci.yml", step_with_space)
        assert fp_steps != fp_trail, (
            "Fingerprint schemes differ for step names containing spaces; "
            "delta matching must normalise to one canonical form."
        )

    def test_trailer_uses_basename_not_full_path(self):
        full = fingerprint_trailer("template-injection", ".github/workflows/deploy.yml", "Build")
        short = fingerprint_trailer("template-injection", "deploy.yml", "Build")
        assert full == short


if __name__ == "__main__":
    unittest.main()
