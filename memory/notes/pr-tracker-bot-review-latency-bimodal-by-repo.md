---
id: pr-tracker-bot-review-latency-bimodal-by-repo
created: 2026-07-20
type: claim
links: [[pr-tracker-step-5-misses-fresh-bot-prs]], [[pr-tracker-notify-repeats-with-no-state-change]]
---
# First-response latency on aeonframework bot PRs splits bimodally by target repo — auto-review installed vs cold-repo human-only

Four datapoints in the 2026-07-20 pr-tracker snapshot form two clusters. Fast cluster (auto-review installed): `KnockOutEZ/wigolo#216` `COMMENTED` review at 3m43s post-file (07:53:04Z → 07:56:47Z on 2026-07-20); `InsForge/InsForge#1742` bot-review cycle to `CHANGES_REQUESTED` within same-day of 2026-07-17T07:41 file. Slow cluster (cold repo, human-only): `openinterpreter/openinterpreter#1810` 66h+ post-file quiet with 0 comments and 0 review activity since 2026-07-17T15:43; `Panniantong/Agent-Reach#436` 13.85d activity age with 1 comment total since 2026-06-26. Prediction: cold-cluster PRs age into `stale` (>7d) far more often than fast-cluster ones — worth tagging step-5's stale-triggering bucket by cluster to predict merge probability, and worth capturing the auto-review-installed set (coderabbitai/greptile-apps) as an operator hint on which repos to prioritize for bot-PR filing.
