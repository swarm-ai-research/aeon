import json, os, sys
from collections import Counter, defaultdict

today = "2026-07-26"
REPO_NAME = "swarm-ai-research/aeon"
REPO_URL = "https://github.com/swarm-ai-research/aeon"

ranked = json.load(open(".audit/unique.json"))
raw = json.load(open(".audit/findings.json"))
by_sev = Counter(f["severity"] for f in ranked)
crit = by_sev.get("Critical", 0)
high = by_sev.get("High", 0)
med = by_sev.get("Medium", 0)
low = by_sev.get("Low", 0)
total = len(ranked)

# Files audited
workflows = sorted({f["file"] for f in raw if f["file"].startswith(".github/workflows/")})
workflow_count = len(workflows)
action_count = 0
files_audited = workflow_count + action_count

new_count = total  # BOOTSTRAP → every finding is NEW
reintroduced_count = 0
unchanged_count = 0
resolved_count = 0
fixed_count = 0  # nothing auto-fixed (all Crit/High are pinning/permissions/secrets-outside-env → Manual)
manual_count = crit + high

VERDICT = f"WORKFLOW_AUDIT_NEW_CRITICAL — {crit} new critical finding(s) (bootstrap run; no prior audit on main)"
PRIOR_DATE = "(no prior audit)"

# High-signal findings grouped
crit_findings = [f for f in ranked if f["severity"] == "Critical"]
high_findings = [f for f in ranked if f["severity"] == "High"]
med_findings = [f for f in ranked if f["severity"] == "Medium"]
low_findings = [f for f in ranked if f["severity"] == "Low"]

def snippet_yaml(finding):
    pat = finding.get("pattern", "").strip()
    return pat if pat else "(binary/unreadable region)"

# Attack chain templates by rule
def attack_chain(f):
    rid = f["rule_id"]
    fp = f["file"]
    step = f["step"]
    if rid == "zizmor/unpinned-uses":
        return {
            "entry": "any trigger for this workflow — schedule (cron every 5 min), workflow_dispatch, workflow_call, issues:labeled",
            "vector": "supply chain — the mutable tag `v5`/`v4` can be moved to a malicious commit by anyone with write access to that action's repo (compromised maintainer account, insider, or a moved tag pushed as a hijack)",
            "sink": f"`{snippet_yaml(f)}` runs as the first step of every skill invocation; the action code executes with the job's full permissions",
            "secrets": "the aeon `run` job has `contents: write`, `pull-requests: write`, `issues: read`, `actions: read`, plus every notification / API secret exposed via workflow env (`FLEET_ENDPOINT`, `FLEET_TOKEN`) and inherited via `GITHUB_TOKEN`",
            "blast": "arbitrary code executes with push access to `main`, ability to open PRs from any branch, and the `GITHUB_TOKEN` bearer scope — full self-modification of the aeon agent",
        }
    if rid == "zizmor/secrets-outside-env":
        return {
            "entry": "any trigger that reaches this job — for messages.yml/chain-runner.yml, the `*/5 * * * *` schedule + `repository_dispatch` events; for fleet-runner.yml, `workflow_dispatch` and `schedule`",
            "vector": "repo-scoped secret is available to every job in every workflow with no environment gate; a compromised action or a malicious workflow_dispatch input that reaches a bash sink can exfiltrate the secret without any deploy-review approval",
            "sink": f"`{snippet_yaml(f)}` — no `environment:` clause on the job, so no reviewer approval, no branch protection, and no logging tie-back beyond the repo-audit-log",
            "secrets": "GH_GLOBAL (org-wide PAT), AEON_PRIVATE_PAT, CLAUDE_CODE_OAUTH_TOKEN (subscription auth), GITLAWB_*_PEM (fleet keys), Telegram/Discord/Slack tokens, Anthropic/xAI/CoinGecko/Alchemy keys",
            "blast": "compromise of any of these secrets = full impersonation of the aeonframework identity across the org, or full drain of API credit, or takeover of the notification fan-out (Telegram/Discord/Slack chatops)",
        }
    if rid == "zizmor/ref-version-mismatch":
        return {
            "entry": "any run of the workflow",
            "vector": "the comment says `v5` (or `v4`) but the pin points to a specific commit — if the comment ever drifts from the commit (during a review, a rebase, or a copy-paste), a reviewer approving the intent (`v5` = presumably-vetted release) may inadvertently approve an unvetted commit",
            "sink": f"`{snippet_yaml(f)}` — the SHA is what runs, but the review signal is the version tag comment",
            "secrets": "same scope as unpinned-uses for the same job",
            "blast": "low-friction supply-chain attack via reviewer misalignment — a malicious maintainer swaps SHA to attacker-controlled build while comment still reads `v5`",
        }
    if rid.startswith("actionlint/SC2086"):
        return {
            "entry": "workflow_dispatch on fleet-runner — external actor with `actions:write` on the repo (only the aeonframework identity today, but bar for compromise is low with unrotated PATs)",
            "vector": "`inputs.agent` reaches `$AGENT` env → unquoted `$AGENT` in `--agent $AGENT` → word split lets a payload like `foo --secret-leak $(cat /etc/passwd)` inject shell arguments",
            "sink": "line 297 `ARGS=\"$ARGS --agent $AGENT\"` inside `run:` of `Run fleet task runner`",
            "secrets": "CLAUDE_CODE_OAUTH_TOKEN, GH_TOKEN (GITHUB_TOKEN)",
            "blast": "argument injection into task-runner.mjs — could exfiltrate the CLAUDE_CODE_OAUTH_TOKEN or GITHUB_TOKEN via a crafted --agent value if any downstream command interpolates it into a shell",
        }
    return None

