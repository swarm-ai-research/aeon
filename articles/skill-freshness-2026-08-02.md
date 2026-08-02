# Skill Freshness — 2026-08-02

**Verdict:** ✅ FRESHNESS_OK — all 7 tracked dependencies are fresh, 0 flagged

*Audited 47 enabled skills · 7 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies within freshness thresholds.)*

## What this means per consumer

All consumers with tracked dependencies read fresh data. No action required.

## Healthy consumers

- planner — 1 dep (`memory/state/planner-state.json`, 2h old, threshold 720h), all fresh.
- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`, 2h old, threshold 720h), all fresh.
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`, 2h old, threshold 168h), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`, 2h old, threshold 168h), all fresh.
- compute-futures-eda — 1 dep (`memory/topics/compute-futures-eda/2026-08-01.md`, threshold 168h), all fresh.
- notegraph — 1 dep (`memory/state/notegraph.json`, 2h old, threshold 720h), all fresh.
- skillpacks — 1 dep (`memory/state/skillpacks.json`, 2h old, threshold 720h), all fresh.
- heartbeat — 0 tracked deps (all refs are optional wildcards), all fresh.

+ 39 more all-fresh consumers (0 tracked deps each — no cross-skill file reads detected by grep extraction).

## Source status

- `aeon.yml`: 156 entries, 47 enabled
- Implicit references discovered: ~25 (pre-filter)
- Explicit `chains: consume:` edges: 0 (all `chains:` blocks are commented out)
- Files not yet on disk (skipped — implicit references that never existed): ~18 (`watched-repos.md`, `stale-models.md`, `pr-review-rules.md`, `compute-tokens.md`, `projects.md`, `suggest-edges.json`, `fleet-control-state.json`, `skill-repair-history.json`, and others)

### Methodology note (GHA shallow-clone)

All file ages are computed via `git log -1 --format=%ct`. This repo is checked out at shallow depth in GitHub Actions — every file shows the same HEAD commit timestamp (2026-08-02T08:02:20Z, ~2h ago). This is the [[skill-freshness-mtime-blind-in-gha]] structural limitation; true ages are longer but cannot be recovered without full history. Since all thresholds are ≥4h and the batch ran this morning, the OK verdict is correct: no producer has been silent longer than this morning's run window.

The `articles/` directory is empty on `main` — skills that write articles open PRs, which are currently blocked by [[github-actions-cannot-create-prs]]. This means the article-class freshness check has nothing to score. If and when PRs are unblocked and articles land on main, this audit will begin flagging stale article consumers immediately.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk git commit times — this skill measures nothing it does not also report.*
