---
id: verdict-relative-to-main-resurfaces-when-branch-pr-blocked
created: 2026-07-26
type: lesson
links: [[github-actions-cannot-create-prs]], [[skill-state-on-blocked-pr-branch-is-lost]], [[fleet-ops]]
---
# Skills that phrase their verdict as "new vs main" re-emit the same "new" verdict every run when the landing PR is blocked

`skillpacks` reported the `outages-fleet` pack as a NEW pack on 2026-07-05, 2026-07-19, and again 2026-07-26 — three consecutive fires of the identical `SKILLPACKS_NEW_PACK` verdict because none of the branches ever merged past [[github-actions-cannot-create-prs]]. Same shape on `workflow-security-audit`: BOOTSTRAP verdict fired 2026-07-19 and 2026-07-26 with the same "no prior article on main" reasoning. Fix: verdict comparators should read the latest committed state (branch OR main), not only main — or the notify text should say "still-unmerged" instead of "new" so the operator doesn't parse it as fresh news.
