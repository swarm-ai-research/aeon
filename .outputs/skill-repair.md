*skill-repair — REPAIR_DIAGNOSED_NO_FIX*
Target: systemic cluster (≥30 skills — compute-futures-eda, notegraph, suggest-edges, ...)
Root cause: 0.7s zero-token fail-fast — likely Anthropic auth/availability ~5.5h window (2026-06-19 20:25Z → 2026-06-20 01:53Z). Recovery batch at 06:05Z+ is now succeeding (34/34).
Fix: blocked — actual fix lives in `.github/workflows/aeon.yml` lines 511–521 (error capture strips `result` field; only the JSON envelope tail reaches cron-state.last_error). Workflow file is off-limits to skill-repair.
PR: none — branch `fix/skill-repair-systemic-2026-06-20` pushed; operator must open PR (gh-actions bot lacks permission). Issue: ISS-001.
Verify: read `memory/issues/ISS-001.md`. After operator patches aeon.yml per its "Operator action" section, re-dispatch any affected skill; new `last_error` should be human-readable.
