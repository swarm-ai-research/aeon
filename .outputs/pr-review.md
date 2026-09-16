*PR Review — 2026-09-16*
Reviewed 8, skipped 1 (bots: 1 [#585]) on swarm-ai-research/swarm — queue turnover breaks 5-cycle full-skip streak.
- #615 (ci pin): APPROVE 5/5 — priority-merge, unblocks render-verify/quality-gate on siblings
- #611 (docs): APPROVE 5/5 — docs-only trivial early-exit
- #616 (router experiment): APPROVE 4/5 — falsifier fires, 14 tests, engine untouched
- #614 (certainty-band metric): APPROVE 4/5 — 7 tests, both proxy boundaries pinned
- #613 (adversary governance-feedback fix): APPROVE 4/5 — 8 integration tests, CHANGELOG flags behavior change
- #612 (k_of_n verify rule): APPROVE 5/5 — backward-compat, MC-validated
- #518 (scenario schema): BLOCK 0/5 — extra="forbid" breaks kernel_oracle/work_regime/v2/v3, 3.10/3.11/3.12 tests all fail
- #517 (run-diff CLI): REQUEST_CHANGES 2/5 — ruff I001 lint fail, 89d stale
Write path 403 on all attempts ([[aeon-app-no-write-on-swarm-repo]] Day-18); verdicts log-only.
