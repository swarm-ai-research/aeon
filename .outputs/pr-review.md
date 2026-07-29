Merge-gate verdicts for `swarm-ai-research/swarm` (19th invocation, both non-bot PRs dup-SHA vs 07-28 but re-derived fresh per operator ask):

## Verdicts

**swarm#543 (rsavitt, "docs: remove AI-slop writing patterns", HEAD `70b20e04`)** — **APPROVE, confidence 4/5**
- 12 files, 36 additions / 40 deletions, all under `README.md` + `docs/{blog,concepts,glossary,comparison,research}`.
- Touched-surface CI all green: lint, type-check, invariants, kb-graph-check, render-verify, CodeQL (js-ts + py×2), Memory Tests Short (3.10/3.11/3.12), Memory Baseline Validation, test (3.10/3.11 compatibility), agentgit-gate, Vercel Preview.
- Sole red: `test (3.12, full)` CANCELLED (matrix cancellation) + `quality-gate` FAILURE (aggregator inheriting from that cancellation). Zero causal link to a docs-only change.
- Not 5/5 because the aggregator is red; flips to 5/5 if maintainers re-trigger CI clean.

**swarm#536 (rsavitt, "Fold beta_swarm (distributional generalization) into the repo", HEAD `76e6200c`)** — **REQUEST_CHANGES, confidence 2/5**
- 56 files, 6699 additions / 27 deletions. PR body claims "Purely additive — no existing `swarm/` code is touched." This is factually contradicted.
- 11 files sit outside the claimed beta scope, including production changes: `swarm/agentgit/__main__.py` (+90/−1), `swarm/agentgit/coordination.py` (+76/−0), plus `.claude/commands/claim.md` (+53), `.claude/hooks/pre-commit` (+24/−23), `tests/test_agentgit_coordination.py` (+71/−0), CHANGELOG/CLAUDE.md/.gitignore/.beads/.kb-graph-orphans.
- The `swarm/agentgit/*` changes are an unrelated **claim/coordination-gate** primitive (cross-worktree duplication prevention). Internally well-tested (71 lines new coordination tests, dedicated `agentgit-gate` CI job green) but scope-orthogonal to "fold beta_swarm subtree".
- CI otherwise: same shape as #543 — 17 SUCCESS + 1 CANCELLED + 1 FAILURE (aggregator) + 2 SKIPPED. All 120 beta tests + 71 coordination tests pass.
- No CRITICAL correctness/security break warrants BLOCK — both features are individually well-tested and green. But the merge-gate rubric's "evidence sufficient to the touched surface" bar fails on (a) mixing two independent features in one 6699-line bundle and (b) mislabeling scope in the body.
- **Ask:** split into two PRs (beta_swarm/tests/scenarios/examples/beta extra vs. agentgit claim gate + tooling), and correct the "purely additive" sentence to enumerate the `swarm/agentgit/` changes explicitly.

**Zero BLOCK verdicts.** 5 dependabot PRs (#537/#538/#539/#540/#545) skipped by bot-author rule. No writes attempted to swarm repo per the standing [[aeon-app-no-write-on-swarm-repo]] pattern (13th confirming invocation); verdicts held log-only and returned here.

## Summary

- Reviewed `swarm-ai-research/swarm` under merge-gate policy (APPROVE / REQUEST_CHANGES / BLOCK).
- 7 open PRs → 5 bot skips, 2 fresh operator verdicts re-derived on dup-SHA rsavitt PRs.
- **swarm#543: APPROVE 4/5. swarm#536: REQUEST_CHANGES 2/5. No BLOCKs.**
- Files modified: `memory/logs/2026-07-29.md` (pr-review section appended).
- Follow-ups: operator PAT provisioning would let verdicts post as real GitHub reviews (rank-1 planner ask, streak-3); dup-SHA suppression drops the next time either branch moves.
