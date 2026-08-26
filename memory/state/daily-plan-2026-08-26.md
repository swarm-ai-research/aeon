# Plan — 2026-08-26

**Today's one thing:** click-merge PR #26 (5/5 checks green, unchanged since 08-24T01:08:19Z) OR install a repo-level auto-merge policy for `dependabot` + `app/github-actions` — Day-20 without a merge means the deliverable is now the *policy*, not the *click*.

## Ranked

1. **Merge PR #26 OR install a `dependabot + app/github-actions` auto-merge policy** *(streak 17 → 18)*. Verified this morning: `state: OPEN`, `mergedAt: null`, all 5 checks SUCCESS, `updatedAt: 2026-08-24T01:08:19Z` (no new pushes). `mergeable/mergeStateStatus` = UNKNOWN/UNKNOWN again — same transient GitHub recompute as yesterday, not a check regression. 0 `app/github-actions` PRs merged in ~461h since 08-07 unblock; 23 open aeon PRs behind. Escalation shape unchanged from Day-17 rotation: the operator either clicks once, or installs the policy so this class stops eating a planner slot daily. Serves the operator-merge-flow-proof goal.

2. **Patch `suggest-edges` to pre-filter templated-corpus siblings** *(streak 17 → 18)*. PR #52 opened this morning with the same `{2026-08-03, 2026-07-17, 2026-08-09, 2026-08-14}` `gitlawb-compute-futures-proofs/` signature — **9th consecutive PR-opening day**, and now **5 open suggest-edges PRs** (#42, #45, #49, #50, #52; +1/day net for 5 straight days). Sits above agi-tracker because agi-tracker's next silent-Mon is 5d out while this bleeds a PR daily. Fix candidate unchanged: pre-filter within-`gitlawb-compute-futures-proofs/` pairs with identical scenario-sweep tokenization before scoring. Serves the fleet-hygiene goal.

3. **Patch `stale-content-pr-sweeper` — but bundle the safety-gate fix with the `ALLOWED_AUTHORS` widening, not just the allowlist** *(streak 19 → 20)*. Yesterday proved the ALLOWED_AUTHORS text isn't the operative block anymore: even under an operator-widened `{aeonframework, app/github-actions}` allowlist, the sweeper still closed 0 of the 3 stale suggest-edges candidates because they're `MERGEABLE + UNSTABLE`, not DIRTY/CONFLICTING/UNKNOWN. With #52 opening today, #42/#45/#49/#50 are now definitively superseded — bundle a "superseded-cluster override" (skip the UNSTABLE gate when a group has ≥3 in-flight duplicates from the same skill) into the same SKILL.md patch, plus the TRACKED-prefix drift fix per [[stale-content-pr-sweeper-tracked-prefix-drift]]. Otherwise tomorrow we'll have 6 open suggest-edges PRs and the same 0 closures.

## Holding / watching

- **agi-tracker `enabled: false` PR** *(streak 10 → 11)* — 9th silent-Mon fires 2026-08-31T13:00Z (5d out). Trigger to promote: T-2 days without action landed.
- **watched-repos populate-or-disable** *(streak 20 → 21, chronic)* — 6 watched-repos-dependent skills continue same-day short-circuit cluster. Not top-3 while merge-flow + suggest-edges churn are +1/day active bleeds.
- **pr-tracker SKILL patch batch (a)–(l)** — **63d overdue** as of today; today's item (l) prefix widening to `{fix/}` bare added yesterday for seaport#1415.
- **ISS-006 messages.yml multi-pocket rewrite** *(Day-25)* — 08-25 batch OK 2/2 in 06:00–07:30Z window; watching for durability confirmation before promotion.
- **docs/status.md snapshot-rebase gate** — 40d past urgency threshold; **29th consecutive** rebase-clobber-then-regen expected on next heartbeat.
- **notegraph fingerprint sandbox friction** — n=3 promoted 08-25; will re-exercise today when notegraph extractor fires.
- **compute-futures 2.5× multiplier** — n=6 as of 08-24 CSV; watching for n=7 rename-threshold at next filing.
- **suggest-edges #49 sweeper eligibility** — hits ≥2d age gate today, but `mergeStateStatus` still gates it — likely still UNSTABLE → still skipped. See rank-3.
- **swarm-repo app-perm gap** *(Day-45)* — 62 pr-review + 41 pr-triage = 103 combined operator invocations, zero writes attempted. Class unexercised.

## Fleet note
0 broken · 0 in-flight · 0 hard-failed (7th consecutive clean morning) · 38 DEGRADED (ISS-001 Day-68 residue, all `cf: 0` + `last_status: success`) · 4 truly HEALTHY · 2 NO_DATA (50th silent day — `ai-framework-watch` + `run-frequency-guard`) · 17 filed open ISS (+1 pending ISS-021 draft, 38d carryover) · 24 open aeon-repo PRs (23 yesterday + suggest-edges #52 today) · 0 open GH issues. Both `gh pr list` / `gh issue list` responded — neither `PR_LIST_UNAVAILABLE` nor `ISSUE_LIST_UNAVAILABLE` fired.
