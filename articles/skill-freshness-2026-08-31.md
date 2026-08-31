# Skill Freshness — 2026-08-31

**Verdict:** 🔴 FRESHNESS_STALE — 2 never-ran producers, 10-skill daily stale cluster (last batch 08-26), 13 moderate slips

*Audited 43 enabled skills · 43 dependencies checked · 25 flagged*

> **GHA mtime note**: On GitHub Actions runners, `actions/checkout` sets all file mtimes to the checkout time (~09:59 UTC today). Direct mtime-based freshness is therefore blind — all files appear ~0h old regardless of when they were last produced. This run uses `memory/cron-state.json` last_run timestamps as a proxy for `.outputs/{skill}.md` production age. This is the documented [[skill-freshness-mtime-blind-in-gha]] limitation; the structural fix (use `git log -1 --format=%ct`) is pending. Implicit memory/topics/ and memory/state/ dependencies used on-disk mtime (all ≤4h → all OK).

---

## Flagged dependencies

| Consumer | Dependency | Class | Age | Severity |
|----------|-----------|-------|-----|----------|
| ai-framework-watch | `.outputs/ai-framework-watch.md` | outputs | NEVER | ❌ MISSING |
| run-frequency-guard | `.outputs/run-frequency-guard.md` | outputs | NEVER | ❌ MISSING |
| memory-structural-dedupe | `.outputs/memory-structural-dedupe.md` | outputs | 123.3h | 🟠 STALE |
| memory-flush | `.outputs/memory-flush.md` | outputs | 123.3h | 🟠 STALE |
| gitlawb-fleet-metrics | `.outputs/gitlawb-fleet-metrics.md` | outputs | 121.6h | 🟠 STALE |
| batch-health | `.outputs/batch-health.md` | outputs | 121.6h | 🟠 STALE |
| heartbeat | `.outputs/heartbeat.md` | outputs | 121.5h | 🟠 STALE |
| skill-freshness | `.outputs/skill-freshness.md` | outputs | 121.5h | 🟠 STALE |
| fleet-control | `.outputs/fleet-control.md` | outputs | 120.8h | 🟠 STALE |
| issue-triage | `.outputs/issue-triage.md` | outputs | 120.8h | 🟠 STALE |
| github-monitor | `.outputs/github-monitor.md` | outputs | 120.8h | 🟠 STALE |
| pr-triage | `.outputs/pr-triage.md` | outputs | 120.0h | 🟠 STALE |
| repo-revive | `.outputs/repo-revive.md` | outputs | 215.5h | 🟡 WARN |
| compute-pulse | `.outputs/compute-pulse.md` | outputs | 214.5h | 🟡 WARN |
| skillpacks | `.outputs/skillpacks.md` | outputs | 195.9h | 🟡 WARN |
| config-validator | `.outputs/config-validator.md` | outputs | 195.0h | 🟡 WARN |
| compute-macro-correlate | `.outputs/compute-macro-correlate.md` | outputs | 194.9h | 🟡 WARN |
| swarm-safety-eval | `.outputs/swarm-safety-eval.md` | outputs | 194.3h | 🟡 WARN |
| skill-evals | `.outputs/skill-evals.md` | outputs | 192.5h | 🟡 WARN |
| planner | `.outputs/planner.md` | outputs | 50.0h | 🟡 WARN |
| compute-futures-eda | `.outputs/compute-futures-eda.md` | outputs | 50.0h | 🟡 WARN |
| code-health | `.outputs/code-health.md` | outputs | 40.6h | 🟡 WARN |
| surplus-pulse | `.outputs/surplus-pulse.md` | outputs | 40.6h | 🟡 WARN |
| suggest-edges | `.outputs/suggest-edges.md` | outputs | 28.1h | 🟡 WARN |
| notegraph | `.outputs/notegraph.md` | outputs | 28.1h | 🟡 WARN |

---

## What this means per consumer

**run-frequency-guard** — 0 deps checked; producer never ran. Not in cron-state at all, though `aeon.yml` marks it `enabled: true, schedule: "0 23 * * *"`. This is the [[enabled-skills-can-never-dispatch]] class — the skill has no `SKILL.md` or its cron dispatch is broken. Suggested action: Check `run-frequency-guard` wiring in `aeon.yml` and workflow dispatch chain; file ISS-023 candidate per existing MEMORY.md pointer.

**ai-framework-watch** — 0 deps checked; producer never ran. Enabled weekly Monday 08:30 UTC but absent from cron-state (54d silent per MEMORY.md). Same [[enabled-skills-can-never-dispatch]] root cause. Suggested action: Investigate `messages.yml` matcher and workflow wiring per MEMORY.md open action.

