# Skill Freshness — 2026-07-30

**Verdict:** ✅ FRESHNESS_OK — all tracked dependencies within freshness thresholds

*Audited 44 enabled skills · 6 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies are within their freshness windows)*

## What this means per consumer

All 44 enabled consumers have dependencies within threshold. No action required from the freshness audit.

### Structural observation: articles/ directory is empty

The `articles/` directory contains zero files. This means no enabled skill has committed a dated article to the `main` branch. This is consistent with the documented ISS-001 / [[github-actions-cannot-create-prs]] blocker — skill runs that produce articles are branching and opening PRs, but those branches cannot merge to main without operator intervention (Repo Settings toggle or `AEON_GH_PAT`).

Under current rules, this does not trigger MISSING flags because:
1. No active `chains:` blocks → zero explicit chain dependencies
2. Cross-skill article reads in enabled SKILL.md files use wildcard globs (`articles/{skill}-*.md`), not the canonical `${today}` pattern that would fire MISSING for daily/weekly producers
3. The only `articles/{other}-${today}.md` references that survive the self-ref filter point to producers not named in `aeon.yml` (e.g. `fleet-status` ≠ `fleet-control`) → treated as on-demand → MISSING suppressed

This is a known gap in freshness coverage: the empty `articles/` directory is silent under the current rule set. A future enhancement could add explicit producer→article-path mappings to catch this class of staleness.

### Structural observation: snapshot timestamp masking

All on-disk files carry the same git commit timestamp (`2026-07-30T07:03:08Z`, the snapshot commit). The recommended fix — using `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]] — does not help here because a single-commit snapshot repo collapses all per-file histories to one point. As a result:

- `.outputs/*.md` (41 files): reported age ~2h → all OK vs 4h threshold
- `memory/topics/*.md` (7 files): reported age ~2h → all OK vs 168h threshold
- `memory/state/*.json` (4 files): reported age ~2h → all OK vs 720h threshold

True staleness for ISS-006-affected skills (heartbeat, batch-health, skill-freshness, gitlawb-fleet-metrics — all stuck at `last_dispatch: 2026-07-27T08:46:39Z`) is masked by the snapshot commit timestamp. In a live multi-commit repo, `git log -1 --format=%ct` would surface these as STALE; in the snapshot, the audit cannot detect them.

## Healthy consumers

All 44 enabled consumers pass. Sample (capped at 8; remainder collapsed):

- planner — 1 dep, all fresh. (`memory/state/planner-state.json`, ~2h, threshold 720h)
- notegraph — 1 dep, all fresh. (`memory/state/notegraph.json`, ~2h, threshold 720h)
- skillpacks — 1 dep, all fresh. (`memory/state/skillpacks.json`, ~2h, threshold 720h)
- surplus-pulse — 1 dep on-disk, all fresh. (`memory/topics/surplus-pulse.md`, ~2h, threshold 168h)
- compute-pulse — 1 dep on-disk, all fresh. (`memory/topics/compute-pulse.md`, ~2h, threshold 168h)
- ai-framework-watch — 0 tracked cross-skill deps.
- skill-health — 0 tracked cross-skill deps.
- heartbeat — 0 tracked cross-skill deps. (Implicit `articles/token-report-*.md` ref never existed → skipped per rule.)

+ 36 more all-fresh consumers (all `.outputs/` deps: 41 files, ~2h, threshold 4h).

## Source status

- `aeon.yml`: 180+ entries parsed, 44 enabled
- Active `chains:` blocks: 0 (all commented out)
- Explicit `chains: consume:` edges: 0
- Implicit references discovered: ~120 (across 44 enabled SKILL.md files)
- Implicit cross-skill references surviving self-ref filter: ~6
- Files not yet on disk (skipped — implicit references that never existed): ~30 (includes `memory/topics/projects.md`, `.outputs/github-trending.md`, `memory/topics/compute-tokens.md`, `articles/push-recap-*.md`, etc.)
- Canonical `articles/{producer}-${today}.md` MISSING candidates: 0 (all either self-ref or producer not in aeon.yml → on-demand cadence → suppressed)

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk file timestamps (git log or stat) — this skill measures nothing it does not also report. Known structural limitation in single-commit snapshot repos: all file ages collapse to the snapshot commit timestamp, masking true staleness. See [[skill-freshness-mtime-blind-in-gha]].*
