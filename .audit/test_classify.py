"""
Tests for the severity-classification and fingerprint-generation logic in
classify.py and delta.py.  Those scripts read from disk at import time so
the pure functions are copied here and tested in isolation.

Run from the repo root:
    python3 .audit/test_classify.py
"""
import hashlib
import os
import re


# ── functions under test (copied from classify.py) ──────────────────────────

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


def make_fingerprint(rule_id, file_path, snippet):
    """Fingerprint as computed in classify.py."""
    short_rule = rule_id.split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_path)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# ── functions under test (copied from delta.py) ──────────────────────────────

def fp_for(rule, fname, step):
    """Step-based fingerprint as computed in delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── helpers ──────────────────────────────────────────────────────────────────

passed = 0
failed = 0


def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f'  OK  {label}')
    else:
        failed += 1
        print(f'FAIL  {label}')


# ── our_severity: all branches ───────────────────────────────────────────────

print("our_severity:")

check(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
      "error + high → Critical")

# confidence is .lower()'d so uppercase should still hit the Critical branch
check(our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical',
      "error + HIGH (uppercase confidence) → Critical")

check(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
      "error + medium confidence → High")

check(our_severity({'level': 'error', 'confidence': 'low'}) == 'High',
      "error + low confidence → High")

# missing key defaults to '' which is not 'high', so not Critical
check(our_severity({'level': 'error'}) == 'High',
      "error + missing confidence key → High (not Critical)")

check(our_severity({'level': 'error', 'confidence': ''}) == 'High',
      "error + empty confidence string → High")

check(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
      "warning + high → High")

check(our_severity({'level': 'warning', 'confidence': 'medium'}) == 'Medium',
      "warning + medium → Medium")

check(our_severity({'level': 'warning'}) == 'Medium',
      "warning + missing confidence → Medium")

check(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
      "note + high confidence → Low (note is always Low)")

check(our_severity({'level': 'note'}) == 'Low',
      "note → Low")

check(our_severity({'level': 'info'}) == 'Low',
      "unrecognised level → Low")

check(our_severity({'level': '', 'confidence': 'high'}) == 'Low',
      "empty level → Low")


# ── make_fingerprint (snippet-based, classify.py) ────────────────────────────

print("\nmake_fingerprint:")

fp1 = make_fingerprint('zizmor/template-injection', '.github/workflows/aeon.yml',
                       'run: ${{ inputs.msg }}')
check(len(fp1) == 16, "fingerprint is 16 chars")
check(all(c in '0123456789abcdef' for c in fp1), "fingerprint is lowercase hex")

# same inputs → same output
fp2 = make_fingerprint('zizmor/template-injection', '.github/workflows/aeon.yml',
                       'run: ${{ inputs.msg }}')
check(fp1 == fp2, "fingerprint is deterministic")

# rule_id is split on '/' — only the last segment is used
fp_qualified = make_fingerprint('zizmor/unpinned-uses', 'aeon.yml', 'uses: actions/checkout@v3')
fp_bare      = make_fingerprint('unpinned-uses',        'aeon.yml', 'uses: actions/checkout@v3')
check(fp_qualified == fp_bare, "qualified rule id matches bare rule id (suffix only)")

# only the basename of the file path matters
fp_abs = make_fingerprint('rule', '/home/runner/work/.github/workflows/aeon.yml', 'snip')
fp_rel = make_fingerprint('rule', '.github/workflows/aeon.yml', 'snip')
fp_base = make_fingerprint('rule', 'aeon.yml', 'snip')
check(fp_abs == fp_rel == fp_base, "fingerprint uses basename only — path prefix is ignored")

# whitespace is normalised before fingerprinting
fp_ws1 = make_fingerprint('rule', 'f.yml', '  run:  echo  hello  ')
fp_ws2 = make_fingerprint('rule', 'f.yml', ' run: echo hello ')
check(fp_ws1 == fp_ws2, "multiple whitespace chars collapsed to single space")

# snippet is truncated to 60 chars before hashing
fp_60 = make_fingerprint('rule', 'f.yml', 'x' * 60)
fp_61 = make_fingerprint('rule', 'f.yml', 'x' * 61)
check(fp_60 == fp_61, "snippet truncated at 60 chars — 61-char and 60-char produce same fp")

# but 59 chars is distinct from 60
fp_59 = make_fingerprint('rule', 'f.yml', 'x' * 59 + 'y')
check(fp_59 != fp_60, "different snippet content produces different fingerprint")

# empty snippet is valid
fp_empty = make_fingerprint('rule', 'f.yml', '')
check(len(fp_empty) == 16, "empty snippet still yields a valid 16-char fingerprint")


# ── fp_for (step-based, delta.py) ────────────────────────────────────────────

print("\nfp_for:")

fp3 = fp_for('template-injection', '.github/workflows/aeon.yml', 'Build image')
check(len(fp3) == 16, "step-based fingerprint is 16 chars")

# basename-only like classify.py
fp_path_a = fp_for('rule', '/abs/path/aeon.yml', 'step')
fp_path_b = fp_for('rule', 'aeon.yml', 'step')
check(fp_path_a == fp_path_b, "fp_for uses basename only")

# step name matters — underscore vs space are NOT normalised (delta.py adds both)
fp_underscore = fp_for('rule', 'f.yml', 'Setup_Node')
fp_space      = fp_for('rule', 'f.yml', 'Setup Node')
check(fp_underscore != fp_space,
      "underscore and space step names produce different fps (delta.py adds both explicitly)")

# different steps produce different fingerprints
fp_step_a = fp_for('rule', 'f.yml', 'Checkout')
fp_step_b = fp_for('rule', 'f.yml', 'Build')
check(fp_step_a != fp_step_b, "different step names produce different fingerprints")


# ── result ────────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
if failed:
    raise SystemExit(1)
