## Summary

Repo-revive skill ran and exited on the `REPO_REVIVE_NO_CONFIG` clean-exit path — `memory/topics/watched-repos.md` is missing (same state as prior 2026-06-20 / 06-27 / 07-04 runs and flagged in MEMORY.md "Next priorities"). `${var}` was empty so no override, no auto-selection possible, no PR / tweet / notify. Logged to `memory/logs/2026-07-11.md`. Follow-up: operator must populate `memory/topics/watched-repos.md` (≥100★ non-archived repos, one `- owner/repo` per line) to activate this skill; optionally add `memory/topics/stale-models.md` to enable the stale-model fix category.
