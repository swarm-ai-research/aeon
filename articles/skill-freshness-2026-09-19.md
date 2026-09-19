# Skill Freshness — 2026-09-19

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within freshness thresholds

*Audited 44 enabled skills · 36 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all checked dependencies are within their freshness thresholds.)*

## What this means per consumer

No consumer has a degraded dependency. Every file-on-disk dependency scored OK against its per-class threshold.

## Healthy consumers

- planner — 2 deps, all fresh.
- batch-health — 1 dep, all fresh.
- notegraph — 1 dep, all fresh.
- skillpacks — 1 dep, all fresh.
- suggest-edges — 1 dep, all fresh.
- skill-health — 1 dep, all fresh.
- skill-analytics — 1 dep, all fresh.
- reflect — 1 dep, all fresh.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~176 entries, 44 enabled
- Implicit references discovered: 24
- Explicit `chains: consume:` edges: 0 (daily-routine chain is commented out — no active chain steps)
- Files not yet on disk (skipped — implicit references that never existed): 8

### Skipped implicit references (never-existed, not flagged)

| Consumer | Reference | Producer | Note |
|----------|-----------|----------|------|
| heartbeat | `articles/token-report-*.md` | token-report | Producer disabled; no articles ever written |
| weekly-shiplog | `articles/push-recap-*.md` | push-recap | Producer disabled; no articles ever written |
| vuln-scanner | `.outputs/github-trending.md` | github-trending | Producer disabled; file never created |
| surplus-pulse | `memory/topics/projects.md` | (operator config) | File not present; not a skill-produced dep |
| repo-revive | `memory/topics/watched-repos.md` | (operator config) | File missing; streak-48 known issue |
| repo-revive | `memory/topics/stale-models.md` | (operator config) | File not present |
| pr-review | `memory/topics/pr-review-rules.md` | (operator config) | File not present |
| compute-pulse | `memory/topics/compute-tokens.md` | (operator config) | File not present |

These implicit references were discovered by grepping each consumer's SKILL.md but do not fire as MISSING because no file has ever existed on disk for them (per methodology: implicit-only refs that simply never existed are not flagged).

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git commit timestamps (`git log -1 --format=%ct`) — this skill measures nothing it does not also report.*
