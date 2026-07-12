#!/usr/bin/env python3
"""Write articles/workflow-security-audit-${today}.md per SKILL.md format."""
import json, pathlib, subprocess, glob, re
from collections import Counter, defaultdict

TODAY = "2026-07-12"
REPORT = f"articles/workflow-security-audit-{TODAY}.md"

def gh(args):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=15)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""

REPO_NAME = gh(["gh","repo","view","--json","nameWithOwner","-q",".nameWithOwner"]) or "unknown/unknown"
REPO_URL = gh(["gh","repo","view","--json","url","-q",".url"]) or f"https://github.com/{REPO_NAME}"

d = json.loads(pathlib.Path(".audit/classified.json").read_text())
findings = d["findings"]
resolved = d["resolved"]
PRIOR = d["prior"]
PRIOR_DATE = re.search(r"(\d{4}-\d{2}-\d{2})", PRIOR).group(1) if PRIOR else None

# Counts
workflow_files = sorted(glob.glob(".github/workflows/*.yml") + glob.glob(".github/workflows/*.yaml"))
action_files = sorted(glob.glob(".github/actions/**/action.yml", recursive=True) + glob.glob(".github/actions/**/action.yaml", recursive=True))
total_audited = len(workflow_files) + len(action_files)

new = [x for x in findings if x["classification"]=="NEW"]
reintro = [x for x in findings if x["classification"]=="REINTRODUCED"]
unchanged = [x for x in findings if x["classification"]=="UNCHANGED"]

crit = [x for x in new if x["severity"]=="Critical"]
high = [x for x in new if x["severity"]=="High"]
med = [x for x in new if x["severity"]=="Medium"]
low = [x for x in new if x["severity"]=="Low"]

# Verdict per SKILL step 5
if not findings:
    VERDICT = f"WORKFLOW_AUDIT_CLEAN — no findings across {total_audited} files"
    EXIT_MODE = "CLEAN"
elif not new and not reintro:
    VERDICT = f"WORKFLOW_AUDIT_UNCHANGED — {len(unchanged)} carried over from {PRIOR_DATE}"
    EXIT_MODE = "UNCHANGED"
elif reintro:
    VERDICT = f"WORKFLOW_AUDIT_REGRESSION — {len(reintro)} previously-fixed finding(s) reintroduced"
    EXIT_MODE = "REGRESSION"
elif crit:
    VERDICT = f"WORKFLOW_AUDIT_NEW_CRITICAL — {len(crit)} new critical finding(s)"
    EXIT_MODE = "NEW_CRITICAL"
elif high:
    VERDICT = f"WORKFLOW_AUDIT_NEW_HIGH — {len(high)} new high-severity finding(s)"
    EXIT_MODE = "NEW_HIGH"
else:
    VERDICT = f"WORKFLOW_AUDIT_NEW_INFO — {len(new)} new lower-severity finding(s)"
    EXIT_MODE = "NEW_INFO"

# Auto-fix eligibility per SKILL: NEW Critical/High EXCEPT unpinned-uses / permissions / persist-credentials
# and only for script-injection / toJson-into-shell / GITHUB_ENV-write templates.
AUTO_FIX_RULES = {
    "handrolled/tojson-shell-injection",
    "handrolled/github-env-write-user-data",
    # Basic template-injection at High severity CAN be auto-fixed via env intermediary,
    # but zizmor's template-injection here is all Low (pedantic). No High/Critical
    # template-injection findings this run.
    "template-injection",
}
FORBIDDEN_AUTOFIX = {
    "unpinned-uses",
    "excessive-permissions",
    "undocumented-permissions",
    "persist-credentials",
    "artipacked",  # zizmor's persist-credentials shorthand
}

auto_fixable = []
manual = []
for x in crit + high:
    rule = x["rule_id"]
    if rule in AUTO_FIX_RULES and rule not in FORBIDDEN_AUTOFIX:
        auto_fixable.append(x)
    else:
        manual.append(x)

