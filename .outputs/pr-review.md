*PR Review — 2026-10-11*
`swarm-ai-research/swarm` operator run, merge-gate policy.
Reviewed 9, skipped 5 (bots: 5 dependabot).

APPROVE (3):
- swarm#628 (5/5) — docs blog, all checks green
- swarm#619 (5/5) — council rankers reasoning + RANKING: marker; 20/20 green
- swarm#518 (4/5) — scenario YAML schema; fork but 18/18 real checks green

REQUEST_CHANGES (6):
- swarm#618 (3/5) — slashing wire-up: code+tests clean, but merge DIRTY — rebase
- swarm#616 (2/5) — router intermediary: render-verify FAIL + merge DIRTY (4w stale)
- swarm#614 (2/5) — certainty-band audit: render-verify FAIL + BLOCKED (4w stale)
- swarm#612 (2/5) — verification agg rule: render-verify FAIL + BLOCKED (4w stale)
- swarm#611 (2/5) — Greenblatt docs addendum: render-verify FAIL + BLOCKED (4w stale)
- swarm#517 (2/5) — run-diff utility: fork PR with NO lint/type/test CI run — only Vercel; merge-gate requires evidence

BLOCK (0) — no critical correctness/security breaks.
Writes all 403'd (standing `aeon-app-no-write-on-swarm-repo`); verdicts in `memory/logs/2026-10-11.md`.
