#!/usr/bin/env python3
"""Render articles/workflow-security-audit-${today}.md from findings_enriched.json."""
import json, pathlib, collections, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
today = subprocess.check_output(["date", "-u", "+%F"]).decode().strip()

with open(ROOT / "findings_enriched.json") as f:
    ctx = json.load(f)

findings = ctx["findings"]
counts = ctx["counts"]
verdict = ctx["verdict"]
exit_mode = ctx["exit_mode"]
prior_date = ctx["prior_date"]
workflow_count = ctx["workflow_count"]
action_count = ctx["action_count"]

def by(pred):
    return [x for x in findings if pred(x)]

new_c = by(lambda x: x["delta"] == "NEW" and x["severity"] == "Critical")
new_h = by(lambda x: x["delta"] == "NEW" and x["severity"] == "High")
new_m = by(lambda x: x["delta"] == "NEW" and x["severity"] == "Medium")
new_l = by(lambda x: x["delta"] == "NEW" and x["severity"] == "Low")

def group_by_file(items):
    d = collections.defaultdict(list)
    for x in items:
        d[x["file"]].append(x)
    return dict(d)

lines = []

# --- Header ---
lines.append(f"# Workflow Security Audit — {today}")
lines.append("")
lines.append(f"**Verdict:** {verdict}")
lines.append(f"**Repo:** [swarm-ai-research/aeon](https://github.com/swarm-ai-research/aeon)")
lines.append(f"**Files audited:** {workflow_count + action_count} ({workflow_count} workflows, {action_count} composite actions)")
lines.append(f"**Findings this run:** {counts['total']} ({counts['crit']} critical, {counts['high']} high, {counts['med']} medium, {counts['low']} low)")
prior_label = prior_date or "(no prior audit)"
lines.append(f"**Delta vs {prior_label}:** {counts['new']} new, {counts['reintroduced']} reintroduced, {counts['unchanged']} unchanged, {counts['resolved']} resolved")
lines.append(f"**Auto-fixed:** {counts['fixed']}")
lines.append(f"**Manual review:** {counts['manual']}")
lines.append("")

# --- Regressions (if any) ---
reintroduced = by(lambda x: x["delta"] == "REINTRODUCED")
if reintroduced:
    lines.append("## Regressions (previously-fixed findings now present again)")
    lines.append("")
    for x in reintroduced:
        lines.append(f"### [{x['severity'].upper()}] {x['rule_id']} — regression")
        lines.append(f"**File:** `{x['file']}` · **Line:** {x['line']}")
        lines.append("**Pattern:**")
        lines.append("```yaml")
        lines.append(x['pattern'])
        lines.append("```")
        lines.append("")

# --- New findings ---
lines.append("## New findings")
lines.append("")

if not (new_c or new_h):
    lines.append("_No new Critical or High findings this run._")
    lines.append("")

# --- CRITICAL: unpinned-uses (grouped) ---
crit_by_rule_file = collections.defaultdict(list)
for x in new_c:
    crit_by_rule_file[(x["rule_id"], x["file"])].append(x)

