# Skill Freshness — 2026-08-07

**Verdict:** ✅ FRESHNESS_OK — all 2 scored dependencies are within threshold; 0 flagged

*Audited 44 enabled skills · 12 dependencies discovered · 0 flagged*

## Flagged dependencies

*(None — all scored dependencies are within threshold.)*

## What this means per consumer

*(No consumers with non-OK verdicts.)*

## Healthy consumers

- **pr-tracker** — 1 dep (`memory/topics/pr-status.md`, topics class, age ~22 min, threshold 168 h), all fresh.
- **stale-content-pr-sweeper** — 1 dep (`memory/state/notegraph.json`, state class, age ~22 min, threshold 720 h), all fresh. *(Note: likely false positive — reference appears in a "Why this skill exists" prose section of SKILL.md, not an actual file-read step in the workflow.)*
- + 42 more all-fresh consumers (no on-disk discoverable dependencies).

## Audit notes

### GHA mtime blind spot (structural, unfixed)

All on-disk files show mtime `2026-08-07T09:06:48Z` — the git checkout timestamp. This puts every file within every freshness threshold regardless of actual content age. The fix documented in [[skill-freshness-mtime-blind-in-gha]] (use `git log -1 --format=%ct` instead of `stat --format=%Y`) is not yet applied. Freshness scoring in this GHA environment is structurally anchored to checkout time and cannot distinguish a file committed yesterday from one committed 30 days ago.

### No `articles/` directory on disk

The `articles/` directory is absent (articles are written during skill runs but are not committed to git). All article-pattern implicit references resolve to non-existent; since all are implicit (no active `chains: consume:` edges), the MISSING flag does not fire per spec. An active run that calls `./notify` or writes an article creates the directory transiently.

### `fleet-control` producer prefix mismatch

`fleet-control` reads `articles/fleet-status-${today}.md` for prior-run delta context. The prefix `fleet-status` does not match any skill name in `aeon.yml`, so no producer cadence can be derived from `PRODUCER_CADENCE` and this canonical `${today}` pattern cannot be scored as MISSING under the daily/weekly producer rule. The actual producer is `fleet-control` itself (it writes then reads its own fleet-status articles). This is a self-referential read that fell through the prefix-match self-reference filter because `fleet-status ≠ fleet-control`.

### 10 implicit references to non-existent files (not flagged — per spec)

| Consumer | Referenced path | Note |
|---|---|---|
| heartbeat | `articles/token-report-2026-04-28.md` | Hardcoded example date in SKILL.md; `articles/` absent |
| fleet-control | `articles/fleet-status-${today}.md` | No `articles/` dir; unknown producer prefix (see above) |
| vuln-scanner | `.outputs/github-trending.md` | `github-trending` is disabled; `.outputs/` absent |
| pr-review | `memory/topics/pr-review-rules.md` | File never created |
| repo-revive | `memory/topics/watched-repos.md` | File never created; blocks `repo-revive`, `code-health`, 4 other skills per MEMORY.md |
| repo-revive | `memory/topics/stale-models.md` | File never created |
| surplus-pulse | `memory/topics/projects.md` | File never created |
| compute-pulse | `memory/topics/compute-tokens.md` | File never created |
| compute-macro-correlate | `memory/topics/compute-futures-macro-correlations.md` | Exists only on unmerged branch per [[github-actions-cannot-create-prs]] |
| memory-flush | `memory/topics/skills-history.md` | File never created |

These are legitimately "never existed" per the implicit-reference policy. The highest-impact gap is `memory/topics/watched-repos.md` — its absence short-circuits `repo-revive`, `code-health`, `github-monitor`, `issue-triage`, `changelog`, and `weekly-shiplog` daily (confirmed in MEMORY.md pointers).

## Source status

- `aeon.yml`: 370+ lines, 44 enabled skills parsed
- Implicit references discovered: 12 (across 9 consumer skills, after self-reference exclusions)
- Explicit `chains: consume:` edges: 0 (chains section is entirely commented out)
- Files on disk and scored: 2 (both OK)
- Files not yet on disk (skipped — implicit references that never existed): 10

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
