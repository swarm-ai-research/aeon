---
id: github-actions-cannot-create-prs
created: 2026-06-20
type: lesson
links: [[aeon-app-no-write-on-swarm-repo]]
---
# The default GitHub Actions token cannot create or approve pull requests

`gh pr create` (and the `createPullRequest` GraphQL mutation) returns "GitHub Actions is not permitted to create or approve pull requests" — observed on `skillpacks/2026-06-20` and `notegraph/2026-06-20` branches. Skills that build branches must push and then surface the `compare/<branch>` link in the notify; operator opens the PR manually, or the repo enables the "Allow GitHub Actions to create PRs" toggle.
