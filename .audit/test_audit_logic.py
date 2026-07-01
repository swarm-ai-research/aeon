"""
test_audit_logic.py — Unit tests for audit script logic.

Tests the pure functions extracted from classify.py, delta.py, and
parse_sarif.py without touching the filesystem.

Run: python3 .audit/test_audit_logic.py
"""

import hashlib
import os
import sys

passed = 0
failed = 0


def assert_eq(got, want, label):
    global passed, failed
    if got == want:
        passed += 1
        print(f"  ✓ {label}")
    else:
        failed += 1
        print(f"  ✗ {label}: got {got!r}, want {want!r}", file=sys.stderr)


# ── our_severity (classify.py) ────────────────────────────────────────────────
#
# Mapping:
#   error  + high confidence  → Critical
#   error  + other confidence → High
#   warning + high confidence → High
#   warning + other           → Medium
#   anything else             → Low

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

assert_eq(our_severity({"level": "error", "confidence": "high"}), "Critical", "error+high → Critical")
assert_eq(our_severity({"level": "error", "confidence": "HIGH"}), "Critical", "error+HIGH (uppercase) → Critical (case-insensitive)")
assert_eq(our_severity({"level": "error", "confidence": "medium"}), "High", "error+medium → High")
assert_eq(our_severity({"level": "error", "confidence": "low"}), "High", "error+low → High")
assert_eq(our_severity({"level": "error", "confidence": ""}), "High", "error+empty confidence → High")
assert_eq(our_severity({"level": "error"}), "High", "error+missing confidence → High")
assert_eq(our_severity({"level": "warning", "confidence": "high"}), "High", "warning+high → High")
assert_eq(our_severity({"level": "warning", "confidence": "HIGH"}), "High", "warning+HIGH (uppercase) → High (case-insensitive)")
assert_eq(our_severity({"level": "warning", "confidence": "medium"}), "Medium", "warning+medium → Medium")
assert_eq(our_severity({"level": "warning", "confidence": "low"}), "Medium", "warning+low → Medium")
assert_eq(our_severity({"level": "warning", "confidence": ""}), "Medium", "warning+empty → Medium")
assert_eq(our_severity({"level": "note", "confidence": "high"}), "Low", "note+high → Low (else branch)")
assert_eq(our_severity({"level": "note", "confidence": ""}), "Low", "note+empty → Low")
assert_eq(our_severity({"level": "none", "confidence": "high"}), "Low", "unknown level → Low")
assert_eq(our_severity({"level": ""}), "Low", "empty level → Low")


# ── fp_for (delta.py) ─────────────────────────────────────────────────────────
#
# Fingerprint: sha256(rule|basename(file)|step)[:16]

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


print("\nfp_for:")

# Determinism
fp1 = fp_for("unpinned-uses", ".github/workflows/ci.yml", "Setup Node")
fp2 = fp_for("unpinned-uses", ".github/workflows/ci.yml", "Setup Node")
assert_eq(fp1, fp2, "same inputs → identical fingerprint (deterministic)")

# Basename extraction: full path vs just filename should produce same result
fp_full = fp_for("unpinned-uses", "/home/runner/work/repo/.github/workflows/ci.yml", "Setup Node")
fp_base = fp_for("unpinned-uses", ".github/workflows/ci.yml", "Setup Node")
assert_eq(fp_full, fp_base, "full path and relative path produce same fingerprint (basename)")

# Different rule → different fingerprint
fp_rule_a = fp_for("injection", "ci.yml", "Build")
fp_rule_b = fp_for("unpinned-uses", "ci.yml", "Build")
assert_eq(fp_rule_a == fp_rule_b, False, "different rules → different fingerprints")

# Different file → different fingerprint
fp_file_a = fp_for("injection", "ci.yml", "Build")
fp_file_b = fp_for("injection", "deploy.yml", "Build")
assert_eq(fp_file_a == fp_file_b, False, "different files → different fingerprints")

# Different step → different fingerprint
fp_step_a = fp_for("injection", "ci.yml", "Setup Node")
fp_step_b = fp_for("injection", "ci.yml", "Build")
assert_eq(fp_step_a == fp_step_b, False, "different steps → different fingerprints")

# Output is always 16 hex chars
assert_eq(len(fp_for("x", "y", "z")), 16, "fingerprint is 16 characters")
assert_eq(all(c in "0123456789abcdef" for c in fp_for("x", "y", "z")), True, "fingerprint is hex")

# Step underscore vs space (delta.py normalises by trying both variants)
fp_underscore = fp_for("injection", "ci.yml", "Setup_Node")
fp_space = fp_for("injection", "ci.yml", "Setup Node")
assert_eq(fp_underscore == fp_space, False, "underscore vs space step → different fps (caller normalises)")


# ── parse_sarif severity fallback (parse_sarif.py) ───────────────────────────
#
# props.get('problem.severity') or props.get('zizmor/severity') or props.get('security-severity', '')

def sarif_severity(props):
    return (
        props.get("problem.severity")
        or props.get("zizmor/severity")
        or props.get("security-severity", "")
    )


print("\nsarif_severity fallback chain:")

assert_eq(sarif_severity({"problem.severity": "high"}), "high", "problem.severity wins when present")
assert_eq(
    sarif_severity({"problem.severity": "high", "zizmor/severity": "medium", "security-severity": "low"}),
    "high",
    "problem.severity wins over all others",
)
assert_eq(
    sarif_severity({"zizmor/severity": "medium", "security-severity": "low"}),
    "medium",
    "falls back to zizmor/severity when problem.severity absent",
)
assert_eq(
    sarif_severity({"problem.severity": "", "zizmor/severity": "medium"}),
    "medium",
    "empty problem.severity falls through to zizmor/severity",
)
assert_eq(
    sarif_severity({"security-severity": "8.0"}),
    "8.0",
    "falls back to security-severity when both others absent",
)
assert_eq(
    sarif_severity({}),
    "",
    "all absent → empty string",
)
assert_eq(
    sarif_severity({"problem.severity": None, "zizmor/severity": "low"}),
    "low",
    "None problem.severity falls through (falsy)",
)


# ── Results ──────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
if failed:
    sys.exit(1)
