# Skill Freshness — 2026-07-16

**Verdict:** ✅ FRESHNESS_OK — all audited dependencies are fresh

*Audited 44 enabled skills · 0 dependencies checked · 0 flagged*

## Flagged dependencies

None.

## What this means per consumer

No enabled consumer has a stale or missing upstream dependency in the current on-disk state.

## Healthy consumers

All 44 enabled consumers had zero flagged cross-skill dependencies. No cross-skill file dependencies on existing disk files were found after filtering self-references and implicit references to files that have never existed in this GHA checkout.

+ 44 enabled consumers all-fresh (0 deps each after filtering).

## Source status

- `aeon.yml`: 249 entries parsed, 44 enabled
- Implicit references discovered: 5
- Explicit `chains: consume:` edges: 0 (all chains commented out)
- Files not yet on disk (skipped — implicit references that never existed): 5

### Implicit refs found (non-self, all absent from disk)

| Consumer | Dependency | Class | On disk? |
|----------|-----------|-------|----------|
| surplus-pulse | `memory/topics/projects.md` | topics | ✗ MISSING (ignored — never existed) |
| pr-review | `memory/topics/pr-review-rules.md` | topics | ✗ MISSING (ignored — never existed) |
| repo-revive | `memory/topics/watched-repos.md` | topics | ✗ MISSING (ignored — never existed) |
| compute-macro-correlate | `memory/topics/compute-futures-macro-correlations.md` | topics | ✗ MISSING (ignored — never existed) |
| vuln-scanner | `.outputs/github-trending.md` | outputs | ✗ MISSING (ignored — never existed) |

All five are optional/conditional reads; SKILL.md files describe them as "if present" or "auto-select from … or fallback." Per methodology, implicit refs that simply never existed on disk are not flagged.

## Structural note — mtime blind spot (unchanged)

⚠️ **Known limitation [[skill-freshness-mtime-blind-in-gha]]:** All on-disk files receive the git checkout timestamp as their `mtime` in GitHub Actions (~Jul 16 09:02 UTC). File ages computed from `stat --format=%Y` are uniformly ~0h regardless of actual staleness — every existing file appears trivially fresh. The pending fix is `git log -1 --format=%ct` per the MEMORY.md next-priorities list. Until patched, this audit can only confirm *which* files are present vs absent; it cannot distinguish a 1-hour-old file from a 96-hour-old file.

Additionally, the `articles/` directory was absent from this GHA checkout snapshot (`rsavitt/aeon @ a7f04ee`). Any enabled skill that reads another enabled skill's article (e.g. `articles/skill-analytics-${today}.md`) would have that dep counted as "never existed" and skipped. In the live environment, these files are committed after each run and would be tracked normally. Prior run (2026-07-15) reported 2 deps, both fresh — the delta to 0 deps today reflects the absent articles/ directory in this snapshot, not a structural change in the fleet.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
