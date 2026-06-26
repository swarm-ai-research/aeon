"""Tests for severity-mapping and fingerprint logic used by classify.py and gen_trailer.py.

The .audit scripts are not importable (top-level file I/O), so the pure functions
are re-stated here verbatim and tested for edge cases.
"""
import hashlib
import os
import re


# ── Pure helpers from classify.py ─────────────────────────────────────────────

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


def classify_fingerprint(short_rule, file_path, snippet):
    """Mirror of the fingerprint built in classify.py (keyed on snippet, not step)."""
    snip_key = re.sub(r"\s+", " ", snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── Pure helper from gen_trailer.py ───────────────────────────────────────────

def trailer_fp(rule, fname, step):
    """Mirror of fp() in gen_trailer.py — spaces in step become underscores."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Tests: our_severity ───────────────────────────────────────────────────────

class TestOurSeverity:
    def test_error_high_confidence_is_critical(self):
        assert our_severity({"level": "error", "confidence": "high"}) == "Critical"

    def test_confidence_comparison_is_case_insensitive(self):
        # .lower() is called before comparison, so uppercase variants must still map Critical
        assert our_severity({"level": "error", "confidence": "HIGH"}) == "Critical"
        assert our_severity({"level": "error", "confidence": "High"}) == "Critical"

    def test_error_medium_confidence_is_high_not_critical(self):
        # Only 'high' confidence escalates to Critical; anything else stays High
        assert our_severity({"level": "error", "confidence": "medium"}) == "High"

    def test_error_missing_confidence_key_is_high(self):
        # .get("confidence", "") defaults to "" which is not "high"
        assert our_severity({"level": "error"}) == "High"

    def test_error_empty_confidence_is_high(self):
        assert our_severity({"level": "error", "confidence": ""}) == "High"

    def test_warning_high_confidence_is_high(self):
        assert our_severity({"level": "warning", "confidence": "high"}) == "High"

    def test_warning_low_confidence_is_medium(self):
        assert our_severity({"level": "warning", "confidence": "low"}) == "Medium"

    def test_warning_missing_confidence_is_medium(self):
        assert our_severity({"level": "warning"}) == "Medium"

    def test_note_level_is_low_regardless_of_confidence(self):
        # note-level findings fall through all conditions to the final 'Low'
        assert our_severity({"level": "note", "confidence": "high"}) == "Low"
        assert our_severity({"level": "note"}) == "Low"

    def test_unrecognised_level_is_low(self):
        assert our_severity({"level": "none"}) == "Low"
        assert our_severity({"level": ""}) == "Low"

    # Boundary relevant to delta.py calibration override:
    # unpinned-uses with error+high gets Critical here, then delta.py downgrades
    # it to High. The override only fires when severity == 'Critical', so the
    # mapping must be exact.
    def test_calibration_prereq_unpinned_uses_scenario(self):
        finding = {"level": "error", "confidence": "high"}
        assert our_severity(finding) == "Critical"  # triggers calibration in delta.py


# ── Tests: classify_fingerprint ───────────────────────────────────────────────

class TestClassifyFingerprint:
    def test_output_is_16_lowercase_hex_chars(self):
        fp = classify_fingerprint("injection", ".github/workflows/aeon.yml", "foo bar")
        assert len(fp) == 16
        assert all(c in "0123456789abcdef" for c in fp)

    def test_directory_portion_of_file_is_ignored(self):
        fp_full = classify_fingerprint("injection", ".github/workflows/aeon.yml", "foo")
        fp_base = classify_fingerprint("injection", "aeon.yml", "foo")
        assert fp_full == fp_base

    def test_whitespace_in_snippet_is_collapsed(self):
        fp1 = classify_fingerprint("rule", "file.yml", "foo   bar")
        fp2 = classify_fingerprint("rule", "file.yml", "foo bar")
        assert fp1 == fp2

    def test_snippet_truncated_at_60_chars(self):
        long_snippet = "x" * 100
        truncated = "x" * 60
        assert classify_fingerprint("r", "f.yml", long_snippet) == classify_fingerprint("r", "f.yml", truncated)

    def test_snippet_under_60_chars_not_padded(self):
        short = "abc"
        assert classify_fingerprint("r", "f.yml", short) != classify_fingerprint("r", "f.yml", short + " ")

    def test_different_rules_produce_different_fingerprints(self):
        assert classify_fingerprint("rule-a", "f.yml", "s") != classify_fingerprint("rule-b", "f.yml", "s")

    def test_different_files_produce_different_fingerprints(self):
        assert classify_fingerprint("rule", "a.yml", "s") != classify_fingerprint("rule", "b.yml", "s")

    def test_empty_snippet_is_valid(self):
        fp = classify_fingerprint("rule", "f.yml", "")
        assert len(fp) == 16


# ── Tests: trailer_fp ─────────────────────────────────────────────────────────

class TestTrailerFp:
    def test_output_is_16_lowercase_hex_chars(self):
        fp = trailer_fp("injection", ".github/workflows/aeon.yml", "Checkout")
        assert len(fp) == 16
        assert all(c in "0123456789abcdef" for c in fp)

    def test_spaces_in_step_become_underscores(self):
        # gen_trailer writes steps with underscores; delta.py reads them back the same way
        fp_space = trailer_fp("rule", "f.yml", "Setup Node")
        fp_under = trailer_fp("rule", "f.yml", "Setup_Node")
        assert fp_space == fp_under

    def test_basename_only_for_file(self):
        fp_full = trailer_fp("rule", ".github/workflows/aeon.yml", "step")
        fp_base = trailer_fp("rule", "aeon.yml", "step")
        assert fp_full == fp_base

    def test_different_steps_produce_different_fingerprints(self):
        assert trailer_fp("rule", "f.yml", "step-a") != trailer_fp("rule", "f.yml", "step-b")

    def test_empty_step_is_valid(self):
        fp = trailer_fp("rule", "f.yml", "")
        assert len(fp) == 16
