#!/usr/bin/env python3
"""Render the audit markdown report + fingerprint trailer."""
import json, os
from collections import Counter, defaultdict

TODAY = '2026-08-09'
REPO_NAME = 'swarm-ai-research/aeon'
REPO_URL = 'https://github.com/swarm-ai-research/aeon'
PRIOR_DATE = '2026-07-26'

d = json.load(open('.audit/findings.json'))
s = d['summary']
new = d['new']
unchanged = d['unchanged']
resolved = d['resolved']
reintroduced = d['reintroduced']

exit_mode = 'NEW_HIGH'  # 0 crit, 1 high (secrets-outside-env in new file)
verdict_line = f'WORKFLOW_AUDIT_NEW_HIGH — {s["new_high"]} new high-severity finding(s)'

def sev_key(f):
    return {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}.get(f.get('severity', 'Low'), 4)

def basename(f):
    return os.path.basename(f)

def rule_title(rid):
    return rid.replace('zizmor/', '').replace('actionlint/', '')

lines = []
lines.append(f'# Workflow Security Audit — {TODAY}')
lines.append('')
lines.append(f'**Verdict:** {verdict_line}')
lines.append(f'**Repo:** [{REPO_NAME}]({REPO_URL})')
lines.append(f'**Files audited:** {s["file_count"]} ({s["workflow_count"]} workflows, {s["action_count"]} composite actions)')
lines.append(f'**Findings this run:** {s["total_current"]} ({s["crit"]} critical, {s["high"]} high, {s["med"]} medium, {s["low"]} low)')
lines.append(f'**Delta vs {PRIOR_DATE}:** {s["new_count"]} new, {s["reintroduced_count"]} reintroduced, {s["unchanged_count"]} unchanged (of which {s["fuzzy_carryover_count"]} matched via fuzzy anchor), {s["resolved_count"]} resolved')
lines.append(f'**Auto-fixed:** 0')
lines.append('')

# Reintroduced (empty)
lines.append('## Regressions (previously-fixed findings now present again)')
lines.append('')
if reintroduced:
    for f in reintroduced:
        lines.append(f'- [{f["severity"]}] `{f["rule_id"]}` at `{f["file"]}:{f["line"]}` step `{f["step"]}`')
else:
    lines.append('_None — no fingerprint from the prior audit was marked `auto-fixed` or `resolved`, so no regressions to report._')
lines.append('')

# New findings
lines.append('## New findings')
lines.append('')
lines.append(f'{s["new_count"]} new finding(s) surfaced this run, all in the newly-added workflow `gitlawb-repo-bootstrap.yml` (introduced since the {PRIOR_DATE} audit). The workflow is dispatch-only (`workflow_dispatch` with `permissions: {{}}` at the top level), which bounds the blast radius — but the one **High** finding (private-key secret in inline shell) deserves a proper environment gate before it accumulates operator use.')
lines.append('')

# High / Critical each get full attack chain
crit_high_new = [f for f in new if f['severity'] in ('Critical', 'High')]
low_med_new = [f for f in new if f['severity'] in ('Low', 'Medium')]

