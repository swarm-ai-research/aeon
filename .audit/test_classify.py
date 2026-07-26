"""Tests for classify.py and gen_trailer.py helper functions.

Run: python .audit/test_classify.py
"""
import hashlib
import os
import re
import sys

passed = 0
failed = 0


def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}", file=sys.stderr)


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


def classify_fingerprint(short_rule, file_path, snippet):
    snip_key = re.sub(r"\s+", " ", snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── Extracted from gen_trailer.py ─────────────────────────────────────────────

def trailer_fp(rule, fname, step):
    """gen_trailer.py normalises step spaces → underscores before hashing."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Extracted from delta.py ───────────────────────────────────────────────────

def delta_fp_for(rule, fname, step):
    """delta.py does NOT normalise spaces in step."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── our_severity tests ────────────────────────────────────────────────────────

print("our_severity:")

check(
    our_severity({"level": "error", "confidence": "high"}) == "Critical",
    "error + high confidence → Critical",
)
check(
    our_severity({"level": "error", "confidence": "High"}) == "Critical",
    "error + title-cased confidence → Critical (case-insensitive)",
)
check(
    our_severity({"level": "error", "confidence": "medium"}) == "High",
    "error + non-high confidence → High",
)
check(
    our_severity({"level": "error"}) == "High",
    "error with no confidence key → High",
)
check(
    our_severity({"level": "error", "confidence": ""}) == "High",
    "error with empty confidence → High",
)
check(
    our_severity({"level": "warning", "confidence": "high"}) == "High",
    "warning + high confidence → High",
)
check(
    our_severity({"level": "warning", "confidence": "low"}) == "Medium",
    "warning + low confidence → Medium",
)
check(
    our_severity({"level": "warning"}) == "Medium",
    "warning with no confidence key → Medium",
)
check(
    our_severity({"level": "note", "confidence": "high"}) == "Low",
    "note level → Low regardless of confidence",
)
check(
    our_severity({"level": "none", "confidence": "high"}) == "Low",
    "unknown level → Low (default branch)",
)

# ── classify_fingerprint tests ────────────────────────────────────────────────

print("\nclassify_fingerprint:")

fp1 = classify_fingerprint("unpinned-uses", ".github/workflows/aeon.yml", "uses: actions/checkout@v3")
check(len(fp1) == 16, "fingerprint is 16 hex chars")
check(all(c in "0123456789abcdef" for c in fp1), "fingerprint is lowercase hex")

# Deterministic: same inputs → same output
fp2 = classify_fingerprint("unpinned-uses", ".github/workflows/aeon.yml", "uses: actions/checkout@v3")
check(fp1 == fp2, "fingerprint is deterministic")

# Different rule → different fingerprint
fp3 = classify_fingerprint("artipacked", ".github/workflows/aeon.yml", "uses: actions/checkout@v3")
check(fp1 != fp3, "different rule → different fingerprint")

# File path is basename-only (full path == basename path)
fp_full = classify_fingerprint("artipacked", "/long/path/to/aeon.yml", "snippet")
fp_base = classify_fingerprint("artipacked", "aeon.yml", "snippet")
check(fp_full == fp_base, "full path and basename give same fingerprint")

# Snippet whitespace is collapsed before the 60-char slice
fp_ws1 = classify_fingerprint("rule", "f.yml", "hello   world")
fp_ws2 = classify_fingerprint("rule", "f.yml", "hello world")
check(fp_ws1 == fp_ws2, "snippet whitespace is normalised before fingerprinting")

# Long snippet is sliced to 60 chars
long_snip = "x" * 100
short_snip = "x" * 60
check(
    classify_fingerprint("rule", "f.yml", long_snip) == classify_fingerprint("rule", "f.yml", short_snip),
    "snippet truncated to 60 chars before fingerprinting",
)

# ── gen_trailer vs delta fingerprint scheme ───────────────────────────────────

print("\nfingerprint scheme consistency (gen_trailer vs delta):")

# Steps without spaces: both schemes agree
fp_t = trailer_fp("unpinned-uses", "aeon.yml", "Checkout")
fp_d = delta_fp_for("unpinned-uses", "aeon.yml", "Checkout")
check(fp_t == fp_d, "no-space step: gen_trailer and delta agree")

# Steps WITH spaces: the two schemes intentionally differ
fp_t2 = trailer_fp("unpinned-uses", "aeon.yml", "Setup Node")
fp_d2 = delta_fp_for("unpinned-uses", "aeon.yml", "Setup Node")
check(fp_t2 != fp_d2, "spaced step: gen_trailer (underscore) and delta (raw) differ")

# delta_fp_for with pre-underscored step matches trailer_fp with spaced step
fp_d3 = delta_fp_for("unpinned-uses", "aeon.yml", "Setup_Node")
check(fp_t2 == fp_d3, "delta with underscore step matches trailer with spaced step")


# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
