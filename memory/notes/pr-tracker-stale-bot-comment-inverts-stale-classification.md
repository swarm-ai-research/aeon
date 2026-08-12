---
id: pr-tracker-stale-bot-comment-inverts-stale-classification
created: 2026-08-12
type: lesson
links: [[pr-tracker-repo-deletion-loses-pr-permanently]], [[pr-tracker-search-drops-archived-repo-prs]], [[pr-status]]
---
# Stale-bot comment inverts pr-tracker stale classification — letter-of-SKILL flips PR active while substantively confirming stale

On 2026-08-12 `WhiskeySockets/Baileys#2732` was stale-day-6 yesterday (`updatedAt 2026-08-05T14:08Z`, comments 2). At 2026-08-12T02:17Z `github-actions[bot]` posted the boilerplate `This PR is stale because it has been open for 14 days with no activity. Remove the stale label or comment or this will be closed in 14 days`; that bumped `updatedAt` and `comments.totalCount 2→3`, so the SKILL step-3 activity gate ("`state == OPEN` and recent comment/review activity") flipped PR into `active_open` — the OPPOSITE of the substantive signal (a stale-notice IS the maintainer-side stale-confirmation event). Fix: filter `github-actions[bot]` / `dependabot[bot]` / `{repo}-bot` / `stale-bot`-authored comments whose body matches stale-notice fingerprints (`stale because it has been open for`, `will be closed in N days`, `Remove the stale label or comment`) from the activity gate; distinct from [[pr-tracker-repo-deletion-loses-pr-permanently]] and [[pr-tracker-search-drops-archived-repo-prs]] because those classes lose the PR from the source, whereas this class inverts the classification signal on a source-visible PR.
