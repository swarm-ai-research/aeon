#!/usr/bin/env python3
"""Build the audit report from findings.json."""
import json, pathlib, subprocess, collections

ROOT = pathlib.Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
today = subprocess.check_output(["date", "-u", "+%F"]).decode().strip()

def gh(args):
    try:
        return subprocess.check_output(["gh"] + args, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""

REPO_NAME = gh(["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]) or "unknown/unknown"
REPO_URL = gh(["repo", "view", "--json", "url", "-q", ".url"]) or ""

with open(ROOT / "findings.json") as f:
    findings = json.load(f)

# Delta vs prior audit
prior_files = sorted((REPO_ROOT / "articles").glob("workflow-security-audit-*.md"))
prior_fps = {}
prior_date = None
if prior_files:
    prior_path = prior_files[-1]
    prior_date = prior_path.stem.split("workflow-security-audit-")[-1]
    text = prior_path.read_text()
    if "workflow-security-audit-fingerprints" in text:
        block = text.split("workflow-security-audit-fingerprints", 1)[1]
        block = block.split("-->", 1)[0]
        for ln in block.splitlines():
            ln = ln.strip()
            if not ln:
                continue
            fp = ln.split()[0]
            attrs = {}
            for tok in ln.split()[1:]:
                if "=" in tok:
                    k, v = tok.split("=", 1)
                    attrs[k] = v
            prior_fps[fp] = attrs

for x in findings:
    fp = x["fingerprint"]
    if fp in prior_fps:
        prior_status = prior_fps[fp].get("status", "")
        if prior_status in ("auto-fixed", "resolved"):
            x["delta"] = "REINTRODUCED"
        else:
            x["delta"] = "UNCHANGED"
    else:
        x["delta"] = "NEW"

# Resolved (in prior, not in current)
current_fps = {x["fingerprint"] for x in findings}
resolved = []
for fp, attrs in prior_fps.items():
    if fp not in current_fps and attrs.get("status") != "resolved":
        resolved.append((fp, attrs))

# Counts
counts = collections.Counter()
for x in findings:
    counts[(x["delta"], x["severity"])] += 1
    counts[("total",)] += 1
    counts[("sev", x["severity"])] += 1
    counts[("delta", x["delta"])] += 1

new_crit = counts[("NEW", "Critical")]
new_high = counts[("NEW", "High")]
new_med = counts[("NEW", "Medium")]
new_low = counts[("NEW", "Low")]
new_count = new_crit + new_high + new_med + new_low
reintroduced_count = sum(counts[("REINTRODUCED", s)] for s in ("Critical", "High", "Medium", "Low"))
unchanged_count = sum(counts[("UNCHANGED", s)] for s in ("Critical", "High", "Medium", "Low"))
resolved_count = len(resolved)
total = counts[("total",)]
crit = counts[("sev", "Critical")]
high = counts[("sev", "High")]
med = counts[("sev", "Medium")]
low = counts[("sev", "Low")]

# Verdict + exit mode
if total == 0:
    verdict = f"WORKFLOW_AUDIT_CLEAN — no findings across 7 files"
    exit_mode = "CLEAN"
elif new_count == 0 and reintroduced_count == 0:
    verdict = f"WORKFLOW_AUDIT_UNCHANGED — {unchanged_count} carried over from {prior_date}"
    exit_mode = "UNCHANGED"
elif reintroduced_count > 0:
    verdict = f"WORKFLOW_AUDIT_REGRESSION — {reintroduced_count} previously-fixed finding(s) reintroduced"
    exit_mode = "REGRESSION"
elif new_crit > 0:
    verdict = f"WORKFLOW_AUDIT_NEW_CRITICAL — {new_crit} new critical finding(s)"
    exit_mode = "NEW_CRITICAL"
elif new_high > 0:
    verdict = f"WORKFLOW_AUDIT_NEW_HIGH — {new_high} new high-severity finding(s)"
    exit_mode = "NEW_HIGH"
else:
    verdict = f"WORKFLOW_AUDIT_NEW_INFO — {new_count} new lower-severity finding(s)"
    exit_mode = "NEW_INFO"

# Workflow / action counts
workflow_count = len(list((REPO_ROOT / ".github/workflows").glob("*.y*ml")))
action_count = 0

# Auto-fix decisions (script marks findings; we don't apply here — per skill rules
# none of the NEW C/H findings match the fix templates).
MANUAL_ONLY_RULES = {
    "zizmor/unpinned-uses",       # skill: never auto-fix, operator picks SHA
    "zizmor/secrets-outside-env", # not a script-injection, needs env boundary
    "zizmor/artipacked",          # persist-credentials pattern — always manual
    "zizmor/undocumented-permissions",
    "zizmor/anonymous-definition",
    "zizmor/concurrency-limits",
    "zizmor/template-injection",  # each needs case-by-case env extraction
    "actionlint-shellcheck",      # style/lint, not auto-fixable at report time
}

fixed_count = 0
manual_count = 0
for x in findings:
    x["status"] = "Manual review required"
    if x["delta"] == "NEW" and x["severity"] in ("Critical", "High"):
        if x["rule_id"] in MANUAL_ONLY_RULES:
            manual_count += 1
        else:
            manual_count += 1  # nothing auto-fixed in this audit

# Save enriched findings for the notify step
with open(ROOT / "findings_enriched.json", "w") as f:
    json.dump({
        "findings": findings,
        "verdict": verdict,
        "exit_mode": exit_mode,
        "counts": {
            "total": total,
            "crit": crit, "high": high, "med": med, "low": low,
            "new": new_count, "new_crit": new_crit, "new_high": new_high,
            "new_med": new_med, "new_low": new_low,
            "reintroduced": reintroduced_count,
            "unchanged": unchanged_count,
            "resolved": resolved_count,
            "fixed": fixed_count,
            "manual": manual_count,
        },
        "prior_date": prior_date,
        "workflow_count": workflow_count,
        "action_count": action_count,
    }, f, indent=2)

print(f"verdict={verdict}")
print(f"exit_mode={exit_mode}")
print(f"total={total} crit={crit} high={high} med={med} low={low}")
print(f"new={new_count} reintroduced={reintroduced_count} unchanged={unchanged_count} resolved={resolved_count}")
print(f"fixed={fixed_count} manual={manual_count}")
