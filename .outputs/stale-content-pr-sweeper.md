No notify per spec (n_closed === 0 → no notify).

## Summary

- **Groups scanned:** 0 (no eligible PRs)
- **Open PRs in repo:** 0 — `gh pr list --state open --limit 100` returned `[]`
- **PRs closed:** 0
- **Skips:** none (nothing to skip)
- **`./notify` fired:** no (steady state per spec — only notify on close)
- **Log:** appended `memory/logs/2026-06-27.md` with `SWEEPER_OK`

Steady state — the PR queue is empty, so the sweeper has nothing to do.
