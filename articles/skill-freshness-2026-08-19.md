# Skill Freshness — 2026-08-19

**Verdict:** ✅ FRESHNESS_OK — all 45 enabled consumers have fresh upstream inputs

*Audited 45 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all 2 tracked dependencies are within their freshness thresholds)*

## What this means per consumer

All consumers are reading fresh data. No action required.

## Healthy consumers

- pr-tracker — 1 dep (`memory/topics/pr-status.md`), all fresh (age 1.4h, threshold 168h).
- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`), all fresh (age 1.4h, threshold 720h).
- notegraph — 0 deps, all fresh.
- suggest-edges — 0 deps, all fresh.
- compute-futures-eda — 0 deps, all fresh.
- skill-health — 0 deps, all fresh.
- heartbeat — 0 deps, all fresh.
- planner — 0 deps, all fresh.

+ 37 more all-fresh consumers.

## Source status

- `aeon.yml`: 70+ entries, 45 enabled
- Implicit references discovered: 8 (grep across 45 enabled SKILL.md files)
- Explicit `chains: consume:` edges: 0 (all chain definitions in `aeon.yml` are commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6 (`skills-history.md`, `stale-models.md`, `watched-repos.md`, `projects.md`, `.outputs/github-trending.md`, example placeholder in skill-freshness SKILL.md)

### Freshness note

All tracked dependencies were committed in today's morning snapshot at 2026-08-19T06:48:34Z, giving an age of ~1.4h against thresholds of 168h (`memory/topics/`) and 720h (`memory/state/`). No staleness possible from a same-day commit.

The `articles/` directory was absent when this run began (no prior article outputs on disk). Any cross-skill `articles/` dependencies would be flagged MISSING, but no enabled consumer has a non-self canonical `articles/{producer}-${today}.md` reference to an enabled daily/weekly producer — all article path references in enabled SKILL.md files are either self-writes, wildcard patterns outside the canonical grep match, or from disabled producers.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git-log commit timestamps — this skill measures nothing it does not also report.*
