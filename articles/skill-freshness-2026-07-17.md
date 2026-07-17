# Skill Freshness — 2026-07-17

**Verdict:** ✅ FRESHNESS_OK — all checked dependencies are within freshness thresholds

*Audited 44 enabled skills · 0 cross-skill dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all deps OK)*

## What this means per consumer

No consumer has a flagged dependency this run. Every file that could be checked was within its freshness window.

## Healthy consumers

- planner — 0 cross-skill deps (state files are self-writes, filtered)
- batch-health — 0 deps
- memory-flush — 0 deps
- memory-structural-dedupe — 0 deps
- janitor — 0 deps
- stale-content-pr-sweeper — 0 deps
- issue-triage — 0 deps
- pr-triage — 0 deps

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~160 entries parsed, 44 enabled
- Implicit references discovered: 0 cross-skill (after filtering self-writes, disabled producers, absent-directory refs)
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out in `aeon.yml`)
- Files not yet on disk (skipped — implicit references that never existed): `articles/` directory absent (same structural GHA snapshot blind spot as 2026-07-16; see note below)

## Structural note: GHA mtime blind spot

All on-disk files carry mtime `2026-07-17T08:57 UTC` (the GitHub Actions checkout time), not their true commit-time ages. This means:

- `.outputs/` files (30 present, all stamped 08:57): reported age ≈ 0h — well within the 4h threshold, but the true age is unknowable from `stat`.
- `memory/topics/` files (5 present): reported age ≈ 0h — well within the 7d threshold.
- `memory/state/` files (11 present): reported age ≈ 0h — well within the 30d threshold.
- `articles/` directory: **absent from this GHA snapshot** — same situation as 2026-07-16. No enabled skill writes `articles/` into the checkout, so no article-based dependencies can be scored.

Per `memory/topics/skill-freshness-mtime-blind-in-gha`, the fix is to replace `stat --format=%Y` with `git log -1 --format=%ct` for true commit ages. Until that fix lands, this skill's results reflect **snapshot-pull freshness, not true file ages**.

No explicit `chains: consume:` edges exist (all chain definitions are commented out), so zero `.outputs/` cross-consumer pairs are audited.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