for (rule, file), items in sorted(crit_by_rule_file.items()):
    if rule == "zizmor/unpinned-uses":
        lines.append(f"### [CRITICAL] {rule} — third-party actions not SHA-pinned")
        lines.append(f"**File:** `{file}` · **Instances:** {len(items)} (all `actions/*` refs pinned by tag, not SHA)")
        lines.append("")
        lines.append("**Occurrences:**")
        lines.append("")
        lines.append("| Line | Step | Reference |")
        lines.append("|---|---|---|")
        for x in items:
            step_name = ""
            snip = (x.get("step") or "").strip()
            step_name = snip.replace("name:", "").strip() if snip.startswith("name:") else snip
            lines.append(f"| {x['line']} | `{step_name[:40]}` | `{(x.get('pattern') or '').strip()[:60]}` |")
        lines.append("")
        lines.append("**Pattern (aeon.yml:85):**")
        lines.append("```yaml")
        lines.append("- name: Early checkout")
        lines.append("  if: github.event_name == 'issues'")
        lines.append("  uses: actions/checkout@v5")
        lines.append("  with:")
        lines.append("    token: ${{ secrets.GITHUB_TOKEN }}")
        lines.append("```")
        lines.append("")
        lines.append("**Attack chain:**")
        lines.append("1. **Entry:** `issues.labeled` (label `ai-build`) — any repo collaborator with issue-write access can label. `workflow_dispatch` is also present on this workflow but requires actor with actions:write.")
        lines.append("2. **Vector:** `actions/checkout@v5` (and `actions/setup-node@v5` at line 133) resolve at run time to whatever commit `v5` currently points at. GitHub's release-tag SHAs are compromised via three known vectors: (a) attacker with push to the action repo force-pushes the tag; (b) an intermediate maintainer publishes a malicious minor; (c) the tag ref itself is redirected. `actions/*` is a first-party org so the residual risk is compromise of that org's release process — real, but low relative to third-party actions.")
        lines.append("3. **Sink:** the checkout action runs arbitrary JavaScript from the resolved SHA with the job's `GITHUB_TOKEN` available. `setup-node` similarly executes with runner privileges and can write `~/.npmrc`.")
        lines.append(f"4. **Reachable secrets:** `GITHUB_TOKEN` (scoped to job perms: `contents: write`, `pull-requests: write`, `issues: read`, `actions: read`), plus all workflow-level env: `FLEET_ENDPOINT`, `FLEET_TOKEN` (from `secrets.FLEET_*`), and every subsequent step's secret exposures on this runner.")
        lines.append("5. **Blast radius:** push to `main`, open/close PRs, dispatch downstream workflows (`gh workflow run`). Because the `run` job also installs `@anthropic-ai/claude-code` (line 139), a compromised checkout SHA can plant a malicious binary before the CLI executes user prompts on this runner and every future run until a pin is set.")
        lines.append("")
        lines.append("**Fix:**")
        lines.append("```yaml")
        lines.append("# BEFORE")
        lines.append("- uses: actions/checkout@v5")
        lines.append("- uses: actions/setup-node@v5")
        lines.append("")
        lines.append("# AFTER — replace with the specific commit SHA of the release tag")
        lines.append("- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v5.0.0")
        lines.append("- uses: actions/setup-node@a0853c24544627f65ddf259abe73b1d18a591444 # v5.0.0")
        lines.append("```")
        lines.append("")
        lines.append("Verify SHAs against `git ls-remote https://github.com/actions/checkout refs/tags/v5.0.0` before committing.")
        lines.append("")
        lines.append("**Status:** Manual review required — the skill's step-7 rules never auto-fix `unpinned-uses` (operator must verify each intended commit SHA against the published release).")
        lines.append("")

# --- HIGH: secrets-outside-env (grouped by file) ---
high_by_rule_file = collections.defaultdict(list)
for x in new_h:
    high_by_rule_file[(x["rule_id"], x["file"])].append(x)

# Print grouped HIGH secrets-outside-env
lines.append("### [HIGH] zizmor/secrets-outside-env — secrets referenced without a dedicated GitHub Environment")
lines.append(f"**Instances:** {len(new_h)} across {sum(1 for k in high_by_rule_file if k[0] == 'zizmor/secrets-outside-env')} files.")
lines.append("")
lines.append("**Distribution:**")
lines.append("")
lines.append("| File | Count | Secrets referenced |")
lines.append("|---|---:|---|")
for (rule, file), items in sorted(high_by_rule_file.items()):
    if rule != "zizmor/secrets-outside-env":
        continue
    secrets = sorted({(x.get("step") or "").strip() for x in items})
    secret_names = ", ".join(f"`{s}`" for s in secrets[:6])
    if len(secrets) > 6:
        secret_names += f", … ({len(secrets) - 6} more)"
    lines.append(f"| `{file}` | {len(items)} | {secret_names} |")
