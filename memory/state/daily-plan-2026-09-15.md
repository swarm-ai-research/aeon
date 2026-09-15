# Plan — 2026-09-15

**Today's one thing:** Escalate the `aeonframework` GitHub identity 404 from Day-1 candidate to Day-2 confirmed, and get the operator eyes on the account before the whole PR-authoring fleet silently collapses.

## Ranked

1. **Confirm-and-escalate `[[aeonframework-github-identity-suspension]]` → Day-2 accepted class.** Just re-ran the three probes from yesterday's pr-tracker: `/users/aeonframework` HTTP 404, GraphQL `user()` NOT_FOUND, `search(author:aeonframework is:pr)` `issueCount: 0`. All three still failing, ~20h after the 09-14 detection. This is a fleet-existential signal — every downstream PR path (pr-tracker, external-feature, vuln-scanner disclosure, all `app/github-actions`-authored PR queues) reads through this identity, and the memory-tracked "PR-authoring UNBLOCK Day-37" arc is meaningless if the identity itself is suppressed server-side. Concrete steps today: (a) promote the candidate class in `[[fleet-ops]]` to accepted; (b) file ISS-028 (category `permanent-limitation` pending root cause, severity `high`) — needs a skill dispatch, not planner-authored per the health-vs-repair separation; (c) surface loudly via notify so operator can check account status / appeals inbox on github.com. Waiting for `self-review` to file it Sunday burns another 5 days of quiet degradation.

2. **ISS-006 pocket-slot migration — stuck-goal escalation, no restatement.** `iss-006-messages-yml-multi-pocket-rewrite` streak advances to 32 today; the interim mitigation (`planner` 30 6 + `compute-futures-eda` 0 6 → live-pocket slots) has been rank-1 or rank-2 for a full week without movement. Both skills 7d silent at their crons (last_success 2026-09-08T07:47:39Z for both). Today's planner dispatch at 06:46Z is happening because the operator invoked it manually — so the 06:00Z pocket is *not* self-recovering. Stop re-listing this and either (a) migrate the two crons to `30 8` / `0 9` in a branch+PR today, or (b) explicitly promote it back to the `[[fleet-ops]]` top-of-file with a hard deadline. The multi-pocket rewrite is the real fix but the migration is the safe interim.

3. **PR #26 regressed — no longer MERGE-READY.** Memory says PR #26 was 5/5 CI SUCCESS since 08-24 and just needed operator-click. Not anymore: dependabot force-rebased at 2026-09-14T01:07:51Z and the new run has **1 FAIL / 4 PASS** — `ShellCheck` on the Lint workflow fails, mergeStateStatus is UNSTABLE, mergeable is MERGEABLE (mechanical) but the merge-gate policy will block. The 22-day rank-3 "prove end-to-end merge flow" framing needs a fresh diagnosis, not another day of "click merge." Someone (skill-repair, or a manual pass) has to look at what ShellCheck flagged in the rebased diff. This is new signal today and outranks the older chronic items below.

## Holding / watching

- **`skill-repair` 86d silent.** Highest-severity chronic gap (blocks ISS resolution progression across the whole 23-open queue), but it needs an operator-scope revive-or-disable decision I can't make from the planner seat. Holding until an operator PR lands or self-review escalates it explicitly next Sunday. Trigger to re-rank: any new CRITICAL/FLAPPING classification skill-health can't file because skill-repair is dark.
- **`agi-tracker: enabled: false`.** 11th silent-Mon already fired 09-14T13:00Z empty. Next slot 2026-09-21. Not urgent this week — hold.
- **`memory/watched-repos.md` populate-or-disable — streak-45 today.** 6 dependents silently short-circuiting. Chronic. Operator-decision boundary. Holding until either the file lands or a PR flips the 6 dependents' `enabled: false`.
- **`pr-tracker` SKILL patches (a)-(o) — 79d overdue.** Moot until #1 above resolves — the identity-suspension anomaly makes almost every one of the (a)-(o) items untestable. Explicitly deferring to whenever `aeonframework` becomes API-resolvable again.
- **`stale-content-pr-sweeper` ALLOWED_AUTHORS patch — Day-8.** Sitting at 9-blocked-per-run (up from 8 on 09-13). Low-blast-radius quality-of-life fix; hold until #1/#2 clear.
- **`docs/status.md` snapshot-rebase gate — 58d past urgency threshold.** Hold — no incident this week attributable to it.

## Fleet note

0 broken · 0 in-flight · 0 hard-failed · 38 DEGRADED (ISS-001 residue Day-86) · 4 HEALTHY · 2 NO_DATA · 23 open ISS · reactive trigger did NOT fire (0 skills at consecutive_failures ≥ 2 in cron-state.json).

## Sources

- `memory/MEMORY.md` (current-focus + action-queue), `memory/cron-state.json`, `memory/logs/2026-09-14.md` + `2026-09-13.md`, `memory/issues/INDEX.md`.
- `memory/state/planner-state.json` (prior run 2026-09-08T06:30:00Z, top_priority `articles-gitkeep-agi-tracker-bundle`).
- `gh pr list` OK (31 open, matches sweeper); `gh issue list` returned empty (0 open).
- Live identity probes for #1: `/users/aeonframework` 404, GraphQL `user()` NOT_FOUND, `search(is:pr)` issueCount=0 — Day-2 confirmed.
- Live CI check for #3: `gh pr checks 26` — ShellCheck FAIL, 4 pass.
