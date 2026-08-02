"""
Tests for classify.py severity mapping and delta.py fingerprint logic.

These functions are defined in scripts that run as top-level programs reading
from files, so we replicate the pure logic here rather than importing it.

Run: python3 .audit/test_classify.py
"""

import hashlib
import os
import sys

# ── Replicate our_severity() from classify.py ──────────────────────────────

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


# ── Replicate fp_for() from delta.py ──────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Test harness ───────────────────────────────────────────────────────────

passed = 0
failed = 0


def ok(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f'  pass  {label}')
    else:
        failed += 1
        print(f'  FAIL  {label}')


# ── our_severity: all five branches ───────────────────────────────────────

print('our_severity — branch coverage')

ok(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
   'error + high conf -> Critical')

# confidence comparison is case-insensitive (.lower())
ok(our_severity({'level': 'error', 'confidence': 'High'}) == 'Critical',
   'error + High (mixed-case) -> Critical (case-insensitive)')

ok(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
   'error + medium conf -> High (not Critical)')

ok(our_severity({'level': 'error', 'confidence': ''}) == 'High',
   'error + empty conf -> High')

# confidence key absent: .get() returns '' which is not 'high'
ok(our_severity({'level': 'error'}) == 'High',
   'error + missing confidence key -> High')

ok(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
   'warning + high conf -> High')

ok(our_severity({'level': 'warning', 'confidence': 'low'}) == 'Medium',
   'warning + low conf -> Medium')

ok(our_severity({'level': 'warning', 'confidence': ''}) == 'Medium',
   'warning + empty conf -> Medium')

ok(our_severity({'level': 'warning'}) == 'Medium',
   'warning + missing confidence key -> Medium')

# note level falls through all conditions to Low
ok(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
   'note + high conf -> Low (note never Critical/High)')

ok(our_severity({'level': 'note', 'confidence': ''}) == 'Low',
   'note + empty conf -> Low')

# unknown / future level also returns Low
ok(our_severity({'level': 'info'}) == 'Low',
   'unknown level -> Low')

# ── fp_for: format and uniqueness invariants ───────────────────────────────

print('\nfp_for — fingerprint invariants')

fp = fp_for('template-injection', '.github/workflows/build.yml', 'Run Tests')

ok(len(fp) == 16, 'fp_for returns exactly 16 characters')
ok(all(c in '0123456789abcdef' for c in fp), 'fp_for output is lowercase hex')

# Only the basename of the file path is used (matching classify.py's os.path.basename)
fp_abs = fp_for('rule', '/long/path/to/build.yml', 'step')
fp_base = fp_for('rule', 'build.yml', 'step')
ok(fp_abs == fp_base,
   'full path and basename give same fingerprint (only basename is hashed)')

# Each dimension is independently significant
ok(fp_for('rule-a', 'file.yml', 'step') != fp_for('rule-b', 'file.yml', 'step'),
   'different rules produce different fingerprints')

ok(fp_for('rule', 'a.yml', 'step') != fp_for('rule', 'b.yml', 'step'),
   'different filenames produce different fingerprints')

ok(fp_for('rule', 'file.yml', 'step-a') != fp_for('rule', 'file.yml', 'step-b'),
   'different step names produce different fingerprints')

# delta.py explicitly handles the space/underscore ambiguity by trying both
# variants — verify they hash differently so the try-both logic is necessary
ok(fp_for('rule', 'file.yml', 'Setup Node') != fp_for('rule', 'file.yml', 'Setup_Node'),
   'space vs underscore in step name -> different fingerprints (delta.py must try both)')

# Deterministic: same inputs always produce the same output
ok(fp_for('r', 'f.yml', 's') == fp_for('r', 'f.yml', 's'),
   'fp_for is deterministic')

# ── Results ───────────────────────────────────────────────────────────────

print(f'\n{passed} passed, {failed} failed')
if failed:
    sys.exit(1)
