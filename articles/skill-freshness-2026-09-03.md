# Skill Freshness — 2026-09-03

**Verdict:** 🔴 FRESHNESS_STALE — 1 dependency MISSING across 1 of 44 enabled consumers

*Audited 44 enabled skills · 1 dependency checked · 1 flagged*

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| vuln-scanner | `.outputs/github-trending.md` | outputs | MISSING | 🔴 MISSING |

*(Sorted by severity desc, then consumer name. OK rows omitted.)*

## What this means per consumer

> **vuln-scanner** — depends on 1 file; 1 flagged. Worst: `.outputs/github-trending.md` last updated: MISSING — file not present on disk (threshold 4h, class outputs). The producer `github-trending` is `enabled: false` in `aeon.yml`. First seen flagged: 2026-09-02T09:05:00Z (escalated STALE → MISSING; file previously existed but is no longer committed). Suggested action: Check `github-trending` run history — skill is disabled. Either re-enable `github-trending` OR update `vuln-scanner` to fall back exclusively to the GitHub trending API (removing the `depends_on: [github-trending]` frontmatter declaration).

## Healthy consumers

- planner — deps within expected ranges, all fresh.
- skill-health — deps within expected ranges, all fresh.
- notegraph — deps within expected ranges, all fresh.
- skill-analytics — deps within expected ranges, all fresh.
- reflect — deps within expected ranges, all fresh.
- heartbeat — deps within expected ranges, all fresh.
- compute-futures-eda — deps within expected ranges, all fresh.
- skill-freshness — deps within expected ranges, all fresh.
+ 35 more all-fresh consumers.

## Source status

- `aeon.yml`: 44 enabled consumers (explicitly tagged `enabled: true`; `reactive`/`workflow_dispatch` entries included where enabled)
- Implicit references discovered: 0 (implicit grep-based refs excluded from dependency count per spec — MISSING only fires for explicit deps)
- Explicit `depends_on:` frontmatter edges: 1 (`vuln-scanner → github-trending`)
- Explicit `chains: consume:` edges: 0 (all chains in `aeon.yml` are commented out)
- Files not yet on disk (skipped — implicit refs that never existed or are self-writes): not counted

### Methodology note — mtime limitation on GHA

This runner has a single-commit shallow clone (commit `530d41f`, 2026-09-03T05:07:51Z). All files share an identical git commit timestamp, making git-log-based age computation unreliable for relative freshness between files. Scoring this run was based on: (a) `depends_on:` explicit frontmatter declarations where the file is verifiably absent; (b) filename-date evidence for `articles/` files; (c) directory existence checks. The known fix — using `git log -1 --format=%ct` per [[skill-freshness-mtime-blind-in-gha]] — will become meaningful once the repo has multi-commit history on the runner. No implicit `.outputs/` or `memory/topics/` WARN/STALE rows were surfaced because the single-timestamp would produce uniformly unreliable ages across the fleet.

**Articles on disk:** `articles/skill-analytics-2026-09-02.md` (yesterday; skill-analytics is weekly Wed 18:30 UTC → ~15h age against 192h threshold → OK).

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk evidence — this skill measures nothing it does not also report.*
