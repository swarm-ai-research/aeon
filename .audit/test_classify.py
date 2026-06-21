"""Tests for the severity-classification and fingerprint logic used by the
workflow-security-audit pipeline (classify.py, delta.py, gen_trailer.py).

These functions can't be imported directly because the source scripts read
from hardcoded paths at module level, so the pure logic is replicated here.

Run:  python3 .audit/test_classify.py
"""

import hashlib
import os
import sys


# ── Replicate our_severity() from classify.py ──────────────────────────────

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


# ── Replicate fingerprint helpers from gen_trailer.py and delta.py ──────────

def fp_trailer(rule, fname, step):
    """gen_trailer.py: stores fingerprints with spaces-replaced-by-underscores."""
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def fp_delta(rule, fname, step):
    """delta.py fp_for(): does NOT replace spaces, relies on caller to try both."""
    s = f"{rule}|{os.path.basename(fname)}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Test runner ─────────────────────────────────────────────────────────────

_failures = []

def check(name, got, expected):
    if got == expected:
        print(f"  OK  {name}")
    else:
        msg = f"FAIL  {name}: expected {expected!r}, got {got!r}"
        print(f"  {msg}", file=sys.stderr)
        _failures.append(msg)


# ── Severity tests ───────────────────────────────────────────────────────────

print("our_severity():")

# error + high confidence → Critical
check("error+high → Critical",
      our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

# uppercase confidence is normalised via .lower()
check("error+HIGH (uppercase) → Critical",
      our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

# mixed-case
check("error+High (mixed) → Critical",
      our_severity({'level': 'error', 'confidence': 'High'}), 'Critical')

# error + non-high confidence → High (not Critical)
check("error+medium → High",
      our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

check("error+low → High",
      our_severity({'level': 'error', 'confidence': 'low'}), 'High')

# missing confidence field uses default '' which != 'high' → High
check("error+missing confidence → High (not Critical)",
      our_severity({'level': 'error'}), 'High')

check("error+empty string confidence → High",
      our_severity({'level': 'error', 'confidence': ''}), 'High')

# warning + high → High
check("warning+high → High",
      our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

check("warning+High (mixed) → High",
      our_severity({'level': 'warning', 'confidence': 'High'}), 'High')

# warning + non-high → Medium
check("warning+medium → Medium",
      our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

check("warning+missing confidence → Medium",
      our_severity({'level': 'warning'}), 'Medium')

# note level always → Low regardless of confidence
check("note+high → Low",
      our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

check("note+missing → Low",
      our_severity({'level': 'note'}), 'Low')

# unknown / future levels fall through to Low
check("unknown level 'none' → Low",
      our_severity({'level': 'none'}), 'Low')

check("unknown level 'info' → Low",
      our_severity({'level': 'info'}), 'Low')


# ── Fingerprint tests ────────────────────────────────────────────────────────

print("\nFingerprint consistency:")

RULE  = "template-injection"
FNAME = ".github/workflows/messages.yml"
STEP_WITH_SPACES    = "Extract message"
STEP_WITH_UNDERSCORES = "Extract_message"

trailer_spaces = fp_trailer(RULE, FNAME, STEP_WITH_SPACES)
trailer_unders = fp_trailer(RULE, FNAME, STEP_WITH_UNDERSCORES)
delta_spaces   = fp_delta(RULE, FNAME, STEP_WITH_SPACES)
delta_unders   = fp_delta(RULE, FNAME, STEP_WITH_UNDERSCORES)

# gen_trailer stores underscores; so a step "Extract message" in trailer == "Extract_message"
check("trailer normalises spaces→underscores: fp('Extract message') == fp('Extract_message')",
      trailer_spaces, trailer_unders)

# delta.py does NOT normalise, so it produces different hashes for "Extract message"
# vs "Extract_message" — it compensates by trying both versions in the prior_fp_set.
check("delta fp('Extract message') != fp('Extract_message') [different without normalisation]",
      delta_spaces != delta_unders, True)

# The delta lookup covers both variants: the trailer's fingerprint must match
# at least one of the two delta variants.
check("trailer fp for 'Extract message' matches delta fp for 'Extract_message'",
      trailer_spaces, delta_unders)

# Basename stripping: full path vs basename give the same fingerprint
check("full path and basename produce identical fingerprint (trailer)",
      fp_trailer(RULE, FNAME, STEP_WITH_SPACES),
      fp_trailer(RULE, os.path.basename(FNAME), STEP_WITH_SPACES))

check("full path and basename produce identical fingerprint (delta)",
      fp_delta(RULE, FNAME, STEP_WITH_SPACES),
      fp_delta(RULE, os.path.basename(FNAME), STEP_WITH_SPACES))

# Fingerprint length is always 16 hex chars
check("fingerprint is 16 hex chars",
      len(trailer_spaces) == 16 and all(c in '0123456789abcdef' for c in trailer_spaces), True)


# ── Result ───────────────────────────────────────────────────────────────────

_total = 15 + 6  # severity + fingerprint tests
if _failures:
    print(f"\n{len(_failures)}/{_total} test(s) FAILED.", file=sys.stderr)
    sys.exit(1)
else:
    print(f"\nAll {_total} classify tests passed.")