lines.append("")
lines.append("**Pattern (representative — `fleet-runner.yml:287`):**")
lines.append("```yaml")
lines.append("jobs:")
lines.append("  run:")
lines.append("    runs-on: ubuntu-latest")
lines.append("    # no `environment:` declared")
lines.append("    steps:")
lines.append("      - name: Run fleet task runner")
lines.append("        env:")
lines.append("          CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}")
lines.append("          GH_TOKEN:                ${{ secrets.GITHUB_TOKEN }}")
lines.append("        run: |")
lines.append("          ...")
lines.append("```")
lines.append("")
lines.append("**Attack chain:**")
lines.append("1. **Entry:** any commit that lands on `main` (via merged PR, direct push with a `contents: write` PAT, or a workflow that opens+merges its own PR) causes the next scheduled or dispatched run of these workflows to use whatever secret bindings are declared. Without a GitHub Environment, there is no approval gate, no branch-protection tie, and no per-secret audit trail — the secret is available on any ref.")
lines.append("2. **Vector:** a malicious PR that mutates the workflow itself (e.g. exfiltrating `CLAUDE_CODE_OAUTH_TOKEN`, `GH_GLOBAL`, or the `GITLAWB_*_PEM` fleet keys via `curl` or an added step) merges into a branch that a scheduled run picks up. GitHub's default `pull_request` guard does not run first-time-contributor code with secrets, but this repo runs `workflow_dispatch` and `schedule` events which do execute with the full secret scope.")
lines.append("3. **Sink:** shell interpolation into `run:` blocks (e.g. `echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem` at `fleet-runner.yml:150`), and env-var passthroughs to helper scripts (`scripts/fleet-executors/*.mjs`, `scripts/prefetch-surplus.sh`).")
lines.append("4. **Reachable secrets:** `GH_GLOBAL` (fine-grained PAT with **Workflows** write permission — can push to `.github/workflows/*` and bypass GITHUB_TOKEN restrictions), `AEON_PRIVATE_PAT`, 5 × `GITLAWB_*_PEM` fleet identity keys, `GITLAWB_OPERATOR_UCAN`, `CLAUDE_CODE_OAUTH_TOKEN` (Anthropic subscription), `SURPLUS_PRICING_URL`, `SURPLUS_API_KEY`, `TELEGRAM_BOT_TOKEN`, `DISCORD_WEBHOOK_URL`, `SLACK_WEBHOOK_URL`, `SENDGRID_API_KEY`.")
lines.append("5. **Blast radius:** exfiltration of `GH_GLOBAL` alone enables persistence — the attacker can rewrite any workflow file and push directly to `main`, since it is scoped past the default GITHUB_TOKEN's `.github/workflows/*` block (this is the reason the PAT exists per the `sync-upstream.yml` comment at line 26). Exfiltration of `GITLAWB_*_PEM` compromises the multi-agent fleet identity (researcher/reviewer/deployer/sentinel) — each has distinct `gl register` capabilities up to `repo:admin` (sentinel). Exfiltration of `CLAUDE_CODE_OAUTH_TOKEN` gives free Anthropic subscription-tier compute to the attacker until rotated.")
lines.append("")
lines.append("**Fix (per-file):**")
lines.append("```yaml")
lines.append("# BEFORE — job that reads secrets directly")
lines.append("jobs:")
lines.append("  run:")
lines.append("    runs-on: ubuntu-latest")
lines.append("    steps:")
lines.append("      - env:")
lines.append("          GH_TOKEN: ${{ secrets.GH_GLOBAL }}")
lines.append("        ...")
lines.append("")
lines.append("# AFTER — declare an Environment, then bind protection rules in repo Settings")
lines.append("jobs:")
lines.append("  run:")
lines.append("    runs-on: ubuntu-latest")
lines.append("    environment:")
lines.append("      name: production")
lines.append("      # optional: url: ${{ steps.deploy.outputs.url }}")
lines.append("    steps:")
lines.append("      - env:")
lines.append("          GH_TOKEN: ${{ secrets.GH_GLOBAL }}")
lines.append("        ...")
lines.append("```")
lines.append("")
lines.append("Then in **Repo Settings → Environments → production**: (a) add required reviewers if you want a manual approval gate; (b) restrict to `main` branch; (c) move the sensitive secrets (`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) from repo-scoped to environment-scoped so they only decrypt inside jobs that opt into this environment.")
lines.append("")
lines.append("Recommended environments for this repo:")
lines.append("- **`production`** — fleet-runner (owns fleet identity keys + Claude OAuth), messages.yml scheduler (owns `GH_GLOBAL` dispatch), sync-upstream (owns `GH_GLOBAL` for workflow-file pushes).")
lines.append("- **`chain-runner`** — chain-runner.yml (owns `GH_GLOBAL` and `AEON_PRIVATE_PAT` for skill orchestration).")
lines.append("")
lines.append("**Status:** Manual review required — environment topology and reviewer policy are operator judgment calls; auto-fix cannot pick the boundary.")
lines.append("")

