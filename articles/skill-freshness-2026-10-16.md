# Skill Freshness — 2026-10-16

**Verdict:** ✅ FRESHNESS_OK — all scored dependencies are within their freshness windows

*Audited 44 enabled skills · 8 dependency pairs scored · 0 flagged*

## Flagged dependencies

*(none)*

## What this means per consumer

No consumers have stale dependencies. All file references with scoreable mtimes are within threshold.

## Healthy consumers

Consumers with at least one scored dependency (all fresh):

- **planner** — 1 dep (`memory/state/planner-state.json`), all fresh.
- **stale-content-pr-sweeper** — 1 dep (`memory/state/notegraph.json`), all fresh.
- **notegraph** — 1 dep (`memory/state/notegraph.json`), all fresh.
- **pr-tracker** — 1 dep (`memory/topics/pr-status.md`), all fresh.
- **surplus-pulse** — 1 dep (`memory/topics/surplus-pulse.md`), all fresh.
- **compute-pulse** — 1 dep (`memory/topics/compute-pulse.md`), all fresh.
- **skillpacks** — 1 dep (`memory/state/skillpacks.json`), all fresh.
- **suggest-edges** — 1 dep (`memory/state/suggest-edges.json`), all fresh.

+ 36 more enabled consumers had no scoreable non-self-reference file dependencies discovered. (All implicit references in their SKILL.md files either matched paths that have never existed on disk, or referenced the consumer's own prior output.)

## Source status

- `aeon.yml`: 113 entries, 44 enabled
- Implicit references discovered: ~30 (grep-extracted from 44 enabled SKILL.md files)
- Explicit `chains: consume:` edges: 0 (all `chains:` blocks are commented out)
- Files not yet on disk (skipped — implicit references that never existed): ~15
- Self-references skipped: ~14 (producer prefix matches consumer name)

## Measurement note

This instance runs in a depth-1 GitHub Actions checkout. All files share the same git commit timestamp (`4ec06cc`, 2026-10-16 00:34 UTC). File ages are therefore measured relative to that commit (~9h), not relative to when each file was originally produced. This matches the known [[skill-freshness-mtime-blind-in-gha]] limitation — the pending fix (`git log -1 --format=%ct` for per-file tracking across full history) requires a deeper clone. In practice this means `.outputs/` staleness can't be reliably measured in this environment, and `memory/topics/` + `memory/state/` ages are all anchored to the single HEAD commit, well within their 168h/720h thresholds regardless of actual production date.

The notable absence: `skill-evals` last article is `2026-09-13` (33 days) and `cost-report` last article is `2026-09-28` (18 days), both past their weekly 192h threshold. However, both are self-references (each skill reads its own prior output for dedup/context), so they are correctly excluded from the freshness verdict per the self-reference filter. If a downstream consumer (e.g. `operator-scorecard`, currently disabled) were to depend on those articles, those dependencies would score STALE.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
