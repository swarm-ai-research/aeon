# Skill Freshness — 2026-08-21

**Verdict:** ✅ FRESHNESS_OK — all checked dependencies are within freshness thresholds

*Audited 44 enabled skills · 3 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all checked dependencies are fresh)*

## What this means per consumer

No consumers have stale or missing dependencies. All three checked dependencies are well within their freshness windows.

## Healthy consumers

- pr-tracker — 1 dep (`memory/topics/pr-status.md`, ~1.3h, threshold 168h), all fresh.
- skill-freshness — 1 dep (`memory/topics/skill-freshness-state.json`, ~1.3h, threshold 168h), all fresh.
- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`, ~1.3h, threshold 720h), all fresh.
- + 41 more consumers with no dependencies discovered (0 checked deps each).

## Source status

- `aeon.yml`: 44+ entries, 44 enabled
- Implicit references discovered: 12 (surviving filter — self-refs, self-outputs, optional disabled-skill deps removed)
- Explicit `chains: consume:` edges: 0 (all chain definitions are currently commented out)
- Files not yet on disk (skipped — implicit references that never existed): 9

### Implicit refs skipped (missing topics — implicit rule, not flagged)

These topic files are referenced in SKILL.md files but do not exist on disk. Per audit rules, implicit references to files that have never existed are not flagged — they are informational only.

| Consumer | Reference | Status |
|----------|-----------|--------|
| ai-framework-watch | `memory/topics/framework-watch-state.json` | never created |
| compute-macro-correlate | `memory/topics/compute-futures-macro-correlations.md` | on unmerged branch `compute-macro/2026-08-16` |
| compute-pulse | `memory/topics/compute-tokens.md` | never created |
| memory-flush | `memory/topics/skills-history.md` | never created |
| pr-review | `memory/topics/pr-review-rules.md` | never created |
| repo-revive | `memory/topics/watched-repos.md` | chronic missing — see [[watched-repos-config-missing-silent-short-circuits-6-skills]] |
| repo-revive | `memory/topics/stale-models.md` | never created |
| skill-graph | `memory/topics/skill-graph-state.json` | never created |
| surplus-pulse | `memory/topics/projects.md` | never created |

Note: `articles/` directory does not exist on disk. Fleet-control and vuln-scanner reference article paths that are their own outputs (filtered as self-references); heartbeat's `articles/token-report-*.md` dependency is explicitly marked optional and its producer (`token-report`) is disabled.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk git log timestamps — this skill measures nothing it does not also report.*
