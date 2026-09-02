# Skill Freshness — 2026-09-02

**Verdict:** 🔴 FRESHNESS_STALE — 1 dependency past 2× staleness threshold across 1 of 44 enabled consumers

*Audited 44 enabled skills · 7 implicit references discovered · 1 dependency scored · 1 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| vuln-scanner | `.outputs/github-trending.md` | outputs | 8h 50m | 🔴 STALE |

## What this means per consumer

> **vuln-scanner** — depends on 1 cross-skill file; 1 flagged. Worst: `.outputs/github-trending.md` last updated ~8h 50m ago (threshold 4h, class outputs, 2× = 8h). The producer `github-trending` has `enabled: false` in `aeon.yml` — it will never produce fresh output under the current schedule. `vuln-scanner` references this file as its auto-select source for target repos and should fall back to the GitHub trending API when absent or stale. Suggested action: Verify `vuln-scanner` SKILL.md fallback path (line 30: `if [ -s .outputs/github-trending.md ]`) triggers correctly when the file is stale; or re-enable `github-trending` if a live feed is desired.

## Healthy consumers

- planner — 0 cross-skill deps, all fresh.
- batch-health — 0 cross-skill deps, all fresh.
- memory-flush — 0 cross-skill deps (broad articles/ scan finds nothing; articles/ was empty this run).
- reflect — 0 cross-skill deps (broad articles/ scan finds nothing; articles/ was empty this run).
- self-review — 0 cross-skill deps, all fresh.
- heartbeat — 1 optional dep (`articles/token-report-*.md`); producer disabled, file absent — silently skipped per SKILL.md.
- weekly-shiplog — 1 optional dep (`articles/push-recap-*.md`); producer disabled, file absent — silently skipped.
- suggest-edges — 1 dep (`notegraph.json` at repo root); file exists, age 8h 50m — outside standard path-class scope, not scored.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 180 entries parsed, 44 enabled
- Implicit references discovered: 7
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6

---

### Methodology note — GHA mtime-blind workaround

On GitHub Actions runners all checked-out files share the same mtime (checkout time). Ages in this report use `git log -1 --format=%ct` per-file rather than `stat --format=%Y`. This is the documented fix for [[skill-freshness-mtime-blind-in-gha]] (pending SKILL.md patch). The single-commit history in this run means all files share git timestamp 2026-09-02T00:15:07Z (age ≈ 8h 50m relative to run time). For `.outputs/` class the threshold is 4h — so all .outputs/ files in isolation are STALE — but skill-freshness only flags files that are *consumed* cross-skill, and only `github-trending` → `vuln-scanner` is an active cross-skill read.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes (git log timestamps on GHA) — this skill measures nothing it does not also report.*
