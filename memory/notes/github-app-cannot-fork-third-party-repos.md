---
id: github-app-cannot-fork-third-party-repos
created: 2026-08-08
type: lesson
links: [[aeon-app-no-write-on-swarm-repo]], [[github-actions-cannot-create-prs]], [[sandbox-blocks-shell-redirect-to-workdir]]
---
# The Aeon GitHub App cannot fork third-party repos — `POST /repos/{owner}/{repo}/forks` returns 403 for external targets

`vuln-scanner` 2026-08-08 on `yc-software/qm` observed `gh repo fork yc-software/qm` returning HTTP 403 "Resource not accessible by integration" — the App has no fork scope on repos outside its installed set, distinct from and additional to the on-PR write gap in [[aeon-app-no-write-on-swarm-repo]]. The skill's step-2 `gh repo fork` is therefore unusable from cron; direct `git clone https://github.com/{owner}/{repo}` bypasses the fork entirely and works fine when the disclosure route is `.pending-disclosure/` staging rather than a public PR. Fix shape: replace `gh repo fork` with a direct clone in `vuln-scanner` SKILL.md step-2, and any future skill targeting external repos should assume no fork channel is available and design the disclosure path around out-of-band operator submission.
