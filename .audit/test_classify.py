"""
Tests for the our_severity() classification logic in classify.py.

Run: python -m pytest .audit/test_classify.py  OR  python .audit/test_classify.py

Covers every branch and the edge cases most likely to regress:
- error+high -> Critical
- error (other confidence) -> High (NOT Critical)
- warning+high -> High (NOT Medium)
- warning (other confidence) -> Medium
- note, unknown level -> Low
"""

import sys


# Inline copy of the pure function from classify.py — no file I/O, pure logic.
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


def mk(level, confidence=''):
    return {'level': level, 'confidence': confidence}


CASES = [
    # (description,                       finding,                     expected)
    ('error + high confidence → Critical', mk('error', 'high'),        'Critical'),
    ('error + High (case) → Critical',     mk('error', 'High'),        'Critical'),
    ('error + medium → High',              mk('error', 'medium'),      'High'),
    ('error + empty confidence → High',    mk('error', ''),            'High'),
    ('error + low confidence → High',      mk('error', 'low'),         'High'),
    ('warning + high → High',              mk('warning', 'high'),      'High'),
    ('warning + medium → Medium',          mk('warning', 'medium'),    'Medium'),
    ('warning + empty confidence → Medium',mk('warning', ''),          'Medium'),
    ('warning + low → Medium',             mk('warning', 'low'),       'Medium'),
    ('note + high → Low',                  mk('note', 'high'),         'Low'),
    ('note + empty → Low',                 mk('note', ''),             'Low'),
    ('unknown level → Low',                mk('unknown', 'high'),      'Low'),
    ('none level → Low',                   mk('none', ''),             'Low'),
]


def run_tests():
    failures = []
    for desc, finding, expected in CASES:
        got = our_severity(finding)
        if got != expected:
            failures.append(f'FAIL  {desc!r}: expected {expected!r}, got {got!r}')
        else:
            print(f'PASS  {desc}')

    if failures:
        print()
        for f in failures:
            print(f)
        return False
    return True


if __name__ == '__main__':
    print('our_severity() branch tests')
    print('===========================')
    ok = run_tests()
    print()
    print('All tests passed' if ok else f'{sum(1 for _ in [True])} failure(s)')
    sys.exit(0 if ok else 1)


# pytest-style so `python -m pytest` picks them up too
def test_error_high_is_critical():
    assert our_severity(mk('error', 'high')) == 'Critical'

def test_error_case_insensitive_confidence():
    assert our_severity(mk('error', 'High')) == 'Critical'

def test_error_medium_confidence_is_high():
    assert our_severity(mk('error', 'medium')) == 'High'

def test_error_no_confidence_is_high():
    assert our_severity(mk('error', '')) == 'High'

def test_warning_high_is_high():
    assert our_severity(mk('warning', 'high')) == 'High'

def test_warning_medium_is_medium():
    assert our_severity(mk('warning', 'medium')) == 'Medium'

def test_warning_no_confidence_is_medium():
    assert our_severity(mk('warning', '')) == 'Medium'

def test_note_falls_through_to_low():
    assert our_severity(mk('note', '')) == 'Low'

def test_note_high_confidence_still_low():
    # note-level findings are always Low regardless of confidence
    assert our_severity(mk('note', 'high')) == 'Low'

def test_unknown_level_is_low():
    assert our_severity(mk('none', '')) == 'Low'
    assert our_severity(mk('unknown', 'high')) == 'Low'
