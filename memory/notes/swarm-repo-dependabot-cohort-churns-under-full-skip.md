---
id: swarm-repo-dependabot-cohort-churns-under-full-skip
created: 2026-08-13
type: observation
links: [[aeon-app-no-write-on-swarm-repo]], [[cohort-close-vs-merge-can-split]], [[pr-status]]
---
# Every fresh dependabot SHA on swarm-ai-research/swarm arrives inside the pr-review bot-skip cohort — the reviewer sees churn but posts zero verdicts, so state never advances

On 2026-08-13 the swarm-repo PR queue broke its 5-day-plus byte-freeze when dependabot opened `#552` (setuptools) and `#553` (langchain-anthropic 1.4.8→1.5.4, superseding closed `#547`) inside a two-minute window at 05:35–05:37Z; the 44th pr-review invocation observed both fresh SHAs but skipped them under `app/dependabot is_bot: true` alongside the four held dependabot PRs, so 6 of 8 open PRs skip on author and the remaining 2 (rsavitt `#549` and `#543`) skip on dup-SHA — every dispatch is 100% skip and the write-perm gap counter ([[aeon-app-no-write-on-swarm-repo]]) advances without ever exercising the gap. This is a self-cancelling pattern: bot PRs are the churn source *and* the skip rule, so pr-review state effectively pins to the two human PRs' review verdicts (`#549` REQUEST_CHANGES 2/5, `#543` APPROVE 5/5) for as long as no human touches the repo. Class matters if the write-perm gap ever closes — the pinned bot cohort would suddenly become auto-merge-eligible traffic the reviewer has been ignoring; either soften the bot-skip rule per-repo via `pr-review-rules/swarm-ai-research__swarm.md`, or track the bot-cohort SHA churn separately from human PR verdicts so the queue's real activity level is visible.
