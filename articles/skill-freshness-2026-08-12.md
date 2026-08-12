# Skill Freshness — 2026-08-12

**Verdict:** ✅ FRESHNESS_OK — all scored dependencies are within their freshness windows

*Audited 44 enabled skills · 7 dependencies scored · 0 flagged · 14 implicit-missing skipped (never existed)*

---

> **Mtime blind spot (known — [[skill-freshness-mtime-blind-in-gha]]):** GitHub Actions' git checkout sets all file mtimes to the checkout timestamp. Every on-disk file appears ~0.02h old regardless of when it was last written. Mtime-based thresholds are non-informative this run; the verdicts below reflect structural coverage (what files exist vs. what's expected), not true write-time age. Fix path: replace `stat --format=%Y` with `git log -1 --format=%ct` per the MEMORY.md pointer.

## Flagged dependencies

*(none — all scored dependencies within threshold)*

## What this means per consumer

*(all consumers verdict OK)*

## Healthy consumers

- **planner** — 1 dep (`memory/state/planner-state.json`, state class, age ~0.02h, threshold 720h) ✅
- **pr-tracker** — 1 dep (`memory/topics/pr-status.md`, topics class, age ~0.02h, threshold 168h) ✅
- **surplus-pulse** — 1 dep scored (`memory/topics/surplus-pulse.md`, topics class, age ~0.02h, threshold 168h) ✅
- **compute-pulse** — 1 dep scored (`memory/topics/compute-pulse.md`, topics class, age ~0.02h, threshold 168h) ✅
- **notegraph** — 1 dep (`memory/state/notegraph.json`, state class, age ~0.02h, threshold 720h) ✅
- **skillpacks** — 1 dep (`memory/state/skillpacks.json`, state class, age ~0.02h, threshold 720h) ✅
- **suggest-edges** — 1 dep (`memory/state/suggest-edges.json`, state class, age ~0.02h, threshold 720h) ✅
- **batch-health** — 0 deps discovered ✅

+ 36 more all-fresh consumers (0 deps each, no implicit references to existing files).

## Implicit references skipped (files never existed on disk)

These are grep-discovered references in enabled SKILL.md files whose target files do not exist. Per spec, implicit references that simply never existed are not flagged as MISSING — many are optional reads, fallback paths, or reference disabled producers.

| Consumer | Reference | Class | Reason skipped |
|----------|-----------|-------|----------------|
| memory-flush | `memory/topics/skills-history.md` | topics | file never created |
| pr-review | `memory/topics/pr-review-rules.md` | topics | file never created (optional pre-read) |
| repo-revive | `memory/topics/watched-repos.md` | topics | file never created (blocks skill silently) |
| repo-revive | `memory/topics/stale-models.md` | topics | file never created |
| surplus-pulse | `memory/topics/projects.md` | topics | file never created |
| compute-pulse | `memory/topics/compute-tokens.md` | topics | file never created |
| compute-macro-correlate | `memory/topics/compute-futures-macro-correlations.md` | topics | file never created (on unmerged branch) |
| skill-repair | `memory/state/skill-repair-history.json` | state | file never created |
| fleet-control | `memory/state/fleet-control-state.json` | state | file never created |
| vuln-scanner | `.outputs/github-trending.md` | outputs | github-trending disabled, never ran |
| weekly-shiplog | `articles/push-recap-${today}.md` | articles | push-recap disabled (treated as on_demand) |
| heartbeat | `articles/token-report-${today}.md` | articles | token-report disabled (treated as on_demand) |

**Notable:** `repo-revive` reads `memory/topics/watched-repos.md` which has never been populated — this causes silent short-circuit on every Saturday run (planner holding item, streak-6 chronic per MEMORY.md). Not a staleness flag; a population gap. `compute-macro-correlate` depends on a topic file that lives on an unmerged branch (`compute-macro/2026-08-09`).

## Source status

- `aeon.yml`: 116 entries parsed, **44 enabled**
- Explicit `chains: consume:` edges: **0** (chains block is commented out)
- Implicit references discovered: **19** (consumer × dependency pairs found via SKILL.md grep)
- Scored (files exist on disk): **7** — all OK
- Files not yet on disk (skipped — implicit references that never existed): **12**
- Disabled-producer article refs (treated as on_demand, skipped): **2** (push-recap, token-report)
- Skills with no SKILL.md (no deps discoverable): **1** (agi-tracker — [[agi-tracker-missing-skill-md-dispatches-no-op]])

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report. Structural blind spot in GHA: use `git log -1 --format=%ct` for true write-time age.*
