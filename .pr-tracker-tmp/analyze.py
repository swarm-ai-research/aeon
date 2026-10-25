#!/usr/bin/env python3
import json, sys, subprocess
from datetime import datetime, timezone

TODAY = datetime(2026, 10, 25, tzinfo=timezone.utc)
PREFIXES = ("ai/", "security/", "fix/security/", "aeon/", "fix/", "hook-submission/")

raw = subprocess.run(
    ["gh","api","graphql","-f","query=\n{\n  search(query: \"author:aeonframework is:pr sort:updated-desc\", type: ISSUE, first: 60) {\n    issueCount\n    nodes {\n      ... on PullRequest {\n        number title state headRefName url createdAt updatedAt mergedAt closedAt\n        repository { nameWithOwner }\n        reviews(last: 1) { nodes { state submittedAt } }\n        comments { totalCount }\n        commits(last: 1) { nodes { commit { author { email } } } }\n      }\n    }\n  }\n}\n"],
    capture_output=True, text=True
).stdout

j = json.loads(raw)
data = j["data"]["search"]
issueCount = data["issueCount"]
nodes = data["nodes"]
null_slot = sum(1 for n in nodes if n is None)
nodes = [n for n in nodes if n]
total_nodes = len(nodes)

def parse(ts):
    if not ts: return None
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

def days_ago(dt):
    return (TODAY - dt).days

prefixed = [n for n in nodes if any(n["headRefName"].startswith(p) for p in PREFIXES)]
non_prefixed = [n for n in nodes if not any(n["headRefName"].startswith(p) for p in PREFIXES)]

def bucketize(prs):
    merged7, stale_open, closed7, active_open = [], [], [], []
    merged30, closed30 = [], []
    all_open = []
    for n in prs:
        state = n["state"]
        created = parse(n["createdAt"])
        updated = parse(n["updatedAt"])
        merged = parse(n["mergedAt"])
        closed = parse(n["closedAt"])
        if state == "MERGED" and merged and days_ago(merged) <= 7:
            merged7.append(n)
        if state == "MERGED" and merged and days_ago(merged) <= 30:
            merged30.append(n)
        if state == "OPEN":
            all_open.append(n)
            age = days_ago(created)
            last_act = days_ago(updated)
            if age > 7 and last_act > 7:
                stale_open.append(n)
            else:
                active_open.append(n)
        if state == "CLOSED" and closed and days_ago(closed) <= 7:
            closed7.append(n)
        if state == "CLOSED" and closed and days_ago(closed) <= 30:
            closed30.append(n)
    return {
        "merged7": merged7, "stale_open": stale_open, "closed7": closed7,
        "active_open": active_open, "merged30": merged30, "closed30": closed30,
        "all_open": all_open,
    }

b = bucketize(prefixed)
nb = bucketize(non_prefixed)

print(f"ISSUECOUNT: {issueCount}")
print(f"TOTAL_NODES: {total_nodes}")
print(f"NULL_SLOT: {null_slot}")
print(f"PREFIXED: {len(prefixed)}")
print(f"NON_PREFIXED: {len(non_prefixed)}")
print(f"TUPLE: ({len(b['merged7'])}, {len(b['stale_open'])}, {len(b['closed7'])}, {len(b['active_open'])})")
print()
print(f"MERGED7 ({len(b['merged7'])}):")
for n in b["merged7"]:
    merged = parse(n["mergedAt"])
    created = parse(n["createdAt"])
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} {n['title'][:70]} | branch={n['headRefName']} | opened={created.date()} merged={merged.date()} ({days_ago(merged)}d ago, age={days_ago(created)}d)")
print(f"\nMERGED30 ({len(b['merged30'])}):")
for n in b["merged30"]:
    merged = parse(n["mergedAt"])
    created = parse(n["createdAt"])
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} {n['title'][:70]} | branch={n['headRefName']} | opened={created.date()} merged={merged.date()} ({days_ago(merged)}d ago)")
print(f"\nSTALE_OPEN ({len(b['stale_open'])}):")
for n in b["stale_open"]:
    created = parse(n["createdAt"])
    updated = parse(n["updatedAt"])
    rev = n["reviews"]["nodes"]
    rev_s = f"{rev[0]['state']} {rev[0]['submittedAt'][:10]}" if rev else "no review"
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} {n['title'][:70]} | branch={n['headRefName']} | opened={created.date()} ({days_ago(created)}d) upd={updated.date()} ({days_ago(updated)}d) | {rev_s} | comments={n['comments']['totalCount']}")
print(f"\nACTIVE_OPEN ({len(b['active_open'])}):")
for n in b["active_open"]:
    created = parse(n["createdAt"])
    updated = parse(n["updatedAt"])
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} {n['title'][:70]} | branch={n['headRefName']} | opened={created.date()} ({days_ago(created)}d) upd={updated.date()} ({days_ago(updated)}d)")
print(f"\nCLOSED7 ({len(b['closed7'])}):")
for n in b["closed7"]:
    closed = parse(n["closedAt"])
    created = parse(n["createdAt"])
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} {n['title'][:70]} | branch={n['headRefName']} | opened={created.date()} closed={closed.date()} ({days_ago(closed)}d ago)")
print(f"\nCLOSED30 ({len(b['closed30'])}):")
for n in b["closed30"]:
    closed = parse(n["closedAt"])
    created = parse(n["createdAt"])
    print(f"  {n['repository']['nameWithOwner']}#{n['number']} {n['title'][:70]} | branch={n['headRefName']} | opened={created.date()} closed={closed.date()} ({days_ago(closed)}d ago)")

print(f"\n--- NON-PREFIXED ({len(non_prefixed)}) ---")
for n in non_prefixed:
    state = n["state"]
    created = parse(n["createdAt"])
    merged = parse(n["mergedAt"])
    closed = parse(n["closedAt"])
    extra = ""
    if merged:
        extra = f" merged={merged.date()} ({days_ago(merged)}d ago)"
    elif closed:
        extra = f" closed={closed.date()}"
    print(f"  [{state}] {n['repository']['nameWithOwner']}#{n['number']} branch={n['headRefName']} opened={created.date()}{extra}")

print(f"\nNON-PREFIXED by bucket: merged7={len(nb['merged7'])} merged30={len(nb['merged30'])} stale={len(nb['stale_open'])} active={len(nb['active_open'])} closed7={len(nb['closed7'])} closed30={len(nb['closed30'])}")
