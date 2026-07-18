## Summary

Executed the `notegraph` skill for 2026-07-18.

**Fingerprint change:** `96720fb9…` → `dfe80295…` (2nd consecutive day of input change; 166 → 173 md files scanned since 07-17).

**Extractor output:** 172 nodes · 1243 hard · 474 soft · 1 orphan · 44 atomic · 0 bundled (edges 1717).

**Delta vs HEAD** (`notegraph.json` at `5366264`): +1 node, +7 edges, 0 orphans, 0 bundled, +1 atomic.

**New node:** `memory/notes/probes-for-messages-yml-must-dispatch-outside-messages-yml.md` — atomic, landed well-wired (inDeg 2, outDeg 5) on first appearance. This is the note underpinning yesterday's planner rank-2 (draft ISS-020 for `enabled-skills-can-never-dispatch`) — the natural-experiment silencing pattern is now formally in the graph.

**Verdict:** `+1 notes wired in` — priority rule #3 (node_delta>0 && orphan_delta<=0 && bundled_delta<=0). Not bland → **notify fires**.

**PR:** Branch `notegraph/2026-07-18` pushed to origin; `gh pr create` failed 403 as expected per `github-actions-cannot-create-prs`. **Staged branch queue: 15 → 16.** Operator unblock path unchanged: Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests".

**Files modified:**
- `notegraph.json`, `docs/notegraph.md`, `docs/notegraph.html`, `docs/notegraph-speedrun.html` (committed on `notegraph/2026-07-18` branch, pushed)
- `memory/state/notegraph.json` (working tree on main — for auto-commit sweep)
- `memory/logs/2026-07-18.md` (working tree on main — for auto-commit sweep)
- `.pending-notify/1784355869-notegraph.md` (queued for postprocess-notify sweep)

**Exit mode:** `NOTEGRAPH_OK`.

**Follow-up:** Same as 07-17 — operator toggle the Actions PR permission (one-checkbox unblock for 16 staged branches). Streak-3 escalation on `verify-repo-settings-toggle-vs-pat` fires today if scheduled probes stay silent.
