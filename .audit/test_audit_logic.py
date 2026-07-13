#!/usr/bin/env python3
"""
Unit tests for the audit severity-mapping and fingerprinting logic.

These functions live in .audit/classify.py and .audit/delta.py — procedural
scripts that are not safely importable (they read/write files on import), so
the pure functions are reproduced here to be exercised in isolation.

Run: python3 .audit/test_audit_logic.py
"""

import hashlib
import os
import unittest


# ── Severity mapping (mirrors .audit/classify.py :: our_severity) ────────────

def our_severity(f):
    """Map a zizmor SARIF finding dict to Critical / High / Medium / Low."""
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


# ── Fingerprinting (mirrors .audit/delta.py :: fp_for) ───────────────────────

def fp_for(rule, fname, step):
    """Stable 16-char fingerprint: sha256(rule|basename(fname)|step)[:16]."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    @staticmethod
    def _f(level, confidence=None):
        d = {"level": level}
        if confidence is not None:
            d["confidence"] = confidence
        return d

    # Critical: error + high confidence
    def test_error_high_is_critical(self):
        self.assertEqual(our_severity(self._f("error", "high")), "Critical")

    def test_error_high_confidence_case_insensitive(self):
        # classify.py does .lower() — uppercase variants must still be Critical
        self.assertEqual(our_severity(self._f("error", "HIGH")), "Critical")
        self.assertEqual(our_severity(self._f("error", "High")), "Critical")

    # High: error without high confidence
    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity(self._f("error", "medium")), "High")

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity(self._f("error", "low")), "High")

    def test_error_missing_confidence_is_high(self):
        # .get("confidence", "") returns "" when the key is absent
        self.assertEqual(our_severity(self._f("error")), "High")

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity(self._f("error", "")), "High")

    # High: warning + high confidence
    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(self._f("warning", "high")), "High")

    # Medium: warning without high confidence
    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f("warning", "medium")), "Medium")

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f("warning", "low")), "Medium")

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f("warning")), "Medium")

    # Low: note-level and anything else
    def test_note_is_low_regardless_of_confidence(self):
        # A high-confidence note is still Low — important boundary to pin
        self.assertEqual(our_severity(self._f("note", "high")), "Low")
        self.assertEqual(our_severity(self._f("note", "medium")), "Low")
        self.assertEqual(our_severity(self._f("note")), "Low")

    def test_unknown_level_falls_through_to_low(self):
        self.assertEqual(our_severity(self._f("unknown_level")), "Low")


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        fp = fp_for("template-injection", "aeon.yml", "Build")
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))

    def test_is_deterministic(self):
        a = fp_for("unpinned-uses", "messages.yml", "Checkout")
        b = fp_for("unpinned-uses", "messages.yml", "Checkout")
        self.assertEqual(a, b)

    def test_basename_normalisation(self):
        # Two different full paths that share a basename produce the same fp —
        # intentional: delta.py matches prior fingerprints keyed only on basename.
        fp1 = fp_for("rule", ".github/workflows/aeon.yml", "step")
        fp2 = fp_for("rule", "/home/runner/work/aeon.yml", "step")
        self.assertEqual(fp1, fp2)

    def test_different_rules_differ(self):
        a = fp_for("template-injection", "aeon.yml", "Build")
        b = fp_for("unpinned-uses", "aeon.yml", "Build")
        self.assertNotEqual(a, b)

    def test_different_steps_differ(self):
        a = fp_for("rule", "aeon.yml", "Build")
        b = fp_for("rule", "aeon.yml", "Deploy")
        self.assertNotEqual(a, b)

    def test_empty_inputs_return_valid_fp(self):
        fp = fp_for("", "", "")
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))

    def test_step_spaces_vs_underscores_differ(self):
        # delta.py normalises "_" → " " when re-reading prior fingerprints; the
        # raw fp_for does NOT — so "Setup_Node" and "Setup Node" are distinct.
        a = fp_for("rule", "aeon.yml", "Setup Node")
        b = fp_for("rule", "aeon.yml", "Setup_Node")
        self.assertNotEqual(a, b)


if __name__ == "__main__":
    unittest.main()
