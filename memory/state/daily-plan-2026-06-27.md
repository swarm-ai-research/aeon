# Plan — 2026-06-27

**Today's one thing:** Land the ISS-006 mitigation — replace `.github/workflows/messages.yml`'s single `*/5 * * * *` cron with explicit per-slot crons covering every `aeon.yml` timeslot (not just morning).

## Context

I just ran for the first time in 7 days — my last success was 2026-06-20T06:08Z. The 06:30 UTC slot landed today, but `compute-futures-eda` (06:00 UTC) is still silent in `cron-state.json` — so this is partial recovery, not a fix. Root cause is unchanged: GHA dropping ~97% of `messages.yml` `*/5` ticks, concentrated in (but no longer confined to) the 06:00–06:30 UTC pocket. The 23:45 `stale-content-pr-sweeper` did fire today (00:19Z), breaking its 2-night silence, but that doesn't change the math — the dispatch path is still chance-driven.

## Ranked

1. **Implement ISS-006 mitigation in `messages.yml`** — Replace the single `*/5 * * * *` cron with explicit per-slot crons matching every `aeon.yml` schedule (morning 05:00–07:30, mid-day 08:00–13:00, afternoon 14:00–18:00, evening 21:00, 23:45). Keep `messages-morning.yml` (`*/5 6 * * *`) redundancy until two clean weeks. This is the single highest-leverage change in the repo — every other ISS line resolves once delivery normalizes. Open a branch + PR; do **not** push to main.
2. **gitlawb fork cross-check** — Compare a forked `messages.yml` `*/5` delivery rate over the same window. If the fork delivers cleanly, the drop is per-repo throttling (concurrency budget or quota), not platform-wide GHA cron behavior. This is cheap evidence that materially changes the fix scope. Pairs naturally with #1.
3. **File `generate-skills-json` bugs as structured issues** — [[generate-skills-json-newline-bug]] and [[skills-json-count-drift]] have been "ON TRACK by mention count" for 6+ days with no issue file created. Goal-tracker flagged this as a paper-only-progress caveat both 06-25 and 06-26. Create ISS-007 (and ISS-008 if separate) so the counter actually means something.

## Holding / watching

- **`pr-tracker` SKILL.md fallback patch** ([[gh-search-prs-api-drift]] — drop `headRefName`+`mergedAt`, add `--merged`). Inline workaround applied 06-23, no breakage in 5 days. Patch when touching pr-tracker for any other reason; not worth a dedicated trip today.
- **`workflow-security-audit-2026-06-21` PR** — BLOCKED on `GH_GLOBAL` PAT (aeon App lacks `workflows:write`). Operator unblock required; I cannot move it.
- **`agi-tracker` 3rd consecutive Mon miss** — next chance Mon 2026-06-29 13:00 UTC. File a structured issue only if that slot also misses.
- **Close ISS-001 (OAuth outage)** — deferred until ISS-006 stabilizes per existing MEMORY.md guidance. The 38-skill `success_rate < 0.5` count is denominator catch-up, not live failures.

## Fleet note

- 0 skills with `consecutive_failures ≥ 2` · 0 critical · 0 dispatched-stuck.
- 38 skills with `success_rate < 0.5` — all ISS-001 OAuth-residue denominator drag; every one is `last_status: success`. Not actionable.
- ISS-006 day 7 — partial signal today (planner ran, sweeper ran; `compute-futures-eda` still silent at 06:00). Root cause unchanged; fix unimplemented.
