*Skill Analytics — 2026-08-12*
2 scheduled skill(s) didn't run this window — ai-framework-watch, run-frequency-guard

Window: last 7d · 166 runs · 41 skills · 100.0% success
Anomalies: 2

🔴 Critical:
- ai-framework-watch — SILENT: scheduled `30 8 * * 1` (Mon 08:30 UTC), zero runs in 7d window — 35th consecutive silent day; ISS-021 candidate
- run-frequency-guard — SILENT: scheduled `0 23 * * *` (daily 23:00 UTC), zero runs in 7d window — 35th consecutive silent day; same root cause

Top by runs: pr-review (14), planner/fleet-control/github-monitor/goal-tracker/issue-triage/pr-tracker/pr-triage/reflect/skill-health/compute-futures-eda (7 each)

Zero failures fleet-wide. Exit dominant: ok (63%). Notable: suggest-edges 6 runs / 0 useful outputs (NOISE_ABORT streak-4). fleet-control/github-monitor/code-health/gitlawb-fleet-metrics all 100% GHA-success but empty-config short-circuit every run (watched-repos gap, streak-7).

Full: articles/skill-analytics-2026-08-12.md
