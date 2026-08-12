import json
from datetime import datetime, timezone

TODAY_STR = "2026-08-12"
NOW = datetime(2026, 8, 12, 10, 30, 0, tzinfo=timezone.utc)
PREFIXES = ("ai/", "security/", "fix/security/", "aeon/")

def email_matches(email):
    if not email:
        return False
    e = email.lower()
    if "aeonframework.dev" in e or "aeonframework.github" in e or "aeonframework.com" in e:
        return True
    if "aeonframework@users.noreply.github.com" in e:
        return True
    if "aeonframework@proton.me" in e:
        return True
    if e.endswith("+aeonframework@users.noreply.github.com"):
        return True
    return False

with open(".pr-tracker-raw.json") as f:
    raw = json.load(f)

nodes = raw["data"]["search"]["nodes"]
kept = []
dropped = []
for n in nodes:
    head = n.get("headRefName", "") or ""
    email = ((n.get("commits", {}).get("nodes") or [{}])[0].get("commit", {}).get("author", {}) or {}).get("email", "")
    prefix_ok = any(head.startswith(p) for p in PREFIXES)
    email_ok = email_matches(email)
    if prefix_ok or email_ok:
        kept.append({**n, "_email": email, "_prefix_ok": prefix_ok, "_email_ok": email_ok})
    else:
        dropped.append({"num": n["number"], "repo": n["repository"]["nameWithOwner"], "head": head, "email": email})

print("Total nodes:", len(nodes))
print("Kept:", len(kept))
print("Dropped:", len(dropped))
print()
for d in dropped:
    print("  DROP", d["repo"] + "#" + str(d["num"]), "head=" + d["head"], "email=" + d["email"])

def parse_dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

recent_merges = []
stale_open = []
active_open = []
closed_no_merge = []
open_all = []

for n in kept:
    created = parse_dt(n.get("createdAt"))
    merged = parse_dt(n.get("mergedAt"))
    closed = parse_dt(n.get("closedAt"))
    updated = parse_dt(n.get("updatedAt"))
    state = n.get("state")
    rev = n.get("reviews", {}).get("nodes") or []
    last_rev = parse_dt(rev[0]["submittedAt"]) if rev else None
    comments = n.get("comments", {}).get("totalCount", 0)
    commit_date = parse_dt(((n.get("commits", {}).get("nodes") or [{}])[0].get("commit", {}) or {}).get("committedDate"))
    activities = [x for x in [updated, last_rev, commit_date] if x]
    last_activity = max(activities) if activities else created

    age_days = (NOW - created).days if created else 0
    frozen_days = (NOW - last_activity).days if last_activity else 0

    row = {
        "num": n["number"],
        "title": n["title"],
        "url": n["url"],
        "repo": n["repository"]["nameWithOwner"],
        "archived": n["repository"].get("isArchived", False),
        "state": state,
        "head": n["headRefName"],
        "created": created.strftime("%Y-%m-%d") if created else "",
        "created_iso": n.get("createdAt"),
        "merged": merged.strftime("%Y-%m-%d") if merged else None,
        "closed": closed.strftime("%Y-%m-%d") if closed else None,
        "age_days": age_days,
        "frozen_days": frozen_days,
        "comments": comments,
        "last_review": rev[0]["state"] if rev else None,
        "last_review_at": rev[0]["submittedAt"] if rev else None,
        "email": n.get("_email"),
        "last_activity": last_activity.strftime("%Y-%m-%dT%H:%MZ") if last_activity else None,
        "draft": n.get("isDraft"),
    }

    if state == "OPEN":
        open_all.append(row)
        if age_days > 7 and frozen_days > 7:
            stale_open.append(row)
        else:
            active_open.append(row)
    if state == "MERGED" and merged and (NOW - merged).total_seconds() < 7*86400:
        recent_merges.append(row)
    if state == "CLOSED" and closed and (NOW - closed).total_seconds() < 7*86400 and not merged:
        closed_no_merge.append(row)

def fmt_row(r):
    return r["repo"] + "#" + str(r["num"]) + "  age=" + str(r["age_days"]) + "d  frozen=" + str(r["frozen_days"]) + "d  head=" + r["head"] + "  state=" + r["state"] + "  reviews=" + str(r["last_review"]) + "  comments=" + str(r["comments"]) + "  " + r["title"][:70]

print("\n== OPEN (all) ==")
for r in sorted(open_all, key=lambda x: x["created_iso"] or "", reverse=True):
    print(fmt_row(r))
print("\n== ACTIVE OPEN (" + str(len(active_open)) + ") ==")
for r in sorted(active_open, key=lambda x: x["created_iso"] or "", reverse=True):
    print(fmt_row(r))
print("\n== STALE OPEN (" + str(len(stale_open)) + ") ==")
for r in sorted(stale_open, key=lambda x: x["created_iso"] or "", reverse=True):
    print(fmt_row(r))
print("\n== RECENT MERGES 7d (" + str(len(recent_merges)) + ") ==")
for r in sorted(recent_merges, key=lambda x: x["merged"] or "", reverse=True):
    print(fmt_row(r), "merged=", r["merged"])
print("\n== CLOSED NO-MERGE 7d (" + str(len(closed_no_merge)) + ") ==")
for r in sorted(closed_no_merge, key=lambda x: x["closed"] or "", reverse=True):
    print(fmt_row(r), "closed=", r["closed"])

with open(".pr-tracker-parsed.json", "w") as f:
    json.dump({
        "today": TODAY_STR,
        "now_iso": NOW.isoformat(),
        "total_nodes": len(nodes),
        "kept_count": len(kept),
        "dropped": dropped,
        "open": open_all,
        "active_open": active_open,
        "stale_open": stale_open,
        "recent_merges": recent_merges,
        "closed_no_merge": closed_no_merge,
    }, f, indent=2)
print("\nWrote .pr-tracker-parsed.json")
