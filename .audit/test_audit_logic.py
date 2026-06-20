"""
Tests for pure-logic functions shared across the .audit/ scripts.

Covers:
  - our_severity()  (classify.py / extract_steps.py)
  - fingerprint building  (classify.py)
  - fp_for()  (delta.py)
  - shellcheck code classification  (summarize_al.py)

Run: python3 .audit/test_audit_logic.py
"""

import hashlib
import os
import re
from collections import Counter

# ---------------------------------------------------------------------------
# Functions under test (copied verbatim from the scripts so tests stay
# independent of the scripts' file-level I/O and sys.argv requirements).
# ---------------------------------------------------------------------------

def our_severity(f):
    """Severity mapping used in classify.py and extract_steps.py."""
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


def classify_fingerprint(finding):
    """Fingerprint scheme from classify.py."""
    short_rule = finding['rule_id'].split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', finding['snippet'])[:60]
    file_short = os.path.basename(finding['file'])
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


def fp_for(rule, fname, step):
    """Fingerprint scheme from delta.py (uses full step name, not snippet)."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def classify_shellcheck_codes(data):
    """Shellcheck code counter from summarize_al.py."""
    codes = Counter()
    for f in data:
        msg = f.get('message', '')
        matched = False
        for code in ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']:
            if code in msg:
                codes[code] += 1
                matched = True
                break
        if not matched:
            codes['other'] += 1
    return codes


# ---------------------------------------------------------------------------
# our_severity tests
# ---------------------------------------------------------------------------

# error + high confidence → Critical
assert our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical'
print("OK  error/high → Critical")

# error + uppercase 'HIGH' → Critical (case-insensitive via .lower())
assert our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical'
print("OK  error/HIGH (uppercase) → Critical")

# error + medium confidence → High (not Critical)
assert our_severity({'level': 'error', 'confidence': 'medium'}) == 'High'
print("OK  error/medium → High")

# error + empty confidence → High
assert our_severity({'level': 'error', 'confidence': ''}) == 'High'
print("OK  error/'' → High")

# error + missing confidence key → High
assert our_severity({'level': 'error'}) == 'High'
print("OK  error/missing-conf-key → High")

# warning + high confidence → High
assert our_severity({'level': 'warning', 'confidence': 'high'}) == 'High'
print("OK  warning/high → High")

# warning + uppercase 'HIGH' → High
assert our_severity({'level': 'warning', 'confidence': 'HIGH'}) == 'High'
print("OK  warning/HIGH (uppercase) → High")

# warning + low confidence → Medium
assert our_severity({'level': 'warning', 'confidence': 'low'}) == 'Medium'
print("OK  warning/low → Medium")

# warning + missing confidence → Medium
assert our_severity({'level': 'warning'}) == 'Medium'
print("OK  warning/missing-conf-key → Medium")

# note level → Low
assert our_severity({'level': 'note'}) == 'Low'
print("OK  note → Low")

# unknown/none level → Low
assert our_severity({'level': 'none'}) == 'Low'
assert our_severity({'level': ''}) == 'Low'
print("OK  unknown level → Low")

# ---------------------------------------------------------------------------
# classify fingerprint tests
# ---------------------------------------------------------------------------

base_finding = {
    'rule_id': 'zizmor/template-injection',
    'file': '.github/workflows/aeon.yml',
    'snippet': 'run: echo ${{ github.event.issue.body }}',
}

fp = classify_fingerprint(base_finding)
# Fingerprint must be exactly 16 lowercase hex characters
assert len(fp) == 16, f"expected 16 chars, got {len(fp)}"
assert all(c in '0123456789abcdef' for c in fp), f"non-hex chars in {fp!r}"
print("OK  fingerprint is 16 hex chars")

# Deterministic: same input → same output
assert classify_fingerprint(base_finding) == classify_fingerprint(base_finding)
print("OK  fingerprint is deterministic")

# rule_id split on '/': only the last segment is used
finding_a = {**base_finding, 'rule_id': 'template-injection'}
finding_b = {**base_finding, 'rule_id': 'zizmor/template-injection'}
assert classify_fingerprint(finding_a) == classify_fingerprint(finding_b)
print("OK  rule_id segment after '/' is used; prefix does not affect fingerprint")

# Deep path → basename only
finding_deep = {**base_finding, 'file': '/home/runner/work/repo/.github/workflows/aeon.yml'}
finding_base = {**base_finding, 'file': 'aeon.yml'}
assert classify_fingerprint(finding_deep) == classify_fingerprint(finding_base)
print("OK  deep file path uses basename only in fingerprint")

# Snippet whitespace normalised: tab/newline → single space before truncation
finding_ws = {**base_finding, 'snippet': 'run:\n  echo\t${{ github.event }}'}
fp_ws = classify_fingerprint(finding_ws)
# Manually compute expected
snip_key = re.sub(r'\s+', ' ', finding_ws['snippet'])[:60]
fp_src = f"template-injection|aeon.yml|{snip_key}"
expected_fp = hashlib.sha256(fp_src.encode()).hexdigest()[:16]
assert fp_ws == expected_fp
print("OK  snippet whitespace normalised before fingerprinting")

# Snippet longer than 60 chars is truncated to 60
long_snippet = 'x' * 80
finding_long = {**base_finding, 'snippet': long_snippet}
snip_key_long = re.sub(r'\s+', ' ', long_snippet)[:60]
fp_src_long = f"template-injection|aeon.yml|{snip_key_long}"
expected_long = hashlib.sha256(fp_src_long.encode()).hexdigest()[:16]
assert classify_fingerprint(finding_long) == expected_long
print("OK  snippet capped at 60 chars in fingerprint")

# Empty snippet → still produces valid 16-char fingerprint
finding_empty_snip = {**base_finding, 'snippet': ''}
fp_empty = classify_fingerprint(finding_empty_snip)
assert len(fp_empty) == 16
assert fp_empty != fp  # different from non-empty snippet
print("OK  empty snippet produces valid (distinct) fingerprint")

# ---------------------------------------------------------------------------
# fp_for (delta.py) tests
# ---------------------------------------------------------------------------

# Basic: 16 hex chars, deterministic
assert len(fp_for('template-injection', 'aeon.yml', 'Build')) == 16
assert fp_for('template-injection', 'aeon.yml', 'Build') == fp_for('template-injection', 'aeon.yml', 'Build')
print("OK  fp_for returns 16-char deterministic hex string")

# Full path → basename used
assert fp_for('template-injection', '.github/workflows/aeon.yml', 'Build') == \
       fp_for('template-injection', 'aeon.yml', 'Build')
print("OK  fp_for uses basename of file path")

# Underscore vs space in step name → different fingerprints
# (delta.py converts underscores to spaces before calling fp_for so that
# prior-stored "Setup_Node" matches current "Setup Node"; the function itself
# does NOT normalise — callers must pass the right string)
fp_underscore = fp_for('template-injection', 'aeon.yml', 'Setup_Node')
fp_space = fp_for('template-injection', 'aeon.yml', 'Setup Node')
assert fp_underscore != fp_space
print("OK  fp_for treats underscore and space as distinct (caller normalises)")

# ---------------------------------------------------------------------------
# Shellcheck code classification tests (summarize_al.py)
# ---------------------------------------------------------------------------

# SC2086 in message
codes = classify_shellcheck_codes([{'message': 'Double quote to prevent globbing SC2086'}])
assert codes['SC2086'] == 1
assert codes.get('other', 0) == 0
print("OK  SC2086 in message → counted as SC2086")

# SC2046 in message
codes = classify_shellcheck_codes([{'message': 'Quote this to prevent word splitting SC2046'}])
assert codes['SC2046'] == 1
print("OK  SC2046 in message → counted as SC2046")

# Both SC2086 and SC2046 present → first match (SC2086) wins
codes = classify_shellcheck_codes([{'message': 'SC2086 and SC2046 present'}])
assert codes['SC2086'] == 1
assert codes.get('SC2046', 0) == 0
print("OK  SC2086 + SC2046 in same message → only SC2086 counted (first match)")

# No known code → 'other'
codes = classify_shellcheck_codes([{'message': 'something entirely unrelated'}])
assert codes['other'] == 1
print("OK  no known code → 'other'")

# Empty message → 'other'
codes = classify_shellcheck_codes([{'message': ''}])
assert codes['other'] == 1
print("OK  empty message → 'other'")

# Missing 'message' key → 'other'
codes = classify_shellcheck_codes([{}])
assert codes['other'] == 1
print("OK  missing message key → 'other'")

# SC2155 in message
codes = classify_shellcheck_codes([{'message': 'Declare and assign separately to avoid SC2155'}])
assert codes['SC2155'] == 1
print("OK  SC2155 in message → counted as SC2155")

# Multiple findings counted independently
data = [
    {'message': 'SC2086 here'},
    {'message': 'SC2086 again'},
    {'message': 'SC2046 here'},
    {'message': 'no match'},
]
codes = classify_shellcheck_codes(data)
assert codes['SC2086'] == 2
assert codes['SC2046'] == 1
assert codes['other'] == 1
print("OK  multiple findings counted independently")

# HIGH-CANDIDATE check: SC2086 + 'github.' in message
msg_hc = 'Double quote SC2086 to prevent globbing in github.event.issue.title'
assert 'SC2086' in msg_hc and 'github.' in msg_hc.lower()
print("OK  HIGH-CANDIDATE detection pattern (SC2086 + github.) is matchable")

print("\nAll audit logic tests passed.")
