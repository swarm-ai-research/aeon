"""
Tests for the pure helper functions in classify.py and delta.py.

These scripts are not importable (module-level I/O), so the functions are
inlined here. If the production logic changes, update these copies to match.

Run: python3 .audit/test_classify.py
"""
import hashlib
import os

# ── functions under test (inlined from classify.py / delta.py) ─────────────

def our_severity(f):
    """Map a zizmor finding dict to Critical/High/Medium/Low."""
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


def fp_for(rule, fname, step):
    """Stable 16-char hex fingerprint for a finding."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── minimal test harness ─────────────────────────────────────────────────────

_passed = _failed = 0

def check(condition, label):
    global _passed, _failed
    if condition:
        _passed += 1
        print(f"  ✓ {label}")
    else:
        _failed += 1
        print(f"  ✗ {label}")

def raises(exc_type, fn, label):
    global _passed, _failed
    try:
        fn()
        _failed += 1
        print(f"  ✗ {label}  (no exception raised)")
    except exc_type:
        _passed += 1
        print(f"  ✓ {label}")
    except Exception as e:
        _failed += 1
        print(f"  ✗ {label}  (wrong exception: {e!r})")


# ── our_severity ──────────────────────────────────────────────────────────────

print("our_severity — main severity mapping:")
check(our_severity({'level': 'error',   'confidence': 'high'})   == 'Critical', 'error+high → Critical')
check(our_severity({'level': 'error',   'confidence': 'medium'}) == 'High',     'error+medium → High')
check(our_severity({'level': 'error',   'confidence': 'low'})    == 'High',     'error+low → High')
check(our_severity({'level': 'warning', 'confidence': 'high'})   == 'High',     'warning+high → High')
check(our_severity({'level': 'warning', 'confidence': 'medium'}) == 'Medium',   'warning+medium → Medium')
check(our_severity({'level': 'warning', 'confidence': 'low'})    == 'Medium',   'warning+low → Medium')
check(our_severity({'level': 'note',    'confidence': 'high'})   == 'Low',      'note+high → Low (note always Low)')
check(our_severity({'level': 'note',    'confidence': 'low'})    == 'Low',      'note+low → Low')

print("\nour_severity — missing / absent confidence key:")
check(our_severity({'level': 'error'})   == 'High',   'error + absent confidence → High')
check(our_severity({'level': 'warning'}) == 'Medium', 'warning + absent confidence → Medium')
check(our_severity({'level': 'note'})    == 'Low',    'note + absent confidence → Low')

print("\nour_severity — unknown level falls through to Low:")
check(our_severity({'level': 'none',    'confidence': 'high'}) == 'Low', 'unknown level → Low')
check(our_severity({'level': 'unknown', 'confidence': 'high'}) == 'Low', 'unknown level → Low (variant)')

print("\nour_severity — confidence is case-insensitive (zizmor may vary casing):")
check(our_severity({'level': 'error',   'confidence': 'HIGH'})  == 'Critical', 'error+HIGH (upper) → Critical')
check(our_severity({'level': 'error',   'confidence': 'High'})  == 'Critical', 'error+High (title) → Critical')
check(our_severity({'level': 'warning', 'confidence': 'HIGH'})  == 'High',     'warning+HIGH (upper) → High')

print("\nour_severity — confidence=None triggers AttributeError (known edge case):")
raises(AttributeError,
       lambda: our_severity({'level': 'error', 'confidence': None}),
       "confidence=None raises AttributeError (None.lower())")


# ── fp_for ────────────────────────────────────────────────────────────────────

print("\nfp_for — fingerprint properties:")
fp = fp_for('template-injection', '.github/workflows/ci.yml', 'Build')
check(len(fp) == 16, 'fingerprint is 16 chars')
check(all(c in '0123456789abcdef' for c in fp), 'fingerprint is lowercase hex')

print("\nfp_for — stability (same inputs → same output):")
fp1 = fp_for('template-injection', '.github/workflows/ci.yml', 'Build')
fp2 = fp_for('template-injection', '.github/workflows/ci.yml', 'Build')
check(fp1 == fp2, 'same inputs → same fingerprint')

print("\nfp_for — basename extraction (path depth must not matter):")
fp_full = fp_for('rule', '/a/b/c/file.yml', 'step')
fp_base = fp_for('rule', 'file.yml', 'step')
check(fp_full == fp_base, 'full path and bare filename give same fingerprint')

print("\nfp_for — distinct inputs produce distinct fingerprints:")
check(fp_for('rule-a', 'file.yml', 'step') != fp_for('rule-b', 'file.yml', 'step'),
      'different rules → different fingerprints')
check(fp_for('rule', 'file-a.yml', 'step') != fp_for('rule', 'file-b.yml', 'step'),
      'different files → different fingerprints')
check(fp_for('rule', 'file.yml', 'step one') != fp_for('rule', 'file.yml', 'step two'),
      'different steps → different fingerprints')

print("\nfp_for — edge cases:")
check(len(fp_for('rule', 'file.yml', '')) == 16,   'empty step → valid 16-char fingerprint')
check(len(fp_for('', 'file.yml', 'step')) == 16,   'empty rule → valid 16-char fingerprint')
check(len(fp_for('rule', '', 'step')) == 16,        'empty filename → valid 16-char fingerprint')
# Step name with underscores vs spaces (prior audit stored "Setup_Node"; current uses "Setup Node")
check(fp_for('rule', 'f.yml', 'Setup_Node') != fp_for('rule', 'f.yml', 'Setup Node'),
      'underscore and space step names are distinct fingerprints')


# ── results ───────────────────────────────────────────────────────────────────

print(f"\n{_passed} passed, {_failed} failed")
if _failed:
    raise SystemExit(1)
