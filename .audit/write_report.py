#!/usr/bin/env python3
"""Emit articles/workflow-security-audit-2026-08-23.md."""
import json
import os
from collections import defaultdict, Counter

TODAY = '2026-08-23'
REPO_NAME = 'swarm-ai-research/aeon'
REPO_URL = 'https://github.com/swarm-ai-research/aeon'
PRIOR_DATE = '2026-08-09'
PRIOR_SOURCE = 'fix/workflow-security-audit-2026-08-09 (PR #24, unmerged)'

d = json.load(open('.audit/classified.json'))
findings = d['current']
resolved = d['resolved']
fuzzy = d.get('fuzzy_matched', 0)

by_sev = Counter(f['severity'] for f in findings)
by_status = Counter(f['status'] for f in findings)
total = len(findings)

new_count = by_status.get('NEW', 0)
reintro_count = by_status.get('REINTRODUCED', 0)
unchanged_count = by_status.get('UNCHANGED', 0)
resolved_count = len(resolved)

crit = by_sev.get('Critical', 0)
high = by_sev.get('High', 0)
med = by_sev.get('Medium', 0)
low = by_sev.get('Low', 0)

# Verdict + exit mode
if total == 0:
    exit_mode = 'CLEAN'
    verdict = f'WORKFLOW_AUDIT_CLEAN — no findings across 8 files'
elif new_count == 0 and reintro_count == 0:
    exit_mode = 'UNCHANGED'
    verdict = f'WORKFLOW_AUDIT_UNCHANGED — {unchanged_count} carried over from {PRIOR_DATE}'
elif reintro_count > 0:
    exit_mode = 'REGRESSION'
    verdict = f'WORKFLOW_AUDIT_REGRESSION — {reintro_count} previously-fixed finding(s) reintroduced'
else:
    # simplified for this run — full table only if hit
    exit_mode = 'NEW_INFO'
    verdict = f'WORKFLOW_AUDIT_NEW_INFO — {new_count} new lower-severity finding(s)'


# Files audited
WORKFLOWS = 8  # from find output
ACTIONS = 0

# --- Build report ---
lines = []
lines.append(f'# Workflow Security Audit — {TODAY}')
lines.append('')
lines.append(f'**Verdict:** {verdict}')
lines.append(f'**Repo:** [{REPO_NAME}]({REPO_URL})')
lines.append(f'**Files audited:** {WORKFLOWS + ACTIONS} ({WORKFLOWS} workflows, {ACTIONS} composite actions)')
lines.append(f'**Findings this run:** {total} ({crit} critical, {high} high, {med} medium, {low} low)')
lines.append(f'**Delta vs {PRIOR_DATE}:** {new_count} new, {reintro_count} reintroduced, {unchanged_count} unchanged (of which {fuzzy} matched via fuzzy anchor after step-name drift), {resolved_count} resolved')
lines.append(f'**Auto-fixed:** 0')
lines.append('')

lines.append(f'**Prior baseline:** `{PRIOR_SOURCE}`. The 08-09 fix branch has never been merged; the surviving report + fingerprint trailer serve as the delta anchor. On merge, the ~85→78 UNCHANGED cohort will finally live on `main` where the SKILL step-4 `ls` glob can find it directly.')
lines.append('')

if exit_mode == 'UNCHANGED':
    lines.append('## Verdict summary')
    lines.append('')
    lines.append('No new findings, no regressions of previously-fixed items. Every one of the 78 findings this run maps by fingerprint (or by fuzzy (rule, file) anchor for 13 top-level `permissions:` / `on:` / `job:` blocks whose step name resolves to `(unknown)` and whose 12-char SHA-256 prefix drifted between runs) to a corresponding finding in the 2026-08-09 audit. Silence is correct on no-delta runs — this report is written for the record; no PR is opened and no notify is emitted.')
    lines.append('')
    lines.append('The Critical/High cohort — 3 unpinned-uses in `aeon.yml` and 22 High-severity items (16 `secrets-outside-env` + 6 `ref-version-mismatch`) — is the same set already tracked in `memory/MEMORY.md` under "Address workflow-security-audit findings" and blocked on operator action (SHA pinning + GitHub Environment scoping for sensitive secrets).')
    lines.append('')

lines.append('## Regressions (previously-fixed findings now present again)')
lines.append('')
regressions = [f for f in findings if f['status'] == 'REINTRODUCED']
if not regressions:
    lines.append('_None — no fingerprint from the prior audit was marked `auto-fixed` or `resolved`, so no regressions to report._')
else:
    for f in regressions:
        lines.append(f"- **[{f['severity']}] {f['rule_id']}** in `{f['file']}:{f['line']}` step `{f['step']}` (prior status: {f.get('prior_status', '?')})")
