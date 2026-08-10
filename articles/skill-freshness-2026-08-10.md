# Skill Freshness — 2026-08-10

**Verdict:** ✅ FRESHNESS_OK — no active cross-skill file dependencies found after filtering

*Audited 44 enabled skills · 0 dependencies scored · 0 flagged*

*Status: FRESHNESS_NO_CHANGE — fingerprint unchanged from 2026-08-09 run, within 7-day re-emit window*

## Flagged dependencies

*(none — no active cross-skill file dependencies survived filtering)*

## What this means per consumer

All 44 enabled consumers returned OK. After filtering (self-references, on-demand producers, disabled consumers, implicit references to files that never existed on disk), no scoreable cross-skill file dependencies remain.

**Key structural observations (not formal flags):**

1. **`articles/` directory is empty.** No articles files exist on disk. None of the 44 enabled consumers' SKILL.md files reference another enabled skill's article via a canonical `articles/{producer}-${today}.md` pattern, so no MISSING flags fire. However, article-producing skills (code-health, cost-report, ai-framework-watch, skill-analytics, skill-update-check, etc.) have produced no articles in this repo state.

2. **`agi-tracker` enabled but SKILL.md missing.** `skills/agi-tracker/` directory does not exist. The skill runs as a no-op (see [[agi-tracker-missing-skill-md-dispatches-no-op]]). Cannot check for implicit file dependencies; counted in consumer total, no deps extracted.

3. **GHA mtime-blind structural limitation.** This repo is a single-commit snapshot (all files share mtime `2026-08-10T07:54:27Z`). The `stat --format=%Y` approach per [[skill-freshness-mtime-blind-in-gha]] would show all files as equally fresh. Content timestamps used where available to verify; actual freshness confirmed via file content dates (compute-pulse.md: 2026-08-08 ✓, surplus-pulse.md: 2026-08-09 ✓, notegraph.json: 2026-08-10 ✓, planner-state.json: 2026-08-10 ✓). Recommend fixing to `git log -1 --format=%ct` per open MEMORY.md item.

## Healthy consumers

All 44 enabled consumers — 0 scoreable deps each (no active cross-skill file reads after filtering).

Notable consumers with configuration gaps (not freshness failures):

- **repo-revive** — reads `memory/topics/watched-repos.md` (MISSING, implicit ref → ignored) + `memory/topics/stale-models.md` (MISSING, implicit ref → ignored). Skill will short-circuit with `REPO_REVIVE_NO_CONFIG`.
- **pr-review** — reads `memory/topics/pr-review-rules.md` (MISSING, implicit ref → ignored). Skill lacks fleet-wide review rules file.
- **surplus-pulse** — reads `memory/topics/projects.md` (MISSING, implicit ref → ignored). Compute-futures integration status not yet committed.
- **compute-pulse** — reads `memory/topics/compute-tokens.md` (optional, MISSING, implicit ref → ignored). Falls back to default DePIN sweep.
- **heartbeat** — reads `articles/token-report-*.md` (producer: `token-report`, disabled/on_demand → skip per freshness rules).

*+ 39 more all-fresh consumers (no scoreable deps).*

## Source status

- `aeon.yml`: 183 entries, 44 enabled
- Explicit `chains: consume:` edges: 0 (all chains blocks commented out)
- Implicit references discovered: ~35 across 43 SKILL.MD files (1 missing: agi-tracker)
- Files not yet on disk (skipped — implicit references that never existed): 7
  - `memory/topics/projects.md` (surplus-pulse)
  - `memory/topics/compute-tokens.md` (compute-pulse, optional)
  - `memory/topics/watched-repos.md` (repo-revive)
  - `memory/topics/stale-models.md` (repo-revive, optional)
  - `memory/topics/pr-review-rules.md` (pr-review)
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate write target, on unmerged branch)
  - `memory/topics/skills-history.md` (memory-flush archive target)
- Self-references filtered: ~20+ (producer prefix matches consuming skill name)
- On-demand producer deps skipped: 2 (heartbeat ← token-report, vuln-scanner ← github-trending)
- Active cross-skill deps scored: 0

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report. Known limitation: GHA mtime-blind in single-commit snapshots; fix pending per [[skill-freshness-mtime-blind-in-gha]].*
