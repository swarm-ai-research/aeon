# Skill Freshness — 2026-10-03

**Verdict:** ✅ FRESHNESS_OK — no enabled consumer is acting on stale upstream data.

*Audited 44 enabled skills · 2 cross-skill implicit dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all cross-skill dependencies resolved to OK or were excluded per spec.)*

## What this means per consumer

All 44 enabled consumers are healthy. No enabled skill has an upstream file dependency that is past its staleness threshold.

**Cross-skill dependencies evaluated:**

| Consumer | Dependency | Class | Resolution | Severity |
|----------|-----------|-------|------------|----------|
| heartbeat | `articles/token-report-*.md` | articles/daily | File never existed on disk — implicit reference, producer `token-report` is disabled. Per spec, implicit references that never existed are not flagged. | SKIPPED |
| weekly-shiplog | `articles/push-recap-*.md` | articles/daily | File never existed on disk — implicit reference, producer `push-recap` is disabled. Per spec, implicit references that never existed are not flagged. | SKIPPED |

All other discovered references (self-state reads, self-output paths, broad `articles/` directory scans) were filtered as self-references or non-canonical patterns and excluded from the freshness check.

**Notable stale articles in the archive (not consumed by any enabled skill):**
The following articles are past their freshness threshold but are only referenced by disabled skills (`operator-scorecard`, `signal-verdict`) — not flagged because their consumers are `enabled: false`.

| Article | Age | Threshold | Status | Disabled consumer |
|---------|-----|-----------|--------|-------------------|
| `skill-analytics-2026-09-16.md` | 408h | 192h (weekly) | STALE | operator-scorecard |
| `self-review-2026-09-13.md` | 480h | 192h (weekly) | STALE | signal-verdict |
| `skill-evals-2026-09-13.md` | 480h | 192h (weekly) | STALE | signal-verdict |
| `vuln-scan-2026-09-19.md` | 336h | 192h (weekly) | WARN | signal-verdict |

These are informational only. This skill audits *enabled* consumers exclusively.

## Healthy consumers

All 44 enabled consumers have no cross-skill upstream file dependencies in scope (self-reads are excluded; the two implicit cross-skill references above are from disabled producers with no files on disk):

- planner — self-state reads only (memory/state/planner-state.json)
- batch-health — no file dependencies
- memory-flush — broad `articles/` scan (non-canonical, excluded)
- memory-structural-dedupe — no file dependencies
- janitor — no cross-skill file dependencies
- stale-content-pr-sweeper — self-state reads only
- issue-triage — no file dependencies
- pr-triage — no file dependencies
- pr-review — no file dependencies
- pr-tracker — no file dependencies
- github-monitor — no file dependencies
- repo-revive — no file dependencies
- code-health — self-output only
- surplus-pulse — self-state (memory/topics/surplus-pulse.md)
- compute-pulse — self-state (memory/topics/compute-pulse.md)
- compute-macro-correlate — self-state (memory/topics/compute-futures-macro-correlations.md); upstream data fetched live via API
- compute-futures-eda — self-state (memory/topics/compute-futures-eda/)
- changelog — self-output only
- vuln-scanner — self-output only
- goal-tracker — broad `articles/` scan (non-canonical, excluded)
- agi-tracker — no file dependencies
- milestone-tracker — no file dependencies
- skill-health — reads memory/cron-state.json (not a skill-output path class)
- config-validator — reads aeon.yml + skills.json (not a skill-output path class)
- skill-analytics — self-output only
- reflect — broad `articles/` scan (non-canonical, excluded)
+ 18 more all-healthy consumers (self-state reads or no cross-skill dependencies).

## Source status

- `aeon.yml`: ~91 skill definitions, 44 enabled
- Cross-skill implicit references discovered: 2 (heartbeat→token-report, weekly-shiplog→push-recap)
- Explicit `chains: consume:` edges: 0 (all chain definitions are commented out in aeon.yml)
- Files not yet on disk (skipped — implicit references from disabled producers that never ran): 2

**Known limitation:** This skill uses on-disk mtime for freshness scoring per its SKILL.md spec. In GitHub Actions, `git checkout` sets all file mtimes to the checkout timestamp, making every file appear freshly written. The action queue carries an open fix: use `git log -1 --format=%ct` instead of `stat --format=%Y` per [[skill-freshness-mtime-blind-in-gha]]. For this run the article-age analysis above used filename-embedded dates for articles (the most reliable proxy available) and git-log commit timestamps for other file classes. The fleet verdict is FRESHNESS_OK regardless of timestamp method, because the only stale articles in the archive are consumed exclusively by disabled skills.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk timestamps — this skill measures nothing it does not also report.*
