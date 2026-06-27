"""
Unit tests for pure logic extracted from the .audit/ pipeline scripts.

No I/O — all tests operate on in-memory data only.

Run: python -m pytest .audit/test_audit_logic.py
 or: python .audit/test_audit_logic.py
"""
import hashlib
import os
import re
import unittest


# ── Extracted from classify.py ────────────────────────────────────────────────

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


def classify_fingerprint(f):
    """Build fingerprint for a finding, mirroring classify.py."""
    short_rule = f["rule_id"].split("/")[-1]
    snip_key = re.sub(r"\s+", " ", f["snippet"])[:60]
    file_short = os.path.basename(f["file"])
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── Extracted from delta.py ───────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Extracted from gen_trailer.py ─────────────────────────────────────────────

def trailer_fp(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ─────────────────────────────────────────────────────────────────────────────


class TestOurSeverity(unittest.TestCase):

    def _f(self, level, confidence=""):
        return {"level": level, "confidence": confidence}

    def test_error_high_is_critical(self):
        self.assertEqual(our_severity(self._f("error", "high")), "Critical")

    def test_error_high_case_insensitive(self):
        # confidence is lowercased before comparison — 'HIGH' and 'High' must map to Critical
        self.assertEqual(our_severity(self._f("error", "HIGH")), "Critical")
        self.assertEqual(our_severity(self._f("error", "High")), "Critical")

    def test_error_medium_is_high(self):
        self.assertEqual(our_severity(self._f("error", "medium")), "High")

    def test_error_low_is_high(self):
        self.assertEqual(our_severity(self._f("error", "low")), "High")

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity(self._f("error", "")), "High")

    def test_error_missing_confidence_key_is_high(self):
        # confidence key absent — .get() returns '' which is not 'high'
        self.assertEqual(our_severity({"level": "error"}), "High")

    def test_warning_high_is_high(self):
        self.assertEqual(our_severity(self._f("warning", "high")), "High")

    def test_warning_medium_is_medium(self):
        self.assertEqual(our_severity(self._f("warning", "medium")), "Medium")

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f("warning", "")), "Medium")

    def test_warning_missing_confidence_key_is_medium(self):
        self.assertEqual(our_severity({"level": "warning"}), "Medium")

    def test_note_is_low(self):
        self.assertEqual(our_severity(self._f("note")), "Low")

    def test_unknown_level_falls_through_to_low(self):
        # Any level that is not 'error' or 'warning' returns Low
        self.assertEqual(our_severity(self._f("info")), "Low")
        self.assertEqual(our_severity(self._f("")), "Low")
        self.assertEqual(our_severity(self._f("none")), "Low")


class TestCalibrationOverrides(unittest.TestCase):
    """Logic mirrored from delta.py and finalize.py calibration passes."""

    def _apply_delta_calibration(self, findings):
        for f in findings:
            if f["short_rule"] == "unpinned-uses" and f["severity"] == "Critical":
                f["severity"] = "High"
                f["calibrated"] = True
        return findings

    def _apply_finalize_calibration(self, findings):
        for f in findings:
            if f["short_rule"] == "secrets-outside-env" and f["severity"] == "High":
                f["severity"] = "Medium"
        return findings

    def test_unpinned_uses_critical_becomes_high(self):
        findings = [{"short_rule": "unpinned-uses", "severity": "Critical"}]
        self._apply_delta_calibration(findings)
        self.assertEqual(findings[0]["severity"], "High")
        self.assertTrue(findings[0]["calibrated"])

    def test_unpinned_uses_already_high_is_unchanged(self):
        findings = [{"short_rule": "unpinned-uses", "severity": "High"}]
        self._apply_delta_calibration(findings)
        self.assertEqual(findings[0]["severity"], "High")
        self.assertFalse(findings[0].get("calibrated", False))

    def test_other_rule_critical_not_touched_by_delta_calibration(self):
        findings = [{"short_rule": "template-injection", "severity": "Critical"}]
        self._apply_delta_calibration(findings)
        self.assertEqual(findings[0]["severity"], "Critical")

    def test_secrets_outside_env_high_becomes_medium(self):
        findings = [{"short_rule": "secrets-outside-env", "severity": "High"}]
        self._apply_finalize_calibration(findings)
        self.assertEqual(findings[0]["severity"], "Medium")

    def test_secrets_outside_env_medium_stays_medium(self):
        findings = [{"short_rule": "secrets-outside-env", "severity": "Medium"}]
        self._apply_finalize_calibration(findings)
        self.assertEqual(findings[0]["severity"], "Medium")

    def test_other_rule_high_not_touched_by_finalize_calibration(self):
        findings = [{"short_rule": "template-injection", "severity": "High"}]
        self._apply_finalize_calibration(findings)
        self.assertEqual(findings[0]["severity"], "High")

    def test_calibrations_compose_independently(self):
        # unpinned-uses goes Critical→High in delta, then finalize leaves it alone
        findings = [{"short_rule": "unpinned-uses", "severity": "Critical"}]
        self._apply_delta_calibration(findings)
        self._apply_finalize_calibration(findings)
        self.assertEqual(findings[0]["severity"], "High")


