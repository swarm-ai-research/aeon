# Skill Freshness — 2026-08-23

**Verdict:** ✅ FRESHNESS_OK — all scored dependencies are fresh

*Audited 44 enabled skills · 2 cross-consumer dependencies scored · 0 flagged*

## Flagged dependencies

*(None — all dependencies within freshness thresholds.)*

## What this means per consumer

All enabled consumers that have scoreable cross-consumer dependencies are reading fresh files.

## Healthy consumers

- **stale-content-pr-sweeper** — 1 dep (`memory/state/notegraph.json`), fresh (0.055h, threshold 720h).
- **pr-tracker** — 1 dep (`memory/topics/pr-status.md`), fresh (0.055h, threshold 168h).
+ 42 more enabled skills with no scoreable cross-consumer dependencies (self-state reads filtered; implicit references to non-existent files not flagged).

## Source status

- `aeon.yml`: 44 entries parsed, 44 enabled
- Implicit references discovered: 22
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 12
- Self-state reads filtered: 8

### Notes on methodology

All on-disk files show mtime ≈ checkout time (age ~0.055h) due to the [[skill-freshness-mtime-blind-in-gha]] limitation — git checkout sets all file timestamps to the current time in GHA, making every file appear fresh regardless of actual historical age. This is a known structural gap (see MEMORY.md for the fix: use `git log -1 --format=%ct` instead of `stat --format=%Y`). Result: this run cannot detect staleness that predates today's checkout.

Articles directory is empty (0 files) — all `articles/{skill}-${today}.md` references in SKILL.md files are implicit grep-discovered references; since these never existed as on-disk files, they are not flagged per the MISSING-implicit-suppression rule. This is expected for a fleet that has recently had its history reset.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
