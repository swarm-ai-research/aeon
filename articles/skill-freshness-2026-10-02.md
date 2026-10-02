# Skill Freshness — 2026-10-02

**Verdict:** ✅ FRESHNESS_OK — all 8 discovered dependencies reference files that have never existed on disk (implicit refs, not flagged); no enabled consumer is reading a stale file

*Audited 44 enabled skills · 0 dependencies scored · 0 flagged*

## Flagged dependencies

*(none — all dependencies are OK or skipped)*

## What this means per consumer

All enabled consumers with cross-skill file references depend on files that have **never been produced**. Per the skill-freshness spec, implicit grep-discovered references that never existed on disk are not flagged as MISSING — many SKILL.md files cite paths in prose or optional fallback logic that are legitimate no-ops when the producer has never run.

The 8 discovered cross-skill references, all implicit, all MISSING, all skipped:

| Consumer | Dependency | Producer | Producer Status | Skip Reason |
|----------|-----------|---------|-----------------|-------------|
| `weekly-shiplog` | `articles/push-recap-*.md` | `push-recap` | `enabled: false` (daily schedule) | implicit ref, never produced |
| `heartbeat` | `articles/token-report-*.md` | `token-report` | `enabled: false` (daily schedule) | implicit ref, never produced |
| `vuln-scanner` | `.outputs/github-trending.md` | `github-trending` | `enabled: false` | implicit ref, never produced |
| `pr-review` | `memory/topics/pr-review-rules.md` | operator-authored | absent | implicit ref, never created |
| `repo-revive` | `memory/topics/watched-repos.md` | operator-authored | absent | implicit ref, never created |
| `repo-revive` | `memory/topics/stale-models.md` | operator-authored | absent | implicit ref, never created |
| `surplus-pulse` | `memory/topics/projects.md` | operator-authored | absent | implicit ref, never created |
| `compute-pulse` | `memory/topics/compute-tokens.md` | operator-authored | absent | implicit ref, never created |

## Healthy consumers

All 44 enabled consumers have no scored (on-disk) cross-skill dependencies — every implicit reference targets a file that was never produced or created. From the freshness perspective, no consumer is silently reading stale data.

Selected consumers with zero cross-skill deps:

- planner — 0 cross-skill deps (reads memory/MEMORY.md + memory/state/planner-state.json as self-state)
- batch-health — 0 cross-skill deps
- skill-health — 0 cross-skill deps (reads memory/cron-state.json directly)
- reflect — 0 cross-skill deps
- goal-tracker — 0 cross-skill deps
- notegraph — 0 cross-skill deps
- skill-freshness — 0 cross-skill deps (self-auditor)
- heartbeat — 1 implicit dep (`articles/token-report-*.md`) — file never produced, not scored

*+ 36 more all-fresh consumers (zero cross-skill scored deps)*

## Source status

- `aeon.yml`: 44 enabled skills parsed
- Implicit references discovered: 8
- Explicit `chains: consume:` edges: 0 (all chain definitions commented out)
- Files not yet on disk (skipped — implicit references that never existed): 8
- **Net dependencies scored:** 0
- **Flagged:** 0

---

### Dedup note

Fingerprint identical to prior run (2026-09-30T08:54:33Z, verdict FRESHNESS_OK, hash `da39a3ee…`). Last run within 7-day re-emit window. Notification suppressed (FRESHNESS_NO_CHANGE). Next re-emit if fingerprint changes or 7 days elapse without change (next forced re-emit: 2026-10-07).

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk state — this skill measures nothing it does not also report.*
