*Skill Analytics — 2026-09-02*
16 scheduled skill(s) didn't run this window — memory-flush

Window: last 7d · 64 runs · 27 skills · 100% success
Anomalies: 16

🔴 Critical:
- memory-flush — SILENT: scheduled `0 6 2/2 * *`, zero runs (ISS-006-family)
- memory-structural-dedupe — SILENT: scheduled `10 6 2/2 * *`, zero runs (ISS-006-family)
- run-frequency-guard — SILENT: daily `0 23 * * *`, day-56 never-dispatched
- config-validator — SILENT: Sunday `0 7 * * 0`, expected 2026-08-30, zero runs
- skillpacks — SILENT: Sunday `0 6 * * 0`, expected 2026-08-30, zero runs
- swarm-safety-eval — SILENT: Sunday `30 7 * * 0`, expected 2026-08-30, zero runs
- skill-evals — SILENT: Sunday `0 9 * * 0`, expected 2026-08-30, zero runs
- workflow-security-audit — SILENT: Sunday `0 16 * * 0`, expected 2026-08-30, zero runs
- skill-update-check — SILENT: Sunday `0 19 * * 0`, expected 2026-08-30, zero runs
- compute-macro-correlate — SILENT: Sunday `30 6 * * 0`, expected 2026-08-30, zero runs
- repo-revive — SILENT: Saturday `0 10 * * 6`, expected 2026-08-29, zero runs
- compute-pulse — SILENT: Saturday `0 11 * * 6`, expected 2026-08-29, zero runs
- ai-framework-watch — SILENT: Monday `30 8 * * 1`, day-56 never-dispatched
- milestone-tracker — SILENT: Monday `0 12 * * 1`, expected 2026-08-31, zero runs
- agi-tracker — SILENT: Monday `0 13 * * 1`, SKILL.md absent — 9th silent-Mon
- cost-report — SILENT: Monday `0 7 * * 1`, ISS-006 outage triple, next slot 09-07

Top by runs: pr-review (6), code-health (5), surplus-pulse (5)

Full: articles/skill-analytics-2026-09-02.md
