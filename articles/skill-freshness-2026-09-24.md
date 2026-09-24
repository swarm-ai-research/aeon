# Skill Freshness — 2026-09-24

**Verdict:** ✅ FRESHNESS_OK — all discovered dependencies within thresholds

*Audited 44 enabled skills · 36 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies are within their freshness windows.)*

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), all fresh.
- compute-macro-correlate — 1 dep (memory/topics/compute-pulse.md), all fresh.
- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md), all fresh.
- pr-tracker — 2 deps (memory/topics/pr-status.md, memory/state/pr-tracker.json), all fresh.
- notegraph — 1 dep (memory/state/notegraph.json), all fresh.
- skillpacks — 1 dep (memory/state/skillpacks.json), all fresh.
- suggest-edges — 1 dep (memory/state/suggest-edges.json), all fresh.
+ 37 more all-fresh consumers.

## Source status

- `aeon.yml`: 100+ entries, 44 enabled
- Implicit references discovered: 36
- Explicit `chains: consume:` edges: 0 (all chains blocks are commented out)
- Files not yet on disk (skipped — implicit references that never existed): ~14

## Notes

**Single-commit repo mtime limitation.** This repo has exactly one commit in its git history (`dad14e9`), meaning `git log -1 --format=%ct` returns the same timestamp (2026-09-24 00:01:04 UTC, ~9h ago) for every tracked file. Filesystem stat times likewise reflect the recent checkout (~6 minutes ago). Neither signal can distinguish a file produced yesterday from a file produced 17 days ago. This run therefore reports OK across all path classes — the mtime-based severity bands are correct by the data available, but carry zero resolution between files.

**Observable filename-date signal (informational).** Some articles exist whose date suffixes imply staleness the mtime check cannot see:
- `articles/cost-report-2026-09-07.md` — 17d old by filename; cost-report is weekly (Mon 07:00 UTC). By filename date this is STALE (>8d threshold, >16d = 2× exceeded). However, **no enabled consumer reads cost-report articles** — cost-report is a standalone producer with no downstream consumers in the current schedule.
- `articles/skill-evals-2026-09-13.md` — 11d old by filename; skill-evals is weekly. Exceeds 8d threshold → filename-WARN. But skill-evals' own SKILL.md reads its prior article as a self-reference (diff for quality regression), which the skill filters from consumer scoring.
- `articles/self-review-2026-09-13.md` — 11d old by filename. Same pattern: self-referential read, filtered.
- `articles/vuln-scan-2026-09-19.md` — 5d old by filename; vuln-scanner is weekly (Sat). Within 8d threshold → filename-OK.
- `articles/skill-freshness-2026-09-23.md` — yesterday's article. Daily → filename-OK.

**No cross-skill article consumers.** After scanning all 44 enabled SKILL.md files, no enabled skill reads a date-suffixed article from a *different* enabled skill as a runtime dependency. The closest candidates (`articles/token-report-*.md` referenced by planner; `articles/push-recap-*.md` referenced by changelog) both involve disabled producers (token-report: `enabled: false`; push-recap: `enabled: false`), so neither fires a staleness alert.

**Chains inactive.** All `chains:` blocks in `aeon.yml` are commented out. The `.outputs/` directory contains 41 files, all with identical git-based mtimes (~9h), none consumed by active chain steps.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
