# test_audit_logic.py — unit tests for pure logic in classify.py / delta.py / summarize_al.py
#
# Run: python .audit/test_audit_logic.py
#
# These scripts are not importable (side-effectful on import), so we replicate
# their pure functions here and test them directly.

import hashlib
import os
import sys
from collections import Counter

# ── our_severity (classify.py) ──────────────────────────────────────────────

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


# ── fp_for (delta.py) ───────────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── calibration override (delta.py / delta2.py) ─────────────────────────────

def apply_calibration(findings):
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


# ── shellcheck first-match-wins (summarize_al.py) ───────────────────────────

def count_sc_codes(messages):
    codes = Counter()
    for msg in messages:
        matched = False
        for code in ['SC2086', 'SC2046', 'SC2129', 'SC2153', 'SC2155', 'SC2034']:
            if code in msg:
                codes[code] += 1
                matched = True
                break
        if not matched:
            codes['other'] += 1
    return codes


# ── test harness ────────────────────────────────────────────────────────────

failures = []

def check(label, expected, actual):
    if actual != expected:
        failures.append(label)
        print(f"FAIL {label}\n     expected {expected!r}\n     got      {actual!r}")
    else:
        print(f"OK   {label}")


# our_severity — happy paths

check("error+high → Critical",    "Critical", our_severity({"level": "error",   "confidence": "high"}))
check("error+medium → High",      "High",     our_severity({"level": "error",   "confidence": "medium"}))
check("error+empty → High",       "High",     our_severity({"level": "error",   "confidence": ""}))
check("error+missing-conf → High","High",     our_severity({"level": "error"}))
check("warning+high → High",      "High",     our_severity({"level": "warning", "confidence": "high"}))
check("warning+medium → Medium",  "Medium",   our_severity({"level": "warning", "confidence": "medium"}))
check("warning+missing → Medium", "Medium",   our_severity({"level": "warning"}))

# our_severity — note level always → Low regardless of confidence
check("note+high → Low (not High)",   "Low", our_severity({"level": "note", "confidence": "high"}))
check("note+missing → Low",           "Low", our_severity({"level": "note"}))
check("unknown-level → Low",          "Low", our_severity({"level": "none", "confidence": "high"}))

# our_severity — confidence comparison is case-insensitive (.lower())
check("error+HIGH(upper) → Critical", "Critical", our_severity({"level": "error",   "confidence": "HIGH"}))
check("warning+HIGH(upper) → High",   "High",     our_severity({"level": "warning", "confidence": "HIGH"}))


# calibration override — unpinned-uses Critical → High

f_crit = {"short_rule": "unpinned-uses", "severity": "Critical"}
apply_calibration([f_crit])
check("unpinned-uses Critical → High",    "High", f_crit["severity"])
check("unpinned-uses Critical: calibrated=True", True, f_crit.get("calibrated"))

# unpinned-uses already High stays High; calibrated must not be set
f_high = {"short_rule": "unpinned-uses", "severity": "High"}
apply_calibration([f_high])
check("unpinned-uses High unchanged",          "High",  f_high["severity"])
check("unpinned-uses High: calibrated NOT set", False, f_high.get("calibrated", False))

# other rule with Critical stays Critical
f_other = {"short_rule": "template-injection", "severity": "Critical"}
apply_calibration([f_other])
check("other-rule Critical unchanged",        "Critical", f_other["severity"])
check("other-rule Critical: calibrated NOT set", False, f_other.get("calibrated", False))


# fp_for — determinism, distinctness, basename-only

fp_a = fp_for("unpinned-uses", ".github/workflows/ci.yml", "Build")
fp_b = fp_for("unpinned-uses", ".github/workflows/ci.yml", "Build")
check("fp_for deterministic",             fp_a, fp_b)

fp_c = fp_for("unpinned-uses", ".github/workflows/deploy.yml", "Build")
check("fp_for different file → different",  True, fp_a != fp_c)

fp_d = fp_for("unpinned-uses", ".github/workflows/ci.yml", "Build step")
check("fp_for different step → different",  True, fp_a != fp_d)

# basename-only: deep/path/x.yml and other/path/x.yml share the same basename
fp_e = fp_for("rule", "a/b/c.yml", "S")
fp_f = fp_for("rule", "x/y/c.yml", "S")
check("fp_for: same basename → same fp",   fp_e, fp_f)

check("fp_for output is 16 hex chars", True, len(fp_a) == 16 and all(c in '0123456789abcdef' for c in fp_a))


# shellcheck first-match-wins — break stops at first matching code

# single code
c = count_sc_codes(["SC2086: Double quote to prevent globbing"])
check("SC2086 only → SC2086 counted", 1, c['SC2086'])

# message containing both SC2086 and SC2046: only SC2086 counted (comes first in list)
c = count_sc_codes(["SC2086 and SC2046 found"])
check("SC2086+SC2046 in message → only SC2086 counted", 1, c['SC2086'])
check("SC2086+SC2046 in message → SC2046 NOT counted",  0, c['SC2046'])

# SC2046 alone (not shadowed by SC2086)
c = count_sc_codes(["SC2046: Quote this to prevent word splitting"])
check("SC2046 alone → SC2046 counted", 1, c['SC2046'])

# no known code → 'other'
c = count_sc_codes(["some unrecognized warning message"])
check("no SC code → other", 1, c['other'])

# multiple distinct messages
c = count_sc_codes(["SC2086 issue", "SC2153 issue", "unrelated warning"])
check("multiple messages: SC2086=1 SC2153=1 other=1",
      {"SC2086": 1, "SC2153": 1, "other": 1}, dict(c))

# SC2034 at end of priority list
c = count_sc_codes(["SC2034: var appears unused"])
check("SC2034 alone → SC2034 counted", 1, c['SC2034'])


# ── result ──────────────────────────────────────────────────────────────────

print(f"\n{'='*55}")
if failures:
    print(f"FAILED: {len(failures)} test(s): {failures}")
    sys.exit(1)
else:
    print(f"All {sum(1 for line in open(__file__) if line.strip().startswith('check('))} tests passed.")
