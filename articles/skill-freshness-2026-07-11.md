# Skill Freshness — 2026-07-11

**Verdict:** ✅ FRESHNESS_OK — all audited cross-skill dependencies are fresh

*Audited 44 enabled skills · 2 cross-skill dependencies checked · 0 flagged*

## Flagged dependencies

*(None — no flagged rows this run.)*

## Healthy consumers

- suggest-edges — 1 dep (`memory/state/notegraph.json`), fresh (~2h, notegraph ran 06:39 UTC today).
- compute-macro-correlate — 1 dep (`memory/topics/compute-futures-eda/*.md`), fresh (compute-futures-eda ran 06:42 UTC today; latest EDA file ≤24h).
- + 42 more enabled skills — 0 audited cross-skill deps (self-references filtered; broad `articles/` and `memory/topics/*.md` reads excluded as non-pattern-specific).

## What this means per consumer

All cross-skill consumer-producer edges are within threshold. No action required.

**Note on articles/ directory:** The `articles/` directory contains no files on the main branch — skill article outputs are committed to dated branches that accumulate in pull requests. No enabled consuming skill explicitly references another enabled producer's article output (the two disabled skills that do — `operator-scorecard` and `signal-verdict` — are not audited as consumers). MISSING is not triggered.

## Source status

- `aeon.yml`: 131 skill entries, 44 enabled
- Implicit cross-skill references discovered: 2
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out)
- Self-references filtered (own outputs, own state): ~12
- Broad reads excluded (non-pattern-specific `articles/`, `memory/topics/*.md`): ~4
- Files not yet on disk (skipped — implicit references that never existed): 0

**Age methodology note:** GHA snapshot checkout assigns the same mtime (2026-07-11 08:27 UTC) to every file, and the single-commit repo history (`git log -1 --format=%ct`) returns the same snapshot epoch for all paths. Producer ages derived from `memory/cron-state.json` `last_success` timestamps — the most reliable per-skill run-time record available. This is a known structural limitation per [[skill-freshness-mtime-blind-in-gha]]; the fix (`git log -1 --format=%ct` per file in a multi-commit history) will restore true mtime-based detection once the repo has per-file commit history.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
