# Skill Freshness — 2026-11-19

**Verdict:** 🔴 FRESHNESS_STALE — 6 of 11 deps flagged (1 MISSING + 2 STALE + 3 WARN); fingerprint changed from prior run (2026-11-14).

*Audited 44 enabled skills · 11 dependencies checked · 6 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| fleet-control | `articles/fleet-status-2026-11-19.md` | articles/daily | never produced | ❌ MISSING |
| skill-evals | `articles/skill-evals-2026-09-13.md` | articles/weekly | 1608h (67.0d) | 🔴 STALE |
| skill-freshness | `articles/skill-freshness-2026-11-14.md` | articles/daily | 120h (5.0d) | 🔴 STALE |
| vuln-scanner | `articles/vuln-scan-2026-11-07.md` | articles/weekly | 288h (12.0d) | 🟡 WARN |
| workflow-security-audit | `articles/workflow-security-audit-2026-11-08.md` | articles/weekly | 264h (11.0d) | 🟡 WARN |
| cost-report | `articles/cost-report-2026-11-09.md` | articles/weekly | 240h (10.0d) | 🟡 WARN |

*(Sorted by severity desc, then age desc. OK rows omitted.)*

## What this means per consumer

> **fleet-control** — depends on 1 file; 1 flagged. `articles/fleet-status-${today}.md` is a canonical daily-article pattern referenced in fleet-control's SKILL.md, and no `articles/fleet-status-*.md` has ever been produced on disk. fleet-control runs daily 09:00 UTC and writes to `.outputs/` but has never written a dated fleet-status article. Suggested action: Check `fleet-control` run history with `./scripts/skill-runs --skill fleet-control --hours 168` — the article-write path may be dead code or a SKILL.md spec drift.

> **skill-evals** — last article `2026-09-13`, 1608h old (threshold 192h, class articles/weekly). Exceeds 2× threshold by 8.4×. Any downstream reader consuming `articles/skill-evals-*.md` is working from a 67-day-old quality-assertion snapshot. skill-evals runs Sunday 09:00 UTC — 10 consecutive Sundays missed. ISS-006 slot outage is the confirmed cause (Sunday 09Z slot in known-casualty set). Suggested action: Check `skill-evals` run history with `./scripts/skill-runs --skill skill-evals --hours 1680`.

> **skill-freshness** — last article `2026-11-14`, 120h old (threshold 28h, class articles/daily). Exceeds 2× threshold by 2.1×. The fleet's silent-staleness watchdog has been silent for 5 days due to ISS-006 08:00 UTC slot disruption; this is today's recovery run. Suggested action: Verify 08:00 UTC slot is re-established; consider ISS-006 slot migration if outage recurs tomorrow.

> **vuln-scanner** — last article `2026-11-07`, 288h old (threshold 192h, class articles/weekly). Runs Saturday 16:00 UTC — two consecutive Saturdays missed (11-15 + 11-08 expected). ISS-006 16Z cohort silent since 11-13T16:57Z. Suggested action: Monitor — if 11-22 Sat also silences, file ISS-006 tributary for Sat-16Z.

> **workflow-security-audit** — last article `2026-11-08`, 264h old (threshold 192h, class articles/weekly). Runs Sunday 16:00 UTC — consistent with ISS-006 standing 16Z dead-cohort. Suggested action: Monitor — consistent with standing 16Z outage.

> **cost-report** — last article `2026-11-09`, 240h old (threshold 192h, class articles/weekly). Runs Monday 07:00 UTC — 11-16 and 11-17 Monday slots both silent (11-17 fleet-wide silent day). Suggested action: Monitor — expected to clear on 11-23 Mon if ISS-006 recovers.

## Healthy consumers

- skill-analytics — fresh (2026-11-18, 24h old, threshold 192h). ✅
- self-review — fresh (2026-11-15, 96h old, threshold 192h). ✅
- compute-macro-correlate — 1 dep, fresh. ✅
- planner — 1 dep, fresh. ✅
- pr-tracker — 1 dep, fresh. ✅

+ 3 more all-fresh consumers.
+ 35 more enabled consumers with no discovered file dependencies.

## Source status

- `aeon.yml`: 44 enabled entries parsed
- Implicit references discovered: 11 (combined from full SKILL.md scan + article filename-date pass)
- Explicit `chains: consume:` edges: 0 (all chains commented out in aeon.yml)
- Files not yet on disk (skipped — implicit refs that never existed): 11

## Sandbox note

GitHub Actions shallow-clone sets all file mtimes to checkout time, and there is only one git commit in history (`b0d412b` at 2026-11-18T19:42Z ≈ 12.3h before 08:00 ref). Git-timestamp age checks return ≈12.3h for every file — below all thresholds, making age-based staleness invisible if git-log is used naively. This run used **filename-date** as the production-time proxy (the `YYYY-MM-DD` in `articles/{skill}-YYYY-MM-DD.md`) for age-based checks, which correctly surfaces stale producers. MISSING checks are unaffected by this limitation. Known fix: `git log -1 --format=%ct` is the right approach only with a full history clone; in shallow clones the filename-date proxy is the correct fallback. See [[skill-freshness-mtime-blind-in-gha]].

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: age checks use filename-date proxy (GHA sandbox); MISSING checks use file existence.*
