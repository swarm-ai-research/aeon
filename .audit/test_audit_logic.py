"""
Unit tests for pure logic extracted from the .audit/ analysis scripts.

Tests cover severity mapping, fingerprint generation, delta tagging, and
the two calibration overrides (unpinned-uses Critical→High and
secrets-outside-env High→Medium).

Run:  python -m pytest .audit/test_audit_logic.py -v
"""

import hashlib
import os
import pytest


# ---------------------------------------------------------------------------
# Severity mapping  (classify.py / extract_steps.py)
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


class TestOurSeverity:
    def test_error_high_confidence_is_critical(self):
        assert our_severity({"level": "error", "confidence": "high"}) == "Critical"

    def test_error_high_confidence_case_insensitive(self):
        assert our_severity({"level": "error", "confidence": "HIGH"}) == "Critical"

    def test_error_medium_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": "medium"}) == "High"

    def test_error_missing_confidence_is_high(self):
        assert our_severity({"level": "error"}) == "High"

    def test_error_empty_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": ""}) == "High"

    def test_warning_high_confidence_is_high(self):
        assert our_severity({"level": "warning", "confidence": "high"}) == "High"

    def test_warning_low_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": "low"}) == "Medium"

    def test_warning_missing_confidence_is_medium(self):
        assert our_severity({"level": "warning"}) == "Medium"

    def test_note_level_is_low(self):
        # 'note' falls through all branches → Low
        assert our_severity({"level": "note", "confidence": "high"}) == "Low"

    def test_unknown_level_is_low(self):
        assert our_severity({"level": "info"}) == "Low"

    def test_unknown_level_no_confidence_key_is_low(self):
        assert our_severity({"level": "none"}) == "Low"


# ---------------------------------------------------------------------------
# Fingerprint generation  (gen_trailer.py variant — spaces → underscores)
# ---------------------------------------------------------------------------

def fp_trailer(rule, fname, step):
    """Matches gen_trailer.py: replaces spaces with underscores in step."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def fp_delta(rule, fname, step):
    """Matches delta.py fp_for: no underscore substitution in step."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestFingerprinting:
    def test_trailer_strips_directory(self):
        fp1 = fp_trailer("unpinned-uses", ".github/workflows/aeon.yml", "Setup Node")
        fp2 = fp_trailer("unpinned-uses", "aeon.yml", "Setup Node")
        assert fp1 == fp2

    def test_trailer_encodes_spaces_as_underscores(self):
        fp1 = fp_trailer("artipacked", "lint.yml", "Setup Node")
        fp2 = fp_trailer("artipacked", "lint.yml", "Setup_Node")
        assert fp1 == fp2

    def test_delta_does_not_substitute_spaces(self):
        fp1 = fp_delta("artipacked", "lint.yml", "Setup Node")
        fp2 = fp_delta("artipacked", "lint.yml", "Setup_Node")
        assert fp1 != fp2

    def test_trailer_and_delta_agree_when_no_spaces(self):
        # When the step has no spaces the two functions must return the same hash.
        fp1 = fp_trailer("zizmor/artipacked", "messages.yml", "Checkout")
        fp2 = fp_delta("zizmor/artipacked", "messages.yml", "Checkout")
        assert fp1 == fp2

    def test_different_rules_produce_different_fingerprints(self):
        fp1 = fp_trailer("unpinned-uses", "aeon.yml", "top")
        fp2 = fp_trailer("artipacked", "aeon.yml", "top")
        assert fp1 != fp2

    def test_different_files_produce_different_fingerprints(self):
        fp1 = fp_trailer("unpinned-uses", "aeon.yml", "top")
        fp2 = fp_trailer("unpinned-uses", "lint.yml", "top")
        assert fp1 != fp2

    def test_fingerprint_length_is_16_hex_chars(self):
        assert len(fp_trailer("x", "y.yml", "z")) == 16
        assert len(fp_delta("x", "y.yml", "z")) == 16


# ---------------------------------------------------------------------------
# Delta tagging logic  (delta3.py)
# ---------------------------------------------------------------------------

def tag_findings(findings, prior_counts):
    """
    Replicates the per-(rule, basename) tagging loop from delta3.py.
    First prior_count findings (sorted by line) → UNCHANGED; rest → NEW.
    Mutates each finding dict in-place and returns (new_list, unchanged_list).
    """
    seen = {}
    for f in findings:
        key = (f["short_rule"], os.path.basename(f["file"]))
        seen.setdefault(key, []).append(f)

    new_list, unchanged_list = [], []
    for key, group in seen.items():
        group_sorted = sorted(group, key=lambda x: x["line"])
        p = prior_counts.get(key, 0)
        for i, f in enumerate(group_sorted):
            if i < p:
                f["delta"] = "UNCHANGED"
                unchanged_list.append(f)
            else:
                f["delta"] = "NEW"
                new_list.append(f)
    return new_list, unchanged_list