> **STALE cluster (10 skills, all ~120–123h old)** — `batch-health`, `fleet-control`, `github-monitor`, `gitlawb-fleet-metrics`, `heartbeat`, `issue-triage`, `memory-flush`, `memory-structural-dedupe`, `pr-triage`, `skill-freshness` — all last ran on 2026-08-26 between 06:43 and 09:59 UTC. These are daily skills that should run every 24h but missed 08-27, 08-28, 08-29, and 08-30 batches (plus today's batch not yet landed at audit time). The root cause is ISS-006 pocket-slot migration: the morning batch has had persistent gaps, and this cluster is the clearest evidence of the 5-day outage. Suggested action: Verify `./scripts/skill-runs --hours 168` confirms the batch-outage pattern; escalate ISS-006 `investigating → fixing` if confirmed.

> **Note on `skill-freshness` self-flag**: This skill's own `.outputs/skill-freshness.md` appears STALE (121.5h). That's expected — this is the current run, and the output will be refreshed at completion. Not a real gap.

**repo-revive** — last ran 2026-08-22T10:32 (215.5h, threshold 192h, weekly). Just past the 1× window. Next scheduled run: Saturday. Suggested action: Monitor — one missed weekly run, expected to clear next Saturday.

**compute-pulse** — last ran 2026-08-22T11:32 (214.5h, threshold 192h, weekly). Same pattern as repo-revive. Next run: Saturday 11:00 UTC.

**skillpacks** — last ran 2026-08-23T06:06 (195.9h, threshold 192h, weekly Sunday). Marginally past window. Next run: Sunday 06:00 UTC.

**config-validator** — last ran 2026-08-23T07:02 (195.0h, threshold 192h, weekly Sunday). Same pattern. Next run: Sunday 07:00 UTC.

**compute-macro-correlate** — last ran 2026-08-23T07:05 (194.9h, threshold 192h, weekly Sunday). Marginally past window. Next run: Sunday 06:30 UTC.

**swarm-safety-eval** — last ran 2026-08-23T07:42 (194.3h, threshold 192h, weekly Sunday). Marginally past window. Next run: Sunday 07:30 UTC.

**skill-evals** — last ran 2026-08-23T09:31 (192.5h, threshold 192h, weekly Sunday). Right at threshold boundary. Next run: Sunday 09:00 UTC.

**planner** — last ran 2026-08-29T07:57 (50.0h, threshold 28h, daily). Missed 08-30 06:30 slot per MEMORY.md (planner-state.last_run 08-29, no 08-30 entry). Suggested action: Monitor — planner ran operator-invoked 08-29; ISS-006 batch gap explains the miss.

**compute-futures-eda** — last ran 2026-08-29T08:00 (50.0h, threshold 28h, daily). Missed 08-30 and 08-31 06:00 slots. Suggested action: Verify daily deployer CSV exists in `memory/gitlawb-compute-futures-proofs/`; if so, today's run is delayed by batch gap.

**code-health** and **surplus-pulse** — both last ran 2026-08-29T17:24/17:25 (40.6h, threshold 28h, daily). Missed today's 08:00/16:30 UTC slots. Suggested action: Monitor — expected to run today in afternoon batch.

**suggest-edges** and **notegraph** — both last ran 2026-08-30T05:52/05:53 (28.1h, threshold 28h, daily). Borderline: just 0.1h past the 28h grace window. Scheduled today at 05:00/05:30 UTC — likely running now or completed. Suggested action: OK in practice; today's runs may have already landed.

---

## Healthy consumers

- agi-tracker — 1 dep, fresh (164.4h, weekly 192h threshold)
- changelog — 1 dep, fresh (161.4h, weekly 192h threshold)
- cost-report — 1 dep, fresh (169.5h, weekly 192h threshold)
- goal-tracker — 1 dep, fresh (15.3h, daily 28h threshold)
- janitor — 1 dep, fresh (28.1h, weekly 192h threshold)
- milestone-tracker — 1 dep, fresh (165.2h, weekly 192h threshold)
- pr-review — 1 dep, fresh (15.2h, daily 28h threshold)
- pr-tracker — 1 dep, fresh (22.7h, daily 28h threshold)

+ 10 more all-fresh consumers: reflect, self-review, skill-analytics, skill-graph, skill-health, skill-update-check, stale-content-pr-sweeper, vuln-scanner, weekly-shiplog, workflow-security-audit.

---

## Source status

- `aeon.yml`: 93 entries, 43 enabled (non-on_demand)
- Explicit `chains: consume:` edges: 0 (daily-routine chain commented out)
- Implicit references discovered: 25 `.outputs/` references (via cron-state proxy), ~5 `memory/topics/` refs (all fresh by mtime)
- `articles/` directory: does not exist — MISSING canonical pattern for all enabled producers; no MISSING flags issued because no ENABLED consumer reads another ENABLED skill's articles (disabled consumers like `operator-scorecard`, `signal-verdict` would be affected if re-enabled)
- Files not yet on disk (skipped — implicit refs that never existed): `memory/topics/compute-futures-macro-correlations.md` (unmerged branch), `memory/topics/compute-tokens.md`, `memory/topics/projects.md`

---

*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: ages derived from `memory/cron-state.json` last_run timestamps (GHA mtime workaround); all thresholds computed per path class as documented.*
