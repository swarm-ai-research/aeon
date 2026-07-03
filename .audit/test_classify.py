"""
Tests for the classify.py helpers: our_severity() and fingerprint generation.

Run: python3 .audit/test_classify.py

These functions are inlined here to avoid classify.py's module-level JSON reads.
"""

import hashlib
import os
import re
import sys


# --- Functions under test (mirrored from classify.py) ----------------------

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


def make_fingerprint(rule_id, file_uri, snippet):
    short_rule = rule_id.split('/')[-1]
    snip_key = re.sub(r'\s+', ' ', snippet)[:60]
    file_short = os.path.basename(file_uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


# --- Test helpers -----------------------------------------------------------

_failures = []

def check(label, got, want):
    if got != want:
        _failures.append(f"FAIL {label}: got {got!r}, want {want!r}")
    else:
        print(f"  ok  {label}")


# --- our_severity tests -----------------------------------------------------

def test_severity():
    print("our_severity()")

    # error + high → Critical
    check("error/high→Critical",
          our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    # confidence comparison is case-insensitive
    check("error/HIGH→Critical",
          our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    # error + medium → High (not Critical)
    check("error/medium→High",
          our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    # error + low → High
    check("error/low→High",
          our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    # error + missing confidence key → High
    check("error/missing-conf→High",
          our_severity({'level': 'error'}), 'High')

    # error + empty string confidence → High
    check("error/empty-conf→High",
          our_severity({'level': 'error', 'confidence': ''}), 'High')

    # warning + high → High (not Medium)
    check("warning/high→High",
          our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    # warning + medium → Medium
    check("warning/medium→Medium",
          our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    # warning + missing confidence → Medium
    check("warning/missing-conf→Medium",
          our_severity({'level': 'warning'}), 'Medium')

    # note → Low (default branch)
    check("note→Low",
          our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    # unknown level → Low
    check("unknown-level→Low",
          our_severity({'level': 'info', 'confidence': 'high'}), 'Low')


# --- fingerprint tests ------------------------------------------------------

def test_fingerprint():
    print("\nmake_fingerprint()")

    # Deterministic: same inputs → same output
    fp1 = make_fingerprint('template-injection', '.github/workflows/foo.yml', 'echo $INPUT')
    fp2 = make_fingerprint('template-injection', '.github/workflows/foo.yml', 'echo $INPUT')
    check("deterministic", fp1, fp2)

    # Output is exactly 16 hex chars
    check("length-16", len(fp1), 16)
    check("hex-chars", all(c in '0123456789abcdef' for c in fp1), True)

    # Namespaced rule_id: only the last segment is used
    fp_ns  = make_fingerprint('some/ns/template-injection', 'foo.yml', 'snip')
    fp_bare = make_fingerprint('template-injection', 'foo.yml', 'snip')
    check("namespace-stripped", fp_ns, fp_bare)

    # File path: only basename matters
    fp_abs = make_fingerprint('rule', '/full/path/to/aeon.yml', 'snip')
    fp_rel = make_fingerprint('rule', 'aeon.yml', 'snip')
    check("basename-only", fp_abs, fp_rel)

    # Whitespace in snippet is normalised (multiple spaces/newlines → single space)
    fp_multi  = make_fingerprint('rule', 'f.yml', 'echo  \n  $VAR')
    fp_single = make_fingerprint('rule', 'f.yml', 'echo $VAR')
    check("whitespace-normalised", fp_multi, fp_single)

    # Snippet is truncated to 60 chars after normalisation; extra chars don't change fp
    long_snippet  = 'A' * 80
    extra_snippet = 'A' * 80 + 'EXTRA'
    fp_long  = make_fingerprint('rule', 'f.yml', long_snippet)
    fp_extra = make_fingerprint('rule', 'f.yml', extra_snippet)
    check("snippet-truncated-at-60", fp_long, fp_extra)

    # Edge case: empty snippet
    fp_empty = make_fingerprint('rule', 'f.yml', '')
    check("empty-snippet-length", len(fp_empty), 16)

    # Different rules → different fingerprints
    fp_a = make_fingerprint('rule-a', 'f.yml', 'snip')
    fp_b = make_fingerprint('rule-b', 'f.yml', 'snip')
    check("different-rules-differ", fp_a != fp_b, True)


# --- Run --------------------------------------------------------------------

if __name__ == '__main__':
    test_severity()
    test_fingerprint()

    if _failures:
        print(f"\n{len(_failures)} failure(s):")
        for f in _failures:
            print(f"  {f}")
        sys.exit(1)
    else:
        print("\nAll tests passed.")
