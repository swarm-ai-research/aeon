# Skill Freshness — 2026-07-07

**Verdict:** ✅ FRESHNESS_OK — all checked dependencies are within their freshness windows

*Audited 43 enabled skills · 3 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all checked dependencies scored OK)*

## What this means per consumer

*(no consumers with verdict ≠ OK)*

## Healthy consumers

- planner — 1 dep, all fresh. (`memory/state/planner-state.json`, ~1.6h, threshold 720h)
- surplus-pulse — 1 dep, all fresh. (`memory/topics/surplus-pulse.md`, ~1.6h, threshold 168h)
- compute-pulse — 1 dep, all fresh. (`memory/topics/compute-pulse.md`, ~1.6h, threshold 168h)

+ 40 more all-fresh consumers (no discoverable on-disk file dependencies — either dependencies are absent from disk and therefore skipped as implicit-missing, or the skill has no file dependencies in scope).

## Source status

- `aeon.yml`: 43 enabled skills (178+ total entries parsed)
- Implicit references discovered: 12
- Explicit `chains: consume:` edges: 0 (all chain blocks commented out)
- Files not yet on disk (skipped — implicit references that never existed): 9
  - `memory/topics/pr-review-rules.md` (pr-review)
  - `memory/topics/watched-repos.md` (repo-revive)
  - `memory/topics/stale-models.md` (repo-revive)
  - `memory/topics/projects.md` (surplus-pulse)
  - `memory/topics/compute-tokens.md` (compute-pulse)
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate)
  - `.outputs/github-trending.md` (vuln-scanner)
  - `memory/state/skill-repair-history.json` (skill-repair)
  - `memory/state/fleet-control-state.json` (fleet-control)

## Structural note

⚠️ This repo is a single-commit snapshot (`34a9fab`, 2026-07-07T07:22:15Z). Every file's on-disk timestamp reflects today's checkout, not the content's actual last-edit date. Ages computed here (~1.6h for all existing files) are meaningless as a staleness signal — they are checkout ages, not content ages. This is the **9th consecutive FRESHNESS_OK** under these conditions; prior verdicts are structural, not clean. The known fix (`git log -1 --format=%ct` from the source repo's full history instead of `stat`) is documented at [[skill-freshness-mtime-blind-in-gha]]. Until the fix lands, this skill's output accurately describes what it can observe from on-disk timestamps, and is transparent about the limitation.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
