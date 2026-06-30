"""
Tests for audit classification and fingerprinting logic.

Covers edge cases in the pure functions shared across extract_steps.py,
classify.py, delta.py, and gen_trailer.py.

Run: python3 -m unittest .audit/test_audit_logic.py
  or: python3 .audit/test_audit_logic.py
"""

import hashlib
import os
import re
import unittest


# ── Replicated from extract_steps.py (and classify.py — both identical) ─────

def our_severity(level, confidence=""):
    """Map zizmor SARIF level + confidence to Aeon severity grade."""
    conf = confidence.lower()
    if level == "error" and conf == "high":
        return "Critical"
    if level == "error":
        return "High"
    if level == "warning" and conf == "high":
        return "High"
    if level == "warning":
        return "Medium"
    return "Low"


# ── Replicated from extract_steps.py ─────────────────────────────────────────

def extract_steps_fingerprint(short_rule, file_uri, step):
    """Fingerprint as computed in extract_steps.py: rule|file_uri|step (raw)."""
    fp_src = f"{short_rule}|{file_uri}|{step}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── Replicated from gen_trailer.py ───────────────────────────────────────────

def gen_trailer_fingerprint(short_rule, file_uri, step):
    """Fingerprint as computed in gen_trailer.py: rule|basename|step_with_underscores."""
    s = f"{short_rule}|{os.path.basename(file_uri)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Replicated from delta.py ─────────────────────────────────────────────────

