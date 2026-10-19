No candidates to triage — all 4 open PRs on `swarm-ai-research/swarm` within the 14-day window are from `app/dependabot` (bot author), which the skill routes to `auto-merge`/`pr-review` rather than first-touch triage.

## Summary
- **Mode**: repo (`var=swarm-ai-research/swarm`)
- **Outcome**: `PR_TRIAGE_OK no-candidates` — 4 open PRs seen, all skipped as bots (#638/#637/#636/#634, all `app/dependabot` dep bumps).
- **No external authors in-window.** Prior external contributors on swarm (`rsavitt`, `go165` per `memory/triaged-prs.json`) have no new PRs within the last 14 days.
- **No comments posted, no labels applied, no state writes** (nothing new to append to `memory/triaged-prs.json`).
- **Files modified**: `memory/logs/2026-10-19.md` (appended pr-triage section).
- **Notify**: skipped (significance gate not met — no OUT-OF-SCOPE, no first-time ACCEPTED).
- **Follow-up**: none from this run. Standing `pr-review` write-blocked status on swarm (per MEMORY) is unrelated to pr-triage's exit path today since there were no candidates to attempt a comment on.
