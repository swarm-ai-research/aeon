# Skill Freshness — 2026-09-28

**Verdict:** ✅ FRESHNESS_OK — all 44 enabled consumers have fresh or undetectable dependencies

*Audited 44 enabled skills · 0 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — no cross-skill file dependencies in the detectable scope.)*

## What this means per consumer

All 44 enabled consumers returned OK. No consumer was found reading a stale upstream file within the scope of detectable implicit and explicit dependencies.

**Coverage note:** The grep-based implicit discovery found zero cross-skill article or state references in any enabled SKILL.md. The dominant reason is that the skills which DO consume cross-skill articles (`operator-scorecard` reads `articles/skill-analytics-*.md`; `signal-verdict` reads `articles/self-review-*.md`, `skill-evals-*.md`, `vuln-scan-*.md`) are **disabled** in `aeon.yml` this cycle. Their dependencies are not audited while disabled. Articles that are visibly aging on disk — `articles/cost-report-2026-09-07.md` (21d old, STALE by date) and `articles/skill-analytics-2026-09-16.md` (12d old, WARN by date) — are not flagged because no currently-enabled consumer references them in a detectable pattern. This is correct behavior per spec, but it means this run's FRESHNESS_OK verdict reflects a narrow detectable scope, not a guarantee that all output files are fresh.

**Methodology note:** On-disk mtime is unreliable in GitHub Actions (all files share the checkout timestamp). This run used `git log -1 --format=%ct` for file age per [[skill-freshness-mtime-blind-in-gha]]. A bulk snapshot commit at 2026-09-27T20:50Z covers all files in one SHA — individual file ages are therefore indistinguishable via git log. Article filename dates remain the authoritative indicator of skill last-run time, but the current grep-and-score methodology does not use them directly.

## Healthy consumers

- planner — 0 cross-skill deps, all fresh.
- batch-health — 0 cross-skill deps, all fresh.
- memory-flush — 0 cross-skill deps, all fresh.
- memory-structural-dedupe — 0 cross-skill deps, all fresh.
- janitor — 0 cross-skill deps, all fresh.
- stale-content-pr-sweeper — 0 cross-skill deps, all fresh.
- issue-triage — 0 cross-skill deps, all fresh.
- pr-triage — 0 cross-skill deps, all fresh.
+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: 156 entries, 44 enabled
- Implicit references discovered: 0 (all cross-skill references were in disabled consumers or filtered as self-references)
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 0

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: file ages computed via `git log -1 --format=%ct` (GHA-safe) — this skill measures nothing it does not also report.*
