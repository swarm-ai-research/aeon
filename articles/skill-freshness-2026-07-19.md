# Skill Freshness — 2026-07-19

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within freshness thresholds

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — no dependencies exceed their freshness threshold)*

## What this means per consumer

All 44 enabled consumers have fresh dependencies. No action required.

## Healthy consumers

- planner — 0 cross-skill deps, self-contained (reads memory/ directly)
- batch-health — 0 cross-skill deps, reads cron-state.json (not tracked path class)
- memory-flush — 0 cross-skill deps
- memory-structural-dedupe — 0 cross-skill deps
- janitor — 0 cross-skill deps
- stale-content-pr-sweeper — 0 cross-skill deps

+ 38 more all-fresh consumers.

## Source status

- `aeon.yml`: 153 entries parsed, 44 enabled
- Implicit references discovered: 21
- Explicit `chains: consume:` edges: 0 (chains block fully commented out)
- Files not yet on disk (skipped — implicit references that never existed): 8
- Self-references excluded from scoring: 11

## Audit notes

**No active cross-skill data flow in the enabled fleet.** Every implicit article reference found in enabled SKILL.md files points to a disabled producer (`token-report` → heartbeat, `github-trending` → vuln-scanner, `push-recap` → weekly-shiplog). No enabled skill currently reads another enabled skill's article or `.outputs/` file at runtime. The fleet is operating as a set of self-contained skills, not a chained pipeline.

**Two on-disk deps evaluated (both OK):**
- `pr-tracker → memory/topics/pr-status.md` — age ~1.95h, threshold 168h (7d), class `memory/topics`. This is a self-prior read; pr-tracker writes and reads its own status file. Verdict: OK.
- `surplus-pulse → memory/topics/surplus-pulse.md` — age ~1.95h, threshold 168h (7d), class `memory/topics`. Self-prior state. Verdict: OK.

**`agi-tracker` has no SKILL.md** — this skill is enabled (Mon 13:00 UTC, Mon weekly) but `skills/agi-tracker/SKILL.md` does not exist on disk. Implicit dependency scanning was skipped. Captured in today's `config-validator` run as WARN.

**Structural GHA blind spot (known):** All file timestamps reflect the shallow-clone checkout time (~2026-07-19T01:57Z, commit `891cce8`), not individual skill run times. A file last updated three weeks ago and a file updated this morning are indistinguishable by mtime in this environment. The fix — `git log -1 --format=%ct` over full history — requires a non-shallow clone. Tracked in [[skill-freshness-mtime-blind-in-gha]]. This run's freshness scores are structurally optimistic; the real signal is in `.outputs/` file presence vs absence, not age.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
