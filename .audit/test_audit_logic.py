#!/usr/bin/env python3
"""
Tests for the audit pipeline logic.

Run: python .audit/test_audit_logic.py

Covers edge cases in classify.py, summarize_al.py, and parse_sarif.py
that are not exercised by any live audit run.
"""
import hashlib
import os
import re
import sys
from collections import Counter

passed = 0
failed = 0


def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ok  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}", file=sys.stderr)


# ── our_severity (from classify.py) ─────────────────────────────────────────
# Inlined here so tests don't depend on file-reading side effects at import.

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


print("our_severity:")

check(our_severity({"level": "error", "confidence": "high"}) == "Critical",
      "error + high confidence → Critical")

check(our_severity({"level": "error", "confidence": "medium"}) == "High",
      "error + medium confidence → High (not Critical)")

check(our_severity({"level": "error", "confidence": ""}) == "High",
      "error + empty confidence → High")

check(our_severity({"level": "error"}) == "High",
      "error with no confidence key → High")

check(our_severity({"level": "warning", "confidence": "high"}) == "High",
      "warning + high confidence → High")

check(our_severity({"level": "warning", "confidence": "low"}) == "Medium",
      "warning + low confidence → Medium")

check(our_severity({"level": "warning", "confidence": ""}) == "Medium",
      "warning + empty confidence → Medium")

# The else branch — 'note' and any unrecognised level fall through to Low
check(our_severity({"level": "note", "confidence": "high"}) == "Low",
      "note level → Low (else branch, even with high confidence)")

check(our_severity({"level": "note", "confidence": ""}) == "Low",
      "note + empty confidence → Low")

check(our_severity({"level": "open", "confidence": "high"}) == "Low",
      "unknown level → Low (else branch)")

# Confidence comparison is case-insensitive (.lower() applied)
check(our_severity({"level": "error", "confidence": "HIGH"}) == "Critical",
      "confidence 'HIGH' (upper-case) still matches → Critical")

check(our_severity({"level": "warning", "confidence": "High"}) == "High",
      "confidence 'High' (mixed-case) still matches → High")


# ── fingerprint (from classify.py) ──────────────────────────────────────────

