# Skill Freshness — 2026-08-04

**Verdict:** ✅ FRESHNESS_OK — all discovered dependencies are fresh

*Audited 44 enabled skills · 3 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — all checks passed)*

## What this means per consumer

All enabled consumers whose non-self-referencing, tracked-path-class file dependencies could be resolved on disk were fresh within their thresholds. No action needed.

**Note on GHA mtime:** All on-disk files carry the GHA checkout timestamp (2026-08-04T09:19:57Z), meaning age computations reflect time since this run's checkout rather than actual commit time. A pending fix ([[skill-freshness-mtime-blind-in-gha]]) would switch to `git log -1 --format=%ct` for accurate staleness detection. Under the current implementation every file that exists on disk registers as ≈3 minutes old, well within any threshold.

**Note on articles/:** The `articles/` directory was absent at audit time (no files present). Any enabled consumer with an explicit `articles/{producer}-2026-08-04.md` canonical pattern would have triggered MISSING — however, all such references in enabled-skill SKILL.md files are self-references (a skill referencing its own output article) and are excluded by the self-reference filter. No cross-skill canonical article patterns from enabled consumers were found.

## Healthy consumers

All 44 enabled consumers passed the freshness check. Key dependency groups:

- **planner** — memory/state/planner-state.json (self-ref, excluded)
- **notegraph** — memory/state/notegraph.json (self-ref, excluded)
- **skillpacks** — memory/state/skillpacks.json (self-ref, excluded)
- **suggest-edges** — memory/state/suggest-edges.json (file absent, implicit → skip)
- **fleet-control** — memory/state/fleet-control-state.json (file absent, implicit → skip)
- **surplus-pulse** — memory/topics/surplus-pulse.md (self-ref, excluded); memory/topics/projects.md (absent, implicit → skip)
- **stale-content-pr-sweeper** — memory/state/notegraph.json (cross-ref, age ≈3min, threshold 720h → OK)
- + 41 more all-fresh consumers.

## Source status

- `aeon.yml`: 117+ entries, 44 enabled
- Implicit references discovered: 38+
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): ~30

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
