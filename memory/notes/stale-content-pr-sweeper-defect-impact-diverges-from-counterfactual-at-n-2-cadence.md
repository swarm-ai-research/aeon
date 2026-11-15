---
id: stale-content-pr-sweeper-defect-impact-diverges-from-counterfactual-at-n-2-cadence
created: 2026-11-15
type: lesson
links: [[stale-content-pr-sweeper-defect-impact-bounded-by-upstream-backlog]], [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]], [[stale-content-pr-sweeper-tracked-prefix-drift]]
---
# stale-content-pr-sweeper defect impact diverges from its patched-config counterfactual once the upstream notegraph cadence fills the group to ≥2 stale entries

**Why:** 2026-11-15 scan surfaced 3 TRACKED-prefix `notegraph/*` PRs all authored by `app/github-actions` (#115 2026-11-08 survivor, #114 2026-10-29 at 17 days, #107 2026-10-26 at 20 days); under patched `ALLOWED_AUTHORS` the group is 3-entry with 2 stale candidates past the ≥2-day min-age gate, so the counterfactual close-count is ≥1 (conflict-only + `[keep]` still require per-PR fetch). Actual close-count stays 0 because the `aeonframework`-only filter rejects all 3. First observation where defect output diverges from patched-config output since the bounded-by-backlog claim in [[stale-content-pr-sweeper-defect-impact-bounded-by-upstream-backlog]]; the 10-29 zero-impact finding held only while the group had 1 entry (10-29 and 11-01 both single-entry).

**How to apply:** the bounded-blast-radius framing from [[stale-content-pr-sweeper-defect-impact-bounded-by-upstream-backlog]] is now defeated at n=2 cadence — the notegraph weekly cycle naturally refills the group past `keep_latest=1`, so the defect's zero-close line is correct-by-coincidence only during post-sweep troughs that last ≤1 notegraph fire. Treat the author-allowlist patch from [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]] as having reactivated urgency: each notegraph fire past the first one in a trough is now a missed close, so the patch SLA is tighter than the coarse "next refill" framing suggested. Monitor the running `notegraph/*` tracked-prefix count; when it crosses 2, re-engage the patch.
