"""Tests for audit classification, fingerprinting, and calibration logic.

Functions are inlined from classify.py, delta.py, and finalize.py so the
tests don't depend on those scripts' file-reading side effects.

Run:
  python .audit/test_audit_logic.py
  python -m pytest .audit/test_audit_logic.py -v
"""

import hashlib
import os
import re

# ── from classify.py ─────────────────────────────────────────────────────────

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


def make_fingerprint(short_rule, file_path, snippet):
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── from delta.py ─────────────────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def calibrate_unpinned_uses(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


# ── from finalize.py ──────────────────────────────────────────────────────────

def calibrate_secrets_outside_env(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
            )
    return findings


# ── test harness ──────────────────────────────────────────────────────────────

passed = 0
failed = 0

def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {label}")
    else:
        failed += 1
        print(f"  ✗ {label}")


# ── our_severity — all 5 branches + edge cases ───────────────────────────────

print("our_severity:")

# Critical branch: error + high confidence
check(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
      "error+high → Critical")
# Case-insensitive: conf.lower() must handle 'HIGH'
check(our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical',
      "error+HIGH (case-insensitive) → Critical")

# High branch via error (non-high confidence)
check(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
      "error+medium → High")
check(our_severity({'level': 'error', 'confidence': ''}) == 'High',
      "error+empty confidence → High")
# Missing confidence key falls back to '' via .get default
check(our_severity({'level': 'error'}) == 'High',
      "error, no confidence key → High (default empty string)")

# High branch via warning + high confidence
check(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
      "warning+high → High")

# Medium branch: warning, non-high confidence
check(our_severity({'level': 'warning', 'confidence': 'low'}) == 'Medium',
      "warning+low → Medium")
check(our_severity({'level': 'warning', 'confidence': ''}) == 'Medium',
      "warning+empty → Medium")
check(our_severity({'level': 'warning'}) == 'Medium',
      "warning, no confidence key → Medium")

# Low branch: anything else (note, none, unknown)
check(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
      "note+high → Low (note does not get High)")
check(our_severity({'level': 'note', 'confidence': ''}) == 'Low',
      "note → Low")
check(our_severity({'level': 'none', 'confidence': 'high'}) == 'Low',
      "unknown level → Low")


# ── make_fingerprint — determinism, normalisation, path stripping ─────────────

print("\nmake_fingerprint:")

fp1 = make_fingerprint('script-injection', '.github/workflows/ci.yml', 'run: echo $X')
fp2 = make_fingerprint('script-injection', '.github/workflows/ci.yml', 'run: echo $X')
check(fp1 == fp2, "same inputs produce identical fingerprint")
check(len(fp1) == 16, "fingerprint is 16 characters")
check(all(c in '0123456789abcdef' for c in fp1), "fingerprint is lowercase hex")

# Basename stripping: full path and bare filename must match
fp_full = make_fingerprint('rule', '/full/path/to/file.yml', 'snip')
fp_base = make_fingerprint('rule', 'file.yml', 'snip')
check(fp_full == fp_base, "full path and bare filename produce same fingerprint")

# Whitespace normalisation: multiple spaces/tabs → single space
fp_ws1 = make_fingerprint('rule', 'f.yml', 'a  b\tc')
fp_ws2 = make_fingerprint('rule', 'f.yml', 'a b c')
check(fp_ws1 == fp_ws2, "whitespace collapsed in snippet before hashing")

# Different rules must not collide
fp_a = make_fingerprint('rule-a', 'f.yml', 'snip')
fp_b = make_fingerprint('rule-b', 'f.yml', 'snip')
check(fp_a != fp_b, "different rules → different fingerprints")

# Different files must not collide
fp_x = make_fingerprint('rule', 'x.yml', 'snip')
fp_y = make_fingerprint('rule', 'y.yml', 'snip')
check(fp_x != fp_y, "different files → different fingerprints")


# ── fp_for (delta.py) — determinism, path handling ───────────────────────────

print("\nfp_for:")

check(fp_for('unpinned-uses', 'ci.yml', 'Setup Node') ==
      fp_for('unpinned-uses', 'ci.yml', 'Setup Node'),
      "deterministic across calls")
check(len(fp_for('r', 'f', 's')) == 16, "output is 16 chars")

# Directory is stripped from fname
check(fp_for('unpinned-uses', '.github/workflows/ci.yml', 'step') ==
      fp_for('unpinned-uses', 'ci.yml', 'step'),
      "directory stripped from fname in fp_for")

# Step value matters: different steps → different fingerprints
fp_s1 = fp_for('rule', 'f.yml', 'step A')
fp_s2 = fp_for('rule', 'f.yml', 'step B')
check(fp_s1 != fp_s2, "different steps → different fingerprints")


# ── calibrate_unpinned_uses — only Critical is downgraded ────────────────────

print("\ncalibrate_unpinned_uses:")

findings = [
    {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
    {'short_rule': 'unpinned-uses', 'severity': 'High'},    # already High — unchanged
    {'short_rule': 'script-injection', 'severity': 'Critical'},  # wrong rule — unchanged
]
calibrate_unpinned_uses(findings)

check(findings[0]['severity'] == 'High', "unpinned-uses Critical → High")
check(findings[0].get('calibrated') is True, "calibrated flag set on downgraded finding")
check(findings[1]['severity'] == 'High', "unpinned-uses High already correct, unchanged")
check('calibrated' not in findings[1], "calibrated flag absent when not changed")
check(findings[2]['severity'] == 'Critical', "other rule Critical not touched")


# ── calibrate_secrets_outside_env — only High is downgraded ──────────────────

print("\ncalibrate_secrets_outside_env:")

findings2 = [
    {'short_rule': 'secrets-outside-env', 'severity': 'High'},
    {'short_rule': 'secrets-outside-env', 'severity': 'Medium'},  # already Medium — unchanged
    {'short_rule': 'script-injection', 'severity': 'High'},       # wrong rule — unchanged
]
calibrate_secrets_outside_env(findings2)

check(findings2[0]['severity'] == 'Medium', "secrets-outside-env High → Medium")
check('calibrated_notes' in findings2[0], "calibrated_notes list added")
check(len(findings2[0]['calibrated_notes']) == 1, "exactly one calibration note added")
check(findings2[1]['severity'] == 'Medium', "secrets-outside-env Medium unchanged")
check('calibrated_notes' not in findings2[1], "no notes added when already Medium")
check(findings2[2]['severity'] == 'High', "other rule High untouched")


# ── summary ───────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
