---
id: advisory-verdict-can-be-operator-overridden-via-merge
created: 2026-08-10
type: lesson
links: [[aeon-app-no-write-on-swarm-repo]], [[pr-status]]
---
# On write-blocked repos, an operator merge overrides a log-only `REQUEST_CHANGES` verdict — advisory verdicts are advisory in both directions

`swarm-ai-research/swarm#551` merged 2026-08-09T13:29:44Z, ~5h55m after `pr-review`'s 38th invocation logged **REQUEST_CHANGES 3/5** (quality-gate red from a `test (3.12, full)` gw1 xdist crash and a governance-lever coverage gap at `tests/test_side_channel.py:139`). This is the first observable operator-override of a swarm-repo `pr-review` verdict in 39 invocations of [[aeon-app-no-write-on-swarm-repo]] — because verdicts land only in the activity log on this repo, they carry no merge-gate weight, and the operator can (and did) merge past a fresh REQUEST_CHANGES. Operational consequence: on write-blocked repos, treat `pr-review`'s standing verdicts as decision inputs, not policy — track `mergedAt` against last-logged verdict as a first-class signal (e.g. "override event") in the confirming-counter log so silent overrides are surfaced next scan.
