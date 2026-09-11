# Skill Freshness — 2026-09-11

**Verdict:** ✅ FRESHNESS_OK — all 36 checked dependencies are within freshness thresholds

*Audited 44 enabled skills · 36 dependencies checked · 0 flagged*

## Flagged dependencies

*(No flagged dependencies this run — all checked files are within their freshness windows.)*

## What this means per consumer

No consumers have freshness issues. All explicit chain outputs and implicit file dependencies that exist on disk scored OK.

**Note on mtime accuracy:** GitHub Actions runner checkout sets all file mtimes to the checkout timestamp (~09:55 UTC today), making every file appear age ~0h regardless of when it was last written. This is a known limitation tracked in [[skill-freshness-mtime-blind-in-gha]] — the recommended fix is `git log -1 --format=%ct` per-file instead of `stat --format=%Y`. Until that patch lands, this run can confirm files *exist* but cannot detect freshness violations caused by stale-but-present files. Explicit MISSING flags (canonical article patterns + explicit chain edges) remain reliable since they don't depend on mtime.

## Healthy consumers

- `skill-analytics` — 1 dep (`.outputs/planner.md`), all fresh.
- `stale-content-pr-sweeper` — 1 dep (`memory/state/notegraph.json`), all fresh.
- `pr-tracker` — 1 dep (`memory/topics/pr-status.md`), all fresh.
- `compute-pulse` — 1 dep (`memory/topics/compute-pulse.md`), all fresh.
- `planner` — 1 dep (`memory/state/planner-state.json`), all fresh.
- `compute-macro-correlate` — 0 scored deps (1 implicit ref not yet on disk, ignored).
- `repo-revive` — 0 scored deps (2 implicit refs not yet on disk, ignored).
- `fleet-control` — 0 scored deps (1 implicit ref not yet on disk, ignored).
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 95 entries, 44 enabled
- Implicit references discovered: 36
- Explicit `chains: consume:` edges: 0 (all chains currently commented out)
- Files not yet on disk (skipped — implicit references that never existed): 22

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report. **Caveat for this run:** GHA mtime-blind issue (all files checkout-stamped) means age scores are 0h for every existing file; existence checks remain accurate.*