def make_fingerprint(rule_id, file_uri, snippet):
    short_rule = rule_id.split("/")[-1]
    snip_key = re.sub(r"\s+", " ", snippet)[:60]
    file_short = os.path.basename(file_uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


print("\nfingerprint:")

fp1 = make_fingerprint(
    "zizmor/unpinned-uses",
    ".github/workflows/aeon.yml",
    "uses: actions/checkout@v4",
)
check(len(fp1) == 16, "fingerprint is 16 hex chars")
check(all(c in "0123456789abcdef" for c in fp1), "fingerprint is lowercase hex")

# Same inputs → same fingerprint (determinism)
fp2 = make_fingerprint(
    "zizmor/unpinned-uses",
    ".github/workflows/aeon.yml",
    "uses: actions/checkout@v4",
)
check(fp1 == fp2, "fingerprint is deterministic")

# Different rule → different fingerprint
fp3 = make_fingerprint(
    "zizmor/secrets-outside-env",
    ".github/workflows/aeon.yml",
    "uses: actions/checkout@v4",
)
check(fp1 != fp3, "different rule → different fingerprint")

# rule_id with slashes: only last segment used (split('/')[-1])
fp_slashed = make_fingerprint("a/b/my-rule", "dir/file.yml", "snip")
fp_bare = make_fingerprint("my-rule", "dir/file.yml", "snip")
check(fp_slashed == fp_bare, "rule_id split('/') uses only last segment")

# file_uri: only basename used
fp_with_path = make_fingerprint("rule", "nested/dir/workflow.yml", "snip")
fp_basename = make_fingerprint("rule", "workflow.yml", "snip")
check(fp_with_path == fp_basename, "file_uri reduced to basename for fingerprint")

# snippet: whitespace is normalised and truncated at 60 chars
long_snippet = "x " * 100  # 200 chars
fp_long = make_fingerprint("rule", "f.yml", long_snippet)
normalised = re.sub(r"\s+", " ", long_snippet)[:60]
fp_norm = make_fingerprint("rule", "f.yml", normalised)
check(fp_long == fp_norm, "snippet normalised and capped at 60 chars in fingerprint")


# ── shellcheck code classification (from summarize_al.py) ────────────────────

KNOWN_CODES = ["SC2086", "SC2046", "SC2129", "SC2153", "SC2155", "SC2034"]


def classify_shellcheck_message(msg):
    """Return the first matching shellcheck code, or 'other'."""
    for code in KNOWN_CODES:
        if code in msg:
            return code
    return "other"


def is_high_candidate(msg):
    """True when message contains an unquoted-expansion code and references github.*."""
    return ("SC2086" in msg or "SC2046" in msg) and "github." in msg.lower()


print("\nshellcheck code classification:")

check(classify_shellcheck_message("SC2086: Double quote to prevent globbing") == "SC2086",
      "SC2086 message → SC2086")

check(classify_shellcheck_message("SC2046: Quote this to prevent word splitting") == "SC2046",
      "SC2046 message → SC2046")

check(classify_shellcheck_message("Some unrelated lint warning") == "other",
      "unrecognised message → other")

# Edge case: message contains BOTH SC2086 and SC2046 — only the first wins (break)
check(
    classify_shellcheck_message("SC2086 and SC2046 both mentioned here") == "SC2086",
    "message with both SC2086 and SC2046 → first match wins (SC2086)",
)

# Another ordering edge: SC2046 appears but not SC2086
check(classify_shellcheck_message("SC2046 only") == "SC2046",
      "SC2046 alone → SC2046")

# HIGH-CANDIDATE detection
check(is_high_candidate("SC2086 applies to ${{ github.event.inputs.var }}"),
      "SC2086 + 'github.' → HIGH-CANDIDATE")

check(is_high_candidate("SC2046 applies to ${{ GITHUB.TOKEN }}"),
      "SC2046 + 'github.' (any case) → HIGH-CANDIDATE")

check(not is_high_candidate("SC2086 applies to $HOME"),
      "SC2086 without 'github.' → not HIGH-CANDIDATE")

check(not is_high_candidate("${{ github.ref }} but no shellcheck code"),
      "'github.' without SC2086/SC2046 → not HIGH-CANDIDATE")


# ── SARIF location parsing (from parse_sarif.py) ─────────────────────────────

def parse_sarif_result(r):
    """Extract location fields from a single SARIF result dict."""
    locs = r.get("locations", [])
    if locs:
        phys = locs[0].get("physicalLocation", {})
        uri = phys.get("artifactLocation", {}).get("uri", "")
        region = phys.get("region", {})
        line = region.get("startLine", 0)
        snippet = region.get("snippet", {}).get("text", "")
    else:
        uri = ""
        line = 0
        snippet = ""
    return uri, line, snippet[:200]


print("\nSARIF location parsing:")

# Normal result with a location
r_normal = {
    "locations": [{
        "physicalLocation": {
            "artifactLocation": {"uri": ".github/workflows/aeon.yml"},
            "region": {"startLine": 42, "snippet": {"text": "uses: actions/checkout@v4"}},
        }
    }]
}
uri, line, snippet = parse_sarif_result(r_normal)
check(uri == ".github/workflows/aeon.yml", "normal result: uri extracted")
check(line == 42, "normal result: line extracted")
check(snippet == "uses: actions/checkout@v4", "normal result: snippet extracted")

# Edge case: empty locations list
r_empty_locs = {"locations": []}
uri, line, snippet = parse_sarif_result(r_empty_locs)
check(uri == "", "empty locations → uri is empty string")
check(line == 0, "empty locations → line is 0")
check(snippet == "", "empty locations → snippet is empty string")

# Edge case: missing locations key entirely
r_no_locs = {}
uri, line, snippet = parse_sarif_result(r_no_locs)
check(uri == "", "missing locations key → uri is empty string")
check(line == 0, "missing locations key → line is 0")

# Edge case: snippet longer than 200 chars is truncated
long_text = "A" * 250
r_long_snip = {
    "locations": [{
        "physicalLocation": {
            "artifactLocation": {"uri": "f.yml"},
            "region": {"startLine": 1, "snippet": {"text": long_text}},
        }
    }]
}
_, _, snip_out = parse_sarif_result(r_long_snip)
check(len(snip_out) == 200, "snippet truncated to 200 chars")
check(snip_out == "A" * 200, "truncated snippet contains correct content")

# Edge case: region present but no snippet key
r_no_snippet = {
    "locations": [{
        "physicalLocation": {
            "artifactLocation": {"uri": "f.yml"},
            "region": {"startLine": 5},
        }
    }]
}
uri, line, snippet = parse_sarif_result(r_no_snippet)
check(snippet == "", "missing snippet key → empty string")
check(line == 5, "startLine still extracted when snippet absent")

# Edge case: missing region entirely
r_no_region = {
    "locations": [{
        "physicalLocation": {
            "artifactLocation": {"uri": "f.yml"},
        }
    }]
}
uri, line, snippet = parse_sarif_result(r_no_region)
check(line == 0, "missing region → line defaults to 0")
check(snippet == "", "missing region → snippet defaults to empty")


# ── Results ──────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
if failed:
    sys.exit(1)
