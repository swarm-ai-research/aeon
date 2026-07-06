# Skill Freshness — 2026-07-06

**Verdict:** ✅ FRESHNESS_OK — 0 cross-skill dependencies scored; 4 implicit references discovered but skipped (referenced files never existed on disk).

*Audited 44 enabled skills · 0 dependencies checked · 0 flagged*

> **Structural note (8th consecutive FRESHNESS_OK):** This skill is operating under a known GHA limitation — `actions/checkout` resets every file's mtime to the checkout instant, and the snapshot commit bundles all `.outputs/` writes under a single git timestamp, making both `stat` and `git log -1 --format=%ct` return the same uniform time for every file. The formal spec result is correct given available timestamps; the Supplementary section below uses content-embedded date proxy to surface the actual operational picture. Fix path: `[[skill-freshness-mtime-blind-in-gha]]`.

## Flagged dependencies

*(None — no formal flags fired.)*

All 4 implicit cross-skill references discovered during SKILL.md scanning point to files that have never been created on disk. Per spec, implicit references to never-existing files are excluded from `MISSING` flagging.

| Consumer | Dependency | Class | Status |
|----------|-----------|-------|--------|
| `compute-pulse` | `memory/topics/compute-tokens.md` | topic | skipped — never created |
| `compute-macro-correlate` | `memory/topics/compute-futures-macro-correlations.md` | topic | skipped — never created |
| `pr-review` | `memory/topics/pr-review-rules.md` | topic | skipped — never created |
| `surplus-pulse` | `memory/topics/projects.md` | topic | skipped — never created |

## What this means per consumer

No consumer has a formally flagged stale dependency. The fleet has no active `chains: consume:` edges (the `chains:` block in `aeon.yml` is fully commented out), so there are zero explicit freshness edges to score.

## Healthy consumers

With 0 explicit chain edges and all implicit cross-skill references pointing to never-created files, every enabled consumer passes the formal check. The content proxy audit below gives the real picture.

*(All 44 consumers: 0 checked deps, 0 flagged — see Supplementary for operational health.)*

## Supplementary: Content-Proxy Audit

Since mtime and git-log timestamps are structurally blind in this environment, the following uses the most recent `YYYY-MM-DD` string found in each `.outputs/{skill}.md` file as a proxy for "last successful write by producer." This is not a formal spec output — it is operational intelligence for the operator.

**Current time:** 2026-07-06T09:45Z

### Daily skills — .outputs freshness by content date

| Producer | Content Date | Age | Threshold | Proxy Verdict |
|----------|-------------|-----|-----------|---------------|
| notegraph | 2026-07-06 | ~0h | 28h | ✅ OK |
| reflect | 2026-07-05 | ~26h | 28h | ✅ OK |
| planner | 2026-07-05 | ~26h | 28h | ✅ OK |
| stale-content-pr-sweeper | 2026-07-05 | ~26h | 28h | ✅ OK |
| skill-health | 2026-07-05 | ~24h | 28h | ✅ OK |
| heartbeat | 2026-07-05 | ~24h | 28h | ✅ OK |
| surplus-pulse | 2026-07-05 | ~18h | 28h | ✅ OK |
| compute-futures-eda | 2026-07-05 | ~26h | 28h | ✅ OK |
| fleet-control | 2026-07-05 | ~26h | 28h | ✅ OK |
| gitlawb-fleet-metrics | 2026-07-05 | ~26h | 28h | ✅ OK |
| goal-tracker | 2026-07-05 | ~26h | 28h | ✅ OK |
| github-monitor | 2026-07-05 | ~26h | 28h | ✅ OK |
| issue-triage | 2026-07-05 | ~26h | 28h | ✅ OK |
| pr-triage | 2026-07-05 | ~26h | 28h | ✅ OK |
| pr-review | 2026-07-05 | ~26h | 28h | ✅ OK |
| pr-tracker | 2026-07-05 | ~26h | 28h | ✅ OK |
| skill-freshness | 2026-07-05 | ~26h | 28h | ✅ OK |
| code-health | 2026-07-06¹ | ~0h | 28h | ✅ OK |
| batch-health | — (corrupt: "-f") | unknown | 28h | ⚠️ UNKNOWN |
| suggest-edges | 2026-06-25 | **264h** | 28h | 🔴 STALE (9.4×) |
| run-frequency-guard | no .outputs file | unknown | 28h | ⚠️ UNKNOWN |

¹ Date found in file content may reflect a reference rather than a run date; treat as OK pending further investigation.

### Weekly skills — .outputs freshness by content date

