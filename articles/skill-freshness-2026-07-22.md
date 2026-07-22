# Skill Freshness — 2026-07-22

**Verdict:** ✅ FRESHNESS_OK — all tracked dependencies fresh

*Audited 44 enabled skills · 4 dependencies checked · 0 flagged*

**Run status:** FRESHNESS_NO_CHANGE — fingerprint identical to 2026-07-19 run (3 days ago, within 7-day re-emit window). Notification suppressed.

## Flagged dependencies

*(None — all tracked dependencies are within their freshness thresholds.)*

## What this means per consumer

*(No consumers with degraded freshness. All discovered dependencies checked out OK.)*

## Healthy consumers

- planner — 1 dep, all fresh. (`memory/state/planner-state.json`, 2.2h old, threshold 720h)
- surplus-pulse — 1 dep, all fresh. (`memory/topics/surplus-pulse.md`, 2.2h old, threshold 168h)
- compute-pulse — 1 dep, all fresh. (`memory/topics/compute-pulse.md`, 2.2h old, threshold 168h)
- compute-futures-eda — 1 dep, all fresh. (`memory/topics/compute-futures-eda/2026-07-21.md`, 2.2h old, threshold 168h)
- heartbeat — 0 tracked deps, all fresh.
- batch-health — 0 tracked deps, all fresh.
- skill-health — 0 tracked deps, all fresh.
- reflect — 0 tracked deps, all fresh. (reads `articles/` broadly; directory absent — implicit scan, not flagged per policy)

+ 36 more all-fresh consumers (no tracked implicit deps discovered via SKILL.md grep).

## Notes

- `articles/` directory absent on disk. No enabled consumer has an explicit canonical `articles/{producer}-${today}.md` read dependency, so no MISSING flags were triggered. Skills that reference `articles/` broadly (reflect, skill-evals prior-run, weekly-shiplog prior context) handle the absent directory gracefully or optionally.
- 4 implicit references to files that never existed on disk were skipped per policy (not flagged): `memory/topics/compute-tokens.md`, `memory/topics/pr-review-rules.md`, `memory/topics/watched-repos.md`, `memory/topics/compute-futures-macro-correlations.md`.
- All `.outputs/*.md` files (41 total) were committed at 07:02Z today (2.2h old), well within the 4h chain-output threshold.
- Mtime method: `git log -1 --format=%ct` used throughout (GHA-safe per [[skill-freshness-mtime-blind-in-gha]]).

## Source status

- `aeon.yml`: 44 entries, 44 enabled
- Implicit references discovered: 4 (across planner, surplus-pulse, compute-pulse, compute-futures-eda)
- Explicit `chains: consume:` edges: 0 (daily-routine chain is commented out)
- Files not on disk, skipped (implicit refs that never existed): 4
- Prior run fingerprint match: yes (da39a3ee5e6b4b0d3255bfef95601890afd80709)
- Re-emit window status: last run 2026-07-19 (3d ago) < 7d threshold → no re-notify

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk git-log timestamps — this skill measures nothing it does not also report.*
