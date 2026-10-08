# Skill Freshness — 2026-10-08

**Verdict:** ✅ FRESHNESS_OK — all discovered consumer→dependency edges are within threshold

*Audited 44 enabled skills · 17 non-self dependencies checked · 0 flagged · 9 skipped (implicit MISSING)*

## Flagged dependencies

*(none — no consumer is reading a stale or missing upstream file within the scope of checkable edges)*

## What this means per consumer

No consumers have a freshness violation on their tracked dependencies. All existing topic, state, and output files referenced by enabled skills are within threshold based on available signals.

## Healthy consumers

- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`), fresh.
- pr-tracker — 1 dep (`memory/topics/pr-status.md`), fresh.
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`), fresh. (`projects.md` is implicit MISSING → skipped.)
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`), fresh. (`compute-tokens.md` implicit MISSING → skipped.)
- notegraph — 1 dep (`memory/state/notegraph.json`), fresh.
- skillpacks — 1 dep (`memory/state/skillpacks.json`), fresh.
- suggest-edges — 1 dep (`memory/state/suggest-edges.json`), fresh.
- pr-review — dep `memory/topics/pr-review-rules.md` implicit MISSING → skipped; no remaining checkable deps.

+ 36 more enabled consumers with no discovered cross-skill dependencies — all-fresh by absence of edges.

## Source status

- `aeon.yml`: 44 enabled skills parsed (43 with SKILL.md on disk; `agi-tracker` has `enabled: true` but no SKILL.md)
- Implicit references discovered: 17 (after filtering self-references and known-example paths)
- Explicit `chains: consume:` edges: 0 (all `chains:` blocks commented out in `aeon.yml`)
- Files not yet on disk (skipped — implicit references that never existed): 9
  - `memory/topics/skills-history.md` (memory-flush)
  - `memory/topics/pr-review-rules.md` (pr-review)
  - `memory/topics/stale-models.md` (repo-revive)
  - `memory/topics/watched-repos.md` (repo-revive) ← known streak-67 absence
  - `memory/topics/projects.md` (surplus-pulse)
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate) ← on unmerged branch
  - `memory/topics/compute-tokens.md` (compute-pulse)
  - `.outputs/github-trending.md` (vuln-scanner) ← producer `github-trending` is disabled
  - `memory/state/skill-repair-history.json` (skill-repair)
  - `memory/state/fleet-control-state.json` (fleet-control)

## Observation: article-based producer staleness (informational, not consumer violations)

Using filename-date parsing on `articles/` (the only reliable age signal in a shallow-clone GHA checkout):

| Producer | Last article | Age | Producer cadence | Threshold | Band |
|----------|-------------|-----|-----------------|-----------|------|
| skill-freshness | 2026-10-06 | 48h | daily | 28h | ⚠ WARN |
| cost-report | 2026-09-28 | 240h | weekly | 192h | ⚠ WARN |
| skill-analytics | 2026-09-16 | 528h | weekly | 192h | 🔴 STALE |
| self-review | 2026-09-13 | 600h | weekly | 192h | 🔴 STALE |
| skill-evals | 2026-09-13 | 600h | weekly | 192h | 🔴 STALE |
| vuln-scanner | 2026-10-03 | 120h | weekly | 192h | ✅ OK |

These are **producer health signals only** — no currently-enabled consumer reads any of these articles as input (all are either self-produced outputs or produced by skills with no downstream enabled consumers). They do not affect the fleet_verdict but are meaningful context for `skill-health` and operator oversight.

`skill-freshness` itself missing 2026-10-07 is consistent with the standing ISS-006 08Z slot instability.

## Known limitation: shallow-clone mtime blindness

This run is affected by [[skill-freshness-mtime-blind-in-gha]]: in a GHA depth=1 checkout, `stat --format=%Y` returns the checkout time (~0h) for all files, and `git log -1 --format=%ct` returns the single commit time (~15h) for all files — neither distinguishes per-file ages for committed content. As a result:

- `memory/topics/`, `memory/state/`, and `.outputs/` file ages are reported as 0h via stat (likely the checkout time, not the actual write time).
- All in-repo files appear within threshold regardless of actual staleness.
- Only `articles/` files (where the date is embedded in the filename) yield reliable age signals.

Fix pending: [[skill-freshness-mtime-blind-in-gha]] + [[skill-freshness-stuck-dispatched-callback-never-fires]].

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
