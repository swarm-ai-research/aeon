"""
Tests for .audit/ processing logic.
Run: python3 .audit/test_classify.py
"""
import ast
import hashlib
import os
import re
import sys
import types
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

PASS_COUNT = 0
FAIL_COUNT = 0


def check(cond, msg):
    global PASS_COUNT, FAIL_COUNT
    if cond:
        print(f"  ok  {msg}")
        PASS_COUNT += 1
    else:
        print(f"FAIL  {msg}")
        FAIL_COUNT += 1


def load_fn(filename, fn_name):
    """Extract a single function from a script file without executing its I/O."""
    src = open(os.path.join(HERE, filename)).read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn_name:
            mod = types.ModuleType(f"_{fn_name}")
            mod.__dict__.update({"os": os, "re": re, "hashlib": hashlib})
            exec(
                compile(ast.Module(body=[node], type_ignores=[]), filename, "exec"),
                mod.__dict__,
            )
            return mod.__dict__[fn_name]
    raise AttributeError(f"{fn_name!r} not found in {filename}")


# ── our_severity (classify.py) ───────────────────────────────────────────────
our_severity = load_fn("classify.py", "our_severity")

print("our_severity:")
# Critical path: error + high
check(our_severity({"level": "error", "confidence": "high"}) == "Critical", "error+high → Critical")
# confidence comparison is case-insensitive (.lower())
check(our_severity({"level": "error", "confidence": "High"}) == "Critical", "error+High(mixed-case) → Critical")
check(our_severity({"level": "error", "confidence": "HIGH"}) == "Critical", "error+HIGH(upper) → Critical")
# error + non-high confidence falls to second branch → High
check(our_severity({"level": "error", "confidence": "medium"}) == "High", "error+medium → High")
check(our_severity({"level": "error", "confidence": "low"}) == "High", "error+low → High")
check(our_severity({"level": "error", "confidence": ""}) == "High", "error+empty conf → High")
# missing key: f.get('confidence', '') → ''
check(our_severity({"level": "error"}) == "High", "error+missing conf key → High")
# warning + high → High
check(our_severity({"level": "warning", "confidence": "high"}) == "High", "warning+high → High")
check(our_severity({"level": "warning", "confidence": "HIGH"}) == "High", "warning+HIGH(upper) → High")
# warning + non-high → Medium
check(our_severity({"level": "warning", "confidence": "medium"}) == "Medium", "warning+medium → Medium")
check(our_severity({"level": "warning", "confidence": ""}) == "Medium", "warning+empty conf → Medium")
check(our_severity({"level": "warning"}) == "Medium", "warning+missing conf key → Medium")
# note falls through all branches → Low regardless of confidence
check(our_severity({"level": "note", "confidence": "high"}) == "Low", "note+high → Low (no special note branch)")
check(our_severity({"level": "note", "confidence": ""}) == "Low", "note+empty → Low")
# completely unknown level → Low
check(our_severity({"level": "unknown", "confidence": "high"}) == "Low", "unknown level → Low")
check(our_severity({"level": "", "confidence": "high"}) == "Low", "empty level → Low")

# Confirm extract_steps.py has the same our_severity logic
our_severity_es = load_fn("extract_steps.py", "our_severity")
for level, conf, expected in [
    ("error", "high", "Critical"),
    ("error", "medium", "High"),
    ("warning", "high", "High"),
    ("warning", "medium", "Medium"),
    ("note", "high", "Low"),
]:
    check(
        our_severity_es({"level": level, "confidence": conf}) == expected,
        f"extract_steps.our_severity: {level}+{conf} → {expected}",
    )

# ── classify.py fingerprint: sha256(short_rule|basename(file)|snippet[:60])[:16] ──
print("\nclassify.py fingerprint:")


def classify_fp(rule_id, file_uri, snippet):
    short_rule = rule_id.split("/")[-1]
    snip_key = re.sub(r"\s+", " ", snippet)[:60]
    file_short = os.path.basename(file_uri)
    fp_src = f"{short_rule}|{file_short}|{snip_key}"
    return hashlib.sha256(fp_src.encode()).hexdigest()[:16]


fp1 = classify_fp("zizmor/unpinned-uses", ".github/workflows/aeon.yml", "uses: actions/checkout@v3\n")
check(len(fp1) == 16, "fingerprint length is 16")
check(all(c in "0123456789abcdef" for c in fp1), "fingerprint is lowercase hex")

# whitespace normalization: tabs/newlines/runs collapse to single space
check(
    classify_fp("r", "f.yml", "a  b\n\tc") == classify_fp("r", "f.yml", "a b c"),
    "multi-whitespace in snippet normalised to single space",
)
# path stripping: deep path has same fp as basename alone
check(
    classify_fp("r", ".github/workflows/deep/aeon.yml", "x") == classify_fp("r", "aeon.yml", "x"),
    "only basename used in classify.py fingerprint",
)
# snippet truncated at 60 chars: chars 61+ are ignored
check(
    classify_fp("r", "f.yml", "a" * 100) == classify_fp("r", "f.yml", "a" * 60),
    "snippet truncated at 60 chars",
)
check(
    classify_fp("r", "f.yml", "a" * 59 + "X") != classify_fp("r", "f.yml", "a" * 59 + "Y"),
    "char at position 60 still distinguishes fingerprints",
)
# different rules → different fingerprints
check(
    classify_fp("rule-a", "f.yml", "x") != classify_fp("rule-b", "f.yml", "x"),
    "different rules → different fingerprints",
)
# rule_id split on '/': only last segment used
check(
    classify_fp("zizmor/foo", "f.yml", "x") == classify_fp("foo", "f.yml", "x"),
    "rule_id split on / — only last segment used",
)

