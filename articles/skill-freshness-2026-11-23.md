# Skill Freshness — 2026-11-23

**Verdict:** 🔴 FRESHNESS_STALE — 7 of 11 deps flagged (1 MISSING + 3 STALE + 3 WARN); fingerprint changed from prior run (2026-11-20): skill-freshness upgraded WARN→STALE (3-day gap), vuln-scanner upgraded WARN→STALE (393h, crossed 2× threshold), self-review newly WARN (201h, crossed 1× threshold).

*Audited 44 enabled skills · 11 dependencies checked · 7 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| fleet-control | `articles/fleet-status-2026-11-23.md` | articles/daily | never produced | ❌ MISSING |
| skill-evals | `articles/skill-evals-2026-09-13.md` | articles/weekly | 1713h (71.4d) | 🔴 STALE |
| skill-freshness | `articles/skill-freshness-2026-11-20.md` | articles/daily | 73h (3.0d) | 🔴 STALE |
| vuln-scanner | `articles/vuln-scan-2026-11-07.md` | articles/weekly | 393h (16.4d) | 🔴 STALE |
| cost-report | `articles/cost-report-2026-11-09.md` | articles/weekly | 345h (14.4d) | 🟡 WARN |
| self-review | `articles/self-review-2026-11-15.md` | articles/weekly | 201h (8.4d) | 🟡 WARN |
| workflow-security-audit | `articles/workflow-security-audit-2026-11-08.md` | articles/weekly | 369h (15.4d) | 🟡 WARN |

*(Sorted by severity desc, then age desc. OK rows omitted.)*

## What this means per consumer

> **fleet-control** — depends on 1 file; 1 flagged. `articles/fleet-status-${today}.md` is a canonical daily-article pattern referenced in fleet-control's SKILL.md, and no `articles/fleet-status-*.md` has ever been produced on disk. Same as prior run — likely a dead SKILL.md code path or spec drift. Suggested action: Check `fleet-control` run history with `./scripts/skill-runs --skill fleet-control --hours 168`.

> **skill-evals** — last article `2026-09-13`, 1713h old (threshold 192h, class articles/weekly). Exceeds 2× threshold by 4.5×. 11 consecutive Sundays (09:00 UTC slot) silent — confirmed ISS-006 Sun-09Z casualty. Suggested action: Check `skill-evals` run history with `./scripts/skill-runs --skill skill-evals --hours 1680`.

> **skill-freshness** — last article `2026-11-20`, 73h old (threshold 28h, class articles/daily). Upgraded WARN→STALE: 3-day gap (11-21 Sat, 11-22 Sun, 11-23 Mon not yet written). Dep path updated from prior run (11-19→11-20). Today's run will write a fresh article and clear this flag. Suggested action: Monitor — this article write resolves the flag.

> **vuln-scanner** — last article `2026-11-07`, 393h old (threshold 192h, class articles/weekly). Crossed the 2× STALE boundary (384h) since the 11-20 report. Two consecutive Saturdays missed: 11-15 and 11-22. ISS-006 Sat-16Z dead cohort. Next window: 2026-11-29 Sat 16:00 UTC. Suggested action: If 11-29 Sat also silences, file a new ISS-006 tributary for Sat-16Z slot.

> **cost-report** — last article `2026-11-09`, 345h old (threshold 192h, class articles/weekly). Mon 07:00 UTC is in the ISS-006 known-casualty slot set (07Z-Mon listed in MEMORY.md). 11-23 Mon 07:00 UTC missed — no new cost-report article landed before this 08:00 run. Will cross STALE at ~384h around 2026-11-25 Wed if no recovery. Suggested action: Monitor — approaching STALE boundary.

> **self-review** — last article `2026-11-15`, 201h old (threshold 192h, class articles/weekly). **New flag this run.** Crossed 1× threshold since 11-20 check (was 128h → now 201h). Runs Sunday 18:30 UTC — ISS-006 18Z dead cohort (silent since at least 11-13T16:57Z). 11-22 Sunday silent, consistent with standing 18Z outage. Will cross STALE at 384h around 2026-12-01 Tue if no recovery. Next window: 2026-11-29 Sun 18:30 UTC. Suggested action: Monitor — consistent with standing 18Z ISS-006 outage.

> **workflow-security-audit** — last article `2026-11-08`, 369h old (threshold 192h, class articles/weekly). Runs Sunday 16:00 UTC — ISS-006 16Z dead cohort. 11-23 Sun 16:00 slot has not yet fired (this run is at ~09:00Z). Will cross STALE at ~384h around 2026-11-24 Mon if 11-23 also silences. Suggested action: Monitor — approaching STALE boundary; file tributary if 11-23 Sun 16Z also silent.

## Healthy consumers

- skill-analytics — fresh (2026-11-18, 129h old, threshold 192h). ✅
- compute-macro-correlate — 1 dep, fresh. ✅
- planner — 1 dep, fresh. ✅
- pr-tracker — 1 dep, fresh. ✅

+ 33 more enabled consumers with no discovered file dependencies.

## Source status

- `aeon.yml`: 44 enabled entries parsed
- Implicit references discovered: 11 (combined from full SKILL.md scan + article filename-date pass)
- Explicit `chains: consume:` edges: 0 (all chains commented out in aeon.yml)
- Files not yet on disk (skipped — implicit refs that never existed): 11

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: age checks use filename-date proxy (GHA sandbox, mtime unreliable); MISSING checks use file existence.*