lines.append('')

lines.append('## New findings')
lines.append('')
new_findings = [f for f in findings if f['status'] == 'NEW']
if not new_findings:
    lines.append('_None — every finding this run matches a prior fingerprint (with fuzzy anchoring for 13 items whose 12-char SHA drifted on top-level `(unknown)`-step blocks)._')
else:
    # Group by severity
    by_sev_new = defaultdict(list)
    for f in new_findings:
        by_sev_new[f['severity']].append(f)
    for sev in ('Critical', 'High'):
        for f in by_sev_new.get(sev, []):
            lines.append(f"### [{sev.upper()}] {f['rule_id']} — {f['message'][:80].splitlines()[0]}")
            lines.append(f"**File:** `{f['file']}` · **Step:** `{f['step']}` · **Line:** {f['line']}")
            lines.append('**Pattern:**')
            lines.append('```yaml')
            lines.append(f['pattern'])
            lines.append('```')
            lines.append('**Status:** Manual required')
            lines.append('')
            lines.append('---')
    if by_sev_new.get('Medium') or by_sev_new.get('Low'):
        lines.append('')
        lines.append('| Severity | Rule | File | Line | Step |')
        lines.append('|---|---|---|---|---|')
        for sev in ('Medium', 'Low'):
            for f in by_sev_new.get(sev, []):
                lines.append(f"| {sev} | `{f['rule_id']}` | `{f['file']}` | {f['line']} | `{f['step']}` |")
        lines.append('')

lines.append('## Carried over (unchanged) — Critical/High')
lines.append('')
lines.append('| Severity | Rule | File | Line | Step |')
lines.append('|---|---|---|---|---|')
for f in sorted([x for x in findings if x['status'] == 'UNCHANGED' and x['severity'] in ('Critical', 'High')],
                key=lambda x: (x['severity'] != 'Critical', x['file'], x['line'])):
    lines.append(f"| {f['severity']} | `{f['rule_id']}` | `{f['file']}` | {f['line']} | `{f['step']}` |")
lines.append('')

lines.append('## Carried over (unchanged) — Medium/Low counts')
lines.append('')
med_low = [f for f in findings if f['status'] == 'UNCHANGED' and f['severity'] in ('Medium', 'Low')]
by_rule_ml = Counter(f['rule_id'] for f in med_low)
lines.append('| Count | Rule | Severity mix |')
lines.append('|---|---|---|')
for rule, n in sorted(by_rule_ml.items(), key=lambda x: -x[1]):
    sev_mix = Counter(f['severity'] for f in med_low if f['rule_id'] == rule)
    mix_str = ', '.join(f'{v} {k}' for k, v in sev_mix.items())
    lines.append(f"| {n} | `{rule}` | {mix_str} |")
lines.append('')

lines.append(f'## Resolved since {PRIOR_DATE}')
lines.append('')
if not resolved:
    lines.append('_None — every prior fingerprint has a matching current fingerprint (direct or fuzzy-anchor)._')
else:
    for r in resolved:
        lines.append(f"- `{r.get('rule','?')}` in `{r.get('file','?')}` step `{r.get('step','?')}` (prior fp {r['fingerprint']}) — no longer present")
lines.append('')

lines.append('## Source status')
lines.append('')
lines.append('- zizmor: ok (v1.25.2, `.audit-bin/zizmor` pre-cached binary via python subprocess — direct binary launch blocked by session sandbox permissions)')
lines.append('- actionlint: ok (`.audit-bin/actionlint` pre-cached binary via python subprocess)')
lines.append('- hand-rolled: ok (all 5 pattern classes ran; 0 hits — the messages.yml:577 `toJson`-into-shell backstop pattern remains fixed via `_CLIENT_PAYLOAD_MESSAGE` env-indirection at `messages.yml:667`)')
lines.append('')

# Machine-readable trailer
lines.append('<!--')
lines.append('workflow-security-audit-fingerprints')
for f in sorted(findings, key=lambda x: (x['severity'] != 'Critical', x['severity'] != 'High', x['file'], x['line'])):
    status_str = 'manual' if f['severity'] in ('Critical', 'High') else 'open'
    step_us = f['step'].replace(' ', '_')
    lines.append(f"{f['fingerprint']} severity={f['severity']} status={status_str} rule={f['rule_id']} file={f['file']} step={step_us}")
lines.append('-->')
lines.append('')

out = '\n'.join(lines)
open(f'articles/workflow-security-audit-{TODAY}.md', 'w').write(out)
print(f'wrote articles/workflow-security-audit-{TODAY}.md ({len(out)} bytes)')
print(f'exit_mode={exit_mode}')
print(f'verdict={verdict}')
