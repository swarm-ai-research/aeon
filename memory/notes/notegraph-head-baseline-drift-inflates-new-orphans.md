---
id: notegraph-head-baseline-drift-inflates-new-orphans
created: 2026-08-17
type: lesson
links: [[notegraph-head-vs-state-delta-misread-as-pr-merge]], [[github-actions-cannot-create-prs]], [[pr-creation-toggle-is-distinct-from-merge-capability]], [[skill-state-on-blocked-pr-branch-is-lost]]
---
# When notegraph's PR chain sits unmerged for weeks, HEAD-baseline drift makes every persistent orphan look "new"

On 2026-08-17 the notegraph extractor produced 283n / 2169e / 1 orphan against `origin/main`'s stored `notegraph.json` at 121n from 2026-06-25 — a **+162 node / +2025 edge** delta vs HEAD driven entirely by the chain #10 ← #27 ← #28 ← #29 ← #30 ← #31 ← #32 ← #35 never merging under the two-lever gap per [[pr-creation-toggle-is-distinct-from-merge-capability]]. The SKILL's HEAD-diff priority ordering then flagged `docs/telegram-instant.md` as a "new orphan" although `memory/state/notegraph.json` correctly recorded it as persistent — every currently-in-state orphan will surface as "new" from HEAD's perspective as the merge-lag grows. Fix path: rank the SKILL's own state file above HEAD when computing "new since last successful run" so orphan-priority reflects state-relative deltas, and fall back to HEAD-diff only when state is genuinely absent.
