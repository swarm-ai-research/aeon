# Skill Freshness — 2026-08-08

**Verdict:** ✅ FRESHNESS_OK — all scored dependencies are within threshold

*Audited 44 enabled skills · 2 dependencies scored · 0 flagged*

## Flagged dependencies

*(none)*

## What this means per consumer

All enabled consumers with scoreable dependencies are fresh. No action required.

## Healthy consumers

- pr-tracker — 1 dep (`memory/topics/pr-status.md`, 1.7h old, threshold 168h), all fresh.
- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`, 1.7h old, threshold 720h), all fresh.

+ 42 more all-fresh consumers (no scoreable deps discovered).

## Dependency scan detail

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| pr-tracker | `memory/topics/pr-status.md` | topics | 1.7h | ✅ OK |
| stale-content-pr-sweeper | `memory/state/notegraph.json` | state | 1.7h | ✅ OK |

### Implicit references not scored (per-class reasoning)

| Consumer | Reference | Reason skipped |
|----------|-----------|----------------|
| compute-macro-correlate | `memory/topics/compute-futures-macro-correlations.md` | Implicit dep, file never existed on disk |
| compute-pulse | `memory/topics/compute-tokens.md` | Implicit dep, file never existed on disk |
| fleet-control | `articles/fleet-status-${today}.md` | Producer `fleet-status` is `on_demand` — no expected cadence |
| memory-flush | `memory/topics/skills-history.md` | Implicit dep, file never existed on disk |
| repo-revive | `memory/topics/watched-repos.md` | Implicit dep, file never existed on disk |
| repo-revive | `memory/topics/stale-models.md` | Implicit dep, file never existed on disk |
| skill-freshness | `articles/foo-2026-01-01.md` | Producer `foo-2026-01-01` is `on_demand` (example path in prose) |
| surplus-pulse | `memory/topics/projects.md` | Implicit dep, file never existed on disk |
| vuln-scanner | `.outputs/github-trending.md` | Implicit dep, file never existed on disk |

## Source status

- `aeon.yml`: 150+ entries, 44 enabled
- Implicit references discovered: 11
- Explicit `chains: consume:` edges: 0 (all chains currently commented out)
- Files not yet on disk (skipped — implicit references that never existed): 7
- On-demand producer refs (skipped — no expected cadence): 2

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk git-log timestamps — this skill measures nothing it does not also report.*
