#!/usr/bin/env python3
"""Inspect specific PRs to reconcile letter-of-SKILL vs substantive activity."""
import json
from pathlib import Path
from datetime import datetime, timezone

NOW = datetime(2026, 8, 13, 11, 0, 0, tzinfo=timezone.utc)

data = json.loads((Path(__file__).parent / "graphql.json").read_text())
nodes = data["data"]["search"]["nodes"]

def days(dt):
    if not dt: return None
    return (NOW - datetime.fromisoformat(dt.replace("Z", "+00:00"))).total_seconds() / 86400

for target in [(2732, "Baileys"), (78346, "posthog"), (871, "router"),
               (1409, "RuView"), (2248, "buzz"), (958, "voicebox"),
               (216, "wigolo"), (6929, "nango"), (2, "aeon-programmable-hooks")]:
    num, repo_hint = target
    for pr in nodes:
        if pr["number"] == num and repo_hint.lower() in pr["repository"]["nameWithOwner"].lower():
            print(f"\n{pr['repository']['nameWithOwner']}#{pr['number']} state={pr['state']}")
            print(f"  createdAt={pr['createdAt']} updatedAt={pr['updatedAt']}")
            print(f"  age={days(pr['createdAt']):.2f}d  since_update={days(pr['updatedAt']):.2f}d")
            revs = (pr.get("reviews") or {}).get("nodes") or []
            for r in revs:
                print(f"  review: {r.get('state')} at {r.get('submittedAt')} by {(r.get('author') or {}).get('login')}")
            comments = pr.get("comments") or {}
            print(f"  commentsTotal={comments.get('totalCount')}")
            for c in comments.get("nodes") or []:
                body = (c.get("bodyText") or "")[:80].replace("\n", " ")
                print(f"  comment: {c.get('createdAt')} by {(c.get('author') or {}).get('login')} :: {body}")
