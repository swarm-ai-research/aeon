import datetime, hashlib

NOW_EPOCH = 1795161722

triples = sorted([
    'cost-report:articles/cost-report-2026-11-09.md:WARN',
    'fleet-control:articles/fleet-status-2026-11-20.md:MISSING',
    'skill-evals:articles/skill-evals-2026-09-13.md:STALE',
    'skill-freshness:articles/skill-freshness-2026-11-19.md:WARN',
    'vuln-scanner:articles/vuln-scan-2026-11-07.md:WARN',
    'workflow-security-audit:articles/workflow-security-audit-2026-11-08.md:WARN',
])
h = hashlib.sha1('\n'.join(triples).encode()).hexdigest()
print('Fingerprint:', h)
print('Triples:')
for t in triples:
    print(' ', t)