def make_finding(rule, fname, line):
    return {"short_rule": rule, "file": fname, "line": line}


class TestDeltaTagging:
    def test_all_new_when_no_prior(self):
        findings = [make_finding("artipacked", "aeon.yml", 10),
                    make_finding("artipacked", "aeon.yml", 20)]
        new, unchanged = tag_findings(findings, prior_counts={})
        assert len(new) == 2
        assert len(unchanged) == 0

    def test_all_unchanged_when_prior_equals_today(self):
        findings = [make_finding("artipacked", "aeon.yml", 10),
                    make_finding("artipacked", "aeon.yml", 20)]
        new, unchanged = tag_findings(findings, {("artipacked", "aeon.yml"): 2})
        assert len(new) == 0
        assert len(unchanged) == 2

    def test_partial_new_when_today_exceeds_prior(self):
        findings = [make_finding("unpinned-uses", "lint.yml", 5),
                    make_finding("unpinned-uses", "lint.yml", 15),
                    make_finding("unpinned-uses", "lint.yml", 25)]
        new, unchanged = tag_findings(findings, {("unpinned-uses", "lint.yml"): 2})
        assert len(unchanged) == 2
        assert len(new) == 1
        # The NEW one must be the finding at the highest line number.
        assert new[0]["line"] == 25

    def test_all_unchanged_when_today_below_prior(self):
        # Only 1 finding today but prior had 3 — all today's are UNCHANGED.
        findings = [make_finding("artipacked", "messages.yml", 7)]
        new, unchanged = tag_findings(findings, {("artipacked", "messages.yml"): 3})
        assert len(new) == 0
        assert len(unchanged) == 1

    def test_independent_per_file(self):
        findings = [
            make_finding("artipacked", "aeon.yml", 1),
            make_finding("artipacked", "lint.yml", 1),
        ]
        prior = {("artipacked", "aeon.yml"): 1, ("artipacked", "lint.yml"): 0}
        new, unchanged = tag_findings(findings, prior)
        assert len(unchanged) == 1
        assert unchanged[0]["file"] == "aeon.yml"
        assert len(new) == 1
        assert new[0]["file"] == "lint.yml"

    def test_basename_normalisation(self):
        # Full paths should behave the same as basenames for matching.
        findings = [make_finding("artipacked", ".github/workflows/aeon.yml", 1)]
        prior = {("artipacked", "aeon.yml"): 1}
        new, unchanged = tag_findings(findings, prior)
        assert len(unchanged) == 1


# ---------------------------------------------------------------------------
# Calibration overrides  (delta.py  +  finalize.py)
# ---------------------------------------------------------------------------

def apply_delta_calibration(findings):
    """Matches delta.py: unpinned-uses Critical → High."""
    for f in findings:
        if f["short_rule"] == "unpinned-uses" and f["severity"] == "Critical":
            f["severity"] = "High"
            f["calibrated"] = True
    return findings


def apply_finalize_calibration(findings):
    """Matches finalize.py: secrets-outside-env High → Medium."""
    for f in findings:
        if f["short_rule"] == "secrets-outside-env" and f["severity"] == "High":
            f["severity"] = "Medium"
            f.setdefault("calibrated_notes", []).append(
                "secrets-outside-env downgraded High->Medium"
            )
    return findings


class TestCalibrationOverrides:
    def test_unpinned_uses_critical_downgraded_to_high(self):
        f = {"short_rule": "unpinned-uses", "severity": "Critical"}
        apply_delta_calibration([f])
        assert f["severity"] == "High"
        assert f.get("calibrated") is True

    def test_unpinned_uses_high_not_changed(self):
        f = {"short_rule": "unpinned-uses", "severity": "High"}
        apply_delta_calibration([f])
        assert f["severity"] == "High"
        assert "calibrated" not in f

    def test_other_rule_critical_not_changed(self):
        f = {"short_rule": "artipacked", "severity": "Critical"}
        apply_delta_calibration([f])
        assert f["severity"] == "Critical"

    def test_secrets_outside_env_high_downgraded_to_medium(self):
        f = {"short_rule": "secrets-outside-env", "severity": "High"}
        apply_finalize_calibration([f])
        assert f["severity"] == "Medium"
        assert f["calibrated_notes"]

    def test_secrets_outside_env_medium_not_changed(self):
        f = {"short_rule": "secrets-outside-env", "severity": "Medium"}
        apply_finalize_calibration([f])
        assert f["severity"] == "Medium"
        assert "calibrated_notes" not in f

    def test_other_rule_high_not_downgraded_by_finalize(self):
        f = {"short_rule": "unpinned-uses", "severity": "High"}
        apply_finalize_calibration([f])
        assert f["severity"] == "High"

    def test_calibrations_are_independent(self):
        # Applying both in sequence should not double-downgrade.
        f = {"short_rule": "unpinned-uses", "severity": "Critical"}
        apply_delta_calibration([f])
        apply_finalize_calibration([f])
        assert f["severity"] == "High"
