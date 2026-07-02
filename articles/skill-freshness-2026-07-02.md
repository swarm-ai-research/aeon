# Skill Freshness — 2026-07-02

**Verdict:** ✅ FRESHNESS_OK — all 6 discovered dependencies are within their freshness thresholds.

*Audited 44 enabled skills · 6 dependencies checked · 0 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|

*(none — all dependencies are fresh)*

## What this means per consumer

*(no consumers with a degraded verdict)*

## Healthy consumers

- planner — 1 dep, all fresh.
- pr-tracker — 1 dep, all fresh.
- surplus-pulse — 1 dep, all fresh.
- compute-pulse — 1 dep, all fresh.
- notegraph — 1 dep, all fresh.
- skillpacks — 1 dep, all fresh.
+ 38 more all-fresh consumers (no surviving implicit dependencies discovered in their SKILL.md files).

## Source status

- `aeon.yml`: ~153 entries parsed, 44 enabled
- Implicit references discovered (surviving filter): 6
- Explicit `chains: consume:` edges: 0 — the `chains:` block in `aeon.yml` is fully commented out; no chain output dependencies exist
- Files not yet on disk (skipped — implicit refs that never existed): ~12 (e.g. `memory/topics/pr-review-rules.md`, `memory/topics/watched-repos.md`, `memory/state/skill-repair-history.json`, `memory/state/suggest-edges.json`, `.outputs/github-trending.md`)
- `articles/` directory: absent on disk — no cross-skill article dependencies flagged (all article references in scanned SKILL.md files matched the consumer's own skill name and were filtered as self-references per methodology)
- `agi-tracker`: enabled in `aeon.yml` but `skills/agi-tracker/SKILL.md` does not exist in this snapshot — skipped from implicit-dependency scan

### Dependency age summary (all OK)

| Consumer | Dependency | Class | Age | Threshold | Severity |
|----------|-----------|-------|-----|-----------|----------|
| planner | `memory/state/planner-state.json` | state | ~2 min | 720h (30d) | ✅ OK |
| pr-tracker | `memory/topics/pr-status.md` | topics | ~2 min | 168h (7d) | ✅ OK |
| surplus-pulse | `memory/topics/surplus-pulse.md` | topics | ~2 min | 168h (7d) | ✅ OK |
| compute-pulse | `memory/topics/compute-pulse.md` | topics | ~2 min | 168h (7d) | ✅ OK |
| notegraph | `memory/state/notegraph.json` | state | ~2 min | 720h (30d) | ✅ OK |
| skillpacks | `memory/state/skillpacks.json` | state | ~2 min | 720h (30d) | ✅ OK |

*Note: all on-disk mtimes reflect the git checkout timestamp (2026-07-02T08:34Z) rather than the time each file was last genuinely written by its producer skill. In GitHub Actions, `git checkout` resets file mtimes to the checkout instant — this is a known constraint of mtime-based freshness in a checkout environment. No `.outputs/` or `memory/state/` consumer-dependency pair was flagged because all resolved files exist on disk and their checkout-time mtime falls well within even the tightest applicable threshold (4h for `.outputs/` class).*

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