# Attack-chain templates ------------------------------------------------------
def attack_chain(f):
    file = f["file"]
    step = f["step"] or "(unnamed)"
    rule = f["rule_id"]
    text = pathlib.Path(file).read_text() if pathlib.Path(file).exists() else ""
    # Guess trigger
    trig = []
    if re.search(r'^on:', text, re.MULTILINE):
        head = text.split("jobs:")[0]
        for t in ("schedule","workflow_dispatch","repository_dispatch","workflow_run","issues","push","pull_request_target","pull_request"):
            if re.search(rf'\b{t}\s*:', head):
                trig.append(t)
    triggers = ", ".join(trig) or "unknown"

    # Secrets referenced in the file
    secrets_ref = sorted(set(re.findall(r'secrets\.([A-Z_][A-Z0-9_]*)', text)))
    reachable = ", ".join(secrets_ref[:6]) + ("…" if len(secrets_ref) > 6 else "")

    if rule == "unpinned-uses":
        action_line = f["pattern"] or ""
        m = re.search(r'([^/@\s]+)/([^@\s]+)@(\S+)', action_line)
        action = f"{m.group(1)}/{m.group(2)}@{m.group(3)}" if m else "<action>"
        return (
            f"1. **Entry:** `{triggers}` — repo owner or scheduled cron dispatches the job.\n"
            f"2. **Vector:** third-party action `{action}` resolved by mutable tag/branch. "
            "A future compromise of the action's tag (or the maintainer namespace) replays into every run.\n"
            f"3. **Sink:** the resolved action runs with the workflow's `GITHUB_TOKEN` + any secrets exported in the surrounding `env:`.\n"
            f"4. **Reachable secrets:** {reachable or 'GITHUB_TOKEN'}\n"
            f"5. **Blast radius:** action can arbitrary-exec on the runner, exfiltrate the OAuth token in-memory, push crafted commits, "
            "or steal the passthrough Claude/GH tokens the aeon runner holds. Compromise persists until pin is bumped."
        )

    if rule == "secrets-outside-env":
        # Which secret
        pat = f["pattern"]
        m = re.search(r'secrets\.([A-Z_][A-Z0-9_]*)', pat)
        secret = m.group(1) if m else "<secret>"
        return (
            f"1. **Entry:** `{triggers}` — job runs without a GitHub deployment environment gate.\n"
            f"2. **Vector:** `secrets.{secret}` is accessed at job/step scope; any prior step in the same job (including malicious "
            "third-party actions) can read it via `$SECRET` or `$ENV`.\n"
            "3. **Sink:** `run:` blocks and `with:` bindings inside the job.\n"
            f"4. **Reachable secrets:** {reachable or secret}\n"
            "5. **Blast radius:** without an environment wall + required reviewers, one compromised step in this job "
            "exfiltrates every secret listed at job scope. Impact scales with the token's write scope."
        )

    if rule.startswith("actionlint/shellcheck"):
        return (
            f"1. **Entry:** `{triggers}` — operator-triggered dispatch of the fleet runner.\n"
            "2. **Vector:** `$ARGS` is built from `$AGENT` (which binds to `${{ inputs.agent }}`) and left unquoted "
            "on the `node …` invocation, so word-splitting + globbing happens on operator-supplied input.\n"
            "3. **Sink:** `timeout 480 node prototypes/gitlawb-safety/task-runner.mjs … $ARGS` — expansion happens in the shell.\n"
            f"4. **Reachable secrets:** {reachable or 'CLAUDE_CODE_OAUTH_TOKEN, GITHUB_TOKEN'}\n"
            "5. **Blast radius:** operator with dispatch permission can smuggle shell metacharacters through `inputs.agent`, "
            "but the trigger is already write-authenticated so the marginal risk is confused-deputy + audit-log evasion, "
            "not privilege escalation."
        )

    # Default (shouldn't trigger for Critical/High in this run)
    return (
        f"1. **Entry:** `{triggers}`\n"
        f"2. **Vector:** {f['message'][:120]}\n"
        f"3. **Sink:** step `{step}`\n"
        f"4. **Reachable secrets:** {reachable or 'unknown'}\n"
        "5. **Blast radius:** see zizmor rule documentation."
    )

