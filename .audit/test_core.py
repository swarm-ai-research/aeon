"""Unit tests for pure functions in the .audit pipeline scripts.

Functions are inlined here rather than imported because the scripts have
top-level file I/O side effects that cannot run in isolation.

Run with:  python -m pytest .audit/test_core.py -v
       or:  python .audit/test_core.py
"""

import hashlib
import os
import tempfile
import unittest


# ---------------------------------------------------------------------------
# our_severity() — copied verbatim from classify.py / extract_steps.py
# ---------------------------------------------------------------------------

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


class TestOurSeverity(unittest.TestCase):

    # --- documented branches ---

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "high"}), "Critical")

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": "medium"}), "High")

    def test_error_no_confidence_is_high(self):
        self.assertEqual(our_severity({"level": "error", "confidence": ""}), "High")

    def test_error_missing_confidence_key_is_high(self):
        self.assertEqual(our_severity({"level": "error"}), "High")

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "high"}), "High")

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "medium"}), "Medium")

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity({"level": "warning"}), "Medium")

    def test_note_level_is_low(self):
        self.assertEqual(our_severity({"level": "note"}), "Low")

    def test_note_level_high_confidence_is_still_low(self):
        # note level has no special confidence branch — always Low
        self.assertEqual(our_severity({"level": "note", "confidence": "high"}), "Low")

    # --- edge cases ---

    def test_confidence_uppercase_folded_for_critical(self):
        # The script lowercases confidence before comparing; "HIGH" should still → Critical
        self.assertEqual(our_severity({"level": "error", "confidence": "HIGH"}), "Critical")

    def test_confidence_uppercase_folded_for_warning(self):
        self.assertEqual(our_severity({"level": "warning", "confidence": "HIGH"}), "High")

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({"level": "unknown"}), "Low")

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({"level": ""}), "Low")

    def test_confidence_low_string_is_not_high(self):
        # "low" != "high" so error+low → High (not Critical)
        self.assertEqual(our_severity({"level": "error", "confidence": "low"}), "High")


# ---------------------------------------------------------------------------
# fp_for() — copied verbatim from delta.py
# ---------------------------------------------------------------------------

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestFpFor(unittest.TestCase):

    def test_returns_16_hex_chars(self):
        fp = fp_for("unpinned-uses", ".github/workflows/aeon.yml", "Checkout")
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))

    def test_deterministic(self):
        fp1 = fp_for("unpinned-uses", "aeon.yml", "Checkout")
        fp2 = fp_for("unpinned-uses", "aeon.yml", "Checkout")
        self.assertEqual(fp1, fp2)

    def test_basename_only_used_for_path(self):
        # Full path and basename should produce the same fingerprint
        fp_full = fp_for("rule", ".github/workflows/aeon.yml", "step")
        fp_base = fp_for("rule", "aeon.yml", "step")
        self.assertEqual(fp_full, fp_base)

    def test_different_rules_differ(self):
        fp1 = fp_for("rule-a", "aeon.yml", "step")
        fp2 = fp_for("rule-b", "aeon.yml", "step")
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_differ(self):
        fp1 = fp_for("rule", "aeon.yml", "Setup Node")
        fp2 = fp_for("rule", "aeon.yml", "Setup_Node")
        self.assertNotEqual(fp1, fp2)

    def test_empty_step_is_valid(self):
        # step can be empty string — should not raise
        fp = fp_for("rule", "aeon.yml", "")
        self.assertEqual(len(fp), 16)

    def test_underscore_space_variant_differs(self):
        # delta.py tries both underscore and space variants to match prior fingerprints
        fp_space = fp_for("unpinned-uses", "aeon.yml", "Setup Node")
        fp_under = fp_for("unpinned-uses", "aeon.yml", "Setup_Node")
        self.assertNotEqual(fp_space, fp_under)


# ---------------------------------------------------------------------------
# resolve_path() — copied verbatim from extract_steps.py, but made testable
# by accepting a root directory argument
# ---------------------------------------------------------------------------

def resolve_path(basename, root="."):
    cand1 = os.path.join(root, ".github", "workflows", basename)
    if os.path.exists(cand1):
        return cand1
    cand2 = os.path.join(root, basename)
    if os.path.exists(cand2):
        return cand2
    return None


class TestResolvePath(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def _mk(self, *parts):
        path = os.path.join(self.tmp, *parts)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
        return path

    def test_resolves_from_github_workflows(self):
        self._mk(".github", "workflows", "aeon.yml")
        result = resolve_path("aeon.yml", root=self.tmp)
        self.assertIsNotNone(result)
        self.assertTrue(result.endswith(os.path.join(".github", "workflows", "aeon.yml")))

    def test_resolves_as_is_when_not_in_workflows(self):
        self._mk("some.yml")
        result = resolve_path("some.yml", root=self.tmp)
        self.assertIsNotNone(result)

    def test_returns_none_when_not_found(self):
        result = resolve_path("nonexistent.yml", root=self.tmp)
        self.assertIsNone(result)

    def test_github_workflows_takes_priority_over_as_is(self):
        # If file exists in both locations, .github/workflows wins (first candidate)
        self._mk(".github", "workflows", "overlap.yml")
        self._mk("overlap.yml")
        result = resolve_path("overlap.yml", root=self.tmp)
        self.assertIn(".github", result)


if __name__ == "__main__":
    unittest.main()
