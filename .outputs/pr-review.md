Merge-gate review complete. All 9 non-bot PRs on `swarm-ai-research/swarm` reviewed against the explicit operator policy (BLOCK on critical, REQUEST_CHANGES on missing coverage, APPROVE on low risk + sufficient evidence).

## Merge-gate verdicts

**APPROVE (3)**
- **#628** docs(blog) AI Village — 22/22 real checks green, CLEAN. 5/5.
- **#619** council rankers reason-before-ranking — 21/21 green including 3 new unit tests, CLEAN. 5/5.
- **#518** scenario YAML schema validation — pydantic `extra="forbid"` + 86-line test suite, 18/18 real checks green; UNSTABLE is only the non-blocking Vercel preview. 4/5.

**REQUEST_CHANGES (6)**
- **#618** fix(ms0f) wire slashing — 21/21 green but `mergeStateStatus: DIRTY`; resolve conflict and this is APPROVE-ready. 3/5.
- **#616** router intermediary — `render-verify` + `quality-gate` FAIL + DIRTY. 2/5.
- **#614** certainty-band audit — `render-verify` + `quality-gate` FAIL + BLOCKED. 2/5.
- **#612** verification aggregation rule — `render-verify` + `quality-gate` FAIL + BLOCKED. 2/5.
- **#611** Greenblatt addendum — docs-only but `render-verify` + `quality-gate` FAIL + BLOCKED. 2/5.
- **#517** fork run-diff utility — 340-line Python + new CLI with **no lint / type-check / test / CI running at all**; operator policy forbids APPROVE without quality signal. 2/5.

**BLOCK (0)** — no critical security/correctness risks.

## Why in-chat only
`gh api .../pulls/*/comments` → **403 Resource not accessible by integration** (standing [[aeon-app-no-write-on-swarm-repo]], confirmed again today). This is cycle n=3 of operator-triggered dedup-saturation — all 9 SHAs are byte-identical to yesterday's and this morning's reviews.

## Files touched
- `memory/logs/2026-10-12.md` — pr-review entry appended
- `.pending-notify/1791832901-pr-review.md` — combined one-paragraph notify queued

## Follow-ups
Standing MEMORY.md action-queue items unchanged: install aeon app with `pull_requests: write` on swarm, or gate `memory/triaged-prs.json` writes on successful post confirmation, or document swarm as report-only.
