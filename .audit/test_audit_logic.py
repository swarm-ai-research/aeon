"""
Unit tests for pure-function audit-pipeline logic.

Run:  python .audit/test_audit_logic.py

Covers:
- our_severity() edge cases (missing/uppercase confidence, note-level, fallthrough)
- Fingerprint computation: basename extraction, space-vs-underscore schema mismatch
- delta.py dual-fp lookup that compensates for the trailer/delta fingerprint divergence
- short_rule extraction from fully-qualified rule IDs
"""

import hashlib
import os
import sys

# ──────────────────────────────────────────────────────────────────────────────
# Functions copied verbatim from the pipeline scripts so tests are self-contained
# and don't depend on file I/O at the top of each script.
# ──────────────────────────────────────────────────────────────────────────────

def our_severity(f):
    """Severity mapping — identical in classify.py and extract_steps.py."""
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


def fp_for_delta(rule, fname, step):
    """Fingerprint from delta.py — preserves spaces in step names."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def fp_for_trailer(rule, fname, step):
    """Fingerprint from gen_trailer.py — encodes spaces as underscores."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ──────────────────────────────────────────────────────────────────────────────
# Test harness
# ──────────────────────────────────────────────────────────────────────────────

failures = []

def check(cond, label):
    if not cond:
        failures.append(label)
        print(f"FAIL  {label}")
    else:
        print(f"OK    {label}")


# ──────────────────────────────────────────────────────────────────────────────
# 1. our_severity — all branches and edge cases
# ──────────────────────────────────────────────────────────────────────────────

check(our_severity({'level': 'error', 'confidence': 'high'}) == 'Critical',
      "error + high -> Critical")

# confidence field is .lower()'d — uppercase must still map to Critical
check(our_severity({'level': 'error', 'confidence': 'HIGH'}) == 'Critical',
      "error + HIGH (uppercase) -> Critical (case-insensitive)")

check(our_severity({'level': 'error', 'confidence': 'High'}) == 'Critical',
      "error + High (mixed case) -> Critical (case-insensitive)")

# error without high confidence falls through to High
check(our_severity({'level': 'error', 'confidence': 'medium'}) == 'High',
      "error + medium confidence -> High")

check(our_severity({'level': 'error', 'confidence': ''}) == 'High',
      "error + empty confidence -> High (not Critical)")

check(our_severity({'level': 'error'}) == 'High',
      "error + missing confidence key -> High (not Critical)")

# warning + high -> High
check(our_severity({'level': 'warning', 'confidence': 'high'}) == 'High',
      "warning + high -> High")

check(our_severity({'level': 'warning', 'confidence': 'medium'}) == 'Medium',
      "warning + medium -> Medium")

check(our_severity({'level': 'warning', 'confidence': ''}) == 'Medium',
      "warning + empty confidence -> Medium")

check(our_severity({'level': 'warning'}) == 'Medium',
      "warning + missing confidence key -> Medium")

# note-level: falls through to Low regardless of confidence
check(our_severity({'level': 'note', 'confidence': 'high'}) == 'Low',
      "note + high confidence -> Low (not High)")

check(our_severity({'level': 'note', 'confidence': ''}) == 'Low',
      "note + empty confidence -> Low")

# Any unrecognised level also falls through to Low
check(our_severity({'level': 'none', 'confidence': 'high'}) == 'Low',
      "unrecognised level -> Low")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Fingerprint — basename extraction strips directory prefix
# ──────────────────────────────────────────────────────────────────────────────

check(fp_for_delta('rule-x', '.github/workflows/foo.yml', 'Setup Node') ==
      fp_for_delta('rule-x', 'foo.yml', 'Setup Node'),
      "fp_for_delta: full path and basename produce identical fingerprint")

check(fp_for_trailer('rule-x', '.github/workflows/foo.yml', 'Setup Node') ==
      fp_for_trailer('rule-x', 'foo.yml', 'Setup Node'),
      "fp_for_trailer: full path and basename produce identical fingerprint")

# ──────────────────────────────────────────────────────────────────────────────
# 3. Space-vs-underscore divergence between delta.py and gen_trailer.py
# ──────────────────────────────────────────────────────────────────────────────

# The two helpers produce DIFFERENT hashes for the same step-with-spaces.
check(fp_for_delta('rule-x', 'foo.yml', 'Setup Node') !=
      fp_for_trailer('rule-x', 'foo.yml', 'Setup Node'),
      "delta and trailer fingerprints diverge for steps containing spaces (known schema split)")

# Step without spaces: both helpers must agree (no replacement happens)
check(fp_for_delta('rule-x', 'foo.yml', 'setup') ==
      fp_for_trailer('rule-x', 'foo.yml', 'setup'),
      "delta and trailer fingerprints agree for steps without spaces")

# ──────────────────────────────────────────────────────────────────────────────
# 4. delta.py dual-fp compensation
#
# The prior trailer stores step names with underscores ('Setup_Node').
# The current finding uses spaces ('Setup Node').
# delta.py adds BOTH variants to prior_fp_set so that lookups succeed.
# ──────────────────────────────────────────────────────────────────────────────

RULE = 'unpinned-uses'
FILE = 'foo.yml'

# Prior report stored by gen_trailer.py using underscore encoding:
prior_step_raw = 'Setup_Node'   # as written in the trailer
fp_prior_in_report = fp_for_trailer(RULE, FILE, prior_step_raw)

# Current finding extracted from the workflow file uses spaces:
current_step = 'Setup Node'
fp_current = fp_for_delta(RULE, FILE, current_step)

# Simulate delta.py's dual-fp insertion:
step_with_spaces = prior_step_raw.replace('_', ' ')   # 'Setup Node'
our_fp  = fp_for_delta(RULE, FILE, step_with_spaces)  # spaces path
our_fp2 = fp_for_delta(RULE, FILE, prior_step_raw)    # underscore path
prior_fp_set = {our_fp, our_fp2}

check(fp_current in prior_fp_set,
      "dual-fp lookup: current space-step finding matches prior underscore-encoded entry")

# Sanity: a genuinely new finding (different step) must NOT appear in prior_fp_set
fp_new = fp_for_delta(RULE, FILE, 'Run tests')
check(fp_new not in prior_fp_set,
      "dual-fp lookup: unrelated step is not falsely matched")

# ──────────────────────────────────────────────────────────────────────────────
# 5. short_rule extraction (rule_id.split('/')[-1])
# ──────────────────────────────────────────────────────────────────────────────

check('zizmor/unpinned-uses'.split('/')[-1] == 'unpinned-uses',
      "short_rule: last segment of namespaced rule id")

check('unpinned-uses'.split('/')[-1] == 'unpinned-uses',
      "short_rule: bare rule id returned unchanged")

check('a/b/c'.split('/')[-1] == 'c',
      "short_rule: handles multiple slashes, returns last segment")

# ──────────────────────────────────────────────────────────────────────────────

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
else:
    print(f"\nAll {22} checks passed.")
