import json
with open('memory/cron-state.json') as f:
    d = json.load(f)
skills = d if isinstance(d, dict) else {}
n_broken = sum(1 for k,v in skills.items() if isinstance(v,dict) and v.get('consecutive_failures',0) >= 2)
n_hard = sum(1 for k,v in skills.items() if isinstance(v,dict) and v.get('consecutive_failures',0) >= 3)
n_dispatched = sum(1 for k,v in skills.items() if isinstance(v,dict) and v.get('last_status')=='dispatched')
n_degraded = sum(1 for k,v in skills.items() if isinstance(v,dict) and v.get('success_rate',1) < 0.5)
total = sum(1 for k,v in skills.items() if isinstance(v,dict))
print(f'broken(cf>=2): {n_broken}')
print(f'hard(cf>=3): {n_hard}')
print(f'dispatched: {n_dispatched}')
print(f'degraded(sr<0.5): {n_degraded}')
print(f'total tracked: {total}')
