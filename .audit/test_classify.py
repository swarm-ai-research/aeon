#!/usr/bin/env python3
"""
Tests for pure logic functions extracted from classify.py, delta.py, and delta2.py.

These scripts are not importable as modules (they execute on load against
specific on-disk files), so the functions under test are inlined here.

Run: python3 .audit/test_classify.py
"""

import hashlib
import os
import sys

failures = []

def check(label, got, want):
    if got != want:
        failures.append(f"FAIL {label}: got {got!r}, want {want!r}")
    else:
        print(f"OK  {label}")

# ──────────────────────────────────────────────────────────────────────────
# our_severity() — classify.py
# Maps zizmor finding level + confidence → 4-tier severity label.
# ──────────────────────────────────────────────────────────────────────────

def our_severity(f):
    level = f['level']
    conf = f.get('confidence', '').lower()
    if level == 'error' and conf == 'high':
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and conf == 'high':
        return 'High'
    if level == 'warning':
        return 'Medium'
    return 'Low'

check("error/high → Critical",
      our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

# Confidence string is lowercased before comparison — uppercase must still map correctly.
check("error/HIGH → Critical (case-insensitive)",
      our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

check("error/medium → High (not Critical)",
      our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

check("error/empty confidence → High",
      our_severity({'level': 'error', 'confidence': ''}), 'High')

# Missing 'confidence' key uses .get() fallback of ''; must not raise.
check("error/missing confidence key → High",
      our_severity({'level': 'error'}), 'High')

check("warning/high → High",
      our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

check("warning/low → Medium (not High)",
      our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

check("warning/missing confidence key → Medium",
      our_severity({'level': 'warning'}), 'Medium')

# note-level findings always fall through to Low regardless of confidence.
check("note/high → Low (fallthrough)",
      our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

check("unknown level → Low (fallthrough)",
      our_severity({'level': 'info', 'confidence': 'high'}), 'Low')

# ──────────────────────────────────────────────────────────────────────────
# fp_for() — delta.py
# Produces a 16-hex-char SHA256 fingerprint keyed on rule|basename|step.
# ──────────────────────────────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]

# Full path must be reduced to basename before hashing.
check("fp_for: full path == bare filename",
      fp_for("unpinned-uses", ".github/workflows/aeon.yml", "Checkout"),
      fp_for("unpinned-uses", "aeon.yml", "Checkout"))

# Distinctness: different files must not collide.
assert fp_for("unpinned-uses", "a.yml", "step") != fp_for("unpinned-uses", "b.yml", "step"), \
    "different files must yield different fingerprints"
print("OK  different files → distinct fingerprints")

# Distinctness: different rules must not collide.
assert fp_for("rule-a", "a.yml", "step") != fp_for("rule-b", "a.yml", "step"), \
    "different rules must yield different fingerprints"
print("OK  different rules → distinct fingerprints")

# Distinctness: different steps must not collide.
assert fp_for("rule", "a.yml", "step-1") != fp_for("rule", "a.yml", "step-2"), \
    "different steps must yield different fingerprints"
print("OK  different steps → distinct fingerprints")

# Determinism: same inputs always produce the same digest.
fp1 = fp_for("template-injection", ".github/workflows/messages.yml", "Extract message")
fp2 = fp_for("template-injection", ".github/workflows/messages.yml", "Extract message")
check("fp_for is deterministic", fp1, fp2)

# Output is exactly 16 hex characters.
check("fp_for output length == 16", len(fp1), 16)

# ──────────────────────────────────────────────────────────────────────────
# Calibration overrides
# delta.py:  unpinned-uses Critical → High
# finalize.py: secrets-outside-env High → Medium
# ──────────────────────────────────────────────────────────────────────────

def apply_delta_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings

def apply_finalize_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append('downgraded')
    return findings

# unpinned-uses Critical → High; calibrated flag set.
fs = apply_delta_calibration([{'short_rule': 'unpinned-uses', 'severity': 'Critical'}])
check("unpinned-uses Critical → High", fs[0]['severity'], 'High')
check("calibrated flag set after downgrade", fs[0].get('calibrated'), True)

# unpinned-uses already at High must not gain the calibrated flag.
fs = apply_delta_calibration([{'short_rule': 'unpinned-uses', 'severity': 'High'}])
check("unpinned-uses High stays High", fs[0]['severity'], 'High')
assert 'calibrated' not in fs[0], "calibrated flag must not be set when no downgrade occurred"
print("OK  unpinned-uses High → no calibrated flag")

# Other rules at Critical are untouched.
fs = apply_delta_calibration([{'short_rule': 'template-injection', 'severity': 'Critical'}])
check("template-injection Critical unchanged by delta calibration", fs[0]['severity'], 'Critical')

# secrets-outside-env High → Medium.
fs = apply_finalize_calibration([{'short_rule': 'secrets-outside-env', 'severity': 'High'}])
check("secrets-outside-env High → Medium", fs[0]['severity'], 'Medium')

# secrets-outside-env already at Medium must not be double-downgraded to Low.
fs = apply_finalize_calibration([{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}])
check("secrets-outside-env Medium stays Medium", fs[0]['severity'], 'Medium')

# Other rules at High are untouched by finalize calibration.
fs = apply_finalize_calibration([{'short_rule': 'unpinned-uses', 'severity': 'High'}])
check("unpinned-uses High unchanged by finalize calibration", fs[0]['severity'], 'High')

# ──────────────────────────────────────────────────────────────────────────
# short_rule() — delta2.py
# Strips the "zizmor/" namespace prefix from a rule ID.
# ──────────────────────────────────────────────────────────────────────────

def short_rule(s):
    return s.split('/')[-1]

check("short_rule strips single prefix", short_rule("zizmor/unpinned-uses"), "unpinned-uses")
check("short_rule: no prefix passthrough", short_rule("template-injection"), "template-injection")
check("short_rule: nested prefix keeps only last segment", short_rule("a/b/c"), "c")
check("short_rule: empty string", short_rule(""), "")

# ──────────────────────────────────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────────────────────────────────

if failures:
    for msg in failures:
        print(msg, file=sys.stderr)
    sys.exit(1)

print("\nAll classify/delta logic tests passed.")
