# Skill Freshness — 2026-09-18

**Verdict:** ✅ FRESHNESS_OK — all active cross-skill data flows are current

*Audited 44 enabled skills · 36 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all discovered dependencies are within freshness thresholds or not applicable.)*

## What this means per consumer

No enabled consumer is reading stale upstream data. The two consumers with cross-skill reads (heartbeat → `articles/token-report-*.md` and weekly-shiplog → `articles/push-recap-*.md`) both reference producers that are currently disabled (`enabled: false`); those producers carry no expected cadence, so MISSING does not fire and no freshness gap exists.

All `chains:` blocks in `aeon.yml` remain commented out, meaning the explicit dependency class (`.outputs/{skill}.md` via `consume:`) has zero active edges. Every enabled skill is effectively self-contained for this run.

**Notable observations (not dependency flags):**

- **skill-freshness output gap**: `articles/skill-freshness-2026-09-12.md` is the most recent prior output — 144 h old against the 28 h daily threshold (STALE-class age). However, skill-freshness has no enabled downstream consumers, so this represents a producer gap (likely ISS-006 dead-window) rather than a consumer-facing staleness problem. Companion skill `skill-health` is the right escalation path.
- **cost-report gap**: `articles/cost-report-2026-09-07.md` is 264 h old (threshold 192 h → WARN-class age). Expected Mon Sep 14 run produced no article. No enabled consumer reads cost-report articles, so this is a producer-health finding, not a freshness gap.
- **Zero active chains**: `aeon.yml` `chains:` block is entirely commented out. `.outputs/` files exist for 41 skills but none is consumed. The 4 h threshold class for chain outputs is therefore inert until a chain is re-activated.

## Healthy consumers

- heartbeat — 1 dep (`articles/token-report-*.md`; producer disabled/on_demand, no freshness gap), all fresh.
- weekly-shiplog — 1 dep (`articles/push-recap-*.md`; producer disabled, no freshness gap), all fresh.
- skill-evals — 1 dep (`articles/skill-evals-*.md`; own prior output, self-read excluded), all fresh.
- swarm-safety-eval — 1 dep (`articles/swarm-safety-eval-*.md`; own prior output, self-read excluded), all fresh.
- fleet-control — 2 deps (`memory/state/fleet-control-state.json`, `articles/fleet-status-*.md`; own outputs, excluded), all fresh.
- compute-pulse — 2 deps (`memory/topics/compute-pulse.md` own output; `memory/topics/compute-tokens.md` optional/absent), all fresh.
- surplus-pulse — 2 deps (`memory/topics/surplus-pulse.md` own output; `memory/topics/projects.md` optional/absent), all fresh.
- ai-framework-watch — 1 dep (`memory/topics/framework-watch-state.json`; own managed state, excluded), all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 200+ entries, 44 enabled
- Implicit references discovered: 36
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 6 (`articles/token-report-*.md`, `articles/push-recap-*.md`, `memory/topics/framework-watch-state.json`, `memory/topics/compute-futures-macro-correlations.md`, `memory/topics/projects.md`, `memory/topics/compute-tokens.md`)

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk file dates — this skill measures nothing it does not also report.*
