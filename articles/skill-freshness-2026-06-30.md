# Skill Freshness — 2026-06-30

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within threshold

*Audited 44 enabled skills · 8 dependencies checked · 0 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|

*(None — all dependencies are fresh.)*

## What this means per consumer

No consumers flagged. Every discovered dependency is within its per-class freshness threshold.

## Healthy consumers

- **planner** — 1 dep (`memory/state/planner-state.json`), all fresh.
- **stale-content-pr-sweeper** — 1 dep (`memory/state/notegraph.json`), all fresh.
- **pr-tracker** — 1 dep (`memory/topics/pr-status.md`), all fresh.
- **surplus-pulse** — 1 dep (`memory/topics/surplus-pulse.md`), all fresh.
- **compute-pulse** — 1 dep (`memory/topics/compute-pulse.md`), all fresh.
- **agi-tracker** — 1 dep (`memory/topics/agi-tracker.md`), all fresh.
- **notegraph** — 1 dep (`memory/state/notegraph.json`), all fresh.
- **skillpacks** — 1 dep (`memory/state/skillpacks.json`), all fresh.

\+ 36 more all-fresh consumers (no resolvable file dependencies discovered).

## Source status

- `aeon.yml`: 44 entries enabled (of ~110 total)
- Explicit `chains: consume:` edges: 0 (daily-routine chain is commented out; no active chains)
- Implicit references discovered: 8 (non-filtered, on-disk, in-scope)
- Self-references filtered: 3 (`planner → .outputs/planner.md`; `vuln-scanner → articles/vuln-scan-${today}.md`; `fleet-control → articles/fleet-status-${today}.md`)
- Files not yet on disk (skipped — implicit references that never existed): 13
  - `memory/topics/skills-history.md` (memory-flush)
  - `memory/topics/pr-review-rules.md` (pr-review)
  - `memory/topics/stale-models.md`, `memory/topics/watched-repos.md` (repo-revive)
  - `memory/topics/projects.md` (surplus-pulse)
  - `memory/topics/compute-tokens.md` (compute-pulse)
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate)
  - `.outputs/github-trending.md` (vuln-scanner — producer skill disabled)
  - `memory/state/skill-repair-history.json` (skill-repair)
  - `memory/state/fleet-control-state.json` (fleet-control)
  - `memory/state/suggest-edges.json` (suggest-edges)
  - `articles/foo-2026-01-01.md` (skill-freshness — example in SKILL.md prose)
  - `articles/token-report-2026-04-28.md` (heartbeat — stale specific-dated reference)
- **Status**: `FRESHNESS_NO_CHANGE` — fingerprint identical to 2026-06-28 run (da39a3ee…), last run within 7-day re-emit window; notification suppressed.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
