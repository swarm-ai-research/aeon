# Skill Freshness — 2026-10-06

**Verdict:** ✅ FRESHNESS_OK — all 2 tracked dependencies are fresh

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all dependencies are within their freshness windows)*

## What this means per consumer

All enabled consumers with tracked dependencies are reading fresh files. No action required.

## Healthy consumers

- stale-content-pr-sweeper — 1 dep, all fresh. (`memory/state/notegraph.json` — 19h old, threshold 720h)
- pr-tracker — 1 dep, all fresh. (`memory/topics/pr-status.md` — 19h old, threshold 168h)
- + 42 more all-fresh consumers (0 tracked deps each — no cross-skill file reads detected).

## Observations (outside formal verdict scope)

Several producer skills have not written a fresh article in significantly longer than their cadence, indicating ISS-006 casualties. No enabled consumer currently depends on these articles, so they do not affect the fleet verdict — but they are signals of dark producers:

| Producer | Last article | Age | Cadence | Status |
|----------|-------------|-----|---------|--------|
| skill-freshness | 2026-10-04 | 48h | daily | Missed 2026-10-05 (08Z pocket, ISS-006 day-2) |
| skill-analytics | 2026-09-16 | 480h | weekly (Wed) | STALE — 20 days dark, ISS-006 Wed 18:30Z slot |
| skill-evals | 2026-09-13 | 552h | weekly (Sun) | STALE — 23 days dark, ISS-006 Sun 09Z slot |
| self-review | 2026-09-13 | 552h | weekly (Sun) | STALE — 23 days dark, ISS-006 Sun 18:30Z slot |

These would become consumer-facing staleness issues if any enabled skill begins consuming them. Currently the only trackers (operator-scorecard, signal-verdict) are disabled.

**Methodology note:** On-disk mtimes are unreliable in GitHub Actions (git checkout resets them). Ages above are derived from git commit timestamps (`git log -1 --format=%ct`). All files in this snapshot share a 19h git timestamp from a bulk commit at 2026-10-05 12:42Z — the memory/topics and memory/state ages reflect that commit, not the last time the file's content was semantically updated. Article ages use filename-date parsing as the authoritative source.

## Source status

- `aeon.yml`: 73 entries, 44 enabled
- Implicit references discovered: 2
- Explicit `chains: consume:` edges: 0
- Files not yet on disk (skipped — implicit references that never existed): 11

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
