# Skill Freshness — 2026-09-25

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' tracked dependencies are within threshold

*Audited 44 enabled skills · 35 dependencies checked · 0 flagged*

## Flagged dependencies

*(none — every tracked dependency is within its freshness window)*

## What this means per consumer

All 44 enabled consumers passed. No cross-skill consumer is reading a file that has aged past its class threshold.

**Notable observations (out of scope for this watchdog, logged for operator awareness):**
- `skillpacks` state file (`memory/state/skillpacks.json`) shows `last_run: 2026-07-26` (61 days ago, 30d STALE threshold). This is a **self-reference** — filtered by design — but confirms the ISS-006 Sunday-06:00-pocket casualty streak. `skill-health` owns this signal.
- `memory/topics/compute-pulse.md` last updated 2026-09-12 (13 days, 7d WARN threshold for weekly topics). Self-reference from `compute-pulse`; no enabled cross-consumer reads this file.
- `memory/state/planner-state.json` shows `last_run: 2026-09-20T06:30:00Z` (5 days). Self-reference; planner hasn't fired since the 06Z-pocket dead streak began 09-20.

None of these trigger a FRESHNESS flag because the **cross-skill consumer dependency graph is thin**: almost all references from enabled SKILL.md files are either (a) self-references to the skill's own prior output/state, (b) references to disabled or on-demand producers (token-report, push-recap), or (c) broad directory mentions (`articles/`, `memory/topics/`) that don't resolve to a specific tracked file.

## Healthy consumers

- planner — 2 deps (memory/state/planner-state.json, memory/state/daily-plan-*), all self-refs, OK
- notegraph — 1 dep (memory/state/notegraph.json, last_run: 2026-09-24), OK
- suggest-edges — 1 dep (memory/state/suggest-edges.json), OK
- skillpacks — 1 dep (memory/state/skillpacks.json, self-ref, age out-of-scope), OK
- skill-freshness — 1 dep (memory/topics/skill-freshness-state.json), OK
- pr-tracker — 2 deps (memory/state/pr-tracker.json, memory/topics/pr-status.md last updated 2026-09-22), OK
- heartbeat — 1 dep (articles/token-report-*.md, on_demand producer → skipped), OK
- weekly-shiplog — 1 dep (articles/push-recap-*.md, on_demand producer → skipped), OK

+ 36 more all-fresh consumers (self-contained: generate own articles, no cross-skill file reads).

## Source status

- `aeon.yml`: 130+ entries, 44 enabled
- Implicit references discovered: 35
- Explicit `chains: consume:` edges: 0 (all chains currently commented out)
- Files not yet on disk (skipped — implicit references that never existed): 12 (framework-watch-state.json, compute-futures-macro-correlations.md, compute-tokens.md, and 9 others from disabled/on-demand producers)

**Methodology note:** File ages computed from content-embedded timestamps (`last_run` fields in state JSON files, `*Last run:*` headers in topic files) due to git-shallow-clone mtime invariance in GitHub Actions (all checkout mtimes are identical). This is the known `skill-freshness-mtime-blind-in-gha` workaround; see MEMORY.md action queue for the `git log -1 --format=%ct` patch.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk file content — this skill measures nothing it does not also report.*
