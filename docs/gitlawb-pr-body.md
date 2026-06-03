# PR Body — GitLawb Prototype Positioning

## Summary

This PR packages the recent GitLawb prototype work into repo-facing docs and positioning.

It adds a concise explanation of why Aeon on GitLawb matters: not just "Aeon on another git host," but a path to scaling Aeon into a much larger autonomous fleet with authority that is scoped, short-lived, observable, and withdrawable.

## What changed

- added a `GitLawb Prototype` section to `README.md`
- added a live demo walkthrough in `docs/gitlawb-demo-script.md`
- added a launch-style recap in `docs/gitlawb-demo-recap.md`
- updated `memory/logs/2026-05-24.md`

## Why it matters

Aeon already had:

- fleet spawning
- fleet monitoring
- a self-healing loop

The GitLawb prototype adds the missing decentralized control layer:

- short-lived capabilities
- gated renewal for safety-critical powers
- diff-bound self-evolution merge approval
- fleet-wide observability and delegated coordination

Together, that gives Aeon a credible path to much larger-scale autonomy without giving up the operator off-switch.

## Validation

Ran the hardened `pr-4` prototype successfully in an isolated worktree:

- `node demo.mjs`
- `node phase2.mjs`
- `node phase3.mjs`
- `node phase5.mjs`

These runs validated:

- capability expiry and escalation rejection
- fleet lifecycle control via renewal, expiry, and blocklist
- portable self-evolution gating outside GitHub branch protection
- observability plus scoped parallel and hierarchical coordination

## Next steps

1. Add screenshots or output excerpts from `phase2`, `phase3`, and `phase5` to the docs.
2. Link the demo recap from the main docs navigation or README quick-start path.
3. Decide whether the `gitlawb-safety` prototype should stay PR-only or land in-tree as an explicit prototype module.
4. Prioritize the transport/activity-feed gap so unattended renewal is backed by real signals instead of prototype scaffolding.
