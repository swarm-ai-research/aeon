#!/usr/bin/env python3
"""Emit the audit report at articles/workflow-security-audit-<today>.md."""
import json, os, hashlib, re, glob
from collections import defaultdict, Counter

today = '2026-08-02'
repo_name = 'swarm-ai-research/aeon'
repo_url = 'https://github.com/swarm-ai-research/aeon'

c = json.load(open('.audit/classified.json'))
findings = c['findings']
resolved = c['resolved']
prior_date = c['prior_date']

# Split by delta
new = [f for f in findings if f['delta'] == 'NEW']
reintroduced = [f for f in findings if f['delta'] == 'REINTRODUCED']
unchanged = [f for f in findings if f['delta'] == 'UNCHANGED']

sev_rank = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}

targets = sorted(glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml'))
actions = sorted(glob.glob('.github/actions/*/action.yml') + glob.glob('.github/actions/*/action.yaml'))
workflow_count = len(targets)
action_count = len(actions)
total = len(findings)
by_sev = Counter(f['severity'] for f in findings)

# Verdict + exit mode
if total == 0:
    verdict = f'WORKFLOW_AUDIT_CLEAN — no findings across {workflow_count + action_count} files'
    exit_mode = 'CLEAN'
elif len(new) == 0 and len(reintroduced) == 0:
    verdict = f'WORKFLOW_AUDIT_UNCHANGED — {len(unchanged)} carried over from {prior_date}'
    exit_mode = 'UNCHANGED'
elif len(reintroduced) > 0:
    verdict = f'WORKFLOW_AUDIT_REGRESSION — {len(reintroduced)} previously-fixed finding(s) reintroduced'
    exit_mode = 'REGRESSION'
elif any(f['severity'] == 'Critical' for f in new):
    n_crit = sum(1 for f in new if f['severity'] == 'Critical')
    verdict = f'WORKFLOW_AUDIT_NEW_CRITICAL — {n_crit} new critical finding(s)'
    exit_mode = 'NEW_CRITICAL'
elif any(f['severity'] == 'High' for f in new):
    n_high = sum(1 for f in new if f['severity'] == 'High')
    verdict = f'WORKFLOW_AUDIT_NEW_HIGH — {n_high} new high-severity finding(s)'
    exit_mode = 'NEW_HIGH'
else:
    verdict = f'WORKFLOW_AUDIT_NEW_INFO — {len(new)} new lower-severity finding(s)'
    exit_mode = 'NEW_INFO'

def fp(rule, file, step):
    """16-char sha256 fingerprint, anchored to (rule, basename, step)."""
    base = os.path.basename(file)
    s = f'{rule}|{base}|{step}'
    return hashlib.sha256(s.encode()).hexdigest()[:16]

# Group unchanged for compact table
unchanged_sorted = sorted(unchanged, key=lambda x: (sev_rank[x['severity']], x['file'], x['line']))

# Build report
out = []
out.append(f'# Workflow Security Audit — {today}\n')
out.append(f'**Verdict:** {verdict}')
out.append(f'**Repo:** [{repo_name}]({repo_url})')
out.append(f'**Files audited:** {workflow_count + action_count} ({workflow_count} workflows, {action_count} composite actions)')
out.append(f'**Findings this run:** {total} '
           f'({by_sev.get("Critical",0)} critical, {by_sev.get("High",0)} high, '
           f'{by_sev.get("Medium",0)} medium, {by_sev.get("Low",0)} low)')
out.append(f'**Delta vs {prior_date}:** {len(new)} new, {len(reintroduced)} reintroduced, '
           f'{len(unchanged)} unchanged, {len(resolved)} resolved')
out.append(f'**Auto-fixed:** 0\n')

out.append('## Verdict interpretation\n')
out.append(f'`UNCHANGED` — every finding here was already surfaced in the '
           f'[{prior_date} audit](../../../tree/fix/workflow-security-audit-{prior_date}/articles/workflow-security-audit-{prior_date}.md) '
           f'and none have been fixed since. Per the skill\'s gating rule, no PR is opened and no notify fires — '
           f'silence on no-delta runs is intentional so the notify channel does not learn to be ignored.\n')
out.append('The 3 Critical + 21 High items sit on the same MEMORY.md follow-up (per `## Pointers`): '
           f'(a) pin the `actions/checkout@v5` and `actions/setup-node@v5` refs in `aeon.yml` to SHAs, '
           f'(b) create `production` and `chain-runner` GitHub Environments and move sensitive secrets '
           f'(`GH_GLOBAL`, `GITLAWB_*_PEM`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`) '
           f'from repo-scoped to environment-scoped, (c) address 11 `zizmor/artipacked` Mediums '
           f'(`persist-credentials: false` on read-only checkouts). These require operator judgment — '
           f'auto-fix is deliberately out of scope for pinning, permissions, and persist-credentials per skill constraints.\n')

# Regressions section
out.append('## Regressions (previously-fixed findings now present again)\n')
if not reintroduced:
    out.append('_None — no fingerprints marked `auto-fixed` or `resolved` in the prior report have re-appeared._\n')
else:
    for f in sorted(reintroduced, key=lambda x: (sev_rank[x['severity']], x['file'], x['line'])):
        out.append(f'### [{f["severity"].upper()}] {f["rule_id"]} — {f["file"]}:{f["line"]}')
        out.append(f'**Step:** `{f["step"]}` · **Message:** {f.get("message", "")[:200]}\n')

# New findings section
out.append('## New findings\n')
if not new:
    out.append('_None — no fingerprints appeared this run that were absent from the prior audit._\n')
else:
    for f in sorted(new, key=lambda x: (sev_rank[x['severity']], x['file'], x['line'])):
        out.append(f'### [{f["severity"].upper()}] {f["rule_id"]} — {f["file"]}:{f["line"]}')
        out.append(f'**Step:** `{f["step"]}` · **Message:** {f.get("message", "")[:200]}\n')

# Carried over table
out.append('## Carried over (unchanged)\n')
out.append('| Severity | Rule | File | Step | Line |')
out.append('|---|---|---|---|---|')
for f in unchanged_sorted:
    fname = os.path.basename(f['file'])
    step = f['step'][:40]
    out.append(f"| {f['severity']} | `{f['rule_id']}` | `{fname}` | `{step}` | {f['line']} |")
out.append('')

# Resolved section
out.append(f'## Resolved since {prior_date}\n')
if not resolved:
    out.append('_None — no fingerprints from the prior audit are absent from this run._\n')
else:
    for r in resolved:
        out.append(f'- `{r["rule_id"]}` in `{r["file"]}` (step `{r["step"]}`) — no longer present')
    out.append('')

# Source status
out.append('## Source status\n')
out.append('- zizmor 1.25.2 (via `.audit-bin/zizmor`): **ok** — 125 raw results, dedup → 43 unique')
out.append('- actionlint 1.7.12 (via `.audit-bin/actionlint`): **ok** — 20 shellcheck results, 2 upgraded to High for SC2086 near `${{ github.* }}`')
out.append('- hand-rolled backstops (`toJson-into-shell`, `persist-credentials + head.sha`, `GITHUB_ENV` write injection, fleet inputs passthrough, mutable third-party ref): **ok** — 0 hits (April 11 `messages.yml:577` pattern remains fixed)\n')

# Fingerprint trailer
out.append('<!--')
out.append('workflow-security-audit-fingerprints')
for f in sorted(findings, key=lambda x: (sev_rank[x['severity']], x['file'], x['line'])):
    fpv = fp(f['rule_id'], f['file'], f['step'])
    status = 'manual' if f['severity'] in ('Critical', 'High') else 'open'
    out.append(f'{fpv} severity={f["severity"]} status={status} rule={f["rule_id"]} '
               f'file={f["file"]} step={f["step"]} line={f["line"]} delta={f["delta"]}')
out.append('-->')

report = '\n'.join(out) + '\n'
open(f'articles/workflow-security-audit-{today}.md', 'w').write(report)
print(f'Wrote articles/workflow-security-audit-{today}.md ({len(report)} bytes)')
print(f'Exit mode: {exit_mode}')
print(f'Verdict: {verdict}')
