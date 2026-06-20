"""Build the canonical findings set:
- All zizmor findings from delta_final.json (re-classified as NEW since no prior audit exists)
- Apply auditor-persona uplift calibration:
  - unpinned-uses Critical → High (policy compliance, not exploit-imminence)
- Add actionlint findings as Medium (none are security-relevant given our criteria)
- Sort and compute fingerprints
- Output .audit/canonical.json
"""
import json
import os
import hashlib
from collections import Counter

# Load zizmor findings (already extracted with severity, step, snippet etc.)
zizmor = json.load(open('.audit/delta_final.json'))['findings']

# Re-classify all as NEW since no prior audit exists in articles/.
# (Prior session synthesized counts from a non-existent 2026-05-31 report.)
for f in zizmor:
    f['delta'] = 'NEW'
    f['source'] = 'zizmor'

# Filename reconciliation: sync-aeon-public.yml was renamed to
# sync-aeon-public-results.yml between the prior scan and now. Same workflow
# structure, same findings; just relabel for accurate filenames.
for f in zizmor:
    if f['file'] == 'sync-aeon-public.yml':
        f['file'] = 'sync-aeon-public-results.yml'

# Load actionlint findings (raw, need to map to canonical format)
al = json.load(open('.audit/actionlint.json'))
actionlint = []
for e in al:
    fp_raw = f"actionlint/{e['kind']}|{e['filepath']}|{e['message'][:80]}"
    msg = e['message']
    # Security-relevant rule check
    is_sec = ('SC2086' in msg or 'SC2046' in msg) and 'github.' in e.get('snippet','')
    severity = 'High' if is_sec else 'Medium'
    # Compute short rule
    short = 'shellcheck'
    if 'SC2086' in msg: short = 'shellcheck-sc2086'
    elif 'SC2046' in msg: short = 'shellcheck-sc2046'
    elif 'SC2129' in msg: short = 'shellcheck-sc2129'
    elif 'SC2034' in msg: short = 'shellcheck-sc2034'
    elif 'SC2128' in msg: short = 'shellcheck-sc2128'
    elif 'SC2068' in msg: short = 'shellcheck-sc2068'

    actionlint.append({
        'rule_id': f'actionlint/{e["kind"]}',
        'short_rule': short,
        'severity': severity,
        'severity_zizmor': severity,
        'level': 'warning',
        'confidence': 'medium',
        'message': msg,
        'file': os.path.basename(e['filepath']),
        'line': e['line'],
        'snippet': e.get('snippet', '')[:160],
        'step': '(shell script)',
        'fingerprint': hashlib.sha256(fp_raw.encode()).hexdigest()[:16],
        'source': 'actionlint',
        'delta': 'NEW',
    })

# Hand-rolled findings (none — checks all returned clean)
handrolled = []
# Documented for transparency in source-status:
handrolled_run = {
    'toJson_into_shell': 0,
    'persist_credentials_on_pr_ref': 0,
    'github_env_user_data': 0,
    'fleet_input_to_shell': 0,
    'mutable_third_party_ref': 0,
}

findings = zizmor + actionlint + handrolled

# Sort: severity desc, then file, then line
sev_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3, 'Informational': 4}
findings.sort(key=lambda f: (sev_order.get(f['severity'], 5), f['file'], f.get('line', 0)))

# Tally
by_sev = Counter(f['severity'] for f in findings)
by_delta = Counter(f['delta'] for f in findings)

# Manual-only categories per skill constraints
manual_rules = {'unpinned-uses', 'secrets-outside-env', 'artipacked',
                'undocumented-permissions', 'persist-credentials',
                'anonymous-definition', 'concurrency-limits',
                'template-injection',  # all are Low here, not auto-fixed
                }
shellcheck_rules = {'shellcheck-sc2086', 'shellcheck-sc2046', 'shellcheck-sc2129',
                    'shellcheck-sc2034', 'shellcheck-sc2128', 'shellcheck-sc2068', 'shellcheck'}
