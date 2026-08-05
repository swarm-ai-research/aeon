# Skill Freshness — 2026-08-05

**Verdict:** ✅ FRESHNESS_OK — all checked dependencies fresh; no flagged rows

*Audited 44 enabled skills · 1 dependency checked · 0 flagged*

## Flagged dependencies

*(none — all checked dependencies are within freshness thresholds)*

## What this means per consumer

All enabled consumers have either fresh dependencies or no tracked cross-skill dependencies on disk. No action required.

**Structural note — `articles/` is empty on main:** Every daily and weekly skill that writes article files (heartbeat, batch-health, reflect, planner, skill-health, code-health, etc.) is running and generating output, but those articles live on unmerged branches due to [[github-actions-cannot-create-prs]]. Implicit article references in SKILL.md files (e.g. `heartbeat → articles/token-report-*.md`) resolve to zero files on main and are classified as never-existed implicit refs → not flagged. This is a known structural state, not a freshness signal.

## Healthy consumers

- pr-tracker — 1 dep (`memory/topics/pr-status.md`), fresh (≤2h, threshold 168h).
- planner — 0 cross-skill deps checked (state self-managed).
- notegraph — 0 cross-skill deps checked (state self-managed).
- skillpacks — 0 cross-skill deps checked (state self-managed).
- surplus-pulse — 0 cross-skill deps checked (state self-managed).
- compute-pulse — 0 cross-skill deps checked (state self-managed).
- compute-futures-eda — 0 cross-skill deps checked (output self-managed; most recent topic file `2026-08-03.md`).
- heartbeat — 0 cross-skill deps checked (`articles/token-report-*.md` is optional/skipped-silently; `token-report` is disabled).
+ 36 more all-fresh consumers (no surviving cross-skill deps — all implicit refs either self-managed or never-existed on main).

## Source status

- `aeon.yml`: 120 entries parsed, 44 enabled
- Explicit `chains: consume:` edges: 0 (daily-routine chain commented out; no other active chains)
- Implicit references discovered: ~20 across 44 SKILL.md files
- Surviving cross-skill deps (existing on disk, not self-refs): 1
- Files not yet on disk — skipped (implicit refs that never existed): ~12
  - All of `articles/` (empty directory — 0 article files on main; blocked PRs)
  - `memory/topics/pr-review-rules.md` (pr-review)
  - `memory/topics/projects.md` (surplus-pulse)
  - `memory/topics/watched-repos.md` (repo-revive)
  - `memory/topics/stale-models.md` (repo-revive)
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate; on unmerged branch)
  - `memory/state/suggest-edges.json` (suggest-edges)
  - `memory/state/fleet-control-state.json` (fleet-control; created on first run)

**Known GHA mtime limitation:** On-disk mtimes reflect the git checkout time, not individual file modification times. Ages computed from stat mtime are therefore near-zero for all files. For this run, freshness was inferred from filename-embedded dates (compute-futures-eda topic files) and git-log commit timestamps. The structural fix — `git log -1 --format=%ct` per file — is tracked in [[skill-freshness-mtime-blind-in-gha]].

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
