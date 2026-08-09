---
id: pr-creation-toggle-is-distinct-from-merge-capability
created: 2026-08-09
type: lesson
links: [[github-actions-cannot-create-prs]], [[skill-state-on-blocked-pr-branch-is-lost]], [[verdict-relative-to-main-resurfaces-when-branch-pr-blocked]]
---
# Unblocking Actions to CREATE PRs does not move the queue — merging is a separately-gated capability

The overnight 2026-08-07 Repo Settings toggle that let `app/github-actions` open PRs on this repo (12 fresh PRs #10-#21 across four bursts within 32h) did nothing for the merge path: 48h+ later, **0 of those 12 PRs merged** and today's queue reached 15 open with `mergeStateStatus: UNKNOWN` and empty `statusCheckRollup` on every spot-checked PR — no CI or branch-protection is gating, they simply sit until an operator merges. `github-actions-cannot-create-prs` is thus one of *two* independent levers: enabling creation without also configuring auto-merge (or scheduling operator sweeps) converts a creation-blocked backlog into a merge-blocked backlog with worse ergonomics (many small PRs vs one waiting branch). Downstream skills that rely on "PR opened → PR merged within days" (notegraph state landing, skillpacks version bumps, `docs/status.md` regen) still hit `skill-state-on-blocked-pr-branch-is-lost` on the same wall clock as before the toggle.