def delta_fp_for(rule, fname, step):
    """Fingerprint recomputation used in delta.py when rebuilding prior fps."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def delta_prior_fp_set(prior_fingerprints):
    """Build the prior_fp_set the way delta.py does (tries both space and underscore forms)."""
    result = set()
    for pf in prior_fingerprints:
        rule = pf.get("rule", "")
        fname = pf.get("file", "")
        step = pf.get("step", "").replace("_", " ")
        step2 = pf.get("step", "")
        result.add(delta_fp_for(rule, fname, step))
        result.add(delta_fp_for(rule, fname, step2))
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Severity mapping
# ─────────────────────────────────────────────────────────────────────────────

class TestSeverityMapping(unittest.TestCase):

    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity("error", "high"), "Critical")

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity("error", "medium"), "High")

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity("error", ""), "High")

    def test_error_low_conf_is_high(self):
        # low confidence error is still High, not Critical
        self.assertEqual(our_severity("error", "low"), "High")

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity("warning", "high"), "High")

    def test_warning_medium_conf_is_medium(self):
        self.assertEqual(our_severity("warning", "medium"), "Medium")

    def test_warning_empty_conf_is_medium(self):
        self.assertEqual(our_severity("warning", ""), "Medium")

    def test_warning_low_conf_is_medium(self):
        self.assertEqual(our_severity("warning", "low"), "Medium")

    def test_note_high_conf_is_low(self):
        # note level never escalates above Low regardless of confidence
        self.assertEqual(our_severity("note", "high"), "Low")

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity("info", "high"), "Low")

    def test_confidence_case_insensitive(self):
        # Confidence strings from zizmor may vary in case
        self.assertEqual(our_severity("error", "High"), "Critical")
        self.assertEqual(our_severity("error", "HIGH"), "Critical")
        self.assertEqual(our_severity("warning", "High"), "High")


# ─────────────────────────────────────────────────────────────────────────────
# Fingerprint determinism and stability
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractStepsFingerprint(unittest.TestCase):

    def test_identical_inputs_produce_identical_hash(self):
        fp1 = extract_steps_fingerprint("unpinned-uses", "aeon.yml", "Checkout")
        fp2 = extract_steps_fingerprint("unpinned-uses", "aeon.yml", "Checkout")
        self.assertEqual(fp1, fp2)

    def test_different_rules_differ(self):
        fp1 = extract_steps_fingerprint("unpinned-uses", "aeon.yml", "Checkout")
        fp2 = extract_steps_fingerprint("artipacked", "aeon.yml", "Checkout")
        self.assertNotEqual(fp1, fp2)

    def test_different_steps_differ(self):
        fp1 = extract_steps_fingerprint("unpinned-uses", "aeon.yml", "Checkout")
        fp2 = extract_steps_fingerprint("unpinned-uses", "aeon.yml", "Setup Node")
        self.assertNotEqual(fp1, fp2)

    def test_hash_length_is_16_hex_chars(self):
        fp = extract_steps_fingerprint("rule", "file.yml", "step")
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r"^[0-9a-f]{16}$")


# ─────────────────────────────────────────────────────────────────────────────
# Space/underscore inconsistency between extract_steps.py and gen_trailer.py
# ─────────────────────────────────────────────────────────────────────────────

class TestFingerprintSpaceUnderscore(unittest.TestCase):
    """
    extract_steps.py stores step names with spaces (raw from YAML).
    gen_trailer.py replaces spaces with underscores before hashing.
    delta.py compensates by trying both forms.
    These tests document that behaviour as a contract.
    """

    RULE = "unpinned-uses"
    FILE = "aeon.yml"
    STEP_SPACE = "Set up Node"
    STEP_UNDER = "Set_up_Node"

    def test_extract_and_gen_trailer_diverge_for_spaced_step(self):
        # extract_steps.py keeps spaces; gen_trailer.py converts to underscores
        fp_extract = extract_steps_fingerprint(self.RULE, self.FILE, self.STEP_SPACE)
        fp_trailer = gen_trailer_fingerprint(self.RULE, self.FILE, self.STEP_SPACE)
        self.assertNotEqual(fp_extract, fp_trailer,
            "extract_steps and gen_trailer produce different hashes when the step "
            "name contains spaces — delta.py must handle both forms to match them.")

    def test_delta_prior_fp_set_covers_both_forms(self):
        # gen_trailer stores STEP_UNDER in the report; delta.py reads it and tries both
        prior_fps = [{"rule": self.RULE, "file": self.FILE, "step": self.STEP_UNDER}]
        fp_set = delta_prior_fp_set(prior_fps)

        current_fp_with_space = delta_fp_for(self.RULE, self.FILE, self.STEP_SPACE)
        current_fp_with_under = delta_fp_for(self.RULE, self.FILE, self.STEP_UNDER)

        self.assertIn(current_fp_with_space, fp_set,
            "delta.py must be able to match a prior underscore step against a "
            "current space step (the replace('_',' ') path).")
        self.assertIn(current_fp_with_under, fp_set,
            "delta.py must also match the raw underscore form.")

    def test_step_already_underscored_in_yaml_round_trips(self):
        # If a YAML step name already has underscores, gen_trailer leaves them;
        # delta.py tries both forms, so it still resolves to UNCHANGED.
        step = "already_underscored"
        prior_fps = [{"rule": "rule", "file": "f.yml", "step": step}]
        fp_set = delta_prior_fp_set(prior_fps)
        current_fp = delta_fp_for("rule", "f.yml", step)
        self.assertIn(current_fp, fp_set)

    def test_no_step_match_resolves_to_new(self):
        # A finding whose step name changed is correctly flagged NEW
        prior_fps = [{"rule": "unpinned-uses", "file": "aeon.yml", "step": "Old Step"}]
        fp_set = delta_prior_fp_set(prior_fps)
        current_fp = delta_fp_for("unpinned-uses", "aeon.yml", "New Step")
        self.assertNotIn(current_fp, fp_set)


# ─────────────────────────────────────────────────────────────────────────────
# Calibration override (delta.py / delta3.py)
# ─────────────────────────────────────────────────────────────────────────────

class TestCalibrationOverride(unittest.TestCase):
    """
    unpinned-uses with severity=Critical gets downgraded to High.
    No other rule should be affected.
    """

    def _apply_calibration(self, findings):
        for f in findings:
            if f["short_rule"] == "unpinned-uses" and f["severity"] == "Critical":
                f["severity"] = "High"
                f["calibrated"] = True
        return findings

    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{"short_rule": "unpinned-uses", "severity": "Critical"}]
        result = self._apply_calibration(findings)
        self.assertEqual(result[0]["severity"], "High")
        self.assertTrue(result[0].get("calibrated"))

    def test_unpinned_uses_high_unchanged(self):
        findings = [{"short_rule": "unpinned-uses", "severity": "High"}]
        result = self._apply_calibration(findings)
        self.assertEqual(result[0]["severity"], "High")
        self.assertNotIn("calibrated", result[0])

    def test_other_rule_critical_not_downgraded(self):
        # Only unpinned-uses is calibrated; other rules must keep their severity
        findings = [{"short_rule": "template-injection", "severity": "Critical"}]
        result = self._apply_calibration(findings)
        self.assertEqual(result[0]["severity"], "Critical")
        self.assertNotIn("calibrated", result[0])

    def test_mixed_findings_only_unpinned_uses_affected(self):
        findings = [
            {"short_rule": "unpinned-uses", "severity": "Critical"},
            {"short_rule": "artipacked", "severity": "Critical"},
            {"short_rule": "unpinned-uses", "severity": "High"},
        ]
        result = self._apply_calibration(findings)
        self.assertEqual(result[0]["severity"], "High")     # downgraded
        self.assertEqual(result[1]["severity"], "Critical") # unchanged
        self.assertEqual(result[2]["severity"], "High")     # already High, unchanged


if __name__ == "__main__":
    unittest.main()