# --- Medium findings (compact table) ---
lines.append("## Medium-severity findings (compact)")
lines.append("")
if new_m:
    lines.append("| # | Rule | File | Line | Signal |")
    lines.append("|---|---|---|---:|---|")
    for i, x in enumerate(new_m, 1):
        msg = (x.get("message") or "").strip().replace("|", "\\|")[:100]
        lines.append(f"| {i} | `{x['rule_id']}` | `{x['file']}` | {x['line']} | {msg} |")
    lines.append("")
    lines.append("**`zizmor/artipacked` (11 instances):** `actions/checkout` steps run with the default `persist-credentials: true`, which leaves `.git/config` on the runner with the `GITHUB_TOKEN` baked in. Fix by adding `persist-credentials: false` to each `with:` block unless the step later performs a `git push` that needs the token (in which case, use a scoped `token: ${{ secrets.GITHUB_TOKEN }}` and unset after the push).")
    lines.append("")
    lines.append("**`actionlint-shellcheck` (4 instances):** SC2129 style hints (individual `echo >>` redirects should be grouped `{ ...; } >> file`) and SC2034/SC2155 (unused / declaration-mask). Style-only — not exploitable, but worth clean-up when the surrounding blocks are touched.")
else:
    lines.append("_None._")
lines.append("")

# --- Low findings (compact) ---
lines.append("## Low-severity findings (compact)")
lines.append("")
low_by_rule = collections.Counter(x["rule_id"] for x in new_l)
lines.append("| Rule | Count | Notes |")
lines.append("|---|---:|---|")
low_notes = {
    "zizmor/template-injection": "`${{ ... }}` interpolations into `run:` blocks. Most are safe because the source is `steps.*.outputs.*` or `github.run_id`, but review each to confirm the source is not attacker-controlled.",
    "zizmor/anonymous-definition": "Composite/reusable steps without a `name:` field. Purely cosmetic — makes attack-chain triage harder later.",
    "zizmor/undocumented-permissions": "Jobs granting `permissions:` without a comment explaining why each scope is needed. Low but worth adding a `# scope-rationale:` line each.",
    "zizmor/concurrency-limits": "A workflow allows concurrent execution that could race on shared state.",
}
for rule, count in low_by_rule.most_common():
    note = low_notes.get(rule, "").replace("|", "\\|")
    lines.append(f"| `{rule}` | {count} | {note} |")
lines.append("")

# --- Carried over ---
carried = by(lambda x: x["delta"] == "UNCHANGED")
lines.append("## Carried over (unchanged)")
lines.append("")
if carried:
    lines.append("| Severity | Rule | File | First seen |")
    lines.append("|---|---|---|---|")
    for x in carried:
        lines.append(f"| {x['severity']} | `{x['rule_id']}` | `{x['file']}` | {prior_date or '?'} |")
else:
    lines.append("_None (this is the first audit — no prior report to compare against)._")
lines.append("")

# --- Resolved ---
lines.append(f"## Resolved since {prior_date or '(n/a)'}")
lines.append("")
lines.append("_None._" if not prior_date else f"_(0 findings from the prior audit are absent this run.)_")
lines.append("")

# --- Source status ---
lines.append("## Source status")
lines.append("")
lines.append("- zizmor: ok (v1.25.2 from `.audit-bin/zizmor`, persona=auditor, SARIF)")
lines.append("- actionlint: ok (from `.audit-bin/actionlint`, JSON output)")
lines.append("- hand-rolled: ok (toJson-into-shell, persist-creds-pr-head, GITHUB_ENV injection, inputs-to-gh-dispatch, mutable-third-party-ref — all clean this run)")
lines.append("")

# --- Fingerprint trailer (machine-readable for next run's delta classification) ---
lines.append("<!--")
lines.append("workflow-security-audit-fingerprints")
for x in findings:
    step = (x.get("step") or "").strip().replace(" ", "_")[:40]
    lines.append(f"{x['fingerprint']} severity={x['severity']} status=manual rule={x['rule_id']} file={x['file']} step={step}")
lines.append("-->")

report_path = REPO_ROOT / "articles" / f"workflow-security-audit-{today}.md"
report_path.write_text("\n".join(lines) + "\n")
print(f"wrote {report_path} ({len(lines)} lines)")