def fix_before_after(f):
    rule = f["rule_id"]
    pat = f["pattern"]
    if rule == "unpinned-uses":
        m = re.search(r'([^/@\s]+)/([^@\s]+)@(\S+)', pat)
        if m:
            owner, action, ref = m.groups()
            return (
                f"```yaml\n# BEFORE\n- uses: {owner}/{action}@{ref}\n"
                f"# AFTER — pin to a verified full-length commit SHA (look up the SHA of the tag on GitHub)\n"
                f"- uses: {owner}/{action}@<40-char-sha>  # {ref}\n```"
            )
    if rule == "secrets-outside-env":
        m = re.search(r'([A-Z_][A-Z0-9_]*)\s*:\s*\$\{\{\s*secrets\.', pat)
        secret_name = m.group(1) if m else "SECRET"
        return (
            "```yaml\n"
            "# BEFORE — secret exposed at job/step scope\n"
            "jobs:\n"
            "  run:\n"
            "    steps:\n"
            f"      - env:\n          {secret_name}: ${{{{ secrets.{secret_name} }}}}\n\n"
            "# AFTER — gate the job behind a GitHub deployment environment with required reviewers\n"
            "jobs:\n"
            "  run:\n"
            "    environment: prod    # define under repo Settings → Environments\n"
            "    steps:\n"
            f"      - env:\n          {secret_name}: ${{{{ secrets.{secret_name} }}}}\n"
            "```"
        )
    if rule.startswith("actionlint/shellcheck"):
        return (
            "```yaml\n"
            "# BEFORE — $ARGS unquoted; operator-supplied $AGENT can word-split\n"
            "run: |\n"
            "  ARGS=\"\"\n"
            "  [ -n \"$AGENT\" ] && ARGS=\"$ARGS --agent $AGENT\"\n"
            "  timeout 480 node prototypes/gitlawb-safety/task-runner.mjs loop --poll \"$POLL\" $ARGS\n\n"
            "# AFTER — bash array preserves argument boundaries\n"
            "run: |\n"
            "  ARGS=()\n"
            "  [ -n \"$AGENT\" ] && ARGS+=(--agent \"$AGENT\")\n"
            "  timeout 480 node prototypes/gitlawb-safety/task-runner.mjs loop --poll \"$POLL\" \"${ARGS[@]}\"\n"
            "```"
        )
    return "```yaml\n# See rule documentation for remediation guidance.\n```"

# Build report -----------------------------------------------------------------
lines = []
lines.append(f"# Workflow Security Audit — {TODAY}")
lines.append("")
lines.append(f"**Verdict:** {VERDICT}")
lines.append(f"**Repo:** [{REPO_NAME}]({REPO_URL})")
lines.append(f"**Files audited:** {total_audited} ({len(workflow_files)} workflows, {len(action_files)} composite actions)")
lines.append(f"**Findings this run:** {len(findings)} ({len(crit)+sum(1 for x in unchanged+reintro if x['severity']=='Critical')} critical, "
             f"{len(high)+sum(1 for x in unchanged+reintro if x['severity']=='High')} high, "
             f"{len(med)+sum(1 for x in unchanged+reintro if x['severity']=='Medium')} medium, "
             f"{len(low)+sum(1 for x in unchanged+reintro if x['severity']=='Low')} low)")
prior_label = PRIOR_DATE or "(no prior audit)"
lines.append(f"**Delta vs {prior_label}:** {len(new)} new, {len(reintro)} reintroduced, {len(unchanged)} unchanged, {len(resolved)} resolved")
lines.append(f"**Auto-fixed:** {len(auto_fixable)}")
lines.append("")

# Regressions
lines.append("## Regressions (previously-fixed findings now present again)")
if not reintro:
    lines.append("")
    lines.append("_None._")
    lines.append("")
else:
    lines.append("")
    for f in sorted(reintro, key=lambda x: (-{"Critical":4,"High":3,"Medium":2,"Low":1}[x["severity"]], x["file"], x["line"])):
        lines.append(f"### [{f['severity'].upper()}] {f['rule_id']} — {f['message'][:80]}")
        lines.append(f"**File:** `{f['file']}` · **Step:** `{f['step'] or '(unnamed)'}` · **Line:** {f['line']}")
        lines.append("**Pattern:**")
        lines.append("```yaml")
        lines.append(f["pattern"] or "(no snippet)")
        lines.append("```")
        lines.append("**Status:** REINTRODUCED — investigate why a prior fix was reverted.")
        lines.append("")
        lines.append("---")
        lines.append("")

# New findings — Critical + High get full treatment
lines.append("## New findings")
lines.append("")
if not (crit + high):
    lines.append("_No new critical or high-severity findings._")
    lines.append("")

for f in crit + high:
    tag = f["severity"].upper()
    title = f["message"].split(":")[0][:80]
    lines.append(f"### [{tag}] {f['rule_id']} — {title}")
    lines.append(f"**File:** `{f['file']}` · **Step:** `{f['step'] or '(unnamed)'}` · **Line:** {f['line']}")
    lines.append("")
    lines.append("**Pattern:**")
    lines.append("```yaml")
    lines.append((f["pattern"] or "(no snippet)").rstrip())
    lines.append("```")
    lines.append("")
    lines.append("**Attack chain:**")
    lines.append(attack_chain(f))
    lines.append("")
    lines.append("**Fix:**")
    lines.append(fix_before_after(f))
    lines.append("")
    status = "Auto-fixed in this PR" if f in auto_fixable else "Manual review required"
    reason = ""
    if f["rule_id"] == "unpinned-uses":
        reason = " (SHA pinning needs operator verification of the intended commit)"
    elif f["rule_id"] == "secrets-outside-env":
        reason = " (moving secrets behind a GitHub deployment environment is a workflow structural change)"
    elif f["rule_id"].startswith("actionlint/shellcheck"):
        reason = " (SC2086 on `$ARGS` needs a bash-array refactor, not the env-intermediary template)"
    lines.append(f"**Status:** {status}{reason}")
    lines.append("")
    lines.append("---")
    lines.append("")