# Build the report

lines = []
lines.append(f"# Workflow Security Audit — {today}")
lines.append("")
lines.append(f"**Verdict:** {VERDICT}")
lines.append(f"**Repo:** [{REPO_NAME}]({REPO_URL})")
lines.append(f"**Files audited:** {files_audited} ({workflow_count} workflows, {action_count} composite actions)")
lines.append(f"**Findings this run:** {total} unique ({crit} critical, {high} high, {med} medium, {low} low) — {len(raw)} total occurrences before dedup by rule×file×step")
lines.append(f"**Delta vs {PRIOR_DATE}:** {new_count} new, {reintroduced_count} reintroduced, {unchanged_count} unchanged, {resolved_count} resolved")
lines.append(f"**Auto-fixed:** {fixed_count}  ·  **Manual review required:** {manual_count}")
lines.append("")
lines.append("> **Why zero auto-fixes on a NEW_CRITICAL run:** every Critical (`unpinned-uses`) and every High finding (`ref-version-mismatch`, `secrets-outside-env`, and the actionlint `SC2086` in a fleet task-runner argument) falls under a category the skill's constraints hold as Manual. `unpinned-uses`, permissions, and `persist-credentials` need operator judgment about which commit SHA to pin (choosing a specific tag → SHA is a review call). `secrets-outside-env` needs the operator to create the `production` and `chain-runner` GitHub Environments and re-scope every secret through the repo Settings UI — the workflow edit alone would break every skill until the environment exists. Auto-fix would produce runs that appear to succeed but silently downgrade security or break the fleet.")
lines.append("")
lines.append("---")
lines.append("")

if reintroduced_count:
    lines.append("## Regressions (previously-fixed findings now present again)")
    lines.append("")
    lines.append("_None — bootstrap run._")
    lines.append("")
else:
    lines.append("## Regressions")
    lines.append("")
    lines.append("_None — bootstrap run, no prior audit on main to regress against. Memory notes the operator ran a prior scan on 2026-07-19 whose report and staged fixes never merged (blocked behind the same Repo Settings toggle that blocks the ≥18-branch queue); those findings are treated as NEW here._")
    lines.append("")
lines.append("---")
lines.append("")

