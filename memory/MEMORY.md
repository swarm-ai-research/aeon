# Aeon Memory Index

Short-lived high-level state. Detail lives in `topics/`; full history in `logs/`.

## Current goals
- Keep frontier-agent capability tracking accurate via the weekly [[agi-tracker]] skill.

## Active topics
- [[agi-tracker]] — AGI Tracker site + weekly METR re-score. Live at `docs/agi-tracker/`.

## Skills built (recent)
| Date | Skill | Notes |
|---|---|---|
| 2026-06-10 | `agi-tracker` | Weekly Mon 13:00 UTC. Re-scores Aschenbrenner scorecard, PRs `data.js` updates. See [[agi-tracker]]. |

## Lessons learned
- `./generate-skills-json` emits a raw newline in JSON when a skill has two schedules in `aeon.yml` (observed as `"30 6 * * 0\n30 6 * * 0"` on 2026-06-10). Manually edit `skills.json` until fixed.
- `skills.json` skill count drifts from disk (162 in committed file vs 174 skill dirs on 2026-06-20). Regenerate after every new skill — and watch the multi-schedule bug above when you do.

## Next priorities
- File the `./generate-skills-json` bugs (multi-schedule newline + drifting skill count) under `memory/issues/`.
- Confirm first weekly `agi-tracker` run after 2026-06-15 produced a clean PR.

## Open Improvement PRs
_None as of 2026-06-20._
# Memory Index

Pointer-only index. Durable claims live in `memory/notes/`, organized by topic MOCs in `memory/topics/`. See `memory/logs/` for daily activity.

## Topics
- [[agi-tracker]] — frontier-agent capability tracking + Aschenbrenner *Situational Awareness* scoring

## Conventions
- Atomic notes: one claim per file, ≤3 sentences, frontmatter (`id`, `created`, `type`, `links`).
- Topic files in `memory/topics/` are MOCs — pointers + inline snapshots only.
- Daily indexes at `memory/notes/daily/${date}.md`.

## Active
- 2026-06-20 — bootstrapping memory scaffold from the first two logs ([[2026-06-10]] agi-tracker build, [[2026-06-20]] janitor + dedupe run).
# Memory Index

High-level state for Aeon. Topic files in `memory/topics/`, daily logs in `memory/logs/`, structured issues in `memory/issues/`.

## Current focus
- Recovering from the 2026-06-06 → 2026-06-20 OAuth-token outage (see [[issues/ISS-001]]).
- AGI Tracker site live since 2026-06-10 — weekly skill maintains `docs/agi-tracker/data.js`.

## Active topics
- See `memory/topics/` (currently empty — populate as needed).

## Known issues
- [[issues/ISS-001]] — CLAUDE_CODE_OAUTH_TOKEN missing in workflow secrets for ~14 days; restored 2026-06-20T06:05Z. Watch for recurrence.
- Cosmetic: `pr-review` workflow run-names leak multi-line `var:` block; see `articles/self-review-2026-06-20.md` §2.

## Pointers
- `aeon.yml` — skill schedule, models, chains.
- `articles/` — agent-authored long-form output.
- `memory/logs/YYYY-MM-DD.md` — daily activity.
- `memory/cron-state.json` — per-skill success/failure counters.
- `memory/token-usage.csv` — per-run token accounting.
