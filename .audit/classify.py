"""Delta classification against prior audit."""
import json, re, os
from collections import Counter

os.chdir('/home/runner/work/aeon/aeon')
findings = json.load(open('.audit/findings.json'))
prior_text = open('.audit/prior/report.md').read()
m = re.search(r'workflow-security-audit-fingerprints\s*\n(.+?)-->', prior_text, re.S)
assert m, 'fingerprint trailer not found'
block = m.group(1)

prior_entries_list = []
for line in block.splitlines():
    line = line.strip()
    if not line: continue
    parts = line.split()
    if not parts: continue
    fp = parts[0]
    if not re.fullmatch(r'[0-9a-f]{16}', fp): continue
    attrs = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1)
            attrs[k] = v
    prior_entries_list.append((fp, attrs))

prior_counter = Counter(fp for fp, _ in prior_entries_list)
prior_attrs_by_fp = {}
for fp, attrs in prior_entries_list:
    prior_attrs_by_fp.setdefault(fp, attrs)

print('Prior trailer entries:', len(prior_entries_list))
print('Current findings:', len(findings))

new_cnt = reintro_cnt = unchanged_cnt = 0

for f in findings:
    fp = f['fingerprint']
    if prior_counter[fp] > 0:
        prior_counter[fp] -= 1
        attrs = prior_attrs_by_fp.get(fp, {})
        status = attrs.get('status', 'manual')
        if status in ('auto-fixed', 'resolved'):
            f['delta'] = 'REINTRODUCED'
            reintro_cnt += 1
        else:
            f['delta'] = 'UNCHANGED'
            unchanged_cnt += 1
    else:
        f['delta'] = 'NEW'
        new_cnt += 1

cur_fps = Counter(f['fingerprint'] for f in findings)
resolved = []
for fp, remaining in prior_counter.items():
    if remaining > 0:
        for _ in range(remaining):
            attrs = prior_attrs_by_fp.get(fp, {})
            resolved.append({'fp': fp, **attrs})

print('NEW:', new_cnt)
print('REINTRODUCED:', reintro_cnt)
print('UNCHANGED:', unchanged_cnt)
print('RESOLVED:', len(resolved))

delta_counts = Counter((f['delta'], f['severity']) for f in findings)
print('By (delta, severity):', dict(delta_counts))

new_crit = sum(1 for f in findings if f['delta'] == 'NEW' and f['severity'] == 'Critical')
new_high = sum(1 for f in findings if f['delta'] == 'NEW' and f['severity'] == 'High')
new_med = sum(1 for f in findings if f['delta'] == 'NEW' and f['severity'] == 'Medium')
new_low = sum(1 for f in findings if f['delta'] == 'NEW' and f['severity'] == 'Low')
reintro = reintro_cnt
total_new = new_cnt
unchanged = unchanged_cnt

if len(findings) == 0:
    verdict = f'WORKFLOW_AUDIT_CLEAN — no findings across 8 files'
    mode = 'CLEAN'
elif total_new == 0 and reintro == 0:
    verdict = f'WORKFLOW_AUDIT_UNCHANGED — {unchanged} carried over from 2026-09-27'
    mode = 'UNCHANGED'
elif reintro >= 1:
    verdict = f'WORKFLOW_AUDIT_REGRESSION — {reintro} previously-fixed finding(s) reintroduced'
    mode = 'REGRESSION'
elif new_crit >= 1:
    verdict = f'WORKFLOW_AUDIT_NEW_CRITICAL — {new_crit} new critical finding(s)'
    mode = 'NEW_CRITICAL'
elif new_high >= 1:
    verdict = f'WORKFLOW_AUDIT_NEW_HIGH — {new_high} new high-severity finding(s)'
    mode = 'NEW_HIGH'
else:
    verdict = f'WORKFLOW_AUDIT_NEW_INFO — {new_med + new_low} new lower-severity finding(s)'
    mode = 'NEW_INFO'

print('\nVERDICT:', verdict)
print('MODE:', mode)

json.dump({'findings': findings, 'resolved': resolved}, open('.audit/classified.json', 'w'), indent=1)
json.dump({'verdict': verdict, 'mode': mode,
           'new_crit': new_crit, 'new_high': new_high, 'new_med': new_med, 'new_low': new_low,
           'reintro': reintro, 'unchanged': unchanged, 'resolved': len(resolved),
           'total': len(findings)},
          open('.audit/verdict.json', 'w'), indent=1)
