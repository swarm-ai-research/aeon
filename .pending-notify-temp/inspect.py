import json
from datetime import datetime, timezone, timedelta
TODAY = datetime(2026,9,20,tzinfo=timezone.utc)
SEVEN = timedelta(days=7)
def dt(s):
    return datetime.fromisoformat(s.replace('Z','+00:00')) if s else None

with open('/home/runner/work/aeon/aeon/.pending-notify-temp/pr-tracker-nodes.json') as f:
    prs = json.load(f)

closed = [p for p in prs if p['state']=='CLOSED' and dt(p['closedAt']) and (TODAY-dt(p['closedAt']))<=SEVEN]
closed.sort(key=lambda p: dt(p['closedAt']), reverse=True)
print('=== closed in 7d (n=%d) ===' % len(closed))
for p in closed:
    print(f'{dt(p["closedAt"]).strftime("%Y-%m-%d %H:%MZ")}  {p["repository"]["nameWithOwner"]}#{p["number"]}  {p["headRefName"]}  {p["title"][:60]}')

print()
stale=[]
active=[]
for p in prs:
    if p['state']!='OPEN': continue
    created = dt(p['createdAt'])
    reviews = p.get('reviews',{}).get('nodes',[])
    lr = dt(reviews[0]['submittedAt']) if reviews else None
    recent_activity = lr and (TODAY-lr)<=SEVEN
    if (TODAY-created)>SEVEN and not recent_activity:
        stale.append(p)
    else:
        active.append(p)
print('=== stale (n=%d) ===' % len(stale))
for p in stale:
    print(f'created={dt(p["createdAt"]).strftime("%Y-%m-%d")}  {p["repository"]["nameWithOwner"]}#{p["number"]}  {p["title"][:60]}')
print()
print('=== active (n=%d) ===' % len(active))
for p in active:
    print(f'created={dt(p["createdAt"]).strftime("%Y-%m-%d")}  {p["repository"]["nameWithOwner"]}#{p["number"]}  {p["title"][:60]}')

print()
merged = [p for p in prs if p['state']=='MERGED' and dt(p['mergedAt']) and (TODAY-dt(p['mergedAt']))<=timedelta(days=30)]
merged.sort(key=lambda p: dt(p['mergedAt']), reverse=True)
print('=== 30d merges (n=%d) ===' % len(merged))
for p in merged:
    print(f'{dt(p["mergedAt"]).strftime("%Y-%m-%d")}  {p["repository"]["nameWithOwner"]}#{p["number"]}  {p["title"][:60]}')