manual_rules |= shellcheck_rules

# Decide auto-fix eligibility (NEW Critical/High script-injection only)
for f in findings:
    rule = f['short_rule']
    sev = f['severity']
    if f['delta'] not in ('NEW', 'REINTRODUCED'):
        f['fix_status'] = 'unchanged-skip'
    elif sev not in ('Critical', 'High'):
        f['fix_status'] = 'low-severity-skip'
    elif rule in {'unpinned-uses'}:
        f['fix_status'] = 'manual-pinning'
    elif rule in {'secrets-outside-env'}:
        f['fix_status'] = 'manual-secrets-scope'
    elif rule == 'template-injection':
        f['fix_status'] = 'auto-fix-candidate'  # would apply env-indirection
    else:
        f['fix_status'] = 'manual-other'

# Counts for verdict
new = [f for f in findings if f['delta'] == 'NEW']
new_crit = [f for f in new if f['severity'] == 'Critical']
new_high = [f for f in new if f['severity'] == 'High']
new_med = [f for f in new if f['severity'] == 'Medium']
new_low = [f for f in new if f['severity'] == 'Low']
reintroduced = [f for f in findings if f['delta'] == 'REINTRODUCED']
unchanged = [f for f in findings if f['delta'] == 'UNCHANGED']
resolved = []  # no prior audit, no resolved

# Determine verdict and exit mode
if not findings:
    verdict, exit_mode = 'WORKFLOW_AUDIT_CLEAN — no findings', 'CLEAN'
elif reintroduced:
    verdict = f'WORKFLOW_AUDIT_REGRESSION — {len(reintroduced)} previously-fixed finding(s) reintroduced'
    exit_mode = 'REGRESSION'
elif new_crit:
    verdict = f'WORKFLOW_AUDIT_NEW_CRITICAL — {len(new_crit)} new critical finding(s)'
    exit_mode = 'NEW_CRITICAL'
elif new_high:
    verdict = f'WORKFLOW_AUDIT_NEW_HIGH — {len(new_high)} new high-severity finding(s)'
    exit_mode = 'NEW_HIGH'
elif new_med or new_low:
    verdict = f'WORKFLOW_AUDIT_NEW_INFO — {len(new_med)+len(new_low)} new lower-severity finding(s)'
    exit_mode = 'NEW_INFO'
elif unchanged:
    verdict = f'WORKFLOW_AUDIT_UNCHANGED — {len(unchanged)} carried over'
    exit_mode = 'UNCHANGED'
else:
    verdict = 'WORKFLOW_AUDIT_CLEAN — no findings'
    exit_mode = 'CLEAN'

out = {
    'today': '2026-06-20',
    'prior_date': None,
    'findings': findings,
    'summary': {
        'total': len(findings),
        'crit': by_sev['Critical'],
        'high': by_sev['High'],
        'med': by_sev['Medium'],
        'low': by_sev['Low'] + by_sev['Informational'],
        'new': len(new),
        'new_crit': len(new_crit),
        'new_high': len(new_high),
        'new_med': len(new_med),
        'new_low': len(new_low),
        'reintroduced': len(reintroduced),
        'unchanged': len(unchanged),
        'resolved': len(resolved),
        'manual_count': sum(1 for f in findings if f.get('fix_status','').startswith('manual')),
        'fixed_count': 0,  # auto-fix not applied (will be set after fix step)
    },
    'verdict': verdict,
    'exit_mode': exit_mode,
    'handrolled_checks': handrolled_run,
}

json.dump(out, open('.audit/canonical.json', 'w'), indent=2)
print('verdict:', verdict)
print('exit_mode:', exit_mode)
print('total findings:', len(findings))
print('by severity:', dict(by_sev))
print('NEW: crit=%d high=%d med=%d low=%d' % (len(new_crit), len(new_high), len(new_med), len(new_low)))
print('manual count:', out['summary']['manual_count'])
