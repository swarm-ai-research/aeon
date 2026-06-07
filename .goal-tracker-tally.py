import json, sys
from collections import Counter
data = json.load(sys.stdin)
print(f'Total PRs in 14d window: {len(data)}')
c = Counter(pr['updatedAt'][:10] for pr in data)
for d in sorted(c.keys()):
    print(f'  {d}: {c[d]}')
print()

def goal_match(title, keys):
    t = title.lower()
    return any(k in t for k in keys)

g1_keys = ['pr-review', 'code-health', 'pr-triage', 'issue-triage', 'security', 'heartbeat', 'vuln', 'skill-health', 'skill-freshness', 'fleet-control', 'github-monitor', 'review pass', 'test pass', 'refactor pass', 'documentation pass']
g2_keys = ['planner', 'self-improve', 'goal-tracker', 'memory-flush', 'memory-structural', 'reflect', 'consolidat']
g3_keys = ['gitlawb', 'compute-futures', 'compute-pulse', 'compute-macro', 'surplus-pulse', 'fleet-runner', 'fleet-state', 'safety']
g4_keys = ['swarm', 'merge-gate']

print('PR matches per goal:')
print('  Goal 1:', sum(1 for pr in data if goal_match(pr['title'], g1_keys)))
print('  Goal 2:', sum(1 for pr in data if goal_match(pr['title'], g2_keys)))
print('  Goal 3:', sum(1 for pr in data if goal_match(pr['title'], g3_keys)))
print('  Goal 4:', sum(1 for pr in data if goal_match(pr['title'], g4_keys)))
