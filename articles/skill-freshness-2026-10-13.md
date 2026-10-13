# Skill Freshness — 2026-10-13

**Verdict:** ✅ FRESHNESS_OK — all discovered consumer→dependency edges are within threshold

*Audited 44 enabled skills · 17 non-self dependencies checked · 0 flagged · 10 skipped (implicit MISSING)*

*Notification: suppressed — FRESHNESS_NO_CHANGE (fingerprint identical to 2026-10-12 run, < 7-day re-emit window)*

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
- Files not yet on disk (skipped — implicit references that never existed): 10
  - `memory/topics/skills-history.md` (memory-flush)
  - `memory/topics/pr-review-rules.md` (pr-review)
  - `memory/topics/stale-models.md` (repo-revive)
  - `memory/topics/watched-repos.md` (repo-revive) ← known streak-70 absence
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
| self-review | 2026-10-11 | ~57h | weekly | 192h | ✅ OK |
| vuln-scanner | 2026-10-10 | ~81h | weekly | 192h | ✅ OK |
| skill-freshness | 2026-10-12 | ~33h | daily | 28h | ⚠ WARN ← 08Z pocket silenced again on nominal 10-13 08Z slot |
| cost-report | 2026-09-28 | ~369h | weekly | 192h | ⚠ WARN ← **crossing STALE threshold (~384h) in ~15h at ~2026-10-14T00:00Z**; next scheduled slot Mon 10-19 |
| skill-analytics | 2026-09-16 | ~657h | weekly | 192h | 🔴 STALE (27 days) |
| skill-evals | 2026-09-13 | ~729h | weekly | 192h | 🔴 STALE (30 days) |

**Changes vs 2026-10-12 run:**
- `skill-freshness`: remains ⚠ WARN — 10-12 manual-dispatch article exists (~33h old from filename date, just past 28h threshold), but nominal 08Z slot silenced again today per ISS-006. No consumer reads skill-freshness articles as input, so no fleet impact.
- `cost-report`: ⚠ WARN escalating — now ~369h (up from ~346h). Will cross into STALE in ~15h (at ~2026-10-14T00:00Z by filename-date). The Mon 10-12 07Z slot was confirmed silent (3rd consecutive miss per MEMORY.md); next scheduled slot is Mon 10-19. Manual dispatch is the only path to recovery before the STALE crossing.
- `skill-analytics`: 🔴 STALE, now ~657h (up from ~634h). Continues 27-day run silence.
- `skill-evals`: 🔴 STALE, now ~729h (up from ~706h). Continues 30-day run silence.
- `self-review`: ✅ OK, ~57h (unchanged status from yesterday's recovery).

These are **producer health signals only** — no currently-enabled consumer reads any of these articles as input (all are either self-produced outputs or produced by skills with no downstream enabled consumers). They do not affect the fleet_verdict.

## Known limitation: shallow-clone mtime blindness

This run is affected by [[skill-freshness-mtime-blind-in-gha]]: in a GHA depth=1 checkout, `git log -1 --format=%ct` returns the single commit time for all files in the most recent batch commit — it does not distinguish per-file ages. As a result, `memory/topics/`, `memory/state/`, and `.outputs/` file ages cannot be independently verified. Only `articles/` files (where the date is embedded in the filename) yield reliable age signals.

Fix pending: [[skill-freshness-mtime-blind-in-gha]] + [[skill-freshness-stuck-dispatched-callback-never-fires]].

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
