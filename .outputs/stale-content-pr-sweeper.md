Skill complete. 0 PRs closed, no notify fired (steady state per `n_closed === 0`).

## Summary

- **Ran** `stale-content-pr-sweeper` per `skills/stale-content-pr-sweeper/SKILL.md` on 2026-11-25.
- **Scanned:** 18 open PRs.
- **Filter breakdown:**
  - 13 non-TRACKED prefix: 9× `aeon/*` reviewer-passes, 2× `skill-graph/*`, 1× `skillpacks/*`, 1× `fix/*`.
  - 5× `notegraph/*` with valid date suffix (#119, #117, #115, #114, #107) — all rejected by `ALLOWED_AUTHORS = {"aeonframework"}` because their author is `app/github-actions`.
- **Closed:** 0. **Notify:** none.
- **Files modified:** `memory/logs/2026-11-25.md` (new).
- **Follow-up:** author-allowlist defect is active — patched counterfactual would supersede 4 stale `notegraph/*` PRs behind survivor #119 (2026-11-24). Divergence from counterfactual has widened to n=5 candidates (vs n=3 on 11-15, n=1 on 10-29). The SKILL.md patch adding `"app/github-actions"` to `ALLOWED_AUTHORS` remains on the action queue in `memory/MEMORY.md`.
