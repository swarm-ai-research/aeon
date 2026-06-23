"""Tests for severity classification and fingerprint logic used by workflow-security-audit.

Extracts and exercises pure functions from classify.py, delta.py, and
gen_trailer.py, covering branches that have no other test coverage.

Run: python3 .audit/test_classify_logic.py
"""

import ast
import hashlib
import os
import sys

AUDIT_DIR = os.path.dirname(os.path.abspath(__file__))


def _extract_fns(path, *names):
    """Compile named function definitions from a script without executing global code."""
    src = open(path).read()
    tree = ast.parse(src)
    nodes = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    ns = {"hashlib": hashlib, "os": os}
    for name in names:
        if name not in nodes:
            raise ValueError(f"{name} not found in {path}")
        mod = ast.Module(body=[nodes[name]], type_ignores=[])
        exec(compile(mod, path, "exec"), ns)
    return ns


classify_ns = _extract_fns(os.path.join(AUDIT_DIR, "classify.py"), "our_severity")
our_severity = classify_ns["our_severity"]

delta_ns = _extract_fns(os.path.join(AUDIT_DIR, "delta.py"), "fp_for")
fp_for = delta_ns["fp_for"]

# gen_trailer.fp() calls base(), so extract both into the same namespace.
trailer_ns = _extract_fns(os.path.join(AUDIT_DIR, "gen_trailer.py"), "base", "fp")
trailer_fp = trailer_ns["fp"]

passed = failed = 0


def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {label}")
    else:
        failed += 1
        print(f"  ✗ {label}", file=sys.stderr)


# ── our_severity() ───────────────────────────────────────────────────────────

print("our_severity():")

check(
    our_severity({"level": "error", "confidence": "high"}) == "Critical",
    "error + high → Critical",
)
# confidence is lowercased before comparison — uppercase must still match
check(
    our_severity({"level": "error", "confidence": "HIGH"}) == "Critical",
    "error + HIGH (uppercase) → Critical after lowercase",
)
# error without high confidence falls to the plain-error branch
check(
    our_severity({"level": "error", "confidence": "medium"}) == "High",
    "error + medium → High (not Critical)",
)
check(
    our_severity({"level": "error", "confidence": ""}) == "High",
    "error + empty confidence → High",
)
check(
    our_severity({"level": "error"}) == "High",
    "error + missing confidence key → High",
)
check(
    our_severity({"level": "warning", "confidence": "high"}) == "High",
    "warning + high → High",
)
check(
    our_severity({"level": "warning", "confidence": "low"}) == "Medium",
    "warning + low → Medium",
)
check(
    our_severity({"level": "warning"}) == "Medium",
    "warning + missing confidence → Medium",
)
# note-level findings stay Low regardless of confidence — confidence only
# uplifts error and warning levels
check(
    our_severity({"level": "note", "confidence": "high"}) == "Low",
    "note + high → Low (confidence irrelevant at note level)",
)
check(
    our_severity({"level": "note"}) == "Low",
    "note → Low",
)
# Any unrecognised level falls through to Low
check(
    our_severity({"level": "none", "confidence": "high"}) == "Low",
    "unknown level → Low (fallthrough)",
)
check(
    our_severity({"level": "", "confidence": "high"}) == "Low",
    "empty level → Low (fallthrough)",
)


# ── fingerprint functions ─────────────────────────────────────────────────────

print("\nfingerprint functions:")

fp1 = fp_for("unpinned-uses", ".github/workflows/aeon.yml", "Setup Node")
fp2 = fp_for("unpinned-uses", ".github/workflows/aeon.yml", "Setup Node")
check(fp1 == fp2, "fp_for() is deterministic")
check(len(fp1) == 16, "fp_for() returns 16 hex chars")
check(all(c in "0123456789abcdef" for c in fp1), "fp_for() output is lowercase hex")

# Only the basename of the file path should matter
check(
    fp_for("rule", ".github/workflows/foo.yml", "step")
    == fp_for("rule", "foo.yml", "step"),
    "fp_for() strips directory components (basename only)",
)

# delta.py preserves spaces in the step; gen_trailer.py converts them to
# underscores.  Same step "Setup Node" → two different fingerprints.  The
# delta workaround (trying both forms) is verified by the third assertion.
fp_spaces = fp_for("unpinned-uses", "aeon.yml", "Setup Node")
fp_underscores = trailer_fp("unpinned-uses", "aeon.yml", "Setup Node")
check(
    fp_spaces != fp_underscores,
    "fp_for(spaces) vs gen_trailer fp(underscores) differ for the same step",
)
fp_underscore_explicit = fp_for("unpinned-uses", "aeon.yml", "Setup_Node")
check(
    fp_underscore_explicit == fp_underscores,
    'fp_for("Setup_Node") matches gen_trailer fp("Setup Node") — delta workaround is sound',
)

# Boundary: all-empty inputs must not crash and must return 16-char hex
check(len(fp_for("", "", "")) == 16, "fp_for() handles all-empty inputs")

# Fingerprints must differ when any component changes
check(fp_for("a", "b", "c") != fp_for("a", "b", "d"), "fp_for() is sensitive to step")
check(fp_for("a", "b", "c") != fp_for("x", "b", "c"), "fp_for() is sensitive to rule")
check(fp_for("a", "b", "c") != fp_for("a", "z", "c"), "fp_for() is sensitive to filename")


# ── Results ──────────────────────────────────────────────────────────────────

print(f"\n{passed} passed, {failed} failed")
if failed:
    sys.exit(1)
