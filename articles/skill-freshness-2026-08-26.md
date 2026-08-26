# Skill Freshness — 2026-08-26

**Verdict:** ✅ FRESHNESS_OK — all audited dependencies are within freshness thresholds

*Audited 44 enabled skills · 7 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies are fresh.)*

## What this means per consumer

*(No consumers with verdict ≠ OK.)*

## Healthy consumers

- planner — 1 dep, all fresh. (`memory/state/planner-state.json`, age ~1.6h, threshold 720h)
- reflect — 6 deps, all fresh. (`memory/topics/` MOCs, age ~1.6h, threshold 168h)
+ 42 more all-fresh consumers.

## Source status

- `aeon.yml`: 155 entries, 44 enabled
- Implicit references discovered: 7
- Explicit `chains: consume:` edges: 0 (all chains sections commented out)
- Files not yet on disk (skipped — implicit references that never existed): 0

### Methodology note — GHA mtime-blind limitation active

File ages derived from git commit timestamps rather than stat mtimes (per [[skill-freshness-mtime-blind-in-gha]]). This repo currently has a single root commit (`310bccd`, 2026-08-26T06:51:34Z), so all tracked files report the same age (~1.6h at audit time). File ages are accurate for files committed in this snapshot; the per-file historical accuracy gap is the known pending fix (`git log -1 --format=%ct` per-file lookup once multi-commit history is established).

`articles/` is absent from the repo tree — skill articles are ephemeral (written per-run, not committed to git). No enabled inter-skill consumer has a canonical `articles/{producer}-${today}.md` dependency that would trigger MISSING detection:
- Self-referential reads (skill-evals, swarm-safety-eval reading own prior articles) → filtered.
- Broad `articles/*` reads (reflect, self-review) → implicit, no canonical producer pattern → no MISSING trigger.
- weekly-shiplog → `articles/push-recap-*.md` (producer `push-recap` is `enabled: false` → cadence `on_demand` → skipped).

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk timestamps — this skill measures nothing it does not also report.*
