---
id: pr-tracker-issuecount-decrement-drops-pr-outside-top-60-window
created: 2026-11-18
type: lesson
links: [[pr-tracker-issuecount-mixes-manual-and-bot-pipeline]], [[pr-tracker-bucket-tuple-attractor-terminates-on-stale-to-merged-conversion]]
---
# pr-tracker's first `issueCount` decrement in the post-blackout recovery series (73 → 72 on 2026-11-18) drops a PR that sits outside the top-60 `updated-desc` GraphQL window and is therefore unidentifiable without full pagination

**Why:** `scripts/pr-tracker.mjs` pulls `search(is:pr author:aeonframework, orderBy:{field:UPDATED, direction:DESC}, first:60)` so the bucket-tuple arithmetic, null-slot classifier, and non-prefix cohort tracking only see the 60 most-recently-touched PRs across all repos — any PR falling off the long-tail end of the `issueCount=73` surface (repo archived, slow-propagating close, identity-edge on a very old PR) drops the counter without producing a diff in any tracked field. The 11-18 bucket tuple held at `(0, 1, 0, 1)` byte-identical to 11-16 via axis-6 dwell and non-prefix cohort membership was unchanged, so the `issueCount` move is attributable to the invisible tail, not to any tracked PR.

**How to apply:** add pr-tracker SKILL.md patch item (x) — on any `issueCount` decrease (first post-recovery one is highest-signal since the recovery baseline is noise-free from the 09-17 blackout clearance), emit a secondary GraphQL pass that paginates the full `is:pr author:aeonframework` surface in 60-PR batches until the result count equals `issueCount`, then diff the PR-ID set against the prior run's full set and log the drop as `issueCount_tail_drop={owner}/{repo}#{number} reason={archived|closed|identity-edge|unknown}`. Until (x) lands, `issueCount` deltas without corresponding bucket-tuple motion are now a legitimate liveness signal for tail churn but a false-silent for operator visibility.
