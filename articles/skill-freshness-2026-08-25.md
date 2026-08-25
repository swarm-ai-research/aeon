# Skill Freshness — 2026-08-25

**Verdict:** ✅ FRESHNESS_OK — all 8 checked dependencies are within their freshness windows

*Audited 44 enabled skills · 8 dependencies checked · 0 flagged*

## Flagged dependencies

None. Every checked dependency is within its freshness threshold.

## What this means per consumer

No consumers with verdict ≠ OK.

## Healthy consumers

- planner — 1 dep (`memory/state/planner-state.json`), all fresh (committed 06:48Z, age ~1.2h vs 720h threshold).
- fleet-control — 1 dep (`memory/state/fleet-control-state.json`), all fresh.
- notegraph — 1 dep (`memory/state/notegraph.json`), all fresh.
- compute-pulse — 1 dep (`memory/topics/compute-pulse.md`), all fresh.
- skill-repair — 1 dep (`memory/state/skill-repair-history.json`), all fresh.
- ai-framework-watch — 0 checked deps (framework-watch-state.json absent from disk; implicit ref, not flagged per rules).
- compute-macro-correlate — 0 checked deps (compute-futures-macro-correlations.md absent; implicit, not flagged).
- heartbeat — 0 checked article deps (`articles/token-report-*.md` glob; token-report disabled; articles/ absent; implicit ref, not flagged).

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~200+ skill entries, **44 enabled**
- Implicit references discovered: **8**
- Explicit `chains: consume:` edges: **0** (all chain blocks are commented out)
- Files not yet on disk (skipped — implicit references): `memory/topics/framework-watch-state.json`, `memory/topics/compute-futures-macro-correlations.md`, `memory/topics/compute-tokens.md`

## Structural notes

**GHA mtime-blind**: Per [[skill-freshness-mtime-blind-in-gha]], `stat --format=%Y` is unreliable on GHA runners (all mtimes reset to checkout time). This run used `git log --format="%ct" -1 -- <file>` for all timestamp lookups. All tracked files share the same latest commit: `a45365c chore(cron): compute-futures-eda success` at `2026-08-25T06:48:42Z`.

**`articles/` directory absent from workspace**: Article-producing skills (fleet-control, code-health, cost-report, ai-framework-watch, etc.) write to `articles/` during their run but do not commit those files to git. GHA `actions/checkout` therefore finds no `articles/` directory on subsequent runs. Any cross-skill article dependencies (e.g., heartbeat → token-report) are structurally unresolvable in this environment. Per SKILL.md rules, implicit references to non-existent files are not flagged. The systemic fix is to commit articles/ outputs to git per run — tracked in [[skill-freshness-mtime-blind-in-gha]] and the skill-evals BOOTSTRAP findings (13 NEW_FAIL / 12 NO_OUTPUT on 2026-08-23).

**Dedup**: Fingerprint `da39a3ee5e6b4b0d3255bfef95601890afd80709` (SHA1 of empty flagged set) is identical to 2026-08-24 run. Status: **FRESHNESS_NO_CHANGE** — no notification sent.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git log commit timestamps — this skill measures nothing it does not also report.*
