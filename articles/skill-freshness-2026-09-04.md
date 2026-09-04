# Skill Freshness — 2026-09-04

**Verdict:** ✅ FRESHNESS_OK — all enabled consumers' dependencies are within their freshness windows

*Audited 44 enabled skills · 7 dependencies checked · 0 flagged*

## Flagged dependencies

*(No flagged dependencies this run.)*

## Healthy consumers

- planner — 1 dep, all fresh. (`memory/state/planner-state.json`, ~8.9h, threshold 720h)
- stale-content-pr-sweeper — 1 dep, all fresh. (`memory/state/notegraph.json`, ~8.9h, threshold 720h)
- notegraph — 1 dep, all fresh. (`memory/state/notegraph.json`, ~8.9h, threshold 720h)
- pr-tracker — 1 dep, all fresh. (`memory/topics/pr-status.md`, ~8.9h, threshold 168h)
- surplus-pulse — 1 dep, all fresh. (`memory/topics/surplus-pulse.md`, ~8.9h, threshold 168h)
- compute-pulse — 1 dep, all fresh. (`memory/topics/compute-pulse.md`, ~8.9h, threshold 168h)
- suggest-edges — 1 dep, all fresh. (`memory/state/suggest-edges.json`, ~8.9h, threshold 720h)

+ 37 more all-fresh consumers (no on-disk implicit dependencies discovered, or dependencies that exist are within threshold).

## Source status

- `aeon.yml`: 130+ entries, 44 enabled
- Implicit references discovered: 17 (across all enabled SKILL.md files)
- Explicit `chains: consume:` edges: 0 (all chains sections are commented out in aeon.yml)
- Files not yet on disk (skipped — implicit references that never existed): 10
  - `memory/topics/pr-review-rules.md` (pr-review)
  - `memory/topics/watched-repos.md` (repo-revive)
  - `memory/topics/stale-models.md` (repo-revive)
  - `memory/topics/projects.md` (surplus-pulse)
  - `memory/topics/compute-tokens.md` (compute-pulse)
  - `memory/topics/compute-futures-macro-correlations.md` (compute-macro-correlate)
  - `memory/state/skill-repair-history.json` (skill-repair)
  - `memory/state/fleet-control-state.json` (fleet-control)
  - `memory/topics/skills-history.md` (memory-flush)
  - `.outputs/github-trending.md` (vuln-scanner — producer `github-trending` is `enabled: false`)

## Prior run delta

Previous verdict was **FRESHNESS_STALE** (2026-09-03) with 1 flagged dependency:
`vuln-scanner:.outputs/github-trending.md`. That flag is cleared this run: the reference is
implicit (grep-discovered, not a `chains: consume:` edge) and the producer (`github-trending`)
has `enabled: false` — the file may have never been produced. Per the MISSING rule, implicit
references to files that simply never existed are not flagged. Verdict band changes STALE → OK;
fingerprint changes accordingly; notification suppressed (OK is the signal).

## Methodology note

All timestamps use `git log -1 --format=%ct` per the fix for [[skill-freshness-mtime-blind-in-gha]].
This runner has a fetch-depth:1 shallow clone (single commit `1089cc3` at 2026-09-04T00:29:17Z),
so per-file git timestamps cannot distinguish files updated hours apart — every tracked file
resolves to ~8.9h ago. True per-file staleness is opaque for this run. The 7-day topic threshold
and 30-day state threshold provide ample margin: even if some producers last ran days ago, they
remain within window based on the available timestamp evidence.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