lines.append("## New findings")
lines.append("")

def emit_full(f, sev_label):
    ac = attack_chain(f)
    lines.append(f"### [{sev_label}] {f['rule_id']} — {f['step']}")
    lines.append(f"**File:** `{f['file']}` · **Step:** `{f['step']}` · **Line:** {f['line']}")
    lines.append("**Pattern:**")
    lines.append("```yaml")
    lines.append(snippet_yaml(f))
    lines.append("```")
    lines.append("")
    if ac:
        lines.append("**Attack chain:**")
        lines.append(f"1. **Entry:** {ac['entry']}")
        lines.append(f"2. **Vector:** {ac['vector']}")
        lines.append(f"3. **Sink:** {ac['sink']}")
        lines.append(f"4. **Reachable secrets:** {ac['secrets']}")
        lines.append(f"5. **Blast radius:** {ac['blast']}")
        lines.append("")
    # Fix
    rid = f["rule_id"]
    lines.append("**Fix:**")
    lines.append("```yaml")
    if rid == "zizmor/unpinned-uses":
        pat = snippet_yaml(f)
        lines.append(f"# BEFORE")
        lines.append(pat)
        lines.append(f"# AFTER (pin to the commit SHA of the intended tag; keep the tag as a review comment)")
        if "checkout" in pat.lower():
            lines.append("uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5.0.0")
        elif "setup-node" in pat.lower():
            lines.append("uses: actions/setup-node@2028fbc5c25fe9cf00d9f06a71cc4710d4507903 # v5.0.0")
        else:
            lines.append("uses: <action>@<40-char SHA>  # <tag>")
        lines.append("```")
    elif rid == "zizmor/secrets-outside-env":
        lines.append("# BEFORE (secret referenced directly at job scope):")
        lines.append("jobs:")
        lines.append("  run:")
        lines.append("    permissions: { contents: write }")
        lines.append("    steps:")
        lines.append("      - run: echo \"${{ secrets.GH_GLOBAL }}\"")
        lines.append("# AFTER (gate the job behind a dedicated GitHub Environment):")
        lines.append("jobs:")
        lines.append("  run:")
        lines.append("    environment: chain-runner  # or `production` — must be created in repo Settings > Environments first")
        lines.append("    permissions: { contents: write }")
        lines.append("    steps:")
        lines.append("      - run: echo \"$_GH_GLOBAL\"")
        lines.append("        env:")
        lines.append("          _GH_GLOBAL: ${{ secrets.GH_GLOBAL }}  # now sourced from the environment scope")
        lines.append("```")
    elif rid == "zizmor/ref-version-mismatch":
        lines.append("# BEFORE (comment drifted from the pinned SHA — reviewer sees the tag but the commit is what runs):")
        lines.append("uses: actions/checkout@93cb6efe18208431cddfb8368fd83d5badbf9bfd # v5")
        lines.append("# AFTER (verify the SHA is the current stable tag and update the comment to match):")
        lines.append("uses: actions/checkout@<SHA of intended tag> # v5.0.0")
        lines.append("```")
    elif rid.startswith("actionlint/SC2086"):
        lines.append("# BEFORE:")
        lines.append("ARGS=\"$ARGS --agent $AGENT\"")
        lines.append("# AFTER (quote everywhere the value reaches the shell; use an array to avoid word-split entirely):")
        lines.append("EXTRA_ARGS=()")
        lines.append("[ -n \"$AGENT\" ] && EXTRA_ARGS+=(--agent \"$AGENT\")")
        lines.append("# ...then invoke:")
        lines.append("node prototypes/gitlawb-safety/task-runner.mjs once \"${EXTRA_ARGS[@]}\"")
        lines.append("```")
    else:
        lines.append("(see finding message)")
        lines.append("```")
    lines.append("")
    lines.append(f"**Status:** Manual review required · **Fingerprint:** `{f['fingerprint']}`")
    lines.append("")
    lines.append("---")
    lines.append("")

