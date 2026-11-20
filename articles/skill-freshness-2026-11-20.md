# Skill Freshness — 2026-11-20

**Verdict:** 🔴 FRESHNESS_STALE — 6 of 11 deps flagged (1 MISSING + 1 STALE + 4 WARN); fingerprint changed from prior run (2026-11-19): skill-freshness upgraded STALE→WARN.

*Audited 44 enabled skills · 11 dependencies checked · 6 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| fleet-control | `articles/fleet-status-2026-11-20.md` | articles/daily | never produced | ❌ MISSING |
| skill-evals | `articles/skill-evals-2026-09-13.md` | articles/weekly | 1640h (68.3d) | 🔴 STALE |
| skill-freshness | `articles/skill-freshness-2026-11-19.md` | articles/daily | 32h | 🟡 WARN |
| vuln-scanner | `articles/vuln-scan-2026-11-07.md` | articles/weekly | 320h (13.3d) | 🟡 WARN |
| workflow-security-audit | `articles/workflow-security-audit-2026-11-08.md` | articles/weekly | 296h (12.3d) | 🟡 WARN |
| cost-report | `articles/cost-report-2026-11-09.md` | articles/weekly | 272h (11.3d) | 🟡 WARN |

*(Sorted by severity desc, then age desc. OK rows omitted.)*

## What this means per consumer

> **fleet-control** — depends on 1 file; 1 flagged. `articles/fleet-status-${today}.md` is a canonical daily-article pattern referenced in fleet-control's SKILL.md, and no `articles/fleet-status-*.md` has ever been produced on disk. fleet-control runs daily 09:00 UTC and writes to `.outputs/` but has never written a dated fleet-status article. Suggested action: Check `fleet-control` run history with `./scripts/skill-runs --skill fleet-control --hours 168` — the article-write path may be dead code or a SKILL.md spec drift.

> **skill-evals** — last article `2026-09-13`, 1640h old (threshold 192h, class articles/weekly). Exceeds 2× threshold by 8.5×. Any downstream reader consuming `articles/skill-evals-*.md` is working from a 68-day-old quality-assertion snapshot. skill-evals runs Sunday 09:00 UTC — 10 consecutive Sundays missed. ISS-006 slot outage is the confirmed cause (Sunday 09Z slot in known-casualty set). Suggested action: Check `skill-evals` run history with `./scripts/skill-runs --skill skill-evals --hours 1680`.

> **skill-freshness** — last article `2026-11-19`, 32h old (threshold 28h, class articles/daily). Between 1× and 2× threshold → WARN (upgraded from STALE on prior run). The 11-19 recovery run wrote yesterday's article; today's run will write a fresh article and clear this flag. This is a known GHA filename-date proxy artifact: 08:02Z run time + midnight-anchored date proxy = 32h apparent age for a ~24h-old file. Suggested action: Monitor — expected to clear completely after today's article is written.

> **vuln-scanner** — last article `2026-11-07`, 320h old (threshold 192h, class articles/weekly). ISS-006 16Z cohort silent since 11-13T16:57Z (1 continuous week). Two consecutive Saturdays missed (11-15, 11-08). Next window: 2026-11-22 Sat 16:00 UTC — if that also silences, age reaches ~360h → still WARN but approaching STALE at ~384h (day 11-24). Suggested action: If 11-22 Sat misses, file ISS-006 tributary for Sat-16Z slot.

> **workflow-security-audit** — last article `2026-11-08`, 296h old (threshold 192h, class articles/weekly). Runs Sunday 16:00 UTC — consistent with ISS-006 standing 16Z dead-cohort (silent since 11-13T16:57Z). Will cross 2× threshold (~384h) around 2026-11-24 if 11-23 Sun also misses. Suggested action: Monitor — consistent with standing 16Z outage; file tributary if 11-23 also silent.

> **cost-report** — last article `2026-11-09`, 272h old (threshold 192h, class articles/weekly). Runs Monday 07:00 UTC — 11-17 fleet-wide silent day dropped the 11-17 Monday slot. Next window: 2026-11-23 Mon 07:00 UTC. If that runs, age clears (new article). Will cross 2× threshold (~384h) around 2026-11-25 if 11-23 Mon also misses. Suggested action: Monitor — expected to clear on 11-23 Mon if ISS-006 recovers.

## Healthy consumers

- skill-analytics — fresh (2026-11-18, 56h old, threshold 192h). ✅
- self-review — fresh (2026-11-15, 128h old, threshold 192h). ✅
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

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: age checks use filename-date proxy (GHA sandbox); MISSING checks use file existence.*
