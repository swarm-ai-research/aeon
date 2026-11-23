## Summary

**Scope**: `swarm-ai-research/swarm` with merge-gate operator policy (APPROVE/REQUEST_CHANGES/BLOCK).

**Result**: 12 open PRs, **all 12 skipped** — no new reviews posted, no notify per "every PR skipped → do not notify" rule.

**Skip breakdown**:
- 4 dependabot (bot author): #661, #660, #657, #655
- 8 non-bot dup-SHA vs 2026-11-21 log: #650, #649, #648, #647, #646, #645, #518, #517 — queue frozen since 2026-10-25T21:30Z

**Carry-forward verdicts** (unchanged, same head SHAs):
- APPROVE × 7 (3/5–5/5 confidence): #650, #649, #648, #647, #646, #645, #518
- REQUEST_CHANGES × 1 (3/5): **#517** — [ISSUE] no e2e test for new `swarm diff` CLI entry; [ISSUE] zero CI gates ran on head SHA (only a failed Vercel auth); [ISSUE] eager top-level import of `swarm.replay.diff` risks breaking existing `from swarm.replay import ...` consumers + unrelated `cast(int, _run_autoresearch(args))` scope-creep
- BLOCK × 0

**Standing constraint**: Day-63+ aeon-app write-block on swarm (403 on `addPullRequestReview`) means even non-dup reviews cannot post; 30th consecutive full-skip cycle recorded.

**Files modified**:
- `memory/logs/2026-11-23.md` (created)

**Follow-up**: Per existing action queue, patch `pr-review` SKILL.md to gate `memory/triaged-prs.json` write on successful post confirmation; swarm needs aeon-app `pull_requests: write` + `issues: write` OR documentation as report-only.
