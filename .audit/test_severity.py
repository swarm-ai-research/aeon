"""
Unit tests for workflow-security-audit severity-mapping and calibration logic.
Covers our_severity() (classify.py) and calibration overrides (delta.py / finalize.py).

Run: python3 .audit/test_severity.py
"""

import hashlib
import os
import sys

# ── our_severity (reproduced from classify.py) ──────────────────────────────

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


# ── calibration helpers (reproduced from delta.py / finalize.py) ─────────────

def apply_unpinned_uses_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


def apply_secrets_outside_env_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
            f.setdefault('calibrated_notes', []).append(
                'secrets-outside-env downgraded High->Medium'
            )
    return findings


# ── test harness ─────────────────────────────────────────────────────────────

passed = []
failed = []

def check(label, got, want):
    if got == want:
        passed.append(label)
        print(f'  ok  {label}')
    else:
        failed.append(label)
        print(f'  FAIL {label}: got {got!r}, want {want!r}')


# ── our_severity branches ─────────────────────────────────────────────────────

print('our_severity — Critical branch:')
check('error + high → Critical',
      our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')
check('error + HIGH (uppercase) → Critical (conf is lowercased)',
      our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

print('\nour_severity — High branches:')
check('error + medium → High',
      our_severity({'level': 'error', 'confidence': 'medium'}), 'High')
check('error + low → High',
      our_severity({'level': 'error', 'confidence': 'low'}), 'High')
check('error + empty string → High',
      our_severity({'level': 'error', 'confidence': ''}), 'High')
check('error + missing key → High',
      our_severity({'level': 'error'}), 'High')
check('warning + high → High',
      our_severity({'level': 'warning', 'confidence': 'high'}), 'High')
check('warning + HIGH (uppercase) → High',
      our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High')

print('\nour_severity — Medium branch:')
check('warning + medium → Medium',
      our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')
check('warning + low → Medium',
      our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')
check('warning + empty string → Medium',
      our_severity({'level': 'warning', 'confidence': ''}), 'Medium')
check('warning + missing key → Medium',
      our_severity({'level': 'warning'}), 'Medium')

print('\nour_severity — Low branch (else, note level):')
check('note → Low',
      our_severity({'level': 'note'}), 'Low')
check('note + high confidence → Low (note does not uplift)',
      our_severity({'level': 'note', 'confidence': 'high'}), 'Low')
check('note + missing key → Low',
      our_severity({'level': 'note', 'confidence': ''}), 'Low')

# ── calibration: unpinned-uses Critical → High ────────────────────────────────

print('\ncalibration — unpinned-uses:')
findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
apply_unpinned_uses_calibration(findings)
check('unpinned-uses Critical → High',
      findings[0]['severity'], 'High')
check('calibrated flag set',
      findings[0].get('calibrated'), True)

findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
apply_unpinned_uses_calibration(findings)
check('unpinned-uses already High → unchanged',
      findings[0]['severity'], 'High')
check('calibrated flag absent when no change',
      findings[0].get('calibrated'), None)

findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
apply_unpinned_uses_calibration(findings)
check('other rule Critical → unchanged by unpinned-uses calibration',
      findings[0]['severity'], 'Critical')

# ── calibration: secrets-outside-env High → Medium ───────────────────────────

print('\ncalibration — secrets-outside-env:')
findings = [{'short_rule': 'secrets-outside-env', 'severity': 'High'}]
apply_secrets_outside_env_calibration(findings)
check('secrets-outside-env High → Medium',
      findings[0]['severity'], 'Medium')
check('calibrated_notes populated',
      len(findings[0].get('calibrated_notes', [])) > 0, True)

findings = [{'short_rule': 'secrets-outside-env', 'severity': 'Medium'}]
apply_secrets_outside_env_calibration(findings)
check('secrets-outside-env already Medium → unchanged (no double-downgrade)',
      findings[0]['severity'], 'Medium')

findings = [{'short_rule': 'template-injection', 'severity': 'High'}]
apply_secrets_outside_env_calibration(findings)
check('other rule High → unchanged by secrets-outside-env calibration',
      findings[0]['severity'], 'High')

# ── fingerprint format ────────────────────────────────────────────────────────

print('\nfingerprint format:')
def make_fingerprint(rule, file_path, snip_key):
    file_short = os.path.basename(file_path)
    fp_src = f"{rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]

fp = make_fingerprint('template-injection', '.github/workflows/aeon.yml', 'some snippet')
check('fingerprint is 16 chars', len(fp), 16)
check('fingerprint is lowercase hex',
      all(c in '0123456789abcdef' for c in fp), True)
check('fingerprint is deterministic',
      make_fingerprint('template-injection', '.github/workflows/aeon.yml', 'some snippet'), fp)
check('fingerprint differs by rule',
      make_fingerprint('unpinned-uses', '.github/workflows/aeon.yml', 'some snippet') != fp, True)
check('fingerprint differs by file basename',
      make_fingerprint('template-injection', '.github/workflows/other.yml', 'some snippet') != fp, True)

# ── results ───────────────────────────────────────────────────────────────────

total = len(passed) + len(failed)
print(f'\n{len(passed)}/{total} passed', end='')
if failed:
    print(f'  — {len(failed)} FAILED:')
    for f in failed:
        print(f'    • {f}')
    sys.exit(1)
else:
    print()
