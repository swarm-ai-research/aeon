*Skill Analytics — 2026-07-15*
3 scheduled skill(s) didn't run this window — run-frequency-guard, weekly-shiplog, ai-framework-watch

Window: last 7d · 143 runs · 40 skills · 100% success
Anomalies: 3

🔴 Critical:
- run-frequency-guard — SILENT: scheduled `0 23 * * *` (daily 23:00 UTC) but zero runs in window — no cron-state entry
- weekly-shiplog — SILENT: scheduled `0 9 * * 1` (Mon 09:00 UTC) — missed 2026-07-13, last ran 2026-07-06
- ai-framework-watch — SILENT: scheduled `30 8 * * 1` (Mon 08:30 UTC) — missed 2026-07-13, no cron-state entry

Top by runs: pr-review (13), code-health (7), goal-tracker (7)

Full: articles/skill-analytics-2026-07-15.md
