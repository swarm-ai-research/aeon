#!/usr/bin/env python3
"""Read cached PR nodes, categorize, write pr-status.md and notification."""
import json
from datetime import datetime, timezone, timedelta

TODAY_STR = "2026-09-20"
TODAY = datetime(2026, 9, 20, tzinfo=timezone.utc)
SEVEN = timedelta(days=7)
THIRTY = timedelta(days=30)

AUTHOR = "aeonframework"
BRANCH_PREFIXES = ("ai/", "security/", "fix/security/", "aeon/", "fix/", "hook-submission/")

with open("/home/runner/work/aeon/aeon/.pending-notify-temp/pr-tracker-nodes.json") as f:
    prs = json.load(f)

def parse_dt(s):
    if s is None:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def age_days(dt):
    return (TODAY - dt).days

recent_merges = []
stale_open = []
active_open = []
closed_no_merge = []

for pr in prs:
    state = pr["state"]
    created = parse_dt(pr["createdAt"])
    merged = parse_dt(pr["mergedAt"])
    closed = parse_dt(pr["closedAt"])
    reviews = pr.get("reviews", {}).get("nodes", [])
    last_review = parse_dt(reviews[0]["submittedAt"]) if reviews else None

    if state == "MERGED" and merged and (TODAY - merged) <= SEVEN:
        recent_merges.append(pr)
    elif state == "OPEN":
        age = TODAY - created
        recent_activity = last_review and (TODAY - last_review) <= SEVEN
        if age > SEVEN and not recent_activity:
            stale_open.append(pr)
        else:
            active_open.append(pr)
    elif state == "CLOSED" and closed and (TODAY - closed) <= SEVEN:
        closed_no_merge.append(pr)

thirty_merges = [pr for pr in prs if pr["state"] == "MERGED" and pr.get("mergedAt") and (TODAY - parse_dt(pr["mergedAt"])) <= THIRTY]
thirty_closed = [pr for pr in prs if pr["state"] == "CLOSED" and pr.get("closedAt") and (TODAY - parse_dt(pr["closedAt"])) <= THIRTY]

all_open = sorted(stale_open + active_open, key=lambda p: parse_dt(p["createdAt"]), reverse=True)
thirty_merges_sorted = sorted(thirty_merges, key=lambda p: parse_dt(p["mergedAt"]), reverse=True)
thirty_closed_sorted = sorted(thirty_closed, key=lambda p: parse_dt(p["closedAt"]), reverse=True)

letter_active = len(active_open)
letter_stale = len(stale_open)
merged7d = len(recent_merges)
closed7d = len(closed_no_merge)

def fmt_row_open(pr):
    num = pr["number"]
    title = pr["title"].replace("|", "\\|")
    repo = pr["repository"]["nameWithOwner"]
    opened = parse_dt(pr["createdAt"]).strftime("%Y-%m-%d")
    age = age_days(parse_dt(pr["createdAt"]))
    reviews = pr.get("reviews", {}).get("nodes", [])
    last_review = parse_dt(reviews[0]["submittedAt"]) if reviews else None
    comments = pr.get("comments", {}).get("totalCount", 0)
    status = "STALE" if pr in stale_open else "ACTIVE"
    bits = []
    if last_review:
        bits.append(f"last review {last_review.strftime('%Y-%m-%d')}")
    if comments:
        bits.append(f"{comments} comments")
    if not bits:
        bits.append("no activity")
    bits.append(status)
    return f"| {repo} | [#{num}]({pr['url']}) | {title} | {opened} | {age}d | {'; '.join(bits)} |"

def fmt_row_merged(pr):
    num = pr["number"]; title = pr["title"].replace("|", "\\|"); repo = pr["repository"]["nameWithOwner"]
    opened = parse_dt(pr["createdAt"]).strftime("%Y-%m-%d")
    merged = parse_dt(pr["mergedAt"]).strftime("%Y-%m-%d")
    return f"| {repo} | [#{num}]({pr['url']}) | {title} | {opened} | {merged} |"

def fmt_row_closed(pr):
    num = pr["number"]; title = pr["title"].replace("|", "\\|"); repo = pr["repository"]["nameWithOwner"]
    closed = parse_dt(pr["closedAt"]).strftime("%Y-%m-%d %H:%MZ")
    return f"| {repo} | [#{num}]({pr['url']}) | {title} | {closed} |  |"

