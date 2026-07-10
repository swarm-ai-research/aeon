"""
Tests for pure logic functions in classify.py, delta.py, and finalize.py.

Run: python .audit/test_audit_logic.py

The scripts themselves open hardcoded files at module-level so cannot be
imported directly.  These tests mirror the functions exactly and verify every
branch, including edge cases that are easy to get wrong.
"""

import hashlib
import os
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


def check_eq(actual, expected, label):
    global passed, failed
    if actual == expected:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}: expected {expected!r}, got {actual!r}", file=sys.stderr)


# ── Mirror of classify.py:our_severity() ────────────────────────────────────

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


# ── Mirror of delta.py:fp_for() ─────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── our_severity() – all five severity branches ──────────────────────────────

print("our_severity(): error + high confidence → Critical")
check_eq(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical',
         "error+high → Critical")

print("our_severity(): error + medium confidence → High")
check_eq(our_severity({'level': 'error', 'confidence': 'medium'}), 'High',
         "error+medium → High")

print("our_severity(): error + missing confidence key → High (not Critical)")
check_eq(our_severity({'level': 'error'}), 'High',
         "error+missing key → High")

print("our_severity(): error + empty string confidence → High (not Critical)")
check_eq(our_severity({'level': 'error', 'confidence': ''}), 'High',
         "error+empty string → High")

print("our_severity(): warning + high confidence → High")
check_eq(our_severity({'level': 'warning', 'confidence': 'high'}), 'High',
         "warning+high → High")

print("our_severity(): warning + low confidence → Medium")
check_eq(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium',
         "warning+low → Medium")

print("our_severity(): warning + missing confidence → Medium (not High)")
check_eq(our_severity({'level': 'warning'}), 'Medium',
         "warning+missing key → Medium")

print("our_severity(): note level → Low")
check_eq(our_severity({'level': 'note'}), 'Low',
         "note → Low")

print("our_severity(): unknown level → Low (fallthrough)")
check_eq(our_severity({'level': 'none'}), 'Low',
         "unknown level → Low")

# Confidence comparison is case-insensitive via .lower()
print("our_severity(): confidence field is case-normalised before compare")
check_eq(our_severity({'level': 'error', 'confidence': 'High'}), 'Critical',
         "error+High (title-case) → Critical")
check_eq(our_severity({'level': 'warning', 'confidence': 'HIGH'}), 'High',
         "warning+HIGH (upper) → High")

# ── fp_for() – determinism, length, uniqueness ───────────────────────────────

print("\nfp_for(): deterministic — same inputs always give same output")
check(fp_for('rule-a', 'foo.yml', 'step 1') == fp_for('rule-a', 'foo.yml', 'step 1'),
      "repeated calls match")

print("fp_for(): output is 16 lower-hex characters")
fp = fp_for('rule-a', 'foo.yml', 'step 1')
check_eq(len(fp), 16, "length == 16")
check(all(c in '0123456789abcdef' for c in fp), "only hex chars")

print("fp_for(): strips directory prefix — deep path == basename")
check_eq(
    fp_for('rule-a', '.github/workflows/ci.yml', 'step 1'),
    fp_for('rule-a', 'ci.yml', 'step 1'),
    "deep path and bare filename produce same fp"
)

print("fp_for(): different rule → different fingerprint")
check(fp_for('rule-a', 'foo.yml', 'step') != fp_for('rule-b', 'foo.yml', 'step'),
      "distinct rules produce distinct fps")

print("fp_for(): different step → different fingerprint")
check(fp_for('rule-a', 'foo.yml', 'step 1') != fp_for('rule-a', 'foo.yml', 'step 2'),
      "distinct steps produce distinct fps")

print("fp_for(): different file basename → different fingerprint")
check(fp_for('rule-a', 'foo.yml', 'step') != fp_for('rule-a', 'bar.yml', 'step'),
      "distinct file basenames produce distinct fps")

