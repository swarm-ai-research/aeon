Executed `skills/pr-review/SKILL.md` against `${var}=swarm-ai-research/swarm` with the operator merge-gate policy layered on top.

## Summary

**Scope**: swarm-ai-research/swarm — 8 open PRs.

**Decisions**: 0 fresh reviews posted. All 8 PRs hit skip rules:
- **6 dependabot bot-authored**: #553 (langchain-anthropic), #552 (setuptools), #550 (langchain-core), #546 (langgraph), #538 (actions/github-script), #537 (actions/setup-python) — SKIP `bot-author`.
- **#549** (rsavitt, Prime Agent, SHA `afe51248`): SKIP `dup-SHA` — headRefOid already reviewed in 08-12 + 08-13 logs (10 prior invocations, ~7d frozen). **Standing merge-gate verdict: REQUEST_CHANGES 2/5** — carried forward.
- **#543** (rsavitt, docs AI-slop removal, SHA `bad79e48`): SKIP `dup-SHA` — same dedup pattern. **Standing merge-gate verdict: APPROVE 5/5** — carried forward.

Bot-reviewer-recently rule not triggered — latest `copilot-pull-request-reviewer` reviews are 2026-08-07, far outside the 30-min window.

**Notify**: not fired (all-skip → log-only per skill).

**Files**: `memory/logs/2026-08-14.md` (this run's `## pr-review` entry). No PR, no inline comments. 45th consecutive invocation on this repo producing zero human-review action.
