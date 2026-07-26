import json
from collections import Counter

findings = json.load(open('.audit/findings.json'))

unique = {}
fp_count = Counter()
for f in findings:
    fp_count[f['fingerprint']] += 1
    if f['fingerprint'] not in unique:
        unique[f['fingerprint']] = f

sev_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
ranked = sorted(unique.values(), key=lambda f: (sev_order[f['severity']], f['file'], f['line']))

by_sev = Counter(f['severity'] for f in ranked)
print("Unique fingerprints: %d" % len(ranked))
for k in ('Critical', 'High', 'Medium', 'Low'):
    print("  %s: %d" % (k, by_sev.get(k, 0)))

json.dump(ranked, open('.audit/unique.json', 'w'), indent=2)
print()
print("Critical/High unique findings:")
for f in ranked:
    if f['severity'] in ('Critical', 'High'):
        print("  [%s] %-38s %s:%d step='%s'" % (f['severity'], f['rule_id'], f['file'], f['line'], f['step'][:40]))