# ── Calibration: unpinned-uses Critical → High (delta.py lines 20-24) ────────

def apply_unpinned_calibration(finding):
    """Mirror of the calibration block in delta.py."""
    if finding['short_rule'] == 'unpinned-uses' and finding['severity'] == 'Critical':
        finding['severity'] = 'High'
        finding['calibrated'] = True
    return finding

print("\ncalibration: unpinned-uses Critical is demoted to High")
f = apply_unpinned_calibration({'short_rule': 'unpinned-uses', 'severity': 'Critical'})
check_eq(f['severity'], 'High', "severity → High")
check_eq(f.get('calibrated'), True, "calibrated flag set")

print("calibration: unpinned-uses High is NOT double-demoted")
f = apply_unpinned_calibration({'short_rule': 'unpinned-uses', 'severity': 'High'})
check_eq(f['severity'], 'High', "High stays High")
check_eq(f.get('calibrated'), None, "no calibrated flag")

print("calibration: other rule at Critical is left unchanged")
f = apply_unpinned_calibration({'short_rule': 'script-injection', 'severity': 'Critical'})
check_eq(f['severity'], 'Critical', "Critical stays Critical")
check_eq(f.get('calibrated'), None, "no calibrated flag")

# ── Calibration: secrets-outside-env High → Medium (finalize.py) ─────────────

def apply_secrets_calibration(finding):
    """Mirror of the calibration block in finalize.py."""
    if finding['short_rule'] == 'secrets-outside-env' and finding['severity'] == 'High':
        finding['severity'] = 'Medium'
        finding.setdefault('calibrated_notes', []).append(
            'secrets-outside-env downgraded High->Medium (GitHub Environments hardening, not exploit)'
        )
    return finding

print("\ncalibration: secrets-outside-env High → Medium")
f = apply_secrets_calibration({'short_rule': 'secrets-outside-env', 'severity': 'High'})
check_eq(f['severity'], 'Medium', "High demoted to Medium")
check(len(f.get('calibrated_notes', [])) == 1, "calibration note appended")

print("calibration: secrets-outside-env Medium left unchanged")
f = apply_secrets_calibration({'short_rule': 'secrets-outside-env', 'severity': 'Medium'})
check_eq(f['severity'], 'Medium', "Medium stays Medium (no double-demotion)")
check_eq(f.get('calibrated_notes'), None, "no calibration note")

print("calibration: other rule at High left unchanged")
f = apply_secrets_calibration({'short_rule': 'script-injection', 'severity': 'High'})
check_eq(f['severity'], 'High', "High stays High for unrelated rule")

# ── Aggregate matching edge case: template-injection-note (delta.py line 112) ─

def should_apply_aggregate(agg_rule, finding_severity):
    """Mirror of the guard inside the aggregate loop in delta.py."""
    if agg_rule == 'template-injection-note' and finding_severity != 'Low':
        return False
    return True

print("\naggregate matching: template-injection-note only applies to Low findings")
check_eq(should_apply_aggregate('template-injection-note', 'Low'), True,
         "Low severity matches template-injection-note aggregate")
check_eq(should_apply_aggregate('template-injection-note', 'Medium'), False,
         "Medium severity excluded from template-injection-note aggregate")
check_eq(should_apply_aggregate('template-injection-note', 'High'), False,
         "High severity excluded from template-injection-note aggregate")
check_eq(should_apply_aggregate('template-injection-note', 'Critical'), False,
         "Critical severity excluded from template-injection-note aggregate")

print("aggregate matching: other aggregate rules are not filtered by severity")
check_eq(should_apply_aggregate('secrets-outside-env', 'High'), True,
         "secrets-outside-env High passes through")
check_eq(should_apply_aggregate('undocumented-permissions', 'Medium'), True,
         "undocumented-permissions Medium passes through")

# ── Results ──────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
if failed > 0:
    sys.exit(1)
