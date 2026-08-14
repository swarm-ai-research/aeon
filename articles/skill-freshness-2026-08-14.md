# Skill Freshness — 2026-08-14

**Verdict:** ⚠️ FRESHNESS_STALE — 3 canonical article patterns MISSING (producers disabled or not yet run)

*Audited 44 enabled skills · 5 cross-skill dependencies scored · 3 flagged · 7 implicit missing refs skipped (never existed on disk)*

---

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| heartbeat | `articles/token-report-*.md` | articles (daily) | MISSING | ⚠️ MISSING |
| weekly-shiplog | `articles/push-recap-*.md` | articles (daily) | MISSING | ⚠️ MISSING |
| fleet-control | `articles/fleet-status-2026-08-14.md` | articles (daily) | MISSING | ⚠️ MISSING |

*(Sorted by severity desc, then consumer name. OK rows omitted.)*

---

## What this means per consumer

> **heartbeat** — depends on 1 cross-skill file; 1 flagged. Worst: `articles/token-report-*.md` — no matching file exists on disk (threshold 28h, class articles/daily). The producer `token-report` is `enabled: false` in `aeon.yml` — it will never write a new article until re-enabled. Heartbeat's SKILL.md notes the dependency is optional ("Skipped silently when no file exists"), so the skill degrades gracefully; but the Token Pulse section of every heartbeat report will remain permanently blank. Suggested action: Enable `token-report` if token data is desired, or add `<!-- skill-freshness:ignore -->` to heartbeat's SKILL.md to suppress the MISSING flag.

> **weekly-shiplog** — depends on 1 cross-skill file; 1 flagged. Worst: `articles/push-recap-*.md` — no matching file on disk (threshold 28h, class articles/daily). Producer `push-recap` is `enabled: false`. SKILL.md says it reads push-recap "if any exist" — graceful degradation. But weekly-shiplog will never have digested diff context from a push-recap companion until the producer is re-enabled. Suggested action: Enable `push-recap` if diff digests are desired, or annotate the reference as ignore.

> **fleet-control** — depends on 1 article reference; 1 flagged. `articles/fleet-status-2026-08-14.md` doesn't exist yet (threshold 28h, class articles/daily). **Note: this is likely a heuristic false positive.** Fleet-control reads its own prior fleet-status article for delta computation — this is a self-state-keeping pattern. The prefix check (`fleet-status` ≠ `fleet-control`) fails to filter it. Fleet-control's SKILL.md handles the missing-file case explicitly ("no prior status to diff against"). No operator action required; this is a known skill-freshness prefix-mismatch limitation noted in [[skill-freshness-mtime-blind-in-gha]].

---

## Healthy consumers

- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`, 0.3h old), all fresh.
- vuln-scanner — 1 dep (`.outputs/github-trending.md`, 0.3h old), all fresh.
- planner — self-state only, all fresh.
- notegraph — self-state only, all fresh.
- skillpacks — self-state only, all fresh.
- suggest-edges — self-state only, all fresh.
- surplus-pulse — 1 self-dep (`memory/topics/surplus-pulse.md`), all fresh.
- compute-pulse — 1 self-dep (`memory/topics/compute-pulse.md`), all fresh.

+ 36 more all-fresh consumers (no tracked cross-skill dependencies).

---

## Source status

- `aeon.yml`: 100+ entries, **44 enabled**
- Explicit `chains: consume:` edges: **0** (all chain definitions are currently commented out)
- Implicit cross-skill references discovered: **5** (after filtering ~16 self-reads)
- Files not yet on disk (skipped — implicit refs that never existed): **7**
  - `memory/topics/projects.md` (referenced by surplus-pulse)
  - `memory/topics/compute-tokens.md` (referenced by compute-pulse)
  - `memory/topics/watched-repos.md` (referenced by repo-revive — see also [[watched-repos-config-missing-silent-short-circuits-6-skills]])
  - `memory/topics/stale-models.md` (referenced by repo-revive)
  - `memory/topics/pr-review-rules.md` (referenced by pr-review)
  - `memory/topics/skills-history.md` (referenced by memory-flush)
  - `memory/topics/compute-futures-macro-correlations.md` (referenced by compute-macro-correlate)

### GHA mtime note

All on-disk files carry the same git commit timestamp (2026-08-14T07:41:39Z, 18 minutes before this run). `git log -1 --format=%ct` was used per [[skill-freshness-mtime-blind-in-gha]]; because the repo is a single-commit snapshot, age-based checks (WARN/STALE) are unreliable for this run — all existing files score OK by age. The three MISSING findings are independent of the mtime issue: they reflect files that genuinely do not exist on disk, not files that went stale.

---

*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from git commit timestamps — this skill measures nothing it does not also report.*
