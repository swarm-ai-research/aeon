import json, datetime, pathlib
from collections import Counter

data = json.loads(pathlib.Path('.pr-tracker-tmp/raw.json').read_text())
nodes = data['data']['search']['nodes']

NOW = datetime.datetime(2026, 7, 18, 10, 0, 0, tzinfo=datetime.timezone.utc)
BOT_EMAILS = {'aeonframework@users.noreply.github.com', 'aeon@aeonframework.dev'}
BRANCH_PREFIXES = ('ai/', 'security/')

def parse(ts):
    if not ts:
        return None
    return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))

filtered = []
for n in nodes:
    email = ((n.get('commits') or {}).get('nodes') or [{}])[0].get('commit', {}).get('author', {}).get('email', '')
    head = n.get('headRefName', '')
    keep = head.startswith(BRANCH_PREFIXES) or (email in BOT_EMAILS)
    if not keep:
        continue
    n['_email'] = email
    filtered.append(n)

print(f"kept {len(filtered)} of {len(nodes)}")
print()

rows = []
for n in filtered:
    created = parse(n['createdAt'])
    updated = parse(n['updatedAt'])
    merged = parse(n.get('mergedAt'))
    closed = parse(n.get('closedAt'))
    age = (NOW - created).total_seconds() / 86400
    activity_age = (NOW - updated).total_seconds() / 86400 if updated else None
    merged_age = (NOW - merged).total_seconds() / 86400 if merged else None
    closed_age = (NOW - closed).total_seconds() / 86400 if closed else None

    if n['state'] == 'MERGED' and merged_age is not None and merged_age <= 7:
        cat = 'recent_merge'
    elif n['state'] == 'OPEN' and age > 7 and activity_age > 7:
        cat = 'stale'
    elif n['state'] == 'OPEN':
        cat = 'active'
    elif n['state'] == 'CLOSED' and closed_age is not None and closed_age <= 7:
        cat = 'closed_no_merge'
    else:
        cat = 'archived'

    print(f"{n['repository']['nameWithOwner']}#{n['number']} state={n['state']} head={n['headRefName']}")
    print(f"  created={n['createdAt']} ({age:.2f}d ago)")
    print(f"  updated={n['updatedAt']} ({activity_age:.2f}d ago)")
    print(f"  merged={n.get('mergedAt')}  closed={n.get('closedAt')}")
    print(f"  email={n['_email']}  category={cat}  comments={n['comments']['totalCount']}")
    print()
    rows.append({'n': n, 'cat': cat, 'age': age, 'activity_age': activity_age,
                 'merged_age': merged_age, 'closed_age': closed_age})

pathlib.Path('.pr-tracker-tmp/rows.json').write_text(json.dumps(
    [{'repo': r['n']['repository']['nameWithOwner'],
      'number': r['n']['number'],
      'title': r['n']['title'],
      'state': r['n']['state'],
      'url': r['n']['url'],
      'headRefName': r['n']['headRefName'],
      'createdAt': r['n']['createdAt'],
      'updatedAt': r['n']['updatedAt'],
      'mergedAt': r['n'].get('mergedAt'),
      'closedAt': r['n'].get('closedAt'),
      'email': r['n']['_email'],
      'comments': r['n']['comments']['totalCount'],
      'category': r['cat'],
      'age_days': r['age'],
      'activity_age_days': r['activity_age'],
      'merged_age_days': r['merged_age'],
      'closed_age_days': r['closed_age']}
     for r in rows], indent=2))

counts = Counter(r['cat'] for r in rows)
print("Category counts:", dict(counts))
