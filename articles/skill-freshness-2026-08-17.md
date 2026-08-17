# Skill Freshness — 2026-08-17

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are fresh or absent-and-implicit

*Audited 45 enabled skills · 8 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies resolved clean)*

## What this means per consumer

All consumers with discovered dependencies are reading from files that either (a) are fresh within their threshold or (b) are implicit references to files that have never existed on disk (never-run disabled producers) — those are not flagged per policy.

## Healthy consumers (with discovered dependencies)

- **heartbeat** — 1 implicit dep (`articles/token-report-*.md`); source skill `token-report` is disabled, file never existed → not flagged.
- **weekly-shiplog** — 1 implicit dep (`articles/push-recap-*.md`); source skill `push-recap` is disabled, file never existed → not flagged.
- **vuln-scanner** — 1 implicit dep (`.outputs/github-trending.md`); source skill `github-trending` is disabled, file never existed → not flagged.
- **pr-review** — 1 implicit dep (`memory/topics/pr-review-rules.md`); operator config file never written → not flagged.
- **repo-revive** — 2 implicit deps (`memory/topics/watched-repos.md`, `memory/topics/stale-models.md`); operator config files never written → not flagged.
- **compute-pulse** — 1 implicit dep (`memory/topics/compute-tokens.md`); operator config file never written → not flagged.
- **surplus-pulse** — 1 implicit dep (`memory/topics/projects.md`); operator config file never written → not flagged.

+ 38 more all-fresh consumers (no discovered file dependencies in audited patterns).

## Anomaly note

**`agi-tracker`** is `enabled: true` in `aeon.yml` but has no `skills/agi-tracker/SKILL.md`. No dependency scan was possible. This is a known issue (ISS-022 candidate; 7th silent Monday fire expected 2026-08-17T13:00Z). No dependency edges to other consumers were found, so this does not affect the fleet verdict.

## Source status

- `aeon.yml`: 45 entries with `enabled: true`
- Implicit references discovered: 8
- Explicit `chains: consume:` edges: 0 (all chains sections commented out)
- Files not yet on disk (skipped — implicit references that never existed): 8

**Note:** File mtimes are unreliable in the GitHub Actions sandbox (all files show checkout time). This run used `git log -1 --format=%ct` to derive commit timestamps per `[[skill-freshness-mtime-blind-in-gha]]`. No file ages were stale against their class thresholds.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk commit timestamps — this skill measures nothing it does not also report.*
