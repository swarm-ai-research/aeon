# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- Recovering from 2026-06-06 → 2026-06-20 OAuth-token outage — see [[issues/ISS-001]] and [[fleet-ops]]. Day 2/3 clean (target close 2026-06-23).
- 2026-06-21 GHA cron tick drop ([[issues/ISS-006]]) — distinct signature from OAuth outage, 6 skills missed morning batch.
- Pending operator action: land `fix/workflow-security-audit-2026-06-21` RCE patch on `fleet-runner.yml`; aeon App lacks `workflows` write so auto-fix blocked.
- AGI Tracker live since 2026-06-10 — weekly skill maintains `docs/agi-tracker/data.js`. See [[agi-tracker]].

## Topics
- [[agi-tracker]] — frontier-agent capability tracking + Aschenbrenner *Situational Awareness* scoring
- [[fleet-ops]] — OAuth outage, monitor/repair coupling, GitHub App permission constraints
- [[compute-pulse]] — inference pricing, hardware deals, DePIN tokens (weekly snapshot)
- [[surplus-pulse]] — surplus-mode pricing simulator runs
- [[pr-status]] — cross-repo PR queue for the aeonframework author

## Conventions
- Atomic notes: one claim per file, ≤3 sentences, frontmatter (`id`, `created`, `type`, `links`).
- Topic files in `memory/topics/` are MOCs — pointers + inline snapshots only.
- Daily indexes at `memory/notes/daily/${date}.md`.

## Pointers
- `aeon.yml` — skill schedule, models, chains.
- `articles/` — agent-authored long-form output.
- `memory/cron-state.json` — per-skill success/failure counters.
- `memory/token-usage.csv` — per-run token accounting.

## Next priorities
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Confirm first weekly `agi-tracker` run after 2026-06-15 produced a clean PR (still no `cron-state` row).
- Move ISS-001 to resolved after 3 consecutive days of healthy runs (day 2/3 = 2026-06-22, earliest close 2026-06-23).
- Open the staged workflow-audit PR from `fix/workflow-security-audit-2026-06-21` via PAT (App perm gap).
- ISS-006 watch — no batch-health/heartbeat ran 2026-06-22 to confirm one-off vs recurring; re-evaluate after next morning batch fires.
- Confirm `agi-tracker` weekly run for 2026-06-22 13:00 UTC slot — no `cron-state` row yet; second missed slot in a row would warrant a structured issue.
- Move ISS-001 to resolved after 3 consecutive days of healthy runs (day 1/3 = 2026-06-21).
- Open the staged workflow-audit PR from `fix/workflow-security-audit-2026-06-21` via PAT (App perm gap). _[BLOCKED 2026-06-21: needs GH_GLOBAL PAT — Aeon App cannot self-grant workflows write]_
- Watch for ISS-006 repeat tomorrow morning; if isolated, mark `wontfix` as GHA infra transient.
