# Skill Freshness — 2026-07-04

**Verdict:** ✅ FRESHNESS_OK — all scored dependencies are within their freshness thresholds

*Audited 44 enabled skills · 3 dependencies checked · 0 flagged*

> **⚠ Structural note:** This is the 6th consecutive FRESHNESS_OK emit. The prescribed mtime-based check is blind in GitHub Actions because `actions/checkout` resets all file mtimes to the run instant — see [[skill-freshness-mtime-blind-in-gha]]. This run uses content-embedded date strings (`Last run:`, `last_run:` fields) as a proxy for actual producer freshness. Fix pending: switch to `git log -1 --format=%ct` per MEMORY.md Next priorities.

## Flagged dependencies

*(none)*

## Healthy consumers

- planner — 1 dep (`memory/state/planner-state.json`, 23.6h old, threshold 720h), all fresh.
- surplus-pulse — 1 dep (`memory/topics/surplus-pulse.md`, ~1d old, threshold 168h), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`, ~165h old, threshold 168h), all fresh. **Borderline: 98.2% of threshold. Will tip to WARN if compute-pulse does not run Saturday 2026-07-05 at 11:00 UTC.**

+ 41 more all-fresh consumers (no scoreable deps resolved).

## Implicit-missing references (not flagged — never existed)

These are grep-discovered references that have never been on disk. Per skill rules, `MISSING` only fires for explicit chain consume entries or canonical today-pattern articles. Documented here for operator awareness:

| Consumer | Missing path | Producer status |
|----------|-------------|-----------------|
| pr-review | `memory/topics/pr-review-rules.md` | never created |
| repo-revive | `memory/topics/watched-repos.md` | never created |
| repo-revive | `memory/topics/stale-models.md` | never created |
| surplus-pulse | `memory/topics/projects.md` | never created |
| compute-pulse | `memory/topics/compute-tokens.md` | never created |
| vuln-scanner | `.outputs/github-trending.md` | github-trending disabled |
| heartbeat | `articles/token-report-*.md` | token-report disabled |
| weekly-shiplog | `articles/push-recap-*.md` | push-recap disabled |

**Articles directory:** `articles/` did not exist on disk prior to this run (created now). No enabled skill has ever written an article in this deployment. Skills like `reflect` and `self-review` that read `articles/` for the last 7 days will see zero entries — normal given current fleet configuration (content-generating skills are disabled).

## Source status

- `aeon.yml`: 44 skills with `enabled: true` (all audited)
- Chains active: 0 (all chain definitions are commented out)
- Explicit `chains: consume:` edges: 0
- Implicit references discovered: 11
- Scored (file exists on disk): 3
- Files not yet on disk (skipped — implicit references that never existed): 8

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk content date strings — this run uses content-embedded dates rather than mtimes due to the GHA checkout mtime reset limitation.*
