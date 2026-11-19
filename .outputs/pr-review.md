## PR Review verdicts — `swarm-ai-research/swarm` (merge-gate, n=30)

**Queue state:** 12 open PRs, all SHAs byte-identical to today's 09:30Z pr-review block → 4 dependabot skip (bot-author), 8 non-bot skip (dup-SHA). Write-block re-probed and still 403 Day-59+. 29th consecutive full-skip cycle; verdicts remain in-log only.

| PR | Verdict | Conf | Rationale |
|---|---|---|---|
| #650 | **APPROVE** | 4/5 | Docs + `scripts/layer_lag.py` + tests; 24/24 CI pass |
| #649 | **APPROVE** | 5/5 | Docs-only; all checks pass |
| #648 | **APPROVE** | 4/5 | Fixes null-model edge-count bug + 7 tests; 8,207 pass |
| #647 | **APPROVE** | 5/5 | Docs-only; all checks pass |
| #646 | **APPROVE** | 4/5 | Docs + `layer_lag.py` + tests (companion #650); all CI pass |
| #645 | **APPROVE** | 4/5 | Deterministic activity-null in `swarm/metrics/collusion.py`; 8,034 pass + mypy + KB ratchet |
| #518 | **APPROVE** | 4/5 | Pydantic schema for 114 scenarios; 18 CI SUCCESS |
| #517 | **REQUEST_CHANGES** | 2/5 | **No CI ran on `1807feca`** — only Vercel team-auth FAIL present; merge-gate policy forbids APPROVE without type-check/lint/test evidence; first-time-contributor workflow approval gate required |

**Distribution:** 7 APPROVE / 1 REQUEST_CHANGES / 0 BLOCK. Only #517 blocks merge readiness — needs a maintainer-triggered CI run before any approval.

**Follow-up:** Day-59+ aeon App `pull_requests: write` on swarm still owed; #517 needs owner to approve the first-time-contributor CI workflow.