for f in crit_findings:
    emit_full(f, "CRITICAL")
for f in high_findings:
    emit_full(f, "HIGH")

# Medium/Low compact tables
lines.append("## Medium findings")
lines.append("")
lines.append("| # | Rule | File | Line | Step |")
lines.append("|---|---|---|---|---|")
for i, f in enumerate(med_findings, 1):
    lines.append(f"| {i} | `{f['rule_id']}` | `{f['file']}` | {f['line']} | {f['step']} |")
lines.append("")

lines.append("## Low findings")
lines.append("")
lines.append("| # | Rule | File | Line | Step |")
lines.append("|---|---|---|---|---|")
for i, f in enumerate(low_findings, 1):
    lines.append(f"| {i} | `{f['rule_id']}` | `{f['file']}` | {f['line']} | {f['step']} |")
lines.append("")

lines.append("## Carried over (unchanged)")
lines.append("")
lines.append("_None — bootstrap run._")
lines.append("")

lines.append(f"## Resolved since {PRIOR_DATE}")
lines.append("")
lines.append("_None — bootstrap run._")
lines.append("")

lines.append("## Source status")
lines.append("")
lines.append("- zizmor 1.25.2 (via `.audit-bin/zizmor`): **ok** — 125 raw results, 3 rules → Critical, 3 rules → High per SKILL mapping")
lines.append("- actionlint 1.7.12 (via `.audit-bin/actionlint`): **ok** — 20 shellcheck results, 2 upgraded to High under the `SC2086` + `${{ github.* }}` rule")
lines.append("- hand-rolled backstops (`toJson-into-shell`, `persist-credentials + head.sha`, `GITHUB_ENV` write injection, fleet inputs passthrough, mutable third-party ref): **ok** — 0 hits (April 11 `messages.yml:577` pattern remains fixed)")
lines.append("")

lines.append("## Top attack chains to read first")
lines.append("")
lines.append("1. `zizmor/unpinned-uses` on `aeon.yml:85/121/133` — every skill run pulls unpinned `actions/checkout@v5` and `actions/setup-node@v5`; a moved tag or maintainer compromise on either action gives an attacker `contents:write` + `pull-requests:write` on this repo, i.e. the ability to self-modify the aeon agent between two runs.")
lines.append("2. `zizmor/secrets-outside-env` × 43 across `messages.yml`, `fleet-runner.yml`, `chain-runner.yml`, `sync-upstream.yml` — every sensitive secret (`GH_GLOBAL`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`, `GITLAWB_*_PEM`, notification tokens, API keys) is repo-scoped; no environment gate, no reviewer approval, no per-run audit trail. One compromised action or one malicious workflow_dispatch input landing in a bash sink is enough to exfiltrate.")
lines.append("3. `actionlint/SC2086` on `fleet-runner.yml:294` — unquoted `$AGENT` (originating from `inputs.agent` on workflow_dispatch) reaches `--agent $AGENT` in the fleet task-runner invocation. A crafted input like `x --secret-leak $(...)` word-splits into extra CLI args. Blast is bounded by task-runner.mjs's arg parsing, but the CLAUDE_CODE_OAUTH_TOKEN and GITHUB_TOKEN are both in scope.")
lines.append("")

# Machine-readable trailer
lines.append("<!--")
lines.append("workflow-security-audit-fingerprints")
for f in ranked:
    fp = f["fingerprint"]
    sev = f["severity"]
    status = "manual"  # nothing auto-fixed on this bootstrap
    rule = f["rule_id"]
    fpath = f["file"]
    step_slug = "_".join((f["step"] or "").split())[:60]
    lines.append(f"{fp} severity={sev} status={status} rule={rule} file={fpath} step={step_slug}")
lines.append("-->")

report = "\n".join(lines) + "\n"
open(f"articles/workflow-security-audit-{today}.md", "w").write(report)
print(f"Wrote articles/workflow-security-audit-{today}.md — {len(report)} bytes, {report.count(chr(10))} lines")
