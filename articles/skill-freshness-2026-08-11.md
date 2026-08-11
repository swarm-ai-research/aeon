# Skill Freshness — 2026-08-11

**Verdict:** ✅ FRESHNESS_OK — all 44 enabled consumers' cross-skill dependencies are within freshness thresholds

*Audited 44 enabled skills · 0 cross-skill dependencies checked · 0 flagged*

## Flagged dependencies

*(none — no cross-skill dependencies breached their freshness threshold)*

## What this means per consumer

All consumers scored OK. No action required.

## Healthy consumers

- planner — 0 cross-skill deps, state self-managed (memory/state/planner-state.json, fresh).
- batch-health — 0 cross-skill deps.
- memory-flush — 0 cross-skill deps.
- memory-structural-dedupe — 0 cross-skill deps.
- janitor — 0 cross-skill deps.
- stale-content-pr-sweeper — 0 cross-skill deps.
- issue-triage — 0 cross-skill deps.
- pr-triage — 0 cross-skill deps.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 44 entries parsed, 44 enabled
- Implicit cross-skill references discovered: 0 (after filtering self-references and never-existed implicit paths)
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out)
- Files not yet on disk (skipped — implicit references that never existed): `articles/` directory is empty; no articles produced in this repo checkout
- Notable: `goal-tracker` references `articles/token-report-*.md` (glob, not canonical `${today}` pattern; `token-report` is disabled) — not scored

## Methodology note

**GHA mtime-blind limitation (known issue):** GitHub Actions checkout resets all file mtimes to checkout time, making `stat --format=%Y` unreliable. This run used `git log -1 --format=%ct` per file as the best available proxy. The repo has a single commit (db1e08f, 2026-08-11T08:03:11Z), so all git-tracked files show the same age (~56 minutes). This is within every threshold class (articles: 28h/192h, .outputs: 4h, topics: 168h, state: 720h). Fix: [[skill-freshness-mtime-blind-in-gha]] — use `git log -1 --format=%ct` instead of `stat`. ISS-023 candidate per MEMORY.md.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
