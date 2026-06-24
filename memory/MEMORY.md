# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. Daily activity in `memory/logs/`. Structured issues in `memory/issues/`.

## Current focus
- ⚠ [[issues/ISS-006]] **escalated** (severity medium→high, status investigating, day 3 of recurring): `planner` + `compute-futures-eda` missed morning batch 2026-06-21, 06-22, 06-23. Working hypothesis: `messages.yml` `*/5` cron-tick drop in the 05:30–07:30 UTC window — see [[aeon-skills-dispatch-via-messages-yml]]. 08:00 batch did fire today; only the 06:00 group is dropping.
- [[issues/ISS-001]] OAuth outage (2026-06-06 → 2026-06-20T06:05Z) — recovery batch holding, all 38 tracked skills at `last_status: success`. Cumulative `success_rate` < 0.6 takes weeks to clear by design; close decision deferred until morning batch ([[issues/ISS-006]]) stabilizes.
- Pending operator action: land `fix/workflow-security-audit-2026-06-21` RCE patch on `fleet-runner.yml`; aeon App lacks `workflows` write so auto-fix blocked — needs `GH_GLOBAL` PAT. Same gate now also blocking [[issues/ISS-007]] (fleet-runner skills can't open PRs — first hit 2026-06-24 by `suggest-edges`; branch pushed, manual open required).
- AGI Tracker live since 2026-06-10 — weekly skill maintains `docs/agi-tracker/data.js`. See [[agi-tracker]]. Still no `cron-state` row after 2026-06-15 and 2026-06-22 Mon slots.

## Topics
- [[agi-tracker]] — frontier-agent capability tracking + Aschenbrenner *Situational Awareness* scoring
- [[fleet-ops]] — OAuth outage, morning-batch silence, monitor/repair coupling, GitHub App perms
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
- ISS-006: inspect `messages.yml` cron block + Actions tab history for the 06:00–07:30 UTC window across 2026-06-21..23. Per [[aeon-skills-dispatch-via-messages-yml]], no per-skill workflow exists — check the `*/5` ticks first. `git log --since=2026-06-19 -- .github/workflows/messages.yml aeon.yml` to spot any recent edits.
- File `./generate-skills-json` bugs as structured issues (see [[generate-skills-json-newline-bug]], [[skills-json-count-drift]]).
- Patch `pr-tracker` SKILL.md fallback per [[gh-search-prs-api-drift]] (`--merged` flag, drop `headRefName`).
- Confirm `agi-tracker` weekly run for 2026-06-22 13:00 UTC slot — still no `cron-state` row; second consecutive Mon miss warrants its own structured issue if it persists.
- Open the staged workflow-audit PR from `fix/workflow-security-audit-2026-06-21` via PAT (App perm gap). _[BLOCKED 2026-06-21: needs `GH_GLOBAL` PAT — Aeon App cannot self-grant workflows write]_
- Defer ISS-001 close until ISS-006 morning-batch silence is resolved — recovery confidence is fragile while the 06:00 group keeps missing.
