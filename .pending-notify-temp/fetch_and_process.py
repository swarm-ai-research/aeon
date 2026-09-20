#!/usr/bin/env python3
"""Fetch aeonframework PRs, filter by branch prefix, categorize, write outputs."""
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta

TODAY_STR = "2026-09-20"
TODAY = datetime(2026, 9, 20, tzinfo=timezone.utc)
SEVEN_DAYS = timedelta(days=7)
THIRTY_DAYS = timedelta(days=30)

AUTHOR = "aeonframework"
BRANCH_PREFIXES = ("ai/", "security/", "fix/security/", "aeon/", "fix/", "hook-submission/")

QUERY = '''
{
  search(query: "author:%s is:pr sort:updated-desc", type: ISSUE, first: 60) {
    issueCount
    nodes {
      ... on PullRequest {
        number
        title
        state
        headRefName
        url
        createdAt
        mergedAt
        closedAt
        repository { nameWithOwner }
        reviews(last: 1) { nodes { state submittedAt } }
        comments { totalCount }
        commits(last: 1) { nodes { commit { author { email } } } }
      }
    }
  }
}
''' % AUTHOR

def fetch():
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", "query=" + QUERY],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)

def parse_dt(s):
    if s is None:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def age_days(dt):
    return (TODAY - dt).days

