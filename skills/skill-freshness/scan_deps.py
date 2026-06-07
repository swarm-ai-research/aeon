import os, re, json
from datetime import datetime, timezone

BASE = '/home/runner/work/aeon/aeon'
TODAY = '2026-06-05'
NOW = datetime(2026, 6, 5, 8, 20, 0, tzinfo=timezone.utc)

ENABLED_SKILLS = [
    'planner','batch-health','memory-flush','memory-structural-dedupe','janitor',
    'stale-content-pr-sweeper','issue-triage','pr-triage','pr-review','pr-tracker',
    'github-monitor','repo-revive','code-health','surplus-pulse','compute-pulse',
    'compute-futures-eda','compute-macro-correlate','changelog','vuln-scanner',
    'goal-tracker','milestone-tracker','skill-health','config-validator',
    'skill-analytics','reflect','self-review','skill-repair','cost-report',
    'ai-framework-watch','skill-evals','swarm-safety-eval','skill-update-check',
    'fleet-control','gitlawb-fleet-metrics','weekly-shiplog','workflow-security-audit',
    'skill-graph','notegraph','skillpacks','suggest-edges','skill-freshness',
    'run-frequency-guard','heartbeat'
]

# cadence derived from schedule in aeon.yml
PRODUCER_CADENCE = {
    'planner': 'daily', 'batch-health': 'daily', 'memory-flush': 'daily',
    'memory-structural-dedupe': 'daily', 'janitor': 'weekly',
    'stale-content-pr-sweeper': 'daily', 'issue-triage': 'daily',
    'pr-triage': 'daily', 'pr-review': 'daily', 'pr-tracker': 'daily',
    'github-monitor': 'daily', 'repo-revive': 'weekly', 'code-health': 'daily',
    'surplus-pulse': 'daily', 'compute-pulse': 'weekly', 'compute-futures-eda': 'daily',
    'compute-macro-correlate': 'weekly', 'changelog': 'weekly', 'vuln-scanner': 'weekly',
    'goal-tracker': 'daily', 'milestone-tracker': 'weekly', 'skill-health': 'daily',
    'config-validator': 'weekly', 'skill-analytics': 'weekly', 'reflect': 'daily',
    'self-review': 'weekly', 'skill-repair': 'on_demand', 'cost-report': 'weekly',
    'ai-framework-watch': 'weekly', 'skill-evals': 'weekly', 'swarm-safety-eval': 'weekly',
    'skill-update-check': 'weekly', 'fleet-control': 'daily', 'gitlawb-fleet-metrics': 'daily',
    'weekly-shiplog': 'weekly', 'workflow-security-audit': 'weekly', 'skill-graph': 'weekly',
    'notegraph': 'daily', 'skillpacks': 'weekly', 'suggest-edges': 'daily',
    'skill-freshness': 'daily', 'run-frequency-guard': 'daily', 'heartbeat': 'daily'
}

# Thresholds in hours
THRESHOLDS = {
    'articles_daily': 28,
    'articles_weekly': 192,
    'outputs': 4,
    'topics': 168,
    'state': 720,
}

def get_path_class(path):
    if path.startswith('articles/'):
        return 'articles'
    elif path.startswith('.outputs/'):
        return 'outputs'
    elif path.startswith('memory/topics/'):
        return 'topics'
    elif path.startswith('memory/state/'):
        return 'state'
    return 'unknown'

def get_threshold(path_class, producer_cadence='daily'):
    if path_class == 'articles':
        return THRESHOLDS['articles_weekly'] if producer_cadence == 'weekly' else THRESHOLDS['articles_daily']
    elif path_class == 'outputs':
        return THRESHOLDS['outputs']
    elif path_class == 'topics':
        return THRESHOLDS['topics']
    elif path_class == 'state':
        return THRESHOLDS['state']
    return 28

def get_severity(age_hours, threshold_hours):
    if age_hours <= threshold_hours:
        return 'OK'
    elif age_hours <= 2 * threshold_hours:
        return 'WARN'
    else:
        return 'STALE'

# Pattern to find file references
REF_PATTERN = re.compile(
    r'(articles/[a-zA-Z0-9_-]+(?:-\$\{today\}|-[0-9]{4}-[0-9]{2}-[0-9]{2})?\.md'
    r'|\.outputs/[a-zA-Z0-9_-]+\.md'
    r'|memory/topics/[a-zA-Z0-9_.\-]+\.md'
    r'|memory/state/[a-zA-Z0-9_.\-]+\.json)'
)

# Also look for generic article patterns: articles/{skill}-${today}.md or articles/{skill}-*.md
ARTICLE_PATTERN = re.compile(r'articles/([a-zA-Z0-9_-]+)-(?:\$\{today\}|\*)\.md')

results = []
all_deps = []
ignored_count = 0

for skill in ENABLED_SKILLS:
    fpath = os.path.join(BASE, 'skills', skill, 'SKILL.md')
    if not os.path.exists(fpath):
        continue
    content = open(fpath).read()

    refs = set(REF_PATTERN.findall(content))

    # Also find article pattern references
    for m in ARTICLE_PATTERN.finditer(content):
        producer = m.group(1)
        # find most recent file
        articles_dir = os.path.join(BASE, 'articles')
        matching = sorted([f for f in os.listdir(articles_dir)
                           if f.startswith(producer + '-') and f.endswith('.md')], reverse=True)
        if matching:
            refs.add('articles/' + matching[0])
        else:
            # MISSING - will be flagged if producer is daily/weekly
            refs.add('articles/' + producer + '-' + TODAY + '.md')

    for ref in sorted(refs):
        # Skip self-references (producer name in own output)
        if skill in ref and ref.startswith('articles/' + skill):
            continue
        if skill in ref and ref.startswith('.outputs/' + skill):
            continue

        path_class = get_path_class(ref)
        full_path = os.path.join(BASE, ref.lstrip('./'))
        if ref.startswith('.outputs/'):
            full_path = os.path.join(BASE, '.outputs', ref[9:])

        exists = os.path.exists(full_path)

        if not exists:
            # For implicit refs that never existed, skip (not explicit chain edges)
            severity = 'MISSING'
            age_hours = None
            threshold_hours = None
            ignored_count += 1
            # Skip implicit missing refs per spec
            results.append({
                'consumer': skill,
                'dep': ref,
                'class': path_class,
                'exists': False,
                'age_hours': None,
                'threshold': None,
                'severity': 'MISSING_IMPLICIT',
                'note': 'implicit ref, file never created — skip'
            })
            continue

        # Get mtime
        mtime = os.path.getmtime(full_path)
        mtime_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        age_hours = (NOW - mtime_dt).total_seconds() / 3600

        # Infer producer from path
        producer_name = None
        if path_class == 'articles':
            fname = ref.split('/')[-1]
            # extract producer from filename
            m = re.match(r'^([a-zA-Z0-9_-]+)-[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$', fname)
            if m:
                producer_name = m.group(1)
        elif path_class == 'outputs':
            producer_name = ref.split('/')[-1].replace('.md', '')

        cadence = PRODUCER_CADENCE.get(producer_name, 'daily') if producer_name else 'daily'
        threshold_hours = get_threshold(path_class, cadence)
        severity = get_severity(age_hours, threshold_hours)

        results.append({
            'consumer': skill,
            'dep': ref,
            'class': path_class,
            'exists': True,
            'age_hours': round(age_hours, 2),
            'threshold': threshold_hours,
            'severity': severity,
            'cadence': cadence
        })
        all_deps.append({'consumer': skill, 'dep': ref, 'severity': severity})

print(json.dumps(results, indent=2))