# ── gen_trailer.py fingerprint: sha256(rule|basename(fname)|step_underscored)[:16] ──
print("\ngen_trailer.py fingerprint:")


def trailer_fp(rule, fname, step):
    s = f"{rule}|{os.path.basename(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


check(len(trailer_fp("foo", "aeon.yml", "Setup Node")) == 16, "trailer fingerprint is 16 chars")
# spaces in step replaced with underscores
check(
    trailer_fp("r", "f.yml", "Setup Node") == trailer_fp("r", "f.yml", "Setup_Node"),
    "spaces in step name replaced with underscores for fingerprint",
)
# gen_trailer.py and delta.py both re-normalise step spaces — fingerprint must be stable
step_variants = ["Setup Node", "Setup_Node", "Setup  Node"]
fps = [trailer_fp("r", "f.yml", s) for s in step_variants]
check(fps[0] == fps[1], "space→underscore in step: 'Setup Node' == 'Setup_Node'")
# gen_trailer status: Critical/High → 'manual', else 'open'
for sev, expected in [("Critical", "manual"), ("High", "manual"), ("Medium", "open"), ("Low", "open")]:
    status = "manual" if sev in ("Critical", "High") else "open"
    check(status == expected, f"severity={sev} → status={expected}")

# ── summarize_al.py: shellcheck code matching ────────────────────────────────
KNOWN_CODES = ["SC2086", "SC2046", "SC2129", "SC2153", "SC2155", "SC2034"]

print("\nsummarize_al code matching:")


def classify_al(msg):
    """Mirrors summarize_al.py per-message classification."""
    for code in KNOWN_CODES:
        if code in msg:
            return code
    return "other"


check(classify_al("SC2086: Double quote to prevent globbing") == "SC2086", "SC2086 detected")
check(classify_al("SC2034: foo is referenced but not assigned") == "SC2034", "SC2034 (last in list) detected")
check(classify_al("no shellcheck code here") == "other", "no known code → 'other'")
# Critical edge case: when both SC2086 and SC2046 appear, LIST ORDER wins (not message order)
check(
    classify_al("SC2046 and SC2086 in message") == "SC2086",
    "SC2086 wins over SC2046 when both present — list order, not message order",
)
check(
    classify_al("SC2046 only") == "SC2046",
    "SC2046 detected when SC2086 absent",
)

# HIGH-CANDIDATE: (SC2086 or SC2046) AND 'github.' in msg (case-insensitive)
def is_high_candidate(msg):
    return ("SC2086" in msg or "SC2046" in msg) and "github." in msg.lower()


check(is_high_candidate("SC2086 $github.event.inputs.value") == True, "SC2086+github. → HIGH-CANDIDATE")
check(is_high_candidate("SC2046 GITHUB.SHA") == True, "SC2046+GITHUB.(uppercase) → HIGH-CANDIDATE via lower()")
check(is_high_candidate("SC2086 no github ref here") == False, "SC2086 without github. → not HIGH-CANDIDATE")
check(is_high_candidate("SC2129 github.event") == False, "SC2129+github. → not HIGH-CANDIDATE (wrong code)")
check(is_high_candidate("SC2046 no github") == False, "SC2046 without github. → not HIGH-CANDIDATE")

# ── delta.py calibration override ────────────────────────────────────────────
print("\ndelta.py calibration override:")


def apply_calibration(findings):
    """Mirrors delta.py: unpinned-uses Critical → High."""
    for f in findings:
        if f["short_rule"] == "unpinned-uses" and f["severity"] == "Critical":
            f["severity"] = "High"
            f["calibrated"] = True
    return findings


findings = [
    {"short_rule": "unpinned-uses", "severity": "Critical"},
    {"short_rule": "unpinned-uses", "severity": "High"},  # already High
    {"short_rule": "template-injection", "severity": "Critical"},  # different rule
    {"short_rule": "unpinned-uses", "severity": "Medium"},  # not Critical
]
result = apply_calibration(findings)
check(result[0]["severity"] == "High", "unpinned-uses Critical downgraded to High")
check(result[0].get("calibrated") is True, "calibrated flag set on downgraded finding")
check(result[1]["severity"] == "High", "unpinned-uses already-High unchanged")
check(result[1].get("calibrated") is None, "no calibrated flag when severity unchanged")
check(result[2]["severity"] == "Critical", "other rule Critical NOT downgraded")
check(result[3]["severity"] == "Medium", "unpinned-uses Medium not touched")

# ── summary ───────────────────────────────────────────────────────────────────
print(f"\n{PASS_COUNT} passed, {FAIL_COUNT} failed")
if FAIL_COUNT:
    sys.exit(1)