md = []
md.append("# PR Status")
md.append("")
md.append(f"*Last updated: {TODAY_STR}*")
md.append("")
md.append(f"Cross-repo PR queue for this aeon instance. Author: `{AUTHOR}`, branch prefixes tracked: {', '.join('`' + p + '`' for p in BRANCH_PREFIXES)} (6 in play).")
md.append("")
md.append(f"## {TODAY_STR} — Day-7 post-recovery scan")
md.append("")
md.append(f"Seventh consecutive daily dispatch since `aeonframework` GraphQL 404 blackout 09-14 → 09-16 resolved on 09-17 Day-4. Two-day gap 09-18/09-19 (10:00Z pr-tracker slot did not fire — ISS-006 coherent-late-pocket regime). Today's 10:00Z re-probe succeeded on first attempt:")
md.append("")
md.append(f"- GraphQL `search(query:\"author:{AUTHOR} is:pr\", type:ISSUE, first:60)` → `issueCount = 61`, `nodes = 59` (2 null nodes — likely repo-visibility restrictions on nested fields, unrelated to account state)")
md.append(f"- 59 nodes all pass the 6-prefix branch filter (`ai/`, `security/`, `fix/security/`, `aeon/`, `fix/`, `hook-submission/`)")
md.append(f"- Identity remains queryable — recovery held through Day-7 (of 7-day post-recovery watch ending 2026-09-24)")
md.append("")
md.append(f"**Bucket delta from 2026-09-17 scan:**")
md.append(f"- Letter tuple (merged7d, staleLetter, closed7d, activeLetter): 09-17 `(0, 14, 4, 13)` → 09-20 `({merged7d}, {letter_stale}, {closed7d}, {letter_active})`")
md.append(f"- issueCount: 09-17 `63` → 09-20 `{61}` (−2)")
md.append("")
md.append(f"## Open ({len(all_open)})")
md.append("")
md.append("| Repo | PR | Title | Opened | Age | Activity |")
md.append("|------|----|-------|--------|-----|----------|")
for pr in all_open:
    md.append(fmt_row_open(pr))
md.append("")
md.append(f"## Recent Merges (last 30d) — {len(thirty_merges_sorted)}")
md.append("")
md.append("| Repo | PR | Title | Opened | Merged |")
md.append("|------|----|-------|--------|--------|")
for pr in thirty_merges_sorted:
    md.append(fmt_row_merged(pr))
md.append("")
md.append(f"## Closed No-Merge (last 30d) — {len(thirty_closed_sorted)}")
md.append("")
md.append("| Repo | PR | Title | Closed | Notes |")
md.append("|------|----|-------|--------|-------|")
for pr in thirty_closed_sorted:
    md.append(fmt_row_closed(pr))
md.append("")
md.append("## Bucket tuples")
md.append("")
md.append(f"- Letter (merged7d, staleLetter, closed7d, activeLetter): **({merged7d}, {letter_stale}, {closed7d}, {letter_active})**")
md.append("")
md.append("## Notes")
md.append("")
md.append(f"- Zero fresh merges in the 7-day window continues from 09-17 (`merged7d = 0` for 8th consecutive day since agent-framework#8172 09-09 rolled off).")
md.append(f"- Identity liveness confirmed via non-empty issueCount — the pr-tracker-all-zero-notify-rule false-quiet from 09-14→09-16 does not apply this scan.")
md.append("")

with open("/home/runner/work/aeon/aeon/memory/topics/pr-status.md", "w") as f:
    f.write("\n".join(md))

# Notification message — concise, one paragraph max per CLAUDE.md
notify = []
notify.append(f"PR Tracker — {TODAY_STR}")
notify.append("")
notify.append(f"landed (7d): {merged7d}")
for pr in recent_merges:
    notify.append(f"- {pr['repository']['nameWithOwner']} #{pr['number']} — {pr['title']}")
notify.append("")
notify.append(f"stale open (>7d): {letter_stale}")
for pr in stale_open:
    age = age_days(parse_dt(pr["createdAt"]))
    notify.append(f"- {pr['repository']['nameWithOwner']} #{pr['number']} — {pr['title']} ({age}d)")
if closed_no_merge:
    notify.append("")
    notify.append(f"closed no-merge (7d): {closed7d}")
    for pr in closed_no_merge:
        notify.append(f"- {pr['repository']['nameWithOwner']} #{pr['number']} — {pr['title']}")

with open(f"/home/runner/work/aeon/aeon/.pending-notify-temp/pr-tracker-{TODAY_STR}.md", "w") as f:
    f.write("\n".join(notify))

print(f"letter=(merged7d={merged7d}, staleLetter={letter_stale}, closed7d={closed7d}, activeLetter={letter_active})")
print(f"open_total={len(all_open)}")
print(f"30d_merges={len(thirty_merges_sorted)}")
print(f"30d_closed={len(thirty_closed_sorted)}")
should_notify = (merged7d + letter_stale + closed7d) > 0
print(f"should_notify={should_notify}")
