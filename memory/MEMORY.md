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
