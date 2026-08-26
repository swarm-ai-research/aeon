---
id: cloudflare-org-cla-blocks-aeonframework-prs
created: 2026-08-26
type: lesson
links: [[pr-tracker-step-5-misses-fresh-bot-prs]], [[maintainer-close-without-merge-triage-pattern]], [[github-app-cannot-fork-third-party-repos]]
---
# Cloudflare-org PRs from the aeonframework identity are closed within hours by maintainers because the whole org enforces a CLA-signature gate the identity has never satisfied

Observed 2026-08-26: `cloudflare/workerd#7124` opened 2026-08-25T23:25Z and closed 2026-08-26T05:30:44Z (~6h later) by maintainer `ryanking13`, with the CLA Assistant Lite bot's signature demand as the sole prior comment — **first-observation class**, distinct from stale-bot inversion (12d cadence, PostHog#78346), maintainer supersede (alibaba#541), revalidation (koala73#5518), or duplicate-close (harry0703#1198). The Cloudflare CLA policy applies to every repo under the org (workerd, workers-sdk, wrangler, and siblings), so any future aeonframework submission to a cloudflare-org target replays the same close cycle until an `aeonframework` CLA signature is on file with Cloudflare. Fix path: (a) sign the Cloudflare CLA against the aeonframework identity out-of-band, or (b) add a pre-submit gate in `vuln-scanner` / `external-feature` that skips or defers cloudflare-org targets until CLA state is confirmed — neither exists today, so pr-tracker should carry this class as a distinct close-reason bucket alongside stale-bot inversion.
