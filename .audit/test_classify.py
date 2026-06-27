#!/usr/bin/env python3
"""Tests for the our_severity() logic in classify.py.

classify.py is a flat script (not a module), so the function is duplicated here.
Run: python3 .audit/test_classify.py
"""
import sys


# Inline copy of the function under test — keep in sync with classify.py.
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


passed = failed = 0


def ok(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f'  ✓ {label}')
    else:
        failed += 1
        print(f'  ✗ {label}', file=sys.stderr)


print('Documented severity branches:')
ok(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
   'error + high confidence -> Critical')
ok(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
   'error + medium confidence -> High')
ok(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
   'warning + high confidence -> High')
ok(our_severity({'level': 'warning', 'confidence': 'low'}) == 'Medium',
   'warning + low confidence -> Medium')

print('\nEdge cases — missing/empty/wrong-case confidence:')
ok(our_severity({'level': 'error'}) == 'High',
   'error with missing confidence key -> High (not Critical)')
ok(our_severity({'level': 'warning'}) == 'Medium',
   'warning with missing confidence key -> Medium')
ok(our_severity({'level': 'error', 'confidence': ''}) == 'High',
   'error with empty confidence string -> High (not Critical)')
ok(our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical',
   'confidence is case-insensitive (HIGH -> high)')
ok(our_severity({'level': 'warning', 'confidence': 'HIGH'}) == 'High',
   'warning + HIGH (uppercase) -> High')

print('\nEdge cases — non-error/warning levels:')
ok(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
   'note + high confidence -> Low (not High; only error/warning get upgraded)')
ok(our_severity({'level': 'note'}) == 'Low',
   'note with missing confidence -> Low')
ok(our_severity({'level': 'none', 'confidence': 'high'}) == 'Low',
   'unknown level -> Low fallback')

print(f'\n{passed} passed, {failed} failed')
sys.exit(1 if failed else 0)