def main():
    data = fetch()
    search = data["data"]["search"]
    issue_count = search["issueCount"]
    nodes = [n for n in search["nodes"] if n]

    prs = [n for n in nodes if any(n["headRefName"].startswith(p) for p in BRANCH_PREFIXES)]

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

        if state == "MERGED" and merged and (TODAY - merged) <= SEVEN_DAYS:
            recent_merges.append(pr)
        elif state == "OPEN":
            age = TODAY - created
            recent_activity = last_review and (TODAY - last_review) <= SEVEN_DAYS
            if age > SEVEN_DAYS and not recent_activity:
                stale_open.append(pr)
            else:
                active_open.append(pr)
        elif state == "CLOSED" and closed and (TODAY - closed) <= SEVEN_DAYS:
            closed_no_merge.append(pr)

    thirty_merges = [pr for pr in prs if pr["state"] == "MERGED" and pr.get("mergedAt") and (TODAY - parse_dt(pr["mergedAt"])) <= THIRTY_DAYS]
    thirty_closed = [pr for pr in prs if pr["state"] == "CLOSED" and pr.get("closedAt") and (TODAY - parse_dt(pr["closedAt"])) <= THIRTY_DAYS]

    def sort_key_open(pr):
        return parse_dt(pr["createdAt"])
    def sort_key_merged(pr):
        return parse_dt(pr["mergedAt"])
    def sort_key_closed(pr):
        return parse_dt(pr["closedAt"])

    all_open = sorted(stale_open + active_open, key=sort_key_open, reverse=True)
    thirty_merges_sorted = sorted(thirty_merges, key=sort_key_merged, reverse=True)
    thirty_closed_sorted = sorted(thirty_closed, key=sort_key_closed, reverse=True)

    # Bucket tuples
    letter_active = len(active_open)
    letter_stale = len(stale_open)
    merged7d = len(recent_merges)
    closed7d = len(closed_no_merge)

    output = {
        "today": TODAY_STR,
        "issue_count": issue_count,
        "nodes_returned": len(nodes),
        "prs_after_prefix_filter": len(prs),
        "recent_merges": recent_merges,
        "stale_open": stale_open,
        "active_open": active_open,
        "closed_no_merge": closed_no_merge,
        "all_open_sorted": all_open,
        "thirty_merges_sorted": thirty_merges_sorted,
        "thirty_closed_sorted": thirty_closed_sorted,
        "letter": {"merged7d": merged7d, "staleLetter": letter_stale, "closed7d": closed7d, "activeLetter": letter_active},
    }

    with open("/home/runner/work/aeon/aeon/.pending-notify-temp/pr-tracker-processed.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    def fmt_row_open(pr):
        num = pr["number"]
        title = pr["title"].replace("|", "\\|")
        repo = pr["repository"]["nameWithOwner"]
        opened = parse_dt(pr["createdAt"]).strftime("%Y-%m-%d")
        age = age_days(parse_dt(pr["createdAt"]))
        reviews = pr.get("reviews", {}).get("nodes", [])
        last_review = parse_dt(reviews[0]["submittedAt"]) if reviews else None
        comments = pr.get("comments", {}).get("totalCount", 0)
        if pr in stale_open:
            status = "STALE"
        else:
            status = "ACTIVE"
        activity_bits = []
        if last_review:
            activity_bits.append(f"review {last_review.strftime('%Y-%m-%d')}")
        if comments:
            activity_bits.append(f"{comments} comments")
        activity_bits.append(status)
        activity = "; ".join(activity_bits)
        return f"| {repo} | [#{num}]({pr['url']}) | {title} | {opened} | {age}d | {activity} |"

    def fmt_row_merged(pr):
        num = pr["number"]
        title = pr["title"].replace("|", "\\|")
        repo = pr["repository"]["nameWithOwner"]
        opened = parse_dt(pr["createdAt"]).strftime("%Y-%m-%d")
        merged = parse_dt(pr["mergedAt"]).strftime("%Y-%m-%d")
        return f"| {repo} | [#{num}]({pr['url']}) | {title} | {opened} | {merged} |"

    def fmt_row_closed(pr):
        num = pr["number"]
        title = pr["title"].replace("|", "\\|")
        repo = pr["repository"]["nameWithOwner"]
        closed = parse_dt(pr["closedAt"]).strftime("%Y-%m-%d %H:%MZ")
        return f"| {repo} | [#{num}]({pr['url']}) | {title} | {closed} |  |"

    # Build pr-status.md
    md_lines = []
    md_lines.append("# PR Status")
    md_lines.append("")
    md_lines.append(f"*Last updated: {TODAY_STR}*")
    md_lines.append("")
    md_lines.append(f"Cross-repo PR queue for this aeon instance. Author: `{AUTHOR}`, branch prefixes tracked: {', '.join('`' + p + '`' for p in BRANCH_PREFIXES)} (6 in play).")
    md_lines.append("")
    md_lines.append(f"GraphQL `search(query:\"author:{AUTHOR} is:pr\", type:ISSUE)` → `issueCount={issue_count}`, nodes={len(nodes)}; {len(prs)} after prefix filter.")
    md_lines.append("")
    md_lines.append(f"## Open ({len(all_open)})")
    md_lines.append("")
    md_lines.append("| Repo | PR | Title | Opened | Age | Activity |")
    md_lines.append("|------|----|-------|--------|-----|----------|")
    for pr in all_open:
        md_lines.append(fmt_row_open(pr))
    md_lines.append("")
    md_lines.append(f"## Recent Merges (last 30d) — {len(thirty_merges_sorted)}")
    md_lines.append("")
    md_lines.append("| Repo | PR | Title | Opened | Merged |")
    md_lines.append("|------|----|-------|--------|--------|")
    for pr in thirty_merges_sorted:
        md_lines.append(fmt_row_merged(pr))
    md_lines.append("")
    md_lines.append(f"## Closed No-Merge (last 30d) — {len(thirty_closed_sorted)}")
    md_lines.append("")
    md_lines.append("| Repo | PR | Title | Closed | Notes |")
    md_lines.append("|------|----|-------|--------|-------|")
    for pr in thirty_closed_sorted:
        md_lines.append(fmt_row_closed(pr))
    md_lines.append("")
    md_lines.append("## Bucket tuples")
    md_lines.append("")
    md_lines.append(f"- Letter (merged7d, staleLetter, closed7d, activeLetter): **({merged7d}, {letter_stale}, {closed7d}, {letter_active})**")
    md_lines.append("")

    with open("/home/runner/work/aeon/aeon/memory/topics/pr-status.md", "w") as f:
        f.write("\n".join(md_lines))

    # Notification message
    notify_lines = []
    notify_lines.append(f"PR Tracker — {TODAY_STR}")
    notify_lines.append("")
    notify_lines.append(f"landed (7d): {merged7d}")
    for pr in recent_merges:
        notify_lines.append(f"- {pr['repository']['nameWithOwner']} #{pr['number']} — {pr['title']}")
    notify_lines.append("")
    notify_lines.append(f"stale open (>7d): {letter_stale}")
    for pr in stale_open:
        age = age_days(parse_dt(pr["createdAt"]))
        notify_lines.append(f"- {pr['repository']['nameWithOwner']} #{pr['number']} — {pr['title']} ({age}d)")
    if closed_no_merge:
        notify_lines.append("")
        notify_lines.append(f"closed no-merge (7d): {closed7d}")
        for pr in closed_no_merge:
            notify_lines.append(f"- {pr['repository']['nameWithOwner']} #{pr['number']} — {pr['title']}")

    with open(f"/home/runner/work/aeon/aeon/.pending-notify-temp/pr-tracker-{TODAY_STR}.md", "w") as f:
        f.write("\n".join(notify_lines))

    # Summary print
    print(f"issueCount={issue_count}")
    print(f"nodes_returned={len(nodes)}")
    print(f"prs_after_prefix_filter={len(prs)}")
    print(f"letter=(merged7d={merged7d}, staleLetter={letter_stale}, closed7d={closed7d}, activeLetter={letter_active})")
    print(f"should_notify={'yes' if (merged7d + letter_stale + closed7d) > 0 else 'no'}")

if __name__ == "__main__":
    main()
