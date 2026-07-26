## Merge-gate decisions — swarm-ai-research/swarm

Queue state at 2026-07-26T19:25Z byte-identical to today's 09:00Z pr-review run: 6 open PRs, zero SHA moves, zero new bot reviews. Per SKILL dup-SHA rule 4 dependabot + 2 dup-SHA skips, so no new inline review posts (would 403 anyway per [[aeon-app-no-write-on-swarm-repo]]). Standing verdicts as operator merge-gate reviewer:

| PR | HEAD | Verdict | Confidence |
|---|---|---|---|
| #543 (rsavitt · docs: remove AI-slop writing patterns · +36/-40) | `70b20e04` | **APPROVE** | **4/5** |
| #536 (rsavitt · Fold beta_swarm into repo · +6699/-27, 55 files) | `76e6200c` | **REQUEST_CHANGES** | **2/5** |
| #537–540 (dependabot bumps) | various | *skip-by-author* — routine dep bumps, out of merge-gate scope for this reviewer | — |

Zero **BLOCK** verdicts. Zero CRITICAL findings across the queue.

**#543 APPROVE 4/5** — docs-only prose edits across `README.md` + `docs/{blog,concepts,glossary,comparison,research}`; zero production code touched. All touched-surface quality checks green: lint, type-check, invariants, kb-graph-check, render-verify, Memory Tests (3.10/3.11/3.12), CodeQL (js-ts + py ×2), Vercel preview — all SUCCESS. Sole red signal is `quality-gate` FAILURE + `test (3.12, full)` CANCELLED, both a pre-existing CI-infra pattern unrelated to a docs PR. Not 5/5 solely because gate reviewer prefers a clean board; flip to 5/5 if maintainers re-trigger CI green.

**#536 REQUEST_CHANGES 2/5** — the 6726-line bundle mixes the actual feature (`beta_swarm/` +17 files, `examples/beta/` +9, `scenarios/beta/` +3, `tests/beta/` +14, `pyproject.toml`) with **unrelated production scope creep** on `swarm/agentgit/__main__.py` (+90/-1) and `swarm/agentgit/coordination.py` (+76/-0), plus infra bundling on `.claude/hooks/pre-commit` (+24/-23), `.gitignore`, `CHANGELOG.md`, `.beads/issues.jsonl`, `.kb-graph-orphans`. Split into (a) `beta_swarm/` + `examples/beta/` + `scenarios/beta/` + `tests/beta/` + `pyproject.toml` (the actual feature, 14 test files) and (b) `swarm/agentgit/*` + hook + gitignore + CHANGELOG cleanup as a separate PR. Type-check + 3.10/3.11 compatibility tests + Memory Tests + CodeQL all SUCCESS. No CRITICAL security or correctness break — the ask is scope/reviewability, not correctness — so REQUEST_CHANGES, not BLOCK. pr-triage independently DEFER-on-size (>500 without `large-ok`).

## Summary
15th pr-review invocation on `swarm-ai-research/swarm` (2nd today). All 6 PRs skipped under SKILL rules; standing merge-gate verdicts restated for the operator: **APPROVE 4/5 #543**, **REQUEST_CHANGES 2/5 #536**, **BLOCK 0**. Notify skipped (all-skipped rule). Files modified: `memory/logs/2026-07-26.md`. Follow-up unchanged — operator PAT provisioning would let these verdicts post as actual GitHub reviews on the swarm repo.
