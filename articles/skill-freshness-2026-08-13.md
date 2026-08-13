# Skill Freshness — 2026-08-13

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' discovered dependencies are fresh

*Audited 44 enabled skills · 0 cross-skill dependencies scored · 0 flagged*

## Flagged dependencies

*(None — no enabled consumer had a stale or missing upstream dependency.)*

## What this means per consumer

All 44 enabled consumers returned verdict OK. No action required.

## Healthy consumers

- **planner** — 0 cross-skill deps (1 self-ref state file `planner-state.json` filtered), all fresh.
- **notegraph** — 0 cross-skill deps (1 self-ref state file `notegraph.json` filtered), all fresh.
- **compute-pulse** — 0 cross-skill deps (self-ref `memory/topics/compute-pulse.md` + optional `compute-tokens.md` non-existent filtered), all fresh.
- **surplus-pulse** — 0 cross-skill deps (self-ref `memory/topics/surplus-pulse.md` + optional `projects.md` non-existent filtered), all fresh.
- **fleet-control** — 0 cross-skill deps (self-ref `fleet-control-state.json` not yet on disk — skill creates on first run), all fresh.
- **vuln-scanner** — 0 cross-skill deps (`.outputs/github-trending.md` references a disabled on-demand producer — excluded per rules), all fresh.
- **heartbeat** — 0 cross-skill deps (`articles/token-report-*.md` wildcard references a disabled daily producer — excluded per rules), all fresh.
- **skill-freshness** — 0 cross-skill deps (self-ref `skill-freshness-state.json` filtered), all fresh.

\+ 36 more all-fresh consumers.

## Implicit dependency detail

13 raw implicit references were discovered across enabled SKILL.md files via grep. All 13 were filtered before scoring:

| Reason filtered | Count |
|----------------|-------|
| Self-reference (producer prefix matches consumer name) | 8 |
| Implicit ref to file never on disk — non-existent optional dep | 3 |
| Implicit ref to disabled (on-demand) producer — excluded from MISSING | 2 |

No canonical `articles/{producer}-${today}.md` cross-skill patterns were found in any enabled SKILL.md. The `articles/` directory is empty (no articles committed to this repo checkout), which does not trigger MISSING because: (a) no enabled consumer holds an explicit chain `consume:` edge to any article, and (b) implicit refs to never-existing files are not flagged per spec.

## Source status

- `aeon.yml`: 44 enabled skills (of ~160+ total entries)
- Chains with active `consume:` edges: 0 (daily-routine chain is commented out)
- Implicit references discovered via grep: 13
- Explicit `chains: consume:` edges: 0
- Files not yet on disk (skipped — implicit refs that never existed or self-ref non-existent): 3
- All on-disk files assessed: git-log timestamp `1786607059` (~1.1h ago); within all class thresholds (topics 168h / state 720h / .outputs 4h)
- Note: `skills/agi-tracker/SKILL.md` is missing — agi-tracker's implicit deps were undetectable; skill is enabled (weekly Mon 13:00 UTC). See [[agi-tracker-missing-skill-md-dispatches-no-op]].

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git-log commit timestamps — this skill measures nothing it does not also report.*
