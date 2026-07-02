"""
test_audit_logic.py — Unit tests for pure functions extracted from the .audit/ pipeline.

Run: python .audit/test_audit_logic.py
"""

import hashlib
import os
import sys

passed = 0
failed = 0


def ok(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}", file=sys.stderr)


# ── our_severity (from classify.py / extract_steps.py) ──────────────────────
# Same function appears in both files; test the shared contract.

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
ok(our_severity({"level": "error", "confidence": "high"}) == "Critical",
   "error + high → Critical")
ok(our_severity({"level": "error", "confidence": "HIGH"}) == "Critical",
   "error + HIGH (uppercase) → Critical (confidence lowercased)")
ok(our_severity({"level": "error", "confidence": "low"}) == "High",
   "error + low → High (not Critical)")
ok(our_severity({"level": "error", "confidence": ""}) == "High",
   "error + empty confidence → High")
ok(our_severity({"level": "error"}) == "High",
   "error + missing confidence key → High")
ok(our_severity({"level": "warning", "confidence": "high"}) == "High",
   "warning + high → High")
ok(our_severity({"level": "warning", "confidence": "low"}) == "Medium",
   "warning + low → Medium")
ok(our_severity({"level": "warning"}) == "Medium",
   "warning + missing confidence → Medium")
ok(our_severity({"level": "note"}) == "Low",
   "note → Low (fallback)")
ok(our_severity({"level": "none", "confidence": "high"}) == "Low",
   "unknown level → Low even with high confidence")


# ── fingerprint computation (extract_steps.py scheme) ───────────────────────
# fp = sha256(short_rule|file|step)[:16]

def compute_fingerprint_step(short_rule, file_path, step):
    src = f"{short_rule}|{file_path}|{step}"
    return hashlib.sha256(src.encode()).hexdigest()[:16]


# delta.py fp_for uses basename(file), extract_steps.py uses full file path
def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


print("\nfingerprint computation:")
fp1 = compute_fingerprint_step("unpinned-uses", "aeon.yml", "Checkout")
ok(len(fp1) == 16, "fingerprint is exactly 16 hex chars")
ok(all(c in "0123456789abcdef" for c in fp1), "fingerprint is lowercase hex")

ok(compute_fingerprint_step("unpinned-uses", "aeon.yml", "Checkout") ==
   compute_fingerprint_step("unpinned-uses", "aeon.yml", "Checkout"),
   "identical inputs → identical fingerprint")
ok(compute_fingerprint_step("unpinned-uses", "aeon.yml", "Checkout") !=
   compute_fingerprint_step("unpinned-uses", "aeon.yml", "Build"),
   "different step → different fingerprint")
ok(compute_fingerprint_step("unpinned-uses", "aeon.yml", "Step") !=
   compute_fingerprint_step("artipacked", "aeon.yml", "Step"),
   "different rule → different fingerprint")

# fp_for uses basename — so full path and basename should match
ok(fp_for("unpinned-uses", ".github/workflows/aeon.yml", "Deploy") ==
   fp_for("unpinned-uses", "aeon.yml", "Deploy"),
   "fp_for: full path and basename produce same fingerprint")
ok(fp_for("unpinned-uses", "aeon.yml", "Setup Node") ==
   fp_for("unpinned-uses", "aeon.yml", "Setup Node"),
   "fp_for: spaces in step names are preserved as-is")
ok(fp_for("unpinned-uses", "aeon.yml", "Setup_Node") !=
   fp_for("unpinned-uses", "aeon.yml", "Setup Node"),
   "fp_for: underscore vs space in step → different fingerprint")


# ── delta assignment (delta2.py / delta3.py algorithm) ──────────────────────
# First `prior_count` findings (by ascending line) are UNCHANGED; the rest are NEW.

