import hashlib, json
from datetime import datetime, timezone

degraded = sorted([
    'batch-health','changelog','code-health','compute-futures-eda','compute-macro-correlate',
    'compute-pulse','cost-report','fleet-control','github-monitor','gitlawb-fleet-metrics',
    'goal-tracker','heartbeat','issue-triage','janitor','memory-flush','memory-structural-dedupe',
    'milestone-tracker','notegraph','planner','pr-review','pr-tracker','pr-triage','reflect',
    'repo-revive','self-review','skill-analytics','skill-evals','skill-freshness','skill-graph',
    'skill-health','skill-repair','skill-update-check','skillpacks','stale-content-pr-sweeper',
    'suggest-edges','surplus-pulse','vuln-scanner','workflow-security-audit'
])
payloadB = json.dumps({'critical':[], 'flapping':[], 'degraded':degraded}, sort_keys=True)
print('hash-variantB (no-systemic):', hashlib.sha256(payloadB.encode()).hexdigest()[:16])

now = datetime(2026,8,13,18,39,46,tzinfo=timezone.utc)
prev_notify = datetime(2026,8,11,19,16,18,tzinfo=timezone.utc)
prev_run = datetime(2026,8,12,18,38,0,tzinfo=timezone.utc)
delta_notify = (now-prev_notify).total_seconds()/3600.0
delta_run = (now-prev_run).total_seconds()/3600.0
print(f'hours since last notify: {delta_notify:.3f}')
print(f'hours since last run: {delta_run:.3f}')
print(f'degraded count: {len(degraded)}')
