#!/usr/bin/env python3
"""Tests for pure-logic functions in the .audit/ pipeline scripts.

extract_steps.py and classify.py define our_severity() identically.
gen_trailer.py and delta.py compute fingerprints with different step
encodings (underscores vs. spaces); delta.py papers over the gap with a
dual-lookup.  None of this had tests.

Run: python3 .audit/test_audit_logic.py
"""
import hashlib
import os
import sys


# ── our_severity ────────────────────────────────────────────────────────────
# Verbatim copy from extract_steps.py (same body exists in classify.py).
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


# ── fingerprint helpers ──────────────────────────────────────────────────────
def _sha16(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# extract_steps.py: rule|file|step  (step preserves spaces; file is SARIF basename)
def fp_current(rule, file, step):
    return _sha16(f"{rule}|{file}|{step}")


# gen_trailer.py: rule|basename(file)|step_with_underscores
def fp_trailer(rule, file, step):
    base = os.path.basename(file)
    return _sha16(f"{rule}|{base}|{step.replace(' ', '_')}")


# delta.py reconstruction from a trailer step field (underscores → spaces before hashing)
def fp_from_trailer_step(rule, file, step_underscored):
    base = os.path.basename(file)
    step_spaces = step_underscored.replace("_", " ")
    return _sha16(f"{rule}|{base}|{step_spaces}")


# ── tests ────────────────────────────────────────────────────────────────────

def test_our_severity():
    # error + high → Critical (case-insensitive confidence)
    assert our_severity({"level": "error", "confidence": "high"}) == "Critical"
    assert our_severity({"level": "error", "confidence": "High"}) == "Critical"
    assert our_severity({"level": "error", "confidence": "HIGH"}) == "Critical"

    # error + non-high confidence → High
    assert our_severity({"level": "error", "confidence": "medium"}) == "High"
    assert our_severity({"level": "error", "confidence": ""}) == "High"
    # missing confidence key defaults to "" → not "high" → High
    assert our_severity({"level": "error"}) == "High"

    # warning + high → High
    assert our_severity({"level": "warning", "confidence": "high"}) == "High"

    # warning + non-high → Medium
    assert our_severity({"level": "warning", "confidence": "medium"}) == "Medium"
    assert our_severity({"level": "warning", "confidence": ""}) == "Medium"
    assert our_severity({"level": "warning"}) == "Medium"

    # note level always → Low, even when confidence is high
    assert our_severity({"level": "note", "confidence": "high"}) == "Low"
    assert our_severity({"level": "note"}) == "Low"

    # unknown / empty levels fall through to Low
    assert our_severity({"level": "info"}) == "Low"
    assert our_severity({"level": ""}) == "Low"

    print("OK  our_severity: 14 branches/edge-cases")


def test_fingerprint_round_trip():
    rule = "artipacked"
    file = "aeon.yml"
    step_spaces = "Early checkout"
    step_underscores = "Early_checkout"

    current_fp = fp_current(rule, file, step_spaces)
    trailer_fp = fp_trailer(rule, file, step_spaces)

    # extract_steps.py (current) and gen_trailer.py produce different hashes
    # for the same step because of the space→underscore encoding difference.
    assert current_fp != trailer_fp, (
        "current and trailer fingerprints should differ (space vs. underscore encoding)"
    )

    # delta.py works around this by converting underscore→space before recomputing.
    # The reconstructed fingerprint must match the current finding's fingerprint.
    reconstructed = fp_from_trailer_step(rule, file, step_underscores)
    assert reconstructed == current_fp, (
        f"delta reconstruction must match current fp: {reconstructed!r} != {current_fp!r}"
    )

    # Step names that naturally contain underscores (not from space→underscore
    # conversion) do NOT round-trip — this is a known limitation of the scheme.
    natural_underscore = "setup_node"
    fp_natural = fp_current(rule, file, natural_underscore)
    fp_rt = fp_from_trailer_step(rule, file, natural_underscore)
    # reconstruction converts 'setup_node' → 'setup node', producing a different hash
    assert fp_natural != fp_rt, (
        "natural underscores in step names break the round-trip (documented limitation)"
    )

    print("OK  fingerprint round-trip: space↔underscore encoding and natural-underscore limitation")


def test_short_rule_extraction():
    # rule_id.split('/')[-1] is used throughout the scripts for display
    assert "zizmor/artipacked".split("/")[-1] == "artipacked"
    assert "zizmor/template-injection".split("/")[-1] == "template-injection"
    assert "artipacked".split("/")[-1] == "artipacked"  # no slash → unchanged
    print("OK  short_rule extraction via split('/')[-1]")


if __name__ == "__main__":
    test_our_severity()
    test_fingerprint_round_trip()
    test_short_rule_extraction()
    print("\nAll .audit logic tests passed.")
    sys.exit(0)
