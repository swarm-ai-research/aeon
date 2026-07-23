## Summary

pr-review on `swarm-ai-research/swarm` under merge-gate policy. Queue non-empty for the first time in 5 days: 5 open PRs, 4 dependabot-skipped, 1 human PR reviewed.

**swarm#536** (`rsavitt`, "Fold beta_swarm (distributional generalization) into the repo", +6699/-27 across 54 files, HEAD `76e6200c`) →
- **Verdict: REQUEST_CHANGES**
- **Confidence: 3/5**

**Evidence**: lint / type-check (mypy) / invariants / CodeQL / Memory Tests / test (3.10 compat) / test (3.11 compat) all PASSED. Blocking: **quality-gate = FAILURE** because `test (3.12, full)` was CANCELLED at 99% (hung on `test_moltipedia_scenario.py::test_moltipedia_scenario_loads`). The primary-Python full-suite run — the only one that would exercise the 120 new `tests/beta/` tests alongside the pre-existing swarm suite — did not complete on this head.

**Findings (4 ISSUE, 0 CRITICAL, 0 NIT):**
1. `swarm/agentgit/coordination.py:47` — PR body says "purely additive, no swarm/ touched" but 166 lines of unrelated `claim`-subcommand + shared-DB helpers are bundled under a beta_swarm title (bisect + revert hazard).
2. `.claude/hooks/pre-commit:462` — §6c replaces the always-on shared-checkout tripwire with a marker-conditional gate that silently no-ops if the developer forgets `/claim` (reopens the 2026-07-22 duplicate-work failure mode).
3. `swarm/agentgit/__main__.py:307` — `cmd_claim` prints `CLAIMED … bead → in_progress` after a best-effort `bd update` whose failure is swallowed (divergent state between claim DB and bead tracker).
4. `pyproject.toml:63` — new `beta` extra is redundant with `analysis` in CI; document for external `pip install swarm[beta]` consumers.

**Delivery**: Inline comments (`gh api …/pulls/536/comments`) and review body (`gh pr review`) both returned 403 "Resource not accessible by integration" — the app-write block on `swarm-ai-research/swarm` per [[aeon-app-no-write-on-swarm-repo]] persists (9th confirming invocation). Per skill fallback, findings preserved verbatim in `memory/logs/2026-07-23.md`.

**Files modified**: `memory/logs/2026-07-23.md` (pr-review section appended), `.pending-notify/1784800953-pr-review.md` (new).

**Follow-ups**: (a) 3.12-full cancellation is likely a pre-existing flake — worth a CI rerun on head to disambiguate; (b) provisioning a repo-scoped PAT for swarm-repo write remains the unblock for actually posting these findings; (c) if #536 merges as-is, the pre-commit reliability regression + scope-creep land on main.
