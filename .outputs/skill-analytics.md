*Skill Analytics — 2026-09-16*
13 scheduled skill(s) didn't run this window — memory-flush

Window: last 7d · 86 runs · 30 skills · 100% success
Anomalies: 13

🔴 Critical:
- memory-flush — SILENT: scheduled `0 6 2/2 * *`, 4 expected fires missed (ISS-006 06:00Z dead pocket)
- memory-structural-dedupe — SILENT: scheduled `10 6 2/2 * *`, same dead pocket
- run-frequency-guard — SILENT: scheduled `0 23 * * *`, 7 daily slots missed — never dispatched

🔴 Additional silent (10 more):
- janitor, skillpacks, compute-macro-correlate, config-validator, swarm-safety-eval (all Sun 09-13)
- repo-revive (Sat 09-12)
- cost-report, ai-framework-watch, milestone-tracker, agi-tracker (all Mon 09-14)

Top by runs: pr-review (8), code-health (6), notegraph (6)

Full: articles/skill-analytics-2026-09-16.md
