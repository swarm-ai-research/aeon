# Plan — 2026-08-10

**Today's one thing:** Ship the `agi-tracker: { enabled: false }` PR on `aeon.yml:188` **and** get it merged before 13:00Z (~5.5h out). Monday is deadline day — the 6th consecutive silent-Mon fire is imminent. Authoring is proven (19 PRs already staged), merging is not — so today's task is both: land the PR, then merge it plus at least one twin to prove flow. Without the merge, the PR just becomes the 20th queued.

## Ranked

1. **`agi-tracker: enabled: false` on `aeon.yml:188` — draft PR AND merge before 13:00Z (~5.5h).** Streak-4 today (was rank-1 streak-3 yesterday). `skills/agi-tracker/` directory re-verified missing this run; the weekly Mon 13:00Z cron fires into thin air per [[agi-tracker-missing-skill-md-dispatches-no-op]] and posts the 6th consecutive silent-Mon success. One-line YAML flip, no dependent state. Ship on a branch like `aeon/disable-agi-tracker-2026-08-10` and pair with an operator merge — the queue-merge escalation below is the twin, not a separate item.
2. **Prove aeon-repo merge flow — merge one low-risk PR (bundled with rank-1).** Streak-2 today; MEMORY.md line 42 escalation trigger fired yesterday and compounded overnight — queue is now **19 open** (15 at yesterday's plan, 17 at today's 00:04Z sweeper, 19 now with #26 dependabot + #27 notegraph added since). **0 merges** across `app/github-actions` PRs in ~72h+ post-unblock. All spot-checked PRs remain `mergeStateStatus: UNKNOWN` + empty `statusCheckRollup` — nothing gates them. Best candidates for the proof-merge: #10 (notegraph orphan flag, 74h+, dep-free), #27 (today's notegraph regen, +2 real nodes, clean diff), or the twin `suggest-edges` pair (#21+#22). Configuring auto-merge for `app/github-actions` PRs after the first proof-merge would end this escalation permanently.
3. **`stale-content-pr-sweeper` `ALLOWED_AUTHORS` patch — one-line map extension.** Streak-4 today (was rank-3 streak-2 yesterday). Today's 00:04Z sweeper run confirmed the silent no-op for the 4th day: **4 branch-prefix matches (#10 notegraph, #14+#21+#22 suggest-edges), 0 passed the `{"aeonframework"}` allowlist, 0 closed.** The #14 ← #21 ← #22 supersession chain now stands at 3-deep. Add `"app/github-actions"` to `ALLOWED_AUTHORS` in step-1; also flag branch-prefix drift on #23 (`compute-macro/*` vs TRACKED `compute-macro-correlate`). Bundle into the same PR wave as rank-1.

## Holding / watching

- **`watched-repos` populate OR disable the 6 dependent skills** — streak-5 in holding. Chronic non-urgent; yesterday produced the daily short-circuit trio (github-monitor + issue-triage + code-health). Re-ranks when the fix lands or a new dependent skill enters the fleet.
- **`pr-tracker` SKILL.md 9-item patch batch** — 47d overdue as of today. Daily inline-enactment continues to work; land only after rank-1/2 clear so the queue doesn't grow another content PR under a live deadline.
- **ISS-006 `messages.yml` per-slot cron rewrite** — this planner fire at 07:25:04Z is **55min late** vs scheduled 06:30Z; compute-futures-eda at 07:25:14Z is **85min late** vs 06:00Z. Late-pocket cluster held again (Day 9). Subordinate to Mon deadline.
- **`docs/status.md` snapshot-rebase clobber gate** — 24d past urgency threshold; expect the 14th consecutive wholesale regen from tonight's heartbeat. Two-part fix in MEMORY.md line 49 still viable.
- **Swarm-repo App-perm gap** — 28th confirming invocation; #551 was merged yesterday at 13:29:44Z under an operator override of the pr-review `REQUEST_CHANGES 3/5` verdict — the first observable override in 39 invocations. DISTINCT from aeon-repo unblock; out of planner scope.

## Fleet note

0 broken · 0 in-flight · 38 DEGRADED (ISS-001 residue day 51 — literal-rule only, substantively green: all at `last_status: success` + `consecutive_failures: 0`) · 4 HEALTHY · 2 NO_DATA (`ai-framework-watch` + `run-frequency-guard`, **33rd** consecutive silent day per [[enabled-skills-can-never-dispatch]]) · skill-health hash `e27c0ac60367e7e5` **45th** consecutive steady-state day · 18 open issues · 19 open aeon PRs (0 merged in 72h+ post-unblock).