def assign_delta(findings, prior_count):
    """Tag each finding dict in-place; returns (new_list, unchanged_list)."""
    sorted_findings = sorted(findings, key=lambda f: f["line"])
    new_f, unch_f = [], []
    for i, f in enumerate(sorted_findings):
        if i < prior_count:
            f["delta"] = "UNCHANGED"
            unch_f.append(f)
        else:
            f["delta"] = "NEW"
            new_f.append(f)
    return new_f, unch_f


print("\ndelta assignment:")
# All NEW when prior_count=0
findings_a = [{"line": 5}, {"line": 10}, {"line": 3}]
new_a, unch_a = assign_delta(findings_a, prior_count=0)
ok(len(new_a) == 3 and len(unch_a) == 0, "prior=0 → all findings NEW")

# All UNCHANGED when today_count ≤ prior_count (resolved case)
findings_b = [{"line": 5}, {"line": 10}]
new_b, unch_b = assign_delta(findings_b, prior_count=5)
ok(len(new_b) == 0 and len(unch_b) == 2, "today_count < prior_count → all UNCHANGED")

# Partial: first prior_count (by ascending line) are UNCHANGED
findings_c = [{"line": 20}, {"line": 5}, {"line": 10}, {"line": 30}]
new_c, unch_c = assign_delta(findings_c, prior_count=2)
ok(len(new_c) == 2 and len(unch_c) == 2, "today=4 prior=2 → 2 NEW 2 UNCHANGED")
# Findings sorted by line: 5, 10, 20, 30 — first 2 (lines 5, 10) are UNCHANGED
ok(all(f["delta"] == "UNCHANGED" for f in unch_c),
   "unchanged findings have correct delta tag")
ok(all(f["delta"] == "NEW" for f in new_c),
   "new findings have correct delta tag")
ok({f["line"] for f in unch_c} == {5, 10},
   "earlier lines (5, 10) are UNCHANGED")
ok({f["line"] for f in new_c} == {20, 30},
   "later lines (20, 30) are NEW")

# Exactly equal counts → all UNCHANGED, zero NEW
findings_d = [{"line": 1}, {"line": 2}]
new_d, unch_d = assign_delta(findings_d, prior_count=2)
ok(len(new_d) == 0 and len(unch_d) == 2, "today_count == prior_count → all UNCHANGED")


# ── calibration overrides ────────────────────────────────────────────────────
# unpinned-uses: Critical → High (delta.py, delta2.py, delta3.py)
# secrets-outside-env: High → Medium (finalize.py)

def apply_calibration(findings):
    for f in findings:
        if f["short_rule"] == "unpinned-uses" and f["severity"] == "Critical":
            f["severity"] = "High"
            f["calibrated"] = True
        elif f["short_rule"] == "secrets-outside-env" and f["severity"] == "High":
            f["severity"] = "Medium"
            f.setdefault("calibrated_notes", []).append("downgraded")
    return findings


print("\ncalibration overrides:")
findings_cal = [
    {"short_rule": "unpinned-uses", "severity": "Critical"},
    {"short_rule": "unpinned-uses", "severity": "High"},
    {"short_rule": "secrets-outside-env", "severity": "High"},
    {"short_rule": "secrets-outside-env", "severity": "Medium"},
    {"short_rule": "artipacked", "severity": "Critical"},
]
apply_calibration(findings_cal)

ok(findings_cal[0]["severity"] == "High",
   "unpinned-uses Critical → downgraded to High")
ok(findings_cal[0].get("calibrated") is True,
   "unpinned-uses downgrade marks calibrated=True")
ok(findings_cal[1]["severity"] == "High",
   "unpinned-uses High → unchanged")
ok(findings_cal[2]["severity"] == "Medium",
   "secrets-outside-env High → downgraded to Medium")
ok(findings_cal[3]["severity"] == "Medium",
   "secrets-outside-env Medium → unchanged")
ok(findings_cal[4]["severity"] == "Critical",
   "artipacked Critical → unchanged (not an overridden rule)")


# ── Results ─────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
if failed:
    sys.exit(1)
