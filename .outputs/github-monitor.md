GITHUB_MONITOR_EMPTY_CONFIG — `memory/watched-repos.md` missing; short-circuited per SKILL step 1. No `gh` calls issued, no notification sent.

## Summary

- **Scope:** `${var}` empty → monitor-all mode (per `memory/watched-repos.md`).
- **Config:** `memory/watched-repos.md` absent at repo root; `memory/topics/watched-repos.md` also absent. Short-circuited per SKILL.md step 1.
- **Output:** `GITHUB_MONITOR_EMPTY_CONFIG` logged; no `gh` calls, no notification, no PR.
- **Streak:** config-missing streak **84 → 85** on github-monitor's witness channel (last witness 2026-10-31).
- **Files modified:** `memory/logs/2026-11-02.md`.
- **Follow-up:** unchanged — standing action-queue item "Populate `memory/watched-repos.md` OR disable 6 dependents" plus the `memory/watched-repos.md` vs `memory/topics/watched-repos.md` path mismatch reconciliation (repo-revive is the one skill still referencing the `topics/` subpath).
