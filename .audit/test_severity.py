"""
Tests for zizmor SARIF severity -> our severity mapping (classify.py logic).

The function is duplicated here (not imported) because classify.py has
module-level side effects (reads .audit/parsed.json at import time).

Run: python3 .audit/test_severity.py
"""

import sys
import hashlib
import os


# ── our_severity — from classify.py ──────────────────────────────────────────
# SKILL.md mapping:
#   error + confidence >= high → Critical
#   error (other confidence) or warning + confidence = high → High
#   warning → Medium
#   note → Low

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


# ── fp_for — from delta.py ────────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── test harness ──────────────────────────────────────────────────────────────

passed = failed = 0

def check(label, got, expected):
    global passed, failed
    if got == expected:
        print(f"  OK  {label}")
        passed += 1
    else:
        print(f"  FAIL {label}: expected {expected!r}, got {got!r}", file=sys.stderr)
        failed += 1


# ── our_severity tests ────────────────────────────────────────────────────────

print("our_severity:")

# Core documented branches
check("error+high → Critical",
      our_severity({"level": "error", "confidence": "high"}), "Critical")
check("error+medium → High",
      our_severity({"level": "error", "confidence": "medium"}), "High")
check("error+low → High",
      our_severity({"level": "error", "confidence": "low"}), "High")
check("warning+high → High",
      our_severity({"level": "warning", "confidence": "high"}), "High")
check("warning+medium → Medium",
      our_severity({"level": "warning", "confidence": "medium"}), "Medium")
check("warning+low → Medium",
      our_severity({"level": "warning", "confidence": "low"}), "Medium")
check("note → Low",
      our_severity({"level": "note", "confidence": "high"}), "Low")
check("note without confidence → Low",
      our_severity({"level": "note"}), "Low")

# Edge cases
check("error+HIGH (uppercase) → Critical — confidence is lowercased before compare",
      our_severity({"level": "error", "confidence": "HIGH"}), "Critical")
check("warning+HIGH (uppercase) → High",
      our_severity({"level": "warning", "confidence": "HIGH"}), "High")
check("error without confidence key → High (missing field treated as other confidence)",
      our_severity({"level": "error"}), "High")
check("warning without confidence key → Medium",
      our_severity({"level": "warning"}), "Medium")
check("unknown level → Low (falls through to default)",
      our_severity({"level": "unknown"}), "Low")
check("empty level → Low",
      our_severity({"level": ""}), "Low")


# ── fp_for tests ──────────────────────────────────────────────────────────────

print("\nfp_for:")

# Fingerprint is 16 hex chars
fp = fp_for("template-injection", ".github/workflows/messages.yml", "Extract message")
check("fingerprint length is 16", len(fp), 16)
check("fingerprint is hex", all(c in "0123456789abcdef" for c in fp), True)

# Uses basename only — full path and bare name produce the same fingerprint
fp_full = fp_for("unpinned-uses", ".github/workflows/aeon.yml", "Checkout")
fp_base = fp_for("unpinned-uses", "aeon.yml", "Checkout")
check("full path and bare filename produce the same fingerprint", fp_full, fp_base)

# Different step names produce different fingerprints
fp_a = fp_for("unpinned-uses", "aeon.yml", "Checkout")
fp_b = fp_for("unpinned-uses", "aeon.yml", "Setup Node")
check("different step → different fingerprint", fp_a != fp_b, True)

# Different rules produce different fingerprints
fp_c = fp_for("template-injection", "aeon.yml", "Run")
fp_d = fp_for("unpinned-uses", "aeon.yml", "Run")
check("different rule → different fingerprint", fp_c != fp_d, True)

# Deterministic across calls
fp_e = fp_for("artipacked", "chain-runner.yml", "Upload artifact")
fp_f = fp_for("artipacked", "chain-runner.yml", "Upload artifact")
check("same inputs → same fingerprint (deterministic)", fp_e, fp_f)

# Empty fname → basename is ""
fp_empty = fp_for("some-rule", "", "step")
check("empty fname produces 16-char fingerprint without error", len(fp_empty), 16)


# ── summary ──────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed.")
if failed:
    sys.exit(1)
