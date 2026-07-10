# test_audit_logic.py — Unit tests for the classification/calibration logic
# used in the workflow-security-audit pipeline to process actionlint and
# zizmor output. Run with: python .audit/test_audit_logic.py

import hashlib
import os
import re
import sys

ERRORS = []
PASS_COUNT = 0


def check(label, got, want):
    global PASS_COUNT
    if got != want:
        ERRORS.append(f"FAIL  {label}: got {got!r}, want {want!r}")
    else:
        print(f"ok    {label}")
        PASS_COUNT += 1


# ── our_severity() — classify.py ─────────────────────────────────────────────
# error+high=Critical; error(other)=High; warning+high=High; warning=Medium;
# anything else (note/none/…)=Low.

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


check("error + high       → Critical",  our_severity({'level': 'error',   'confidence': 'high'}),   'Critical')
check("error + HIGH       → Critical (case-insensitive)",
      our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')
check("error + medium     → High",      our_severity({'level': 'error',   'confidence': 'medium'}), 'High')
check("error + low        → High",      our_severity({'level': 'error',   'confidence': 'low'}),    'High')
check("error (no conf)    → High",      our_severity({'level': 'error'}),                           'High')
check("warning + high     → High",      our_severity({'level': 'warning', 'confidence': 'high'}),   'High')
check("warning + medium   → Medium",    our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')
check("warning (no conf)  → Medium",    our_severity({'level': 'warning'}),                         'Medium')
check("note + high        → Low",       our_severity({'level': 'note',    'confidence': 'high'}),   'Low')
check("unknown level      → Low",       our_severity({'level': 'none'}),                            'Low')


# ── fingerprint computation — classify.py ─────────────────────────────────────
# fp = sha256(short_rule | basename(file) | re.sub(r'\s+', ' ', snippet)[:60])[:16]

def make_fingerprint(rule_id, file_uri, snippet):
    short_rule = rule_id.split('/')[-1]
    file_short = os.path.basename(file_uri)
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


fp_base = make_fingerprint(
    'auditor/unpinned-uses', '.github/workflows/lint.yml', 'uses: actions/checkout@v4')

check("fingerprint is deterministic",
      make_fingerprint('auditor/unpinned-uses', '.github/workflows/lint.yml',
                       'uses: actions/checkout@v4'),
      fp_base)

check("different rule → different fingerprint",
      make_fingerprint('auditor/artipacked', '.github/workflows/lint.yml',
                       'uses: actions/checkout@v4') == fp_base,
      False)

check("different file → different fingerprint",
      make_fingerprint('auditor/unpinned-uses', '.github/workflows/other.yml',
                       'uses: actions/checkout@v4') == fp_base,
      False)

# Only the basename of the file path is used.
check("full path hashes same as basename only",
      make_fingerprint('auditor/unpinned-uses',
                       'path/to/.github/workflows/lint.yml',
                       'uses: actions/checkout@v4'),
      fp_base)

# Whitespace is collapsed before hashing.
check("double-space snippet → same fp as single-space",
      make_fingerprint('auditor/unpinned-uses', '.github/workflows/lint.yml',
                       'uses:  actions/checkout@v4'),
      fp_base)

check("tab in snippet → same fp as space",
      make_fingerprint('auditor/unpinned-uses', '.github/workflows/lint.yml',
                       'uses:\tactions/checkout@v4'),
      fp_base)

# Snippet is truncated to 60 chars before hashing.
fp_long  = make_fingerprint('r', 'f.yml', 'x' * 80)
fp_sixty = make_fingerprint('r', 'f.yml', 'x' * 60)
check("snippet >60 chars truncated to 60 before hashing", fp_long, fp_sixty)

# Rule id: only the part after the last '/' matters.
check("rule without namespace prefix hashes identically",
      make_fingerprint('unpinned-uses', '.github/workflows/lint.yml',
                       'uses: actions/checkout@v4'),
      fp_base)


# ── calibration overrides — delta.py + finalize.py ───────────────────────────
# delta.py:    unpinned-uses Critical → High  (policy uplift, not exploit risk)
# finalize.py: secrets-outside-env High → Medium (GitHub Environments hardening)

def apply_calibrations(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
        if f['short_rule'] == 'secrets-outside-env' and f['severity'] == 'High':
            f['severity'] = 'Medium'
    return findings


cases = [
    {'short_rule': 'unpinned-uses',       'severity': 'Critical'},  # 0: → High
    {'short_rule': 'unpinned-uses',       'severity': 'High'},      # 1: stays High
    {'short_rule': 'secrets-outside-env', 'severity': 'High'},      # 2: → Medium
    {'short_rule': 'secrets-outside-env', 'severity': 'Medium'},    # 3: stays Medium
    {'short_rule': 'artipacked',          'severity': 'High'},      # 4: unaffected
]
apply_calibrations(cases)

check("unpinned-uses Critical → High",              cases[0]['severity'],        'High')
check("unpinned-uses Critical sets calibrated flag", cases[0].get('calibrated'), True)
check("unpinned-uses High stays High",              cases[1]['severity'],        'High')
check("secrets-outside-env High → Medium",          cases[2]['severity'],        'Medium')
check("secrets-outside-env Medium stays Medium",    cases[3]['severity'],        'Medium')
check("artipacked High is not calibrated",          cases[4]['severity'],        'High')


# ── shellcheck code bucketing — summarize_al.py ───────────────────────────────
# First matching code in the ordered list wins; unknown codes → 'other'.

KNOWN_CODES = ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']


def bucket_al_message(msg):
    for code in KNOWN_CODES:
        if code in msg:
            return code
    return 'other'


check("SC2086 matched",                          bucket_al_message("Unquoted var SC2086"),    'SC2086')
check("first match wins (SC2086 before SC2046)", bucket_al_message("SC2086 SC2046 present"), 'SC2086')
check("SC2046 when SC2086 absent",               bucket_al_message("SC2046 issue"),           'SC2046')
check("SC2034 (last in list) matched",           bucket_al_message("unused SC2034"),          'SC2034')
check("unlisted code → other",                   bucket_al_message("SC9999 unknown"),         'other')
check("empty message → other",                   bucket_al_message(""),                       'other')


# ── report ────────────────────────────────────────────────────────────────────

print()
if ERRORS:
    for e in ERRORS:
        print(e, file=sys.stderr)
    sys.exit(1)
else:
    print(f"All {PASS_COUNT} tests passed.")
