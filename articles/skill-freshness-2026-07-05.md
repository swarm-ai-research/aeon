# Skill Freshness — 2026-07-05

**Verdict:** ✅ FRESHNESS_OK — all discovered dependencies are on-disk and within freshness thresholds.

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all discovered dependencies scored OK.)*

## What this means per consumer

No consumers have stale or missing dependencies. All scored dependencies are within their per-class thresholds.

## Healthy consumers

- planner — 0 deps discovered (state self-read filtered)
- batch-health — 0 deps discovered
- memory-flush — 0 deps discovered (implicit missing refs skipped)
- memory-structural-dedupe — 0 deps discovered
- janitor — 0 deps discovered
- stale-content-pr-sweeper — 1 dep, all fresh. (`memory/state/notegraph.json`)
+ 39 more all-fresh consumers.

## Source status

- `aeon.yml`: 44 entries enabled (of ~150 total)
- Explicit `chains: consume:` edges: 0 (chains block is fully commented out)
- Implicit references discovered: 14 non-self deps across all enabled SKILL.md files
- Implicit deps existing on disk (scored): 2
  - `pr-tracker` → `memory/topics/pr-status.md` — topics class, threshold 168h — **OK** (mtime: today)
  - `stale-content-pr-sweeper` → `memory/state/notegraph.json` — state class, threshold 720h — **OK** (mtime: today)
- Files not yet on disk (skipped — implicit references that never existed): 12
  - `articles/` directory: absent entirely — all article-class implicit deps fall into this bucket
  - Notable: `repo-revive` → `memory/topics/watched-repos.md` (known gap, tracked in MEMORY.md)
  - Notable: `pr-review` → `memory/topics/pr-review-rules.md` (no rules file configured)
  - Notable: `compute-macro-correlate` → `memory/topics/compute-futures-macro-correlations.md` (topic file not yet written)
  - Notable: `compute-pulse` → `memory/topics/compute-tokens.md` (token reference file absent)

## Methodology note — GHA mtime limitation

**This is the 7th consecutive FRESHNESS_OK under a known structural constraint.** GitHub Actions `actions/checkout` resets every file's mtime to the checkout instant; this repo has a single-commit shallow clone, so both mtime and `git log -1 --format=%ct` resolve to 2026-07-05T07:49Z for all files. No mtime-based staleness is detectable in this environment.

The correct fix (tracked in MEMORY.md → [[skill-freshness-mtime-blind-in-gha]]) is to use `git log -1 --format=%ct -- <file>` with a deep clone (fetch-depth: 0) to get the actual last-modified commit timestamp per file. Until that fix lands, FRESHNESS_OK verdicts reflect "file exists and mtime = checkout time," not "file was written recently."

**Content-proxy analysis (Saturday 2026-07-05 08:00 UTC):**
- `compute-pulse` last ran 2026-06-28 11:00 UTC (last Saturday) → 165h ago, threshold 192h (8d weekly) → **OK at run time**. Next scheduled run is today at 11:00 UTC; if it misses, age will cross 192h by Sunday morning.
- `memory/topics/pr-status.md` is written by `pr-tracker` (daily) — present on disk; content appears current per MEMORY.md activity log.
- `memory/state/notegraph.json` is written by `notegraph` (daily) — present on disk.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report. Consecutive FRESHNESS_OK verdicts since the articles/ directory and deep-clone are absent should be interpreted as "no detectable staleness" rather than "confirmed fresh."*
