"""Write the UNCHANGED-mode audit report + trailer for 2026-08-16."""
import json, os, hashlib, subprocess, re
from collections import defaultdict, Counter

TODAY = '2026-08-16'
PRIOR_DATE = '2026-08-09'
REPO_NAME = 'swarm-ai-research/aeon'
REPO_URL = 'https://github.com/swarm-ai-research/aeon'

d = json.load(open('.audit/classified2.json'))
findings = d['findings']
summary = d['summary']

# Recompute per-(rule, file) breakdown for the carried-over table
per_file = defaultdict(list)
for f in findings:
    per_file[(f['rule_id'], os.path.basename(f['file']))].append(f)

# Pull prior fingerprints so we can preserve them (semkey → fp) instead of recomputing.
prior_raw = subprocess.check_output(
    ['git', 'show', 'refs/audit-prior:articles/workflow-security-audit-2026-08-09.md']
).decode()

prior_by_semkey = {}
for m in re.finditer(r'^([a-f0-9]{12})\s+severity=(\S+)\s+status=(\S+)\s+rule=(\S+)\s+file=(\S+)\s+step=(\S+)\s*$', prior_raw, re.M):
    fp, sev, status, rule, file, step = m.groups()
    prior_by_semkey[(rule, os.path.basename(file), step)] = (fp, sev, status, file, step)

# Sanity: every finding should have a prior fingerprint (since delta is UNCHANGED)
for f in findings:
    sk = (f['rule_id'], os.path.basename(f['file']), f['step'].replace(' ', '_'))
    assert sk in prior_by_semkey, f'no prior fingerprint for {sk}'

lines = []
lines.append(f'# Workflow Security Audit — {TODAY}')
lines.append('')
lines.append(f'**Verdict:** WORKFLOW_AUDIT_UNCHANGED — {summary["total"]} carried over from {PRIOR_DATE}')
lines.append(f'**Repo:** [{REPO_NAME}]({REPO_URL})')
lines.append(f'**Files audited:** 8 (8 workflows, 0 composite actions)')
lines.append(f'**Findings this run:** {summary["total"]} ({summary["crit"]} critical, {summary["high"]} high, {summary["med"]} medium, {summary["low"]} low)')
lines.append(f'**Delta vs {PRIOR_DATE}:** 0 new, 0 reintroduced, {summary["unchanged"]} unchanged, 0 resolved')
lines.append(f'**Auto-fixed:** 0')
lines.append('')
lines.append('## Regressions (previously-fixed findings now present again)')
lines.append('')
lines.append('_None. No prior fingerprint was marked `auto-fixed` or `resolved`, so there is nothing to regress against._')
lines.append('')
lines.append('## New findings')
lines.append('')
lines.append('_None. Every finding present on this run was also present on `2026-08-09` (same rule / file / step across all 78 items) — no NEW deltas, no auto-fix work, no notify._')
lines.append('')
lines.append(f'Per the SKILL step-5 gating rule, `UNCHANGED` mode does not open a PR and does not notify; silence is correct on no-delta runs so the notify channel stays high-signal. The full carried-over set is captured below for completeness and for the next run\'s delta baseline.')
lines.append('')

# Group carried-over by severity → rule → file for the table
lines.append(f'## Carried over (unchanged from {PRIOR_DATE})')
lines.append('')
lines.append('Every finding below has a stable fingerprint in the trailer at the bottom of this file. The next run keys against those to detect regressions.')
lines.append('')

sev_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}

# By-severity summary table
lines.append('| Severity | Rule | Count | Files |')
lines.append('|---|---|---|---|')
by_rule = defaultdict(lambda: {'count': 0, 'files': set(), 'sev': ''})
for f in findings:
    key = f['rule_id']
    by_rule[key]['count'] += 1
    by_rule[key]['files'].add(os.path.basename(f['file']))
    by_rule[key]['sev'] = f['severity']
for rule in sorted(by_rule, key=lambda r: (sev_order[by_rule[r]['sev']], r)):
    entry = by_rule[rule]
    files_str = ', '.join(f'{fn}({sum(1 for f in findings if f["rule_id"] == rule and os.path.basename(f["file"]) == fn)})' for fn in sorted(entry['files']))
    lines.append(f'| {entry["sev"]} | `{rule}` | {entry["count"]} | {files_str} |')
lines.append('')

# Detailed list of Critical + High for reference (attack-chain style abbreviated to one-liner
# since these are all UNCHANGED and were narrated in prior audits)
lines.append('### Critical + High detail (all carried over, all still `Manual required`)')
lines.append('')
lines.append('| Severity | Rule | File | Step | First seen |')
lines.append('|---|---|---|---|---|')
crit_high = sorted(
    [f for f in findings if f['severity'] in ('Critical', 'High')],
    key=lambda f: (sev_order[f['severity']], f['rule_id'], f['file'], f['step'])
)
for f in crit_high:
    lines.append(f'| {f["severity"]} | `{f["rule_id"]}` | `{os.path.basename(f["file"])}` | `{f["step"]}` | ≤ {PRIOR_DATE} |')
lines.append('')

lines.append('## Resolved since ' + PRIOR_DATE)
lines.append('')
lines.append('_None. Every fingerprint from the prior audit still fires on this run — the operator toggle that keeps the fix branch from merging (`enabled: false` decisions, environment gating, SHA-pin operator approval) is still the primary blocker._')
lines.append('')

lines.append('## Source status')
lines.append('')
lines.append('- zizmor 1.25.2: `ok`')
lines.append('- actionlint 1.7.12: `ok`')
lines.append('- hand-rolled backstops: `ok` (toJson-into-shell, pull_request_target + persist-credentials, GITHUB_ENV injection — 0 hits, April 11 `messages.yml:577` regression pattern remains fixed)')
lines.append('')

lines.append('## Method note')
lines.append('')
lines.append(f'Prior report on `main` is absent (the historical `fix/workflow-security-audit-*` branches remain unmerged per `[[github-actions-cannot-create-prs]]`). Fell back to `git fetch origin fix/workflow-security-audit-{PRIOR_DATE}` for the trailer. Semkey matching is `(rule_id, basename(file), step_name)` — line-fallback via SARIF snippet plus a `- name:` walker back from the reported line — which absorbs unrelated edits that shift line numbers without changing the finding.')
lines.append('')

# Trailer
lines.append('<!--')
lines.append('workflow-security-audit-fingerprints')
for f in sorted(findings, key=lambda x: (sev_order[x['severity']], x['rule_id'], x['file'], x['step'])):
    sk = (f['rule_id'], os.path.basename(f['file']), f['step'].replace(' ', '_'))
    fp, sev_prior, status_prior, file_prior, step_prior = prior_by_semkey[sk]
    # Preserve status from prior (manual/auto-fixed/etc.)
    line = f'{fp} severity={f["severity"]} status={status_prior} rule={f["rule_id"]} file=.github/workflows/{os.path.basename(f["file"])} step={f["step"].replace(" ", "_")}'
    lines.append(line)
lines.append('-->')

report = '\n'.join(lines) + '\n'
with open(f'articles/workflow-security-audit-{TODAY}.md', 'w') as out:
    out.write(report)
print(f'Wrote articles/workflow-security-audit-{TODAY}.md ({len(report)} bytes)')
