# Skill Freshness — 2026-08-18

**Verdict:** ✅ FRESHNESS_OK — all 2 checked dependencies are within freshness thresholds

*Audited 45 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all checked dependencies are fresh.)*

## Healthy consumers

- **pr-tracker** — 1 dep checked, all fresh. (`memory/topics/pr-status.md`, 0.1h old, threshold 168h)
- **stale-content-pr-sweeper** — 1 dep checked, all fresh. (`memory/state/notegraph.json`, 0.1h old, threshold 720h)

+ 43 more consumers with 0 discovered dependencies (trivially OK).

The following 6 consumers have implicit file references that have never existed on disk (skipped per policy — implicit references that simply never materialized are not flagged):

- **heartbeat** — `articles/token-report-*.md` (optional read per SKILL.md; articles/ directory does not exist)
- **memory-flush** — `memory/topics/skills-history.md`
- **repo-revive** — `memory/topics/stale-models.md`, `memory/topics/watched-repos.md`
- **skill-freshness** — `articles/foo-2026-01-01.md` (example placeholder in SKILL.md)
- **surplus-pulse** — `memory/topics/projects.md`
- **vuln-scanner** — `.outputs/github-trending.md` (github-trending is disabled)

## Source status

- `aeon.yml`: 188+ entries, 45 enabled
- Implicit references discovered: 8
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
