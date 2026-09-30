# Skill Freshness — 2026-09-30

**Verdict:** ✅ FRESHNESS_OK — all 2 tracked dependencies fresh across 44 enabled consumers

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all tracked dependencies within freshness thresholds.)*

## What this means per consumer

*(All consumers OK — no action required.)*

## Healthy consumers

- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`, 23h old, threshold 720h), all fresh.
- pr-tracker — 1 dep (`memory/topics/pr-status.md`, 23h old, threshold 168h), all fresh.
- planner — 0 tracked deps, all fresh.
- batch-health — 0 tracked deps, all fresh.
- notegraph — 0 tracked deps, all fresh.
- suggest-edges — 0 tracked deps, all fresh.
- heartbeat — 0 tracked deps, all fresh.
- skill-health — 0 tracked deps, all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~153 total entries, 44 enabled
- Implicit references discovered: 11
- Explicit `chains: consume:` edges: 0
- Files not yet on disk (skipped — implicit references that never existed): 9

### Skipped implicit references (never-existed on disk)

The following file references were grep-discovered in enabled SKILL.md files but the paths do not exist on disk. Per skill design, implicit MISSING is not flagged — these may be pseudocode citations, future planned files, or paths from disabled dependency chains.

| Consumer | Path | Path class |
|----------|------|------------|
| memory-flush | `memory/topics/skills-history.md` | topics |
| pr-review | `memory/topics/pr-review-rules.md` | topics |
| repo-revive | `memory/topics/watched-repos.md` | topics |
| repo-revive | `memory/topics/stale-models.md` | topics |
| surplus-pulse | `memory/topics/projects.md` | topics |
| compute-pulse | `memory/topics/compute-tokens.md` | topics |
| compute-macro-correlate | `memory/topics/compute-futures-macro-correlations.md` | topics |
| vuln-scanner | `.outputs/github-trending.md` | outputs |
| heartbeat | `articles/token-report-2026-04-28.md` | articles |

Note: `repo-revive`, `pr-review`, and several others reference topic files that have never been created. This is a known operational gap (see MEMORY.md "watched-repos config missing" — streak 56+). These consumers short-circuit gracefully when their dependency files are absent, but this represents untracked silent-empty runs.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git commit timestamps (`git log -1 --format=%ct`) — on-disk mtime is unreliable in GitHub Actions checkouts.*