for f in sorted(crit_high_new, key=sev_key):
    lines.append(f'### [{f["severity"].upper()}] {f["rule_id"]} — secret written to disk via inline template interpolation')
    lines.append(f'**File:** `{f["file"]}` · **Step:** `{f["step"]}` · **Line:** {f["line"]}')
    lines.append('**Pattern:**')
    lines.append('```yaml')
    lines.append('- name: Restore operator identity')
    lines.append('  run: |')
    lines.append('    set -euo pipefail')
    lines.append("    if [ -z '${{ secrets.GITLAWB_OPERATOR_PEM }}' ]; then")
    lines.append('      echo "::error::GITLAWB_OPERATOR_PEM is not set — nothing to create the repo as"')
    lines.append('      exit 1')
    lines.append('    fi')
    lines.append('    mkdir -p ~/.gitlawb')
    lines.append("    echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem")
    lines.append("    echo '${{ secrets.GITLAWB_OPERATOR_UCAN }}' > ~/.gitlawb/ucan.json")
    lines.append('    chmod 600 ~/.gitlawb/identity.pem')
    lines.append('```')
    lines.append('')
    lines.append('**Attack chain:**')
    lines.append('1. **Entry:** `workflow_dispatch` — reachable by any user with `actions: write` on this repo (currently: the operator and the aeon GitHub App).')
    lines.append('2. **Vector:** `${{ secrets.GITLAWB_OPERATOR_PEM }}` is expanded by the runner **before** shell execution and pasted into the script body. A single-quoted heredoc protects against shell metachar interpretation for well-formed PEM content, but the secret ends up as a literal in the rendered step body — visible in job debug logs (`ACTIONS_STEP_DEBUG=true`), and captured by any earlier step that reads `/proc/self/status` or intercepts the runner’s temp files.')
    lines.append("3. **Sink:** Written to `~/.gitlawb/identity.pem` and `~/.gitlawb/ucan.json` inside a `run:` block whose environment includes no `env:` intermediary — the more-common runner-log leak path (typical of `secrets-outside-env` rule).")
    lines.append('4. **Reachable secrets:** `GITLAWB_OPERATOR_PEM` (Ed25519 private key that owns the aeon repo on the GitLawb node), `GITLAWB_OPERATOR_UCAN` (delegated-auth capability envelope).')
    lines.append('5. **Blast radius:** An attacker with the operator key can create/rename/delete the aeon repo on gitlawb.com under the current DID, forge UCAN delegations, and impersonate the fleet identity across every future `gl` call — including issue creation for `aeon-reviewer` and `aeon-sentinel` reports (which are the fleet\'s primary integrity signal). Fully re-provisioning the operator identity requires generating a new DID and re-associating every downstream repo.')
    lines.append('')
    lines.append('**Fix:**')
    lines.append('```yaml')
    lines.append('# BEFORE')
    lines.append('- name: Restore operator identity')
    lines.append('  run: |')
    lines.append('    set -euo pipefail')
    lines.append("    if [ -z '${{ secrets.GITLAWB_OPERATOR_PEM }}' ]; then")
    lines.append('      echo "::error::GITLAWB_OPERATOR_PEM is not set — nothing to create the repo as"')
    lines.append('      exit 1')
    lines.append('    fi')
    lines.append('    mkdir -p ~/.gitlawb')
    lines.append("    echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/identity.pem")
    lines.append("    echo '${{ secrets.GITLAWB_OPERATOR_UCAN }}' > ~/.gitlawb/ucan.json")
    lines.append('    chmod 600 ~/.gitlawb/identity.pem')
    lines.append('')
    lines.append('# AFTER — env-indirection + `environment:` gate for approval-required use')
    lines.append('jobs:')
    lines.append('  bootstrap:')
    lines.append('    environment: gitlawb-bootstrap  # create in Repo Settings → Environments; require operator approval')
    lines.append('    ...')
    lines.append('    steps:')
    lines.append('      - name: Restore operator identity')
    lines.append('        env:')
    lines.append('          _PEM: ${{ secrets.GITLAWB_OPERATOR_PEM }}')
    lines.append('          _UCAN: ${{ secrets.GITLAWB_OPERATOR_UCAN }}')
    lines.append('        run: |')
    lines.append('          set -euo pipefail')
    lines.append('          if [ -z "$_PEM" ]; then')
    lines.append('            echo "::error::GITLAWB_OPERATOR_PEM is not set — nothing to create the repo as"')
    lines.append('            exit 1')
    lines.append('          fi')
    lines.append('          mkdir -p ~/.gitlawb')
    lines.append("          printf '%s' \"$_PEM\" > ~/.gitlawb/identity.pem")
    lines.append("          printf '%s' \"$_UCAN\" > ~/.gitlawb/ucan.json")
    lines.append('          chmod 600 ~/.gitlawb/identity.pem')
    lines.append('```')
    lines.append('')
    lines.append('**Status:** Manual required — the fix combines an `env:`-indirection edit (mechanical) with creating a GitHub Environment named `gitlawb-bootstrap` and adding an operator-approval requirement (Repo Settings → Environments → New environment → Required reviewers). Per SKILL constraint, environment-scoping decisions are operator-only, so this audit does not auto-apply the edit.')
    lines.append('')
    lines.append('---')
    lines.append('')

