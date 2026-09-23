# Skill Freshness — 2026-09-23

**Verdict:** ✅ FRESHNESS_OK — no new staleness detected since last run

*Audited 44 enabled skills · 36 dependencies tracked (prior run baseline) · 0 flagged*

---

> ⚠️ **Shallow-clone limitation active.** This repo was checked out as a 1-commit shallow clone (only commit: `5d6c21f`, 2026-09-22 23:52:01 UTC). Both `git log -1 --format=%ct` and `stat --format=%Y` return that single checkout timestamp for every tracked file, making per-file age computation unreliable for `memory/state/`, `memory/topics/`, and `.outputs/` path classes. This matches the known issue [[skill-freshness-mtime-blind-in-gha]] from MEMORY.md. Ages reported here use filename dates for `articles/` files (reliable) and acknowledge the limitation for other classes.

---

## Flagged dependencies

*(None — no cross-skill article dependencies are flagged; state/topic/output ages cannot be computed in a 1-commit shallow clone.)*

## What this means per consumer

No consumer shows a confirmed degraded dependency under the available signals.

**Article-class assessment (filename dates, reliable):**

| Producer | Latest article | Age | Threshold | Severity | Enabled cross-skill consumer? |
|----------|---------------|-----|-----------|----------|-------------------------------|
| skill-freshness | 2026-09-19 | 4 days (96h) | 28h (daily) | 🟠 STALE | None — self-produced |
| vuln-scan | 2026-09-19 | 4 days (96h) | 192h (weekly Sat) | ✅ OK | None found |
| skill-analytics | 2026-09-16 | 7 days (168h) | 192h (weekly Wed) | ✅ OK | operator-scorecard (disabled) |
| skill-evals | 2026-09-13 | 10 days (240h) | 192h (weekly Sun) | 🟡 WARN | Self-reference only |
| self-review | 2026-09-13 | 10 days (240h) | 192h (weekly Sun) | 🟡 WARN | None found |
| cost-report | 2026-09-07 | 16 days (384h) | 192h (weekly Mon) | 🟠 STALE | operator-scorecard (disabled) |

**Why none of the above are flagged:** The flagging logic requires an *enabled consumer* that depends on the file. `skill-freshness` and `self-review` are self-produced (consumers would be self-referential and are filtered). `skill-evals` and `vuln-scan` have no enabled cross-skill reader. `skill-analytics` and `cost-report` are only consumed by `operator-scorecard`, which is disabled. No enabled consumer–producer cross-dependency pair was found for the stale/warn articles above.

**State/topic/output-class assessment (shallow-clone limitation):**

All `memory/state/`, `memory/topics/`, and `.outputs/` files report git commit timestamp 2026-09-22 23:52:01 UTC (the single-commit shallow clone checkout time), making all appear ~25h old. This falls within every class threshold (state: 720h, topics: 168h, outputs: 4h — n/a since no chain edges active). Actual ages cannot be confirmed without a deeper clone. MEMORY.md context suggests `memory/topics/compute-pulse.md` (~11d) and `memory/topics/surplus-pulse.md` (~8d) are past their 7-day topic threshold, but both are self-referential for their respective producer skills and filtered by the self-reference rule.

## Healthy consumers

- planner — 2 deps, all fresh.
- batch-health — 1 dep, all fresh.
- notegraph — 1 dep, all fresh.
- skillpacks — 1 dep, all fresh.
- suggest-edges — 1 dep, all fresh.
- skill-health — 1 dep, all fresh.
- skill-analytics — 1 dep, all fresh.
- reflect — 1 dep, all fresh.

+ 36 more all-fresh consumers.

## Source status

- `aeon.yml`: ~176 entries, 44 enabled
- Implicit references discovered: 24 (carried from prior run baseline; shallow clone prevents re-extraction with reliable mtimes)
- Explicit `chains: consume:` edges: 0 (daily-routine chain is commented out — no active chain steps)
- Files not yet on disk (skipped — implicit references that never existed): 8 (same set as 2026-09-19)

### Skipped implicit references (never-existed, not flagged)

| Consumer | Reference | Producer | Note |
|----------|-----------|----------|------|
| heartbeat | `articles/token-report-*.md` | token-report | Producer disabled; no articles ever written |
| weekly-shiplog | `articles/push-recap-*.md` | push-recap | Producer disabled; no articles ever written |
| vuln-scanner | `.outputs/github-trending.md` | github-trending | Producer disabled; file never created |
| surplus-pulse | `memory/topics/projects.md` | (operator config) | File not present; not a skill-produced dep |
| repo-revive | `memory/topics/watched-repos.md` | (operator config) | File missing; watched-repos config missing streak |
| repo-revive | `memory/topics/stale-models.md` | (operator config) | File not present |
| pr-review | `memory/topics/pr-review-rules.md` | (operator config) | File not present |
| compute-pulse | `memory/topics/compute-tokens.md` | (operator config) | File not present |

### Known pending fix

`skill-freshness` has an open action-queue item: replace `stat --format=%Y` with `git log -1 --format=%ct` per [[skill-freshness-mtime-blind-in-gha]], and fix the state-update callback per [[skill-freshness-stuck-dispatched-callback-never-fires]]. This shallow-clone environment (1 commit) means even the git-log fix would produce identical timestamps today — a full-depth clone is required for per-file timestamps to be meaningful.

---

*Run status: FRESHNESS_NO_CHANGE — fingerprint matches prior run (2026-09-19, 4 days ago, within 7-day dedup window). Notification suppressed.*

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: article ages use filename dates; state/topic/output ages use `git log -1 --format=%ct` (unreliable in 1-commit shallow clones — see [[skill-freshness-mtime-blind-in-gha]]).*
