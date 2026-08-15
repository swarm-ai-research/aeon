# Skill Freshness — 2026-08-15

**Verdict:** 🔴 FRESHNESS_STALE — 2 MISSING dependencies across 2 consumers; producers disabled but cadence is daily

*Audited 44 enabled skills · 8 dependencies checked · 2 flagged*

> **Note — GHA mtime blindness:** All on-disk mtimes resolve to the checkout timestamp (2026-08-15 08:23 UTC) due to a known GitHub Actions limitation ([[skill-freshness-mtime-blind-in-gha]]). Age calculations for existing files are unreliable; staleness signals in this run come exclusively from MISSING files. Fix: use `git log -1 --format=%ct` for age. The structural gap this skill closes — MISSING articles from disabled producers consumed by enabled consumers — remains fully observable and is reported below.

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| weekly-shiplog | `articles/push-recap-*.md` | articles (daily producer) | ∞ (MISSING) | 🔴 MISSING |
| heartbeat | `articles/token-report-*.md` | articles (daily producer) | ∞ (MISSING) | 🔴 MISSING |

## What this means per consumer

> **weekly-shiplog** — depends on 1 tracked file; 1 flagged. Worst: `articles/push-recap-*.md` — no files ever written on disk (articles/ directory absent). Producer `push-recap` has schedule `0 15 * * *` (daily cadence) but is `enabled: false` in aeon.yml. weekly-shiplog reads push-recap articles to populate its "Momentum Check" section — with the producer disabled it silently skips or surfaces stale context. Suggested action: Check `push-recap` run history with `./scripts/skill-runs --skill push-recap --hours 168`. If the producer is intentionally disabled, remove or suppress the push-recap dependency from weekly-shiplog's SKILL.md.

> **heartbeat** — depends on 1 tracked file; 1 flagged. Worst: `articles/token-report-*.md` — no files ever written on disk. Producer `token-report` has schedule `30 12 * * *` (daily cadence) but is `enabled: false` in aeon.yml. heartbeat reads the latest token-report article to power the Token Pulse section of `docs/status.md`. With no file present, the section is silently omitted per the skill's own rule ("No file at all: omit the Token pulse section entirely"). This is gracefully handled but the operator may not realize token data has been absent for 2+ days. Suggested action: Check `token-report` run history with `./scripts/skill-runs --skill token-report --hours 168`. If the producer is intentionally disabled, note this in heartbeat's status page as a deliberate omission rather than a gap.

## Healthy consumers

- planner — 1 dep (memory/state/planner-state.json), all fresh.
- surplus-pulse — 1 dep (memory/topics/surplus-pulse.md), all fresh.
- compute-pulse — 1 dep (memory/topics/compute-pulse.md), all fresh.
- notegraph — 1 dep (memory/state/notegraph.json), all fresh.
- skillpacks — 1 dep (memory/state/skillpacks.json), all fresh.
- suggest-edges — 1 dep (memory/state/suggest-edges.json), all fresh.
- pr-review — 0 tracked deps (memory/topics/pr-review-rules.md absent — implicit ref, never existed, not flagged).
- repo-revive — 0 tracked deps (watched-repos.md, stale-models.md absent — implicit refs, never existed, not flagged).

+ 34 more all-fresh consumers (no discoverable tracked dependencies).

## Source status

- `aeon.yml`: 165+ entries, 44 enabled
- Implicit references discovered: 8
- Explicit `chains: consume:` edges: 0 (all chains commented out in aeon.yml)
- Files not yet on disk (skipped — implicit references that never existed): 6
  - memory/topics/pr-review-rules.md, memory/topics/watched-repos.md, memory/topics/stale-models.md, memory/topics/projects.md, memory/topics/compute-tokens.md, memory/topics/compute-futures-macro-correlations.md
- Implicit .outputs/ references with absent file (skipped — conditional check, never existed): 1
  - vuln-scanner → .outputs/github-trending.md (github-trending is disabled)
- Self-reference edges filtered (consumer == producer prefix): 4
  - skill-evals → articles/skill-evals-*.md, swarm-safety-eval → articles/swarm-safety-eval-*.md, workflow-security-audit → articles/workflow-security-audit-*.md, weekly-shiplog → articles/weekly-shiplog-*.md
- Prior fleet-control flag cleared: articles/fleet-status-*.md producer is `fleet-status` (not in aeon.yml → on_demand cadence → MISSING suppressed)

## Fingerprint delta vs prior run

- Prior run (2026-08-14): 3 flagged — `heartbeat:token-report`, `weekly-shiplog:push-recap`, `fleet-control:fleet-status-2026-08-14`
- This run (2026-08-15): 2 flagged — `heartbeat:token-report`, `weekly-shiplog:push-recap`
- Change: `fleet-control:fleet-status-2026-08-14` cleared (producer not in aeon.yml → on_demand → MISSING suppressed)
- Fingerprint changed → notification sent

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
