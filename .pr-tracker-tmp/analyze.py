#!/usr/bin/env python3
"""Categorize PRs, compute dedup hash, decide notify, format outputs."""
import json, hashlib, pathlib, datetime as dt

TODAY = dt.datetime(2026, 7, 26, 10, 0, 0, tzinfo=dt.timezone.utc)  # 10:00Z skill slot
CUTOFF_7D = TODAY - dt.timedelta(days=7)

prs = json.loads(pathlib.Path(".pr-tracker-tmp/prs.json").read_text())

def parse(ts):
    if not ts:
        return None
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))

def latest_activity(pr):
    """Max of updatedAt, latest review submittedAt."""
    times = []
    for k in ("updatedAt", "createdAt"):
        t = parse(pr.get(k))
        if t: times.append(t)
    for rv in (pr.get("reviews", {}).get("nodes") or []):
        t = parse(rv.get("submittedAt"))
        if t: times.append(t)
    return max(times) if times else None

def age_days(ts):
    if not ts: return None
    return (TODAY - ts).total_seconds() / 86400.0

recent_merges = []  # state==MERGED and mergedAt within 7d
stale_open    = []  # OPEN, createdAt > 7d ago, no activity within 7d
active_open   = []  # OPEN, createdAt within 7d OR recent activity
closed_no_merge = []  # CLOSED (not merged), closedAt within 7d

for p in prs:
    state = p["state"]
    created = parse(p["createdAt"])
    merged  = parse(p.get("mergedAt"))
    closed  = parse(p.get("closedAt"))
    act     = latest_activity(p)

    if state == "MERGED":
        if merged and merged >= CUTOFF_7D:
            recent_merges.append(p)
    elif state == "OPEN":
        recent_activity = act and act >= CUTOFF_7D
        if (created and created >= CUTOFF_7D) or recent_activity:
            active_open.append(p)
        else:
            stale_open.append(p)
    elif state == "CLOSED":
        if closed and closed >= CUTOFF_7D:
            closed_no_merge.append(p)

def label(p):
    r = p["repository"]["nameWithOwner"]
    n = p["number"]
    t = p["title"]
    return f"{r} #{n} — {t}"

# Sort each bucket by createdAt desc
def sort_by_created(lst):
    return sorted(lst, key=lambda p: p["createdAt"], reverse=True)

recent_merges   = sort_by_created(recent_merges)
stale_open      = sort_by_created(stale_open)
active_open     = sort_by_created(active_open)
closed_no_merge = sort_by_created(closed_no_merge)

# Canonical hash: `repo#num:state:updatedAt|…` sorted by (repo, number)
def hash_recipe():
    items = []
    for p in prs:
        r = p["repository"]["nameWithOwner"]
        n = p["number"]
        items.append((r, n, p["state"], p.get("updatedAt", "")))
    items.sort(key=lambda x: (x[0], x[1]))
    lines = [f"{r}#{n}:{s}:{u}" for r,n,s,u in items]
    return hashlib.sha256("|".join(lines).encode()).hexdigest()[:16]

canonical_hash = hash_recipe()

# Fresh-bot-PR trigger — any PR filed within last 24h?
fresh_prs = []
for p in prs:
    created = parse(p["createdAt"])
    if created and (TODAY - created).total_seconds() < 86400:
        fresh_prs.append(p)

# SKILL step-5 content trigger: send if NOT (0 merges AND 0 stale AND 0 closed-no-merge)
skill_trigger = not (len(recent_merges) == 0 and len(stale_open) == 0 and len(closed_no_merge) == 0)

# Prior hash from pr-status.md — parse it
prior_hash = ""
try:
    prior = pathlib.Path("memory/topics/pr-status.md").read_text()
    for line in prior.splitlines():
        if "canonical hash" in line.lower() or "today's canonical hash" in line.lower():
            # look for `hash: 0d4e2c374767939b` style
            import re
            m = re.search(r"`([0-9a-f]{16})`", line)
            if m:
                prior_hash = m.group(1)
                break
except FileNotFoundError:
    pass

hash_diff = (canonical_hash != prior_hash)

# Compose result
result = {
    "today": TODAY.date().isoformat(),
    "canonical_hash": canonical_hash,
    "prior_hash": prior_hash,
    "hash_diff": hash_diff,
    "counts": {
        "recent_merges_7d": len(recent_merges),
        "stale_open_gt7d": len(stale_open),
        "active_open": len(active_open),
        "closed_no_merge_7d": len(closed_no_merge),
    },
    "fresh_bot_prs_lt24h": [{"repo": p["repository"]["nameWithOwner"], "num": p["number"], "title": p["title"]} for p in fresh_prs],
    "skill_content_trigger": skill_trigger,
    "recent_merges":   [{"repo": p["repository"]["nameWithOwner"], "num": p["number"], "title": p["title"], "createdAt": p["createdAt"], "mergedAt": p.get("mergedAt")} for p in recent_merges],
    "stale_open":      [{"repo": p["repository"]["nameWithOwner"], "num": p["number"], "title": p["title"], "createdAt": p["createdAt"], "age_days": round(age_days(parse(p["createdAt"])), 2), "activity_days": round(age_days(latest_activity(p)), 2) if latest_activity(p) else None} for p in stale_open],
    "active_open":     [{"repo": p["repository"]["nameWithOwner"], "num": p["number"], "title": p["title"], "createdAt": p["createdAt"], "age_days": round(age_days(parse(p["createdAt"])), 2)} for p in active_open],
    "closed_no_merge": [{"repo": p["repository"]["nameWithOwner"], "num": p["number"], "title": p["title"], "closedAt": p.get("closedAt")} for p in closed_no_merge],
}

# Decide notify per SKILL step 5: skip only if all three counts are zero. Also check fresh + hash triggers.
notify_reasons = []
if result["counts"]["recent_merges_7d"] > 0: notify_reasons.append(f"{result['counts']['recent_merges_7d']} recent_merges_7d")
if result["counts"]["stale_open_gt7d"] > 0: notify_reasons.append(f"{result['counts']['stale_open_gt7d']} stale_open")
if result["counts"]["closed_no_merge_7d"] > 0: notify_reasons.append(f"{result['counts']['closed_no_merge_7d']} closed_no_merge_7d")
if fresh_prs: notify_reasons.append(f"{len(fresh_prs)} fresh_bot_pr_lt24h")
if hash_diff: notify_reasons.append(f"hash_diff({prior_hash or 'none'}->{canonical_hash})")

# Dedup guard: if hashes match, skip notify unless a genuinely novel content trigger (fresh <24h) fires.
if not hash_diff and not fresh_prs:
    # No state change AND no fresh PR → dedup suppresses even if skill_trigger says send.
    notify_decision = "skip"
    notify_reason = f"dedup: hash unchanged ({canonical_hash}) and no fresh <24h PRs"
else:
    if skill_trigger or fresh_prs or hash_diff:
        notify_decision = "send"
        notify_reason = "; ".join(notify_reasons)
    else:
        notify_decision = "skip"
        notify_reason = "0 merges + 0 stale + 0 closed_no_merge"

result["notify_decision"] = notify_decision
result["notify_reason"]   = notify_reason

pathlib.Path(".pr-tracker-tmp/analysis.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
