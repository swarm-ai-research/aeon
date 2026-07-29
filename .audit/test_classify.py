#!/usr/bin/env python3
"""Unit tests for severity-mapping and fingerprint logic shared across classify.py / extract_steps.py.

Run: python .audit/test_classify.py
"""
import hashlib
import os
import re
import unittest

# ── Functions under test (exact copies from classify.py / extract_steps.py) ────

def our_severity(f):
    """Severity mapping used in classify.py and extract_steps.py."""
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


def compute_classify_fingerprint(rule_id, file_uri, snippet):
    """Fingerprint formula from classify.py."""
    short_rule = rule_id.split("/")[-1]
    snip_key = re.sub(r"\s+", " ", snippet)[:60]
    file_short = os.path.basename(file_uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


def compute_trailer_fingerprint(rule, fname, step):
    """Fingerprint formula from gen_trailer.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Tests ───────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    # ── error level ──────────────────────────────────────────────────────────

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "high"}), "Critical")

    def test_error_high_confidence_case_insensitive(self):
        # .lower() is applied, so uppercase variant must still resolve to Critical
        self.assertEqual(our_severity({"level": "error", "confidence": "HIGH"}), "Critical")

    def test_error_medium_confidence_is_high_not_critical(self):
        # Does NOT hit the first branch; falls through to "if level == 'error'"
        self.assertEqual(our_severity({"level": "error", "confidence": "medium"}), "High")

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "low"}), "High")

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": ""}), "High")

    def test_error_missing_confidence_key_is_high(self):
        # .get("confidence", "") provides "" default when key absent
        self.assertEqual(our_severity({"level": "error"}), "High")

    # ── warning level ─────────────────────────────────────────────────────────

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "high"}), "High")

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "medium"}), "Medium")

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "low"}), "Medium")

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({"level": "warning"}), "Medium")

    # ── else branch (note / unknown levels) ───────────────────────────────────

    def test_note_level_is_low(self):
        # "note" is the SARIF level for informational findings; falls to else
        self.assertEqual(our_severity({"level": "note", "confidence": "high"}), "Low")

    def test_note_level_no_confidence_is_low(self):
        self.assertEqual(our_severity({"level": "note"}), "Low")

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({"level": "none"}), "Low")

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({"level": ""}), "Low")


class TestClassifyFingerprint(unittest.TestCase):

    def test_rule_namespace_stripped(self):
        fp1 = compute_classify_fingerprint("zizmor/unpinned-uses", "aeon.yml", "uses: actions/checkout@v3")
        fp2 = compute_classify_fingerprint("unpinned-uses", "aeon.yml", "uses: actions/checkout@v3")
        self.assertEqual(fp1, fp2, "namespace prefix should be stripped so both produce the same fingerprint")

    def test_directory_components_stripped_from_file(self):
        fp1 = compute_classify_fingerprint("rule", ".github/workflows/aeon.yml", "snippet")
        fp2 = compute_classify_fingerprint("rule", "aeon.yml", "snippet")
        self.assertEqual(fp1, fp2, "only the basename is used in the fingerprint")

    def test_snippet_whitespace_normalised(self):
        fp1 = compute_classify_fingerprint("rule", "file.yml", "foo\t  bar\n  baz")
        fp2 = compute_classify_fingerprint("rule", "file.yml", "foo bar baz")
        self.assertEqual(fp1, fp2, "whitespace runs in the snippet should be collapsed to a single space")

    def test_snippet_truncated_to_60_chars(self):
        long_snip = "x" * 80
        short_snip = "x" * 60
        fp1 = compute_classify_fingerprint("rule", "file.yml", long_snip)
        fp2 = compute_classify_fingerprint("rule", "file.yml", short_snip)
        self.assertEqual(fp1, fp2, "snippet beyond 60 chars should be truncated before hashing")

    def test_snippet_char_at_position_60_is_included(self):
        # The slice is [:60], so index 59 (the 60th char) is included.
        # Two strings differing only at position 59 must hash differently.
        snip_x = "a" * 59 + "x"  # 60 chars — last char is 'x'
        snip_y = "a" * 59 + "y"  # 60 chars — last char is 'y'
        fp1 = compute_classify_fingerprint("rule", "file.yml", snip_x)
        fp2 = compute_classify_fingerprint("rule", "file.yml", snip_y)
        self.assertNotEqual(fp1, fp2, "the 60th character must be included in the fingerprint")

    def test_snippet_char_at_position_61_is_dropped(self):
        # A 61-char string and its 60-char prefix produce the same fingerprint.
        base_snip = "a" * 59 + "x"  # 60 chars
        long_snip = base_snip + "z"   # 61 chars — 'z' at index 60 is beyond the slice
        fp1 = compute_classify_fingerprint("rule", "file.yml", base_snip)
        fp2 = compute_classify_fingerprint("rule", "file.yml", long_snip)
        self.assertEqual(fp1, fp2, "char at index 60 (position 61) must be dropped by [:60]")

    def test_deterministic(self):
        args = ("my-rule", "workflows/check.yml", "run: echo hello")
        self.assertEqual(compute_classify_fingerprint(*args), compute_classify_fingerprint(*args))

    def test_different_rules_produce_different_fingerprints(self):
        fp1 = compute_classify_fingerprint("rule-a", "f.yml", "s")
        fp2 = compute_classify_fingerprint("rule-b", "f.yml", "s")
        self.assertNotEqual(fp1, fp2)

    def test_fingerprint_is_16_hex_chars(self):
        fp = compute_classify_fingerprint("rule", "file.yml", "snip")
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))


class TestTrailerFingerprint(unittest.TestCase):

    def test_spaces_in_step_become_underscores(self):
        fp_with_space = compute_trailer_fingerprint("rule", "aeon.yml", "Set up Node")
        fp_with_under = compute_trailer_fingerprint("rule", "aeon.yml", "Set_up_Node")
        self.assertEqual(fp_with_space, fp_with_under,
                         "step spaces must be replaced with underscores before hashing")

    def test_directory_components_stripped(self):
        fp1 = compute_trailer_fingerprint("rule", ".github/workflows/aeon.yml", "step")
        fp2 = compute_trailer_fingerprint("rule", "aeon.yml", "step")
        self.assertEqual(fp1, fp2)

    def test_deterministic(self):
        args = ("unpinned-uses", "aeon.yml", "Checkout")
        self.assertEqual(compute_trailer_fingerprint(*args), compute_trailer_fingerprint(*args))

    def test_different_steps_produce_different_fingerprints(self):
        fp1 = compute_trailer_fingerprint("rule", "f.yml", "Step A")
        fp2 = compute_trailer_fingerprint("rule", "f.yml", "Step B")
        self.assertNotEqual(fp1, fp2)

    def test_fingerprint_is_16_hex_chars(self):
        fp = compute_trailer_fingerprint("rule", "file.yml", "step")
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))


if __name__ == "__main__":
    unittest.main()
