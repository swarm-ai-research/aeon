import os, re

enabled_skills = [
    'planner','batch-health','memory-flush','memory-structural-dedupe','janitor',
    'stale-content-pr-sweeper','issue-triage','pr-triage','pr-review','pr-tracker',
    'github-monitor','repo-revive','code-health','surplus-pulse','compute-pulse',
    'compute-macro-correlate','compute-futures-eda','changelog','vuln-scanner',
    'goal-tracker','agi-tracker','milestone-tracker','skill-health','config-validator',
    'skill-analytics','reflect','self-review','skill-repair','cost-report',
    'ai-framework-watch','skill-evals','swarm-safety-eval','skill-update-check',
    'fleet-control','gitlawb-fleet-metrics','weekly-shiplog','skill-freshness',
    'run-frequency-guard','workflow-security-audit','skill-graph','notegraph',
    'skillpacks','suggest-edges','heartbeat'
]

pattern = re.compile(
    r'(articles/[a-zA-Z0-9_-]+'
    r'(?:-\$\{today\}|-\$\{date\}|-[0-9]{4}-[0-9]{2}-[0-9]{2})?'
    r'\.md'
    r'|\.outputs/[a-zA-Z0-9_-]+\.md'
    r'|memory/topics/[a-zA-Z0-9_.-]+\.md'
    r'|memory/state/[a-zA-Z0-9_.-]+\.json)'
)

for skill in enabled_skills:
    path = f'skills/{skill}/SKILL.md'
    if not os.path.exists(path):
        continue
    with open(path) as f:
        content = f.read()
    matches = set(pattern.findall(content))
    own_prefix = f'articles/{skill}-'
    filtered = [m for m in matches if not m.startswith(own_prefix)]
    if filtered:
        print(f'=== {skill} ===')
        for m in sorted(filtered):
            print(f'  {m}')