class TestFpFor(unittest.TestCase):
    """Tests for delta.py's fp_for() fingerprint function."""

    def test_returns_16_hex_chars(self):
        result = fp_for("template-injection", "deploy.yml", "Run tests")
        self.assertEqual(len(result), 16)
        self.assertRegex(result, r"^[0-9a-f]{16}$")

    def test_is_deterministic(self):
        a = fp_for("unpinned-uses", "ci.yml", "Setup Node")
        b = fp_for("unpinned-uses", "ci.yml", "Setup Node")
        self.assertEqual(a, b)

    def test_uses_basename_of_path(self):
        with_path = fp_for("rule", ".github/workflows/ci.yml", "step")
        just_name = fp_for("rule", "ci.yml", "step")
        self.assertEqual(with_path, just_name)

    def test_different_rules_produce_different_fps(self):
        self.assertNotEqual(
            fp_for("rule-a", "ci.yml", "step"),
            fp_for("rule-b", "ci.yml", "step"),
        )

    def test_different_files_produce_different_fps(self):
        self.assertNotEqual(
            fp_for("rule", "ci.yml", "step"),
            fp_for("rule", "deploy.yml", "step"),
        )

    def test_different_steps_produce_different_fps(self):
        self.assertNotEqual(
            fp_for("rule", "ci.yml", "step-a"),
            fp_for("rule", "ci.yml", "step-b"),
        )

    def test_step_spaces_are_significant(self):
        # fp_for preserves spaces; "Setup Node" != "Setup_Node"
        self.assertNotEqual(
            fp_for("rule", "ci.yml", "Setup Node"),
            fp_for("rule", "ci.yml", "Setup_Node"),
        )


class TestTrailerFp(unittest.TestCase):
    """Tests for gen_trailer.py's fp() — which normalises spaces to underscores."""

    def test_spaces_become_underscores_in_hash(self):
        # trailer_fp("Setup Node") == fp_for("Setup_Node")
        via_trailer = trailer_fp("rule", "ci.yml", "Setup Node")
        via_fp_for = fp_for("rule", "ci.yml", "Setup_Node")
        self.assertEqual(via_trailer, via_fp_for)

    def test_no_spaces_unchanged(self):
        via_trailer = trailer_fp("rule", "ci.yml", "checkout")
        via_fp_for = fp_for("rule", "ci.yml", "checkout")
        self.assertEqual(via_trailer, via_fp_for)

    def test_trailer_and_fp_for_diverge_on_spaced_step(self):
        # The two functions are NOT equivalent when step contains spaces
        fp1 = fp_for("rule", "ci.yml", "Setup Node")
        fp2 = trailer_fp("rule", "ci.yml", "Setup Node")
        self.assertNotEqual(fp1, fp2)

    def test_roundtrip_underscore_space_underscore(self):
        # Trailer writes "Setup_Node"; delta reads it and does .replace('_', ' ')
        # to get "Setup Node", then calls fp_for("Setup Node") — which does NOT
        # match trailer_fp("Setup Node"). The match is via fp_for("Setup_Node").
        step_with_underscore = "Setup_Node"
        step_with_space = step_with_underscore.replace("_", " ")
        trailer = trailer_fp("rule", "ci.yml", step_with_space)
        reconstructed = fp_for("rule", "ci.yml", step_with_underscore)
        self.assertEqual(trailer, reconstructed)


class TestClassifyFingerprint(unittest.TestCase):
    """Tests for classify.py's per-finding fingerprint construction."""

    def _f(self, rule_id="zizmor/template-injection", snippet="", file_=".github/workflows/ci.yml"):
        return {"rule_id": rule_id, "snippet": snippet, "file": file_}

    def test_strips_rule_namespace_prefix(self):
        f = self._f(rule_id="zizmor/template-injection", snippet="", file_="ci.yml")
        expected_src = "template-injection|ci.yml|"
        expected = hashlib.sha256(expected_src.encode()).hexdigest()[:16]
        self.assertEqual(classify_fingerprint(f), expected)

    def test_rule_without_slash_uses_whole_id(self):
        f = self._f(rule_id="template-injection", snippet="", file_="ci.yml")
        expected_src = "template-injection|ci.yml|"
        expected = hashlib.sha256(expected_src.encode()).hexdigest()[:16]
        self.assertEqual(classify_fingerprint(f), expected)

    def test_uses_basename_not_full_path(self):
        f1 = self._f(file_=".github/workflows/ci.yml")
        f2 = self._f(file_="ci.yml")
        self.assertEqual(classify_fingerprint(f1), classify_fingerprint(f2))

    def test_snippet_whitespace_collapsed(self):
        f1 = self._f(snippet="foo  bar\tbaz")
        f2 = self._f(snippet="foo bar baz")
        self.assertEqual(classify_fingerprint(f1), classify_fingerprint(f2))

    def test_snippet_newlines_collapsed(self):
        f1 = self._f(snippet="foo\nbar\nbaz")
        f2 = self._f(snippet="foo bar baz")
        self.assertEqual(classify_fingerprint(f1), classify_fingerprint(f2))

    def test_snippet_truncated_at_60_chars(self):
        f1 = self._f(snippet="x" * 100)
        f2 = self._f(snippet="x" * 60)
        self.assertEqual(classify_fingerprint(f1), classify_fingerprint(f2))

    def test_snippet_under_60_chars_used_verbatim(self):
        f1 = self._f(snippet="short")
        f2 = self._f(snippet="short_different")
        self.assertNotEqual(classify_fingerprint(f1), classify_fingerprint(f2))

    def test_result_is_16_hex_chars(self):
        f = self._f()
        result = classify_fingerprint(f)
        self.assertEqual(len(result), 16)
        self.assertRegex(result, r"^[0-9a-f]{16}$")


if __name__ == "__main__":
    unittest.main()
