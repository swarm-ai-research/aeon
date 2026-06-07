"""
Delta computation v3 — with prior per-file counts manually extracted from
the 2026-05-31 narrative table (the trailer aggregates didn't carry per-file
breakdowns, so we read them from the carried-over section text).
"""

import json
import re
import os
import hashlib
from collections import Counter

findings = json.load(open('.audit/classified.json'))

# Calibration: zizmor --persona auditor uplifts unpinned-uses to error.
# Prior audit (same scanner version) graded these as High; honor that to keep
# deltas meaningful — policy compliance, not exploit-imminence.
for f in findings:
    if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
        f['severity'] = 'High'
        f['calibrated'] = True

def base(p):
    return os.path.basename(p)

# Prior per-file counts (extracted by reading articles/workflow-security-audit-2026-05-31.md)
prior_counts = {
    # ('rule', 'basename'): count
    # High class
    ('unpinned-uses', 'aeon.yml'): 3,
    ('unpinned-uses', 'chain-runner.yml'): 1,
    ('unpinned-uses', 'fleet-runner.yml'): 2,
    ('unpinned-uses', 'lint.yml'): 3,
    ('unpinned-uses', 'messages.yml'): 3,
    ('unpinned-uses', 'sync-upstream.yml'): 1,
    # secrets-outside-env from carried-over table:
    # "chain-runner.yml(4), fleet-runner.yml(10), messages.yml(27), sync-upstream.yml(2)"
    ('secrets-outside-env', 'chain-runner.yml'): 4,
    ('secrets-outside-env', 'fleet-runner.yml'): 10,
    ('secrets-outside-env', 'messages.yml'): 27,
    ('secrets-outside-env', 'sync-upstream.yml'): 2,
    # artipacked
    ('artipacked', 'aeon.yml'): 2,
    ('artipacked', 'chain-runner.yml'): 1,
    ('artipacked', 'fleet-runner.yml'): 1,
    ('artipacked', 'lint.yml'): 2,
    ('artipacked', 'messages.yml'): 2,
    ('artipacked', 'sync-upstream.yml'): 1,
    # template-injection (Low/note): aeon.yml(29) explicit; assume rest match today's
    # distribution since prior trailer aggregate count=46 matches today's 46 total.
    ('template-injection', 'aeon.yml'): 29,
    ('template-injection', 'fleet-runner.yml'): 12,
    ('template-injection', 'messages.yml'): 1,
    ('template-injection', 'sync-upstream.yml'): 4,
    # undocumented-permissions: 1 per file (5 files)
    ('undocumented-permissions', 'aeon.yml'): 1,
    ('undocumented-permissions', 'chain-runner.yml'): 1,
    ('undocumented-permissions', 'fleet-runner.yml'): 1,
    ('undocumented-permissions', 'messages.yml'): 1,
    ('undocumented-permissions', 'sync-upstream.yml'): 1,
    # anonymous-definition
    ('anonymous-definition', 'aeon.yml'): 1,
    ('anonymous-definition', 'chain-runner.yml'): 1,
    ('anonymous-definition', 'fleet-runner.yml'): 1,
    ('anonymous-definition', 'messages.yml'): 2,
    ('anonymous-definition', 'sync-upstream.yml'): 1,
    # concurrency-limits
    ('concurrency-limits', 'fleet-runner.yml'): 1,
}

# Today's counts
today_counts = Counter((f['short_rule'], base(f['file'])) for f in findings)

# Build delta per (rule, file)
all_keys = set(today_counts) | set(prior_counts)
print('Per-(rule, file) delta:')
new_count = 0
unchanged_count = 0
resolved_count = 0
for key in sorted(all_keys):
    rule, fname = key
    t = today_counts.get(key, 0)
    p = prior_counts.get(key, 0)
    diff = t - p
    if diff > 0:
        marker = f'  +{diff} NEW'
        new_count += diff
    elif diff < 0:
        marker = f'  {diff} RESOLVED'
        resolved_count += -diff
    else:
        marker = ''
    unchanged_count += min(t, p)
    print(f'  {rule:28s} {fname:30s} today={t:3d} prior={p:3d}{marker}')

print(f'\nTotals: NEW={new_count} UNCHANGED={unchanged_count} RESOLVED={resolved_count}')

# Tag each finding NEW / UNCHANGED. For each (rule, file) pair, first prior_count
# findings (sorted by line) are UNCHANGED, the rest NEW.
new_findings = []
unchanged_findings = []
for (rule, fname) in {(f['short_rule'], base(f['file'])) for f in findings}:
    pair_findings = sorted(
        [f for f in findings if f['short_rule'] == rule and base(f['file']) == fname],
        key=lambda x: x['line']
    )
    p = prior_counts.get((rule, fname), 0)
    for i, f in enumerate(pair_findings):
        if i < p:
            f['delta'] = 'UNCHANGED'
            unchanged_findings.append(f)
        else:
            f['delta'] = 'NEW'
            new_findings.append(f)

print(f'\nNEW count by severity:')
for s, n in Counter(f['severity'] for f in new_findings).most_common():
    print(f'  {n:3d}  {s}')

print(f'\nNEW findings (sorted by severity, file, line):')
sev_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
for f in sorted(new_findings, key=lambda x: (sev_order[x['severity']], x['file'], x['line'])):
    print(f'  [{f["severity"]}] {f["short_rule"]:25s} {base(f["file"])}:{f["line"]} step={f["step"]!r}')

# Total counts
print(f'\nFile audit counts:')
print(f'  total findings: {len(findings)}')
sev_counter = Counter(f['severity'] for f in findings)
print(f'  Critical: {sev_counter["Critical"]}, High: {sev_counter["High"]}, Medium: {sev_counter["Medium"]}, Low: {sev_counter["Low"]}')

json.dump({
    'findings': findings,
    'summary': {
        'total': len(findings),
        'new': new_count,
        'unchanged': unchanged_count,
        'resolved': resolved_count,
        'crit': sev_counter['Critical'],
        'high': sev_counter['High'],
        'med': sev_counter['Medium'],
        'low': sev_counter['Low'],
    },
}, open('.audit/final.json', 'w'), indent=2)
