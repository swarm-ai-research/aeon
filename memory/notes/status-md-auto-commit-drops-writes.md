---
id: status-md-auto-commit-drops-writes
created: 2026-07-05
updated: 2026-07-12
type: lesson
links: [[aeon-skills-dispatch-via-messages-yml]], [[snapshot-rebase-clobbers-docs-status-md]]
status: superseded
---
# heartbeat rewrites of `docs/status.md` DELAY (not drop) — writes land ~15h later via stale-content-pr-sweeper's auto-commit sweep

Originally observed 2026-07-05 as "silently lost" — corrected 2026-07-12 memory-flush: the 2026-07-11T08:29Z heartbeat write **did** land on main at 2026-07-12T00:11:28Z (+79 lines vs the prior 2026-06-09 version) via `stale-content-pr-sweeper`'s auto-commit sweep, alongside `articles/skill-freshness-2026-07-11.md` and `articles/vuln-scan-2026-07-11.md`. So heartbeat's own workflow auto-commit `git add` glob still doesn't stage `docs/`, but the pending write is picked up ~15h later by the sweeper's broader glob — the failure mode is **delay**, not **drop**. Fix shape unchanged: audit heartbeat's auto-commit glob in `messages.yml` to include `docs/` so the page ships within the same run instead of 15+h behind. See [[snapshot-rebase-clobbers-docs-status-md]] for a compounding third failure mode discovered same day: even landed writes can be clobbered by upstream-fork snapshot pulls.
