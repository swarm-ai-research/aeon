#!/usr/bin/env python3
"""Tests for pure logic functions in the workflow-security-audit pipeline.

Covers uncovered branches in the two functions shared across classify.py,
extract_steps.py, gen_trailer.py, and delta3.py.

Run: python3 .audit/test_logic.py
"""
import hashlib
import os
import unittest


# --- our_severity() (duplicated in classify.py / extract_steps.py) ---
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


# --- fingerprint helper (gen_trailer.py / delta3.py) ---
def fp(rule, fname, step):
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestOurSeverity(unittest.TestCase):
    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "high"}), "Critical")

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "medium"}), "High")

    def test_error_missing_conf_is_high(self):
        # confidence key absent — falls through to bare `error` branch
        self.assertEqual(our_severity({"level": "error"}), "High")

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": ""}), "High")

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "high"}), "High")

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "medium"}), "Medium")

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity({"level": "warning"}), "Medium")

    def test_note_level_is_low(self):
        self.assertEqual(our_severity({"level": "note"}), "Low")

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({"level": "unknown"}), "Low")

    def test_confidence_check_is_case_insensitive(self):
        # zizmor emits "High" (capital H); .lower() must normalise it
        self.assertEqual(our_severity({"level": "error", "confidence": "High"}), "Critical")
        self.assertEqual(our_severity({"level": "warning", "confidence": "HIGH"}), "High")


class TestFingerprint(unittest.TestCase):
    def test_output_is_16_lowercase_hex_chars(self):
        result = fp("template-injection", "aeon.yml", "Build step")
        self.assertEqual(len(result), 16)
        self.assertTrue(all(c in "0123456789abcdef" for c in result))

    def test_full_path_and_basename_produce_same_fp(self):
        # fp() calls os.path.basename — only the filename matters
        fp_full = fp("template-injection", ".github/workflows/aeon.yml", "Build step")
        fp_base = fp("template-injection", "aeon.yml", "Build step")
        self.assertEqual(fp_full, fp_base)

    def test_spaces_in_step_normalised_to_underscores(self):
        # Prior audit stored steps with underscores; space and underscore must match
        fp_spaces = fp("unpinned-uses", "aeon.yml", "Setup Node")
        fp_under = fp("unpinned-uses", "aeon.yml", "Setup_Node")
        self.assertEqual(fp_spaces, fp_under)

    def test_different_rules_differ(self):
        self.assertNotEqual(
            fp("template-injection", "aeon.yml", "step"),
            fp("unpinned-uses", "aeon.yml", "step"),
        )

    def test_different_files_differ(self):
        self.assertNotEqual(
            fp("unpinned-uses", "aeon.yml", "Checkout"),
            fp("unpinned-uses", "fleet-runner.yml", "Checkout"),
        )

    def test_different_steps_differ(self):
        self.assertNotEqual(
            fp("unpinned-uses", "aeon.yml", "Checkout"),
            fp("unpinned-uses", "aeon.yml", "Build"),
        )

    def test_deterministic_across_calls(self):
        self.assertEqual(
            fp("secrets-outside-env", "messages.yml", "Send message"),
            fp("secrets-outside-env", "messages.yml", "Send message"),
        )


if __name__ == "__main__":
    unittest.main()
