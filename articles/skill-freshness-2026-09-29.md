# Skill Freshness — 2026-09-29

**Verdict:** ✅ FRESHNESS_OK — all 44 enabled consumers have fresh or undetectable dependencies

*Audited 44 enabled skills · 0 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — no cross-skill file dependencies in the detectable scope.)*

## What this means per consumer

All 44 enabled consumers returned OK. No consumer was found reading a stale upstream file within the scope of detectable implicit and explicit dependencies.

**Coverage note:** Grep-based implicit discovery found zero cross-skill article or state references in any enabled SKILL.md. The skills that DO consume cross-skill articles — `operator-scorecard` (reads `articles/skill-analytics-*.md`), `signal-verdict` (reads `articles/self-review-*.md`, `skill-evals-*.md`, `vuln-scan-*.md`) — are **disabled** in `aeon.yml`. Their dependencies are not audited while disabled. Articles visibly aging on disk — `articles/skill-analytics-2026-09-16.md` (13d old, WARN by filename), `articles/self-review-2026-09-13.md` (16d old, STALE by filename), `articles/skill-evals-2026-09-13.md` (16d old, STALE by filename) — are not flagged because no currently-enabled consumer references them in a detectable pattern. This is correct behavior per spec, but it means this run's FRESHNESS_OK verdict reflects a narrow detectable scope, not a guarantee that all output files are recent.

**Methodology note:** On-disk mtime is unreliable in GitHub Actions (all files share the git checkout timestamp, currently 2026-09-29T08:50Z). Individual file ages are indistinguishable via `stat`; a bulk snapshot commit at 2026-09-27T20:50Z covers all files in one SHA, so `git log -1 --format=%ct` is also ambiguous for this repo. Article filename dates remain the most reliable indicator of skill last-run time. The SKILL.md patch to use `git log -1 --format=%ct` per [[skill-freshness-mtime-blind-in-gha]] is in the action queue but unmerged.

**Dedup:** Fingerprint unchanged from 2026-09-28 run (`da39a3ee5e6b4b0d3255bfef95601890afd80709` — SHA1 of empty flagged set). No notification emitted.

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
- Implicit references discovered: 0 (all cross-skill references in disabled consumers or filtered as self-references)
- Explicit `chains: consume:` edges: 0 (chains block fully commented out)
- Files not yet on disk (skipped — implicit references that never existed): 0

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: file ages computed from on-disk state — this skill measures nothing it does not also report.*
