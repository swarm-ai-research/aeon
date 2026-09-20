## Summary

Ran the `notegraph` skill for 2026-09-20.

**Inputs and change detection**
- The step-1 `find … | xargs sha1sum | sha1sum` fingerprint pipeline is still blocked by the sandbox's brace-quote/expansion heuristic (seventh occurrence of [[notegraph-fingerprint-pipeline-blocked-by-sandbox]]); fell back to an ad-hoc `.tmp-fingerprint.mjs` node helper.
- New fingerprint `25dc4a9f…` diverges from state's `1c36254a…` (state's `last_run` was 2026-09-03), so the extractor was run.

**Extractor output**
- `notegraph: 398 nodes · 3173 hard · 998 soft · 0 orphans · 0 bundled`
- HEAD `notegraph.json` was already at 398n/4171e (a prior run landed graph output but never bumped `memory/state/notegraph.json` — a real state-drift I flagged in the daily log). Current extractor output matches HEAD stats exactly, but content differs: one `name-mention` edge upgraded to `path-mention` (0.5 → 0.8), two in-degree shifts (21→22 and 8→7 on the iss-006/batch-outage neighbourhood), and float-rounding drift on a handful of soft edge weights.
- Verdict: `graph refreshed (398n / 4171e / 0b)` (bland form — no new/resolved orphans or bundled).
- Exit mode: **NOTEGRAPH_OK**.

**Files modified**
- `notegraph.json`, `docs/notegraph.md`, `docs/notegraph.html`, `docs/notegraph-speedrun.html` — regenerated.
- `memory/state/notegraph.json` — updated with new fingerprint, stats, verdict, and PR link.
- `memory/logs/2026-09-20.md` — activity log created.

**PR**
- Opened: https://github.com/swarm-ai-research/aeon/pull/75
- Branch: `notegraph/2026-09-20`

**Notify**
- **Skipped** per skill step 5 (bland `graph refreshed` verdict AND no new/resolved orphans).

**Follow-ups**
- The `scripts/notegraph-fingerprint.mjs` helper is still unlanded; the sandbox will keep forcing an ad-hoc `.tmp-fingerprint.mjs` every run until it's checked in. Bundle with the ENOBUFS `maxBuffer: 128 MiB` fix per [[notegraph-fingerprint-helper-enobufs-at-1mb]].
- Investigate why HEAD `notegraph.json` was already at 398n/4171e while `memory/state/notegraph.json` was still at the 2026-09-03 snapshot (351n) — suggests a prior notegraph PR merged without an accompanying state-file update, or the state commit landed on a branch that got reverted (echo of [[notegraph-silent-revert-on-fabricated-merge-claim.md]]).
- `.tmp-fingerprint.mjs` and `.tmp-delta.mjs` (plus a `.tmp-delta.json`) are still in the workspace because the sandbox also refuses `rm` on them; they're `.tmp*`-gitignored so nothing was committed, but a fresh checkout is the only clean-up.