# Low/Medium compact table
if low_med_new:
    lines.append('### Low / Medium new findings (compact)')
    lines.append('')
    lines.append('| Severity | Rule | File | Line | Step | Status |')
    lines.append('|---|---|---|---|---|---|')
    for f in sorted(low_med_new, key=sev_key):
        step = f['step'] if f['step'] != '(unknown)' else '(job/workflow level)'
        # Escape pipes in step names
        step = step.replace('|', '\\|')
        lines.append(f'| {f["severity"]} | `{f["rule_id"]}` | `{basename(f["file"])}` | {f["line"]} | {step} | Manual (Low; not in auto-fix scope) |')
    lines.append('')

# Carried over table (unchanged)
lines.append('## Carried over (unchanged)')
lines.append('')
lines.append(f'{s["unchanged_count"]} finding(s) carried over from {PRIOR_DATE} unchanged. Of these, {s["fuzzy_carryover_count"]} matched via fuzzy anchor (rule+file pair, same class, different step-name after upstream refactor). Aggregated by rule:')
lines.append('')
lines.append('| Severity | Rule | Count | Files |')
lines.append('|---|---|---|---|')
by_rule_sev = defaultdict(lambda: {'count': 0, 'files': set()})
for f in unchanged:
    key = (f['severity'], f['rule_id'])
    by_rule_sev[key]['count'] += 1
    by_rule_sev[key]['files'].add(basename(f['file']))
for (sev, rid), meta in sorted(by_rule_sev.items(), key=lambda kv: (sev_key({'severity': kv[0][0]}), kv[0][1])):
    files_str = ', '.join(sorted(meta['files']))
    lines.append(f'| {sev} | `{rid}` | {meta["count"]} | {files_str} |')
lines.append('')

# Resolved
lines.append(f'## Resolved since {PRIOR_DATE}')
lines.append('')
if resolved:
    for r in resolved:
        rule = r.get('rule', '?')
        f = r.get('file', '?')
        step = r.get('step', '?')
        sev = r.get('severity', '?')
        lines.append(f'- [{sev}] `{rule}` in `{f}` (prior step: `{step}`) — no longer present.')
    if len(resolved) == 1 and resolved[0].get('rule') == 'zizmor/template-injection' and resolved[0].get('file') == '.github/workflows/aeon.yml':
        lines.append('')
        lines.append('The single resolved finding is a template-injection anchor at `aeon.yml` step `line480`. Given that no NEW template-injection appeared in `aeon.yml`, this appears to be a genuine resolution (the interpolation site was cleaned up during an unrelated refactor).')
else:
    lines.append('_None — every prior fingerprint still appears in this scan._')
lines.append('')

# Source status
lines.append('## Source status')
lines.append('')
lines.append('- zizmor: **ok** — pinned `1.25.2` binary from `.audit-bin/`; scanned 8 workflows under `.github/workflows/` with `--persona auditor --format sarif`; 133 raw results before rule×file×step dedup.')
lines.append('- actionlint: **ok** — bundled binary from `.audit-bin/`; 20 shellcheck findings (1 escalated to Medium via `SC2086`, rest Low style-class).')
lines.append('- hand-rolled: **ok** — toJson-into-shell (fix pattern present at `messages.yml:667`), `persist-credentials: true` (0 explicit), `GITHUB_ENV`/`GITHUB_OUTPUT` writes with `${{ github.event.* }}` (0), fleet-specific `${{ inputs.* }}` in raw shell (0 — all env-guarded), mutable third-party ref (0 — every `uses:` is `actions/*` first-party). No new hand-rolled backstops fired.')
lines.append('')

# Fingerprint trailer
lines.append('<!--')
lines.append('workflow-security-audit-fingerprints')

def emit_fp(f, status):
    step_us = (f.get('step') or '(unknown)').replace(' ', '_')
    return f'{f["fingerprint"]} severity={f["severity"]} status={status} rule={f["rule_id"]} file={f["file"]} step={step_us}'

# Emit NEW findings first
for f in sorted(new, key=sev_key):
    lines.append(emit_fp(f, 'manual'))
# Then unchanged (same status as prior — keep 'manual' for consistency)
for f in sorted(unchanged, key=sev_key):
    lines.append(emit_fp(f, 'manual'))
lines.append('-->')

output = '\n'.join(lines) + '\n'
open('.audit/report.md', 'w').write(output)
print(f'report length: {len(output)} bytes, {len(lines)} lines')