| Producer | Content Date | Age | Threshold | Proxy Verdict |
|----------|-------------|-----|-----------|---------------|
| skillpacks | 2026-07-05 | ~24h | 192h | ✅ OK |
| swarm-safety-eval | 2026-07-05 | ~24h | 192h | ✅ OK |
| self-review | 2026-07-05 | ~24h | 192h | ✅ OK |
| skill-evals | 2026-07-05 | ~24h | 192h | ✅ OK |
| skill-update-check | 2026-07-05 | ~24h | 192h | ✅ OK |
| workflow-security-audit | 2026-07-05 | ~26h | 192h | ✅ OK |
| config-validator | 2026-07-05 | ~26h | 192h | ✅ OK |
| vuln-scanner | 2026-07-04 | ~47h | 192h | ✅ OK |
| repo-revive | 2026-07-04 | ~48h | 192h | ✅ OK |
| agi-tracker | 2026-06-29 | 168h | 192h | ✅ OK (Mon 13:00 slot pending today) |
| skill-graph | 2026-06-28 | **192h** | 192h | 🟡 WARN (at threshold; next Sun 17:00) |
| skill-analytics | 2026-06-24 | **288h** | 192h | 🟡 WARN (1.5×; missed Wed 2026-07-01) |
| weekly-shiplog | 2026-06-22 | **336h** | 192h | 🟡 WARN (1.75×; missed Mon 2026-06-29) |
| janitor | 2026-06-20 | **~385h** | 192h | 🔴 STALE (2×+; 4 missed Sun slots) |
| milestone-tracker | 2026-06-20 | **~385h** | 192h | 🔴 STALE (2×+; 3 missed Mon slots) |
| cost-report | 2026-06-20 | **~385h** | 192h | 🔴 STALE (2×+; 3 missed Mon slots) |
| compute-pulse | "-f" (corrupt)² | unknown | 192h | ⚠️ UNKNOWN (memory/topics shows 2026-07-04 ✅) |
| compute-macro-correlate | no .outputs file³ | unknown | 192h | ⚠️ UNKNOWN (heartbeat: ran 2026-07-05) |
| ai-framework-watch | no .outputs file⁴ | unknown | 192h | ⚠️ UNKNOWN (scheduled Mon 08:30 today) |
| changelog | no date found⁵ | unknown | 192h | ⚠️ UNKNOWN |

² `.outputs/compute-pulse.md` contains only `-f` — corrupted by the `./notify -f` bug (`[[notify-script-has-no-f-flag]]`). `memory/topics/compute-pulse.md` reads "Last run: 2026-07-04" → **fresh by topic proxy**.

³ No `.outputs/compute-macro-correlate.md` exists. Per heartbeat 2026-07-05: "07:44Z burst broke 15-day silence for compute-macro-correlate" — ran successfully yesterday. No .outputs artifact written.

⁴ No `.outputs/ai-framework-watch.md` exists. Scheduled Monday 08:30 UTC (today); may not have run yet at time of this audit (09:45 UTC).

⁵ `.outputs/changelog.md` reads "`memory/watched-repos.md` missing — nothing to scan." No date embedded; changelog early-exits silently when `watched-repos.md` is absent.

### Skill-level context proxy

Proxy STALE/WARN signals by content date are consistent with ISS-006 (scheduler pocket underdelivery, day 15) and ISS-001 denominator burn-down. None of these create a formal freshness flag in this run because no active `chains: consume:` edge makes a downstream consumer dependent on these files. The operator action is:

- **suggest-edges** (STALE 9.4×): Check `./scripts/skill-runs --skill suggest-edges --hours 336` — 11 consecutive missed daily runs is anomalous even under ISS-006. May need skill-repair.
- **cost-report / milestone-tracker / janitor** (STALE 2×): All three missed multiple slots. Tied to ISS-006 pocket recovery pattern. Monitor next scheduled slots (Mon 07:00, Mon 12:00, Sun 05:30).
- **skill-analytics** (WARN 1.5×): Missed Wed 2026-07-01. Next slot Wed 2026-07-08.
- **weekly-shiplog** (WARN 1.75×): Missed Mon 2026-06-29. Today is Mon — watch 09:00 UTC slot.
- **skill-graph** (at threshold): Ran last Sun 2026-06-28. Next slot Sun 2026-07-12.

## Source status

- `aeon.yml`: ~130 entries, 44 enabled
- Implicit cross-skill references discovered: 4
- Explicit `chains: consume:` edges: 0
- Self-referential references filtered: ~12 (each skill referencing its own output path)
- Files not yet on disk (skipped — implicit references that never existed): 4
- Content proxy observations: 6 .outputs files with anomalous dates (see Supplementary)
- Formal dependencies scored: 0
- Formal flags: 0

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk timestamps — formal flags require a consumer-producer dependency edge; supplementary content proxy uses date strings embedded in `.outputs/` file content as a GHA-compatible substitute. See `[[skill-freshness-mtime-blind-in-gha]]` for the fix path.*