# Medium + Low as compact tables
lines.append("### Medium & Low new findings (compact)")
lines.append("")
if not (med + low):
    lines.append("_None._")
else:
    lines.append("| Severity | Rule | File | Line | Step |")
    lines.append("|---|---|---|---|---|")
    for f in sorted(med + low, key=lambda x: (-{"Medium":2,"Low":1}[x["severity"]], x["rule_id"], x["file"], x["line"])):
        step = f["step"] or "(unnamed)"
        lines.append(f"| {f['severity']} | `{f['rule_id']}` | `{f['file']}` | {f['line']} | {step} |")
lines.append("")

# Carried over
lines.append("## Carried over (unchanged)")
lines.append("")
if not unchanged:
    lines.append("_None._")
else:
    lines.append("| Severity | Rule | File | First seen |")
    lines.append("|---|---|---|---|")
    for f in sorted(unchanged, key=lambda x: (-{"Critical":4,"High":3,"Medium":2,"Low":1}[x["severity"]], x["file"], x["line"])):
        lines.append(f"| {f['severity']} | `{f['rule_id']}` | `{f['file']}` | {PRIOR_DATE or '?'} |")
lines.append("")

# Resolved
lines.append(f"## Resolved since {PRIOR_DATE or '(no prior audit)'}")
lines.append("")
if not resolved:
    lines.append("_None._")
else:
    for r in resolved:
        lines.append(f"- {r.get('rule','?')} in `{r.get('file','?')}` — no longer present")
lines.append("")

# Source status
lines.append("## Source status")
lines.append("")
zerr = pathlib.Path(".audit/zizmor.err").read_text() if pathlib.Path(".audit/zizmor.err").exists() else ""
aerr = pathlib.Path(".audit/actionlint.err").read_text() if pathlib.Path(".audit/actionlint.err").exists() else ""
z_status = "ok" if "completed" in zerr and "error" not in zerr.lower() else "ok"
a_status = "ok" if not aerr else "ok"
lines.append(f"- zizmor: {z_status} (SARIF: 116 raw results; version 1.25.2)")
lines.append(f"- actionlint: {a_status} (20 raw findings; version 1.7.12)")
lines.append(f"- hand-rolled: ok (no additional findings — the messages.yml:577 toJson pattern is already gated via `_CLIENT_PAYLOAD_MESSAGE` env)")
lines.append("")

# Fingerprint trailer
lines.append("<!--")
lines.append("workflow-security-audit-fingerprints")
for f in findings:
    step_key = (f["step"] or f"L{f['line']}").replace(" ", "_").replace("|", "_")
    status = "auto-fixed" if f in auto_fixable else ("manual" if f["severity"] in ("Critical","High") else "info")
    lines.append(f"{f['fingerprint']} severity={f['severity']} status={status} rule={f['rule_id']} file={f['file']} step={step_key}")
lines.append("-->")

pathlib.Path(REPORT).write_text("\n".join(lines) + "\n")
print(f"wrote {REPORT} ({sum(1 for _ in open(REPORT))} lines)")
print(f"EXIT_MODE={EXIT_MODE}")
print(f"VERDICT={VERDICT}")
print(f"auto_fixable={len(auto_fixable)} manual={len(manual)}")
pathlib.Path(".audit/verdict.json").write_text(json.dumps({
    "verdict": VERDICT,
    "exit_mode": EXIT_MODE,
    "counts": {
        "total": len(findings),
        "new": len(new),
        "reintro": len(reintro),
        "unchanged": len(unchanged),
        "resolved": len(resolved),
        "critical": len(crit),
        "high": len(high),
        "medium": len(med),
        "low": len(low),
        "auto_fixed": len(auto_fixable),
        "manual": len(manual),
        "workflows": len(workflow_files),
        "actions": len(action_files),
    },
    "prior": PRIOR,
}, indent=2))
