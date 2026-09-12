# Skill Freshness — 2026-09-12

**Verdict:** ✅ FRESHNESS_OK — all enabled consumer dependencies are within freshness thresholds

*Audited 44 enabled skills · 36 dependencies checked · 0 flagged*

## Flagged dependencies

None. All checked dependencies are within their per-class freshness thresholds.

## What this means per consumer

No consumers are degraded. All enabled skills with trackable file dependencies are reading fresh data.

## Healthy consumers

- planner — 2 deps (planner-state.json, daily-plan state), all fresh.
- heartbeat — token-report-*.md optional (producer disabled, skipped), all fresh.
- surplus-pulse — 1 dep (topics/surplus-pulse.md, last run 2026-09-11), all fresh.
- fleet-control — 2 deps (fleet-control-state.json, fleet-status prior), all fresh.
- compute-futures-eda — 1 dep (topics/compute-futures-eda/2026-09-07.md), all fresh.
- notegraph — 1 dep (state/notegraph.json), all fresh.
- suggest-edges — 1 dep (state/suggest-edges.json), all fresh.
- skillpacks — 1 dep (state/skillpacks.json), all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 136 entries, 44 enabled
- Implicit references discovered: 36
- Explicit `chains: consume:` edges: 0 (all chains currently commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6 (watched-repos.md, stale-models.md, projects.md, skills-history.md, pr-review-rules.md, compute-futures-macro-correlations.md — all implicit-only, MISSING not fired per spec)

### Key articles checked

| Producer | Most Recent Article | Age | Cadence | Threshold | Severity |
|----------|-------------------|-----|---------|-----------|----------|
| cost-report | cost-report-2026-09-07.md | 120h | weekly | 192h | ✅ OK |
| vuln-scanner | vuln-scan-2026-09-05.md | 168h | weekly | 192h | ✅ OK |
| skill-freshness | skill-freshness-2026-09-11.md | 24h | daily | 28h | ✅ OK |

### Notable non-flagged conditions

- **`memory/topics/watched-repos.md` MISSING** — 6 skills (code-health, github-monitor, issue-triage, changelog, weekly-shiplog, repo-revive) reference this file but it does not exist. Per spec, MISSING is not fired for implicit grep-discovered references. These skills self-gate cleanly when the file is absent. Open action item: populate `memory/watched-repos.md` or disable the 6 dependents (see MEMORY.md action queue, streak-41 of the watched-repos short-circuit cluster).
- **`memory/topics/compute-pulse.md` age 504h** — compute-pulse last ran 2026-08-22 (21 days). Self-reference excluded from freshness scoring; no downstream consumers of this topic file were found in enabled SKILL.md files. compute-pulse runs Sat 11:00 UTC — today's run is expected.
- **`vuln-scan-2026-09-05.md` at 168h** — exactly at the 192h weekly threshold (28h grace window remains). vuln-scanner runs Sat 16:00 UTC; today's scan is scheduled and within the grace window.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk timestamps — this skill measures nothing it does not also report. Note: in GitHub Actions, file mtime equals checkout time; this run used filename-embedded dates for articles and JSON-embedded timestamps for state files per [[skill-freshness-mtime-blind-in-gha]].*
