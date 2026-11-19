import hashlib, datetime

today = datetime.date(2026, 11, 19)

def age_hours(date_str):
    d = datetime.date.fromisoformat(date_str)
    return (today - d).days * 24

producers = {
    'skill-freshness': ('2026-11-14', 'daily'),
    'skill-analytics': ('2026-11-18', 'weekly'),
    'self-review': ('2026-11-15', 'weekly'),
    'cost-report': ('2026-11-09', 'weekly'),
    'vuln-scanner': ('2026-11-07', 'weekly'),
    'workflow-security-audit': ('2026-11-08', 'weekly'),
    'skill-evals': ('2026-09-13', 'weekly'),
}

thresholds = {'daily': 28, 'weekly': 192}

flagged = []
ok_list = []

for skill, (last_date, cadence) in producers.items():
    age = age_hours(last_date)
    thr = thresholds[cadence]
    if age <= thr:
        sev = 'OK'
        ok_list.append((skill, last_date, age, thr, cadence))
    elif age <= 2 * thr:
        sev = 'WARN'
        flagged.append((skill, last_date, age, thr, cadence, sev))
    else:
        sev = 'STALE'
        flagged.append((skill, last_date, age, thr, cadence, sev))

order = {'STALE': 0, 'WARN': 1, 'MISSING': -1}
flagged.sort(key=lambda x: (order.get(x[5], 2), -x[2]))

for f in flagged:
    skill, last_date, age, thr, cadence, sev = f
    days = age / 24
    print(f'{sev} | {skill} | {last_date} | {age:.0f}h ({days:.1f}d) | threshold {thr}h')

for o in ok_list:
    skill, last_date, age, thr, cadence = o
    print(f'OK   | {skill} | {last_date} | {age:.0f}h | threshold {thr}h')

dep_map = {
    'skill-freshness': 'articles/skill-freshness-2026-11-14.md',
    'skill-analytics': 'articles/skill-analytics-2026-11-18.md',
    'self-review': 'articles/self-review-2026-11-15.md',
    'cost-report': 'articles/cost-report-2026-11-09.md',
    'vuln-scanner': 'articles/vuln-scan-2026-11-07.md',
    'workflow-security-audit': 'articles/workflow-security-audit-2026-11-08.md',
    'skill-evals': 'articles/skill-evals-2026-09-13.md',
}

triples = []
for skill, last_date, age, thr, cadence, sev in flagged:
    dep = dep_map.get(skill, f'articles/{skill}-{last_date}.md')
    triples.append(f'{skill}:{dep}:{sev}')

triples.sort()
fp_input = '\n'.join(triples)
fp = hashlib.sha1(fp_input.encode()).hexdigest()
print(f'\nFingerprint: {fp}')
print(f'Prior fp:    905cf2c771f4066d0a8c7b74ab5b1c0e76127e75')
print(f'Changed: {fp != "905cf2c771f4066d0a8c7b74ab5b1c0e76127e75"}')
print(f'\nFlagged count: {len(flagged)}')
print(f'OK count: {len(ok_list)}')
