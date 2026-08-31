from datetime import datetime, timezone

NOW = datetime(2026, 8, 31, 10, 0, 0, tzinfo=timezone.utc)

cron = {
    "planner": "2026-08-29T07:57:37Z",
    "batch-health": "2026-08-26T08:26:01Z",
    "memory-flush": "2026-08-26T06:44:07Z",
    "memory-structural-dedupe": "2026-08-26T06:43:12Z",
    "janitor": "2026-08-30T05:52:37Z",
    "stale-content-pr-sweeper": "2026-08-30T23:57:15Z",
    "issue-triage": "2026-08-26T09:12:23Z",
    "pr-triage": "2026-08-26T09:59:42Z",
    "pr-review": "2026-08-30T18:47:27Z",
    "pr-tracker": "2026-08-30T11:18:47Z",
    "github-monitor": "2026-08-26T09:12:34Z",
    "repo-revive": "2026-08-22T10:32:55Z",
    "code-health": "2026-08-29T17:24:48Z",
    "surplus-pulse": "2026-08-29T17:25:45Z",
    "compute-pulse": "2026-08-22T11:32:23Z",
    "compute-macro-correlate": "2026-08-23T07:05:36Z",
    "compute-futures-eda": "2026-08-29T08:00:28Z",
    "changelog": "2026-08-24T16:35:45Z",
    "vuln-scanner": "2026-08-29T17:35:36Z",
    "goal-tracker": "2026-08-30T18:44:33Z",
    "agi-tracker": "2026-08-24T13:38:04Z",
    "milestone-tracker": "2026-08-24T12:45:51Z",
    "skill-health": "2026-08-30T18:45:36Z",
    "config-validator": "2026-08-23T07:02:50Z",
    "skill-analytics": "2026-08-26T19:05:10Z",
    "reflect": "2026-08-30T18:53:12Z",
    "self-review": "2026-08-30T18:48:35Z",
    "skill-repair": "2026-06-20T06:21:00Z",
    "cost-report": "2026-08-24T08:30:52Z",
    "skill-evals": "2026-08-23T09:31:45Z",
    "swarm-safety-eval": "2026-08-23T07:42:10Z",
    "skill-update-check": "2026-08-23T19:04:17Z",
    "fleet-control": "2026-08-26T09:12:16Z",
    "gitlawb-fleet-metrics": "2026-08-26T08:25:02Z",
    "weekly-shiplog": "2026-08-24T09:14:36Z",
    "workflow-security-audit": "2026-08-23T16:35:21Z",
    "skill-graph": "2026-08-30T18:52:15Z",
    "notegraph": "2026-08-30T05:53:47Z",
    "skillpacks": "2026-08-23T06:06:05Z",
    "suggest-edges": "2026-08-30T05:52:43Z",
    "skill-freshness": "2026-08-26T08:32:35Z",
    "heartbeat": "2026-08-26T08:27:27Z",
}

schedules = {
    "planner": "daily", "batch-health": "daily", "memory-flush": "daily",
    "memory-structural-dedupe": "daily", "janitor": "weekly",
    "stale-content-pr-sweeper": "daily", "issue-triage": "daily",
    "pr-triage": "daily", "pr-review": "daily", "pr-tracker": "daily",
    "github-monitor": "daily", "repo-revive": "weekly",
    "code-health": "daily", "surplus-pulse": "daily",
    "compute-pulse": "weekly", "compute-macro-correlate": "weekly",
    "compute-futures-eda": "daily", "changelog": "weekly",
    "vuln-scanner": "weekly", "goal-tracker": "daily",
    "agi-tracker": "weekly", "milestone-tracker": "weekly",
    "skill-health": "daily", "config-validator": "weekly",
    "skill-analytics": "weekly", "reflect": "daily", "self-review": "weekly",
    "skill-repair": "on_demand", "cost-report": "weekly",
    "ai-framework-watch": "weekly", "skill-evals": "weekly",
    "swarm-safety-eval": "weekly", "skill-update-check": "weekly",
    "fleet-control": "daily", "gitlawb-fleet-metrics": "daily",
    "weekly-shiplog": "weekly", "workflow-security-audit": "weekly",
    "skill-graph": "weekly", "notegraph": "daily", "skillpacks": "weekly",
    "suggest-edges": "daily", "skill-freshness": "daily",
    "run-frequency-guard": "daily", "heartbeat": "daily",
}

thresholds = {"daily": 28, "weekly": 192, "on_demand": None}

all_skills = sorted(set(list(cron.keys()) + ["run-frequency-guard", "ai-framework-watch"]))

flagged = []
ok_list = []

for skill in all_skills:
    cadence = schedules.get(skill, "daily")
    if cadence == "on_demand":
        continue
    threshold = thresholds[cadence]
    if skill not in cron:
        sev = "MISSING"
        age_h = float('inf')
        age_str = "NEVER"
    else:
        last_run = datetime.fromisoformat(cron[skill].replace("Z", "+00:00"))
        age_h = (NOW - last_run).total_seconds() / 3600
        age_str = f"{age_h:.1f}"
        if age_h <= threshold:
            sev = "OK"
        elif age_h <= 2 * threshold:
            sev = "WARN"
        else:
            sev = "STALE"

    if sev != "OK":
        flagged.append((skill, cadence, age_h, threshold, sev, age_str))
    else:
        ok_list.append(skill)

sev_order = {"MISSING": 0, "STALE": 1, "WARN": 2}
flagged_sorted = sorted(flagged, key=lambda x: (sev_order.get(x[4], 3), -x[2] if x[2] != float('inf') else -9999))

print("=== ALL RESULTS ===")
for item in all_skills:
    cadence = schedules.get(item, "daily")
    if cadence == "on_demand":
        continue
    threshold = thresholds[cadence]
    if item not in cron:
        age_str = "NEVER"
        sev = "MISSING"
    else:
        last_run = datetime.fromisoformat(cron[item].replace("Z", "+00:00"))
        age_h = (NOW - last_run).total_seconds() / 3600
        age_str = f"{age_h:.1f}"
        if age_h <= threshold:
            sev = "OK"
        elif age_h <= 2 * threshold:
            sev = "WARN"
        else:
            sev = "STALE"
    print(f"{sev:8} {item:<40} {cadence:<8} age={age_str:>8}h thresh={threshold}h")

print("\n=== FLAGGED ===")
for item in flagged_sorted:
    print(f"{item[4]:8} {item[0]:<40} {item[5]:>8}h (thresh {item[3]}h, {item[1]})")

print(f"\nEnabled (non-on_demand): {len(all_skills) - 1}")
print(f"Flagged: {len(flagged)}")
print(f"OK: {len(ok_list)}")
