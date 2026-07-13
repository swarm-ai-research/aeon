# Skill Freshness — 2026-07-13

**Verdict:** ✅ FRESHNESS_OK — all checked dependencies are within their freshness windows

*Audited 44 enabled skills · 2 cross-skill dependencies checked · 0 flagged*

## Flagged dependencies

*(None — clean run. All tracked dependencies are fresh.)*

## What this means per consumer

No consumers have flagged dependencies. Every enabled skill consuming another skill's output or topic file is reading data within its expected freshness window.

## Healthy consumers

- **pr-tracker** — 1 dep (`memory/topics/pr-status.md`, topics, age ~0h, thresh 168h, OK)
- **stale-content-pr-sweeper** — 1 dep (`memory/state/notegraph.json`, state, age ~0h, thresh 720h, OK)
+ 42 more enabled consumers with no tracked cross-skill dependencies — all fresh by default.

## Source status

- `aeon.yml`: 44 entries parsed, 44 enabled
- Implicit references discovered across enabled SKILL.md files: 22
- Explicit `chains: consume:` edges: 0 (chains block is commented out in aeon.yml)
- Files not yet on disk (implicit references, skipped per spec): 15
- Cross-skill deps evaluated against on-disk files: 2

## Notes

- **Structural mtime blind spot** (unchanged): GitHub Actions resets all file mtimes on checkout. Every file in this run appears ~0h old regardless of actual content age. This is a known limitation documented in `[[skill-freshness-mtime-blind-in-gha]]` — the audit is reliable only when run outside GHA or against a worktree that preserves git object timestamps (via `git log -1 --format=%ct`). A fix is tracked in MEMORY.md next priorities.
- **agi-tracker anomaly**: `agi-tracker` has `enabled: true` in `aeon.yml` (schedule: Mon 13:00) but has no `skills/agi-tracker/SKILL.md` on disk. No deps could be extracted for it. This is a pre-existing condition — no new action needed beyond what's already tracked.
- **Chains**: No active chain steps. The `chains:` block in `aeon.yml` is fully commented out, so there are zero explicit `consume:` edges to audit.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
