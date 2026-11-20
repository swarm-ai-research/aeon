import datetime, hashlib

NOW_EPOCH = 1795161722
today = '2026-11-20'

articles = {
    'skill-evals': '2026-09-13',
    'vuln-scan': '2026-11-07',
    'workflow-security-audit': '2026-11-08',
    'cost-report': '2026-11-09',
    'skill-freshness': '2026-11-19',
    'skill-analytics': '2026-11-18',
    'self-review': '2026-11-15',
}

print('=== Article ages by filename date (hours) ===')
for skill, date in articles.items():
    d = datetime.datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
    age_h = (NOW_EPOCH - int(d.timestamp())) // 3600
    print(f'{skill}: {age_h}h ({age_h/24:.1f}d)')

thresholds = {
    'skill-evals': ('weekly', 192),
    'vuln-scan': ('weekly', 192),
    'workflow-security-audit': ('weekly', 192),
    'cost-report': ('weekly', 192),
    'skill-freshness': ('daily', 28),
    'skill-analytics': ('weekly', 192),
    'self-review': ('weekly', 192),
}

print()
print('=== Severity check ===')
for skill, date in articles.items():
    d = datetime.datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
    age_h = (NOW_EPOCH - int(d.timestamp())) // 3600
    cadence, thresh = thresholds[skill]
    if age_h <= thresh:
        sev = 'OK'
    elif age_h <= 2*thresh:
        sev = 'WARN'
    else:
        sev = 'STALE'
    print(f'{skill}: {age_h}h, thresh={thresh}h, 2x={2*thresh}h -> {sev}')

print()
print('=== Fingerprint ===')
triples = sorted([
    'cost-report:articles/cost-report-2026-11-09.md:WARN',
    'fleet-control:articles/fleet-status-2026-11-20.md:MISSING',
    'skill-evals:articles/skill-evals-2026-09-13.md:STALE',
    'vuln-scanner:articles/vuln-scan-2026-11-07.md:WARN',
    'workflow-security-audit:articles/workflow-security-audit-2026-11-08.md:WARN',
])
h = hashlib.sha1('\n'.join(triples).encode()).hexdigest()
print('SHA1:', h)
