*PR Review — 2026-06-20*
Reviewed 2 PRs in swarm-ai-research/swarm.
- swarm-ai-research/swarm#518: BLOCK (0/5) — 1 critical, 2 issues. New scenario YAML schema's `extra="forbid"` is missing real top-level fields (`kernel_oracle`, `work_regime`, ...); CI shows 16 existing scenario-loader tests failing with ValidationError on this head SHA.
- swarm-ai-research/swarm#517: REQUEST_CHANGES (3/5) — 0 critical, 1 issue. Tests pass on 3.10/3.11/3.12, type-check green. Lint fails on a trivial I001 import-sort in `swarm/replay/__init__.py`; quality-gate fails downstream of lint.

Review posting was blocked — aeon's GitHub App token has no write access to swarm-ai-research/swarm (403 on reviews, inline comments, and pr comment). Verdicts emitted via this notify + memory log only.
