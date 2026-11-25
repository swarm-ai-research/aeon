# Skill Freshness — 2026-11-25

**Verdict:** ✅ FRESHNESS_OK — 0 flagged cross-skill dependencies across 44 enabled consumers

*Audited 44 enabled skills · 11 dependencies examined · 0 flagged*

## Flagged dependencies

*(None — all qualifying dependencies are within threshold or filtered.)*

## What this means per consumer

No enabled consumer has a stale cross-skill dependency. All qualifying (consumer, dependency) pairs passed the freshness check.

**Methodology note:** This run applies the self-reference filter strictly per SKILL.md § 4: "References to the consumer's own output paths (a producer self-reading its prior file is not a freshness gap; that's its own state-keeping). Detected when the producer prefix matches the consuming skill name." All 7 entries flagged in the prior run (2026-11-23) were self-references where the article prefix equals the consuming skill name — `skill-evals`, `workflow-security-audit`, `cost-report`, `self-review`, `skill-freshness` — or false positives (`vuln-scanner` reads `memory/vuln-scanned.json` for dedup, not prior articles). These are correctly excluded this run. Cross-skill skill staleness (e.g., skill-evals at 73d, vuln-scanner at 18d) is properly the domain of `skill-health` and `heartbeat`, not this watchdog.

**Known structural gap — fleet-control → articles/fleet-status-*.md:** `fleet-control` reads prior `articles/fleet-status-*.md` for delta comparison. No fleet-status article has ever been written to disk (fleet-control's article prefix `fleet-status` differs from its skill name `fleet-control`, exposing the gap). Per SKILL.md rules, implicit references that simply never existed are not flagged as MISSING. `fleet-control` handles the missing case gracefully ("no prior status to diff against"). This gap has been open since first observed 2026-11-19 (6d). If a fleet-status article IS produced and then goes stale, this watchdog will flag it.

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), all fresh.
- batch-health — 0 qualifying cross-skill deps.
- skill-freshness — 1 dep (memory/topics/skill-freshness-state.json, self-state), filtered.
- fleet-control — 1 implicit dep (articles/fleet-status-*.md), never-existed → not flagged.
- heartbeat — 1 dep (articles/token-report-*.md, explicitly optional), not flagged.
- weekly-shiplog — 1 dep (articles/push-recap-*.md, explicitly optional), not flagged.
- compute-pulse — 1 dep (memory/topics/compute-pulse.md, self-state), filtered.
- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md, self-state), filtered.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 76 entries total, 44 enabled
- Implicit references discovered: 11
- Explicit `chains: consume:` edges: 0 (chains block is commented out)
- Self-references filtered (prefix == skill name): 7
- Optional/guard-pattern refs skipped: 2 (push-recap, token-report)
- Never-existed implicit refs skipped: 1 (fleet-status)
- Files not yet on disk (skipped — implicit refs that never existed): 1

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: filename-embedded dates used as age proxy this run (all on-disk mtimes are identical to repo clone time per [[skill-freshness-mtime-blind-in-gha]] — fix pending).*
