## Merge-gate verdicts — swarm-ai-research/swarm (2026-11-25)

**Run posture:** every open PR was skippable under skill rules (4 dependabot + 8 dup-SHA against 11-23 log, same byte-identical SHAs), and the aeon GitHub App token still has no write scope on this repo (Day-65+), so no GitHub-side reviews were posted. Verdicts below carry forward from the 2026-11-21 fresh evaluation at unchanged head SHAs — non-bot queue has been frozen since 2026-10-25T21:30:09Z.

| PR | SHA | Verdict | Confidence | Why |
|---|---|---|---|---|
| swarm-ai-research/swarm#650 | 31dbe49 | APPROVE | 5/5 | rsavitt pace-layers reopen variant; no protected paths touched |
| swarm-ai-research/swarm#649 | ecc31b8 | APPROVE | 5/5 | docs-only cross-link fix (+11/-8) |
| swarm-ai-research/swarm#648 | 3f6a577 | APPROVE | 5/5 | rsavitt null-model audit with tests, no protected paths |
| swarm-ai-research/swarm#647 | b13ccc9 | APPROVE | 5/5 | docs-only, +177/-0 |
| swarm-ai-research/swarm#646 | 47f451b | APPROVE | 4/5 | rsavitt pace-layers note + `scripts/layer_lag.py` + tests |
| swarm-ai-research/swarm#645 | 1f3d01e | APPROVE | 4/5 | collusion activity-null calibration with tests |
| swarm-ai-research/swarm#518 | a4773a2 | APPROVE | 4/5 | go165 scenario YAML schema validation; all 20+ CI checks green. Human nudge: PR body contains unsolicited "Payout wallet" from first-time external contributor — verify identity + bounty authorization before merge |
| swarm-ai-research/swarm#517 | 1807fec | **REQUEST_CHANGES** | 3/5 | **[ISSUE]** new `python -m swarm diff` CLI has no e2e test; **[ISSUE]** zero CI gates ran on head SHA (CI / CodeQL / Memory Management Tests all `action_required`); **[ISSUE]** eager top-level import of `swarm.replay.diff` risks breaking every `from swarm.replay import ...` consumer; **[ISSUE]** unrelated `cast(int, _run_autoresearch(args))` scope-creep in `cmd_autoresearch` without PR-body justification |

**Distribution:** 7 APPROVE / 1 REQUEST_CHANGES / 0 BLOCK across the 8-PR non-bot cohort. No critical security or correctness risk surfaced; the sole REQUEST_CHANGES (#517) is blocked on missing test/type-check evidence and an import-time contract hazard, not a confirmed break.

## Summary
- Ran `skills/pr-review/SKILL.md` against `swarm-ai-research/swarm` under merge-gate operator policy; 12/12 open PRs skipped (4 dependabot, 8 dup-SHA vs 11-23 log).
- No GitHub-side posts — Day-65+ aeon-app write-block on this repo per [[aeon-app-no-write-on-swarm-repo]]; verdicts captured in `memory/logs/2026-11-25.md` only.
- Carry-forward merge-gate decisions: **7A / 1R / 0B**; `#517` is the sole REQUEST_CHANGES, `#518` has an operator-nudge flag about an unsolicited payout-wallet line from a first-time external contributor.
- Files modified: `memory/logs/2026-11-25.md` (appended `### pr-review` section).
- No notification sent per SKILL rule (every PR skipped). Follow-up still owed: patch `pr-review` SKILL.md to gate `memory/triaged-prs.json` write on successful post + optionally emit a one-line notify after N consecutive full-skip cycles (standing action-queue item in `memory/MEMORY.md`).
