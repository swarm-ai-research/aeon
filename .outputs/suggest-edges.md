Done. Summary:

**suggest-edges 2026-08-17 — day-9 recurrence, class break to second templated cluster**

The script emitted 3 proposals (top-3 sim=1.000) from `gitlawb-compute-futures-proofs/` — **class break** from the 6-day-locked source triple `{06-24, 06-27, 07-04}` × `[cash, darkbloom, synthetic, basket, spread]` onto NEW all-pairs within `{05-25, 05-26, 05-27}` × NEW shared-term signature `[sha, settlement, task, physical, cash]`. Second templated cluster surfacing after prior-triple combinations exhausted the reject list.

- **Reverted** source-note edits on `2026-05-25.md` and `2026-05-26.md` via `git checkout --`.
- **Moved** the 3 today's `applied` entries to `rejected` in `memory/state/suggest-edges.json` with class-break note. State now **3 applied + 21 rejected** (+3/day rate held).
- **No PR, no notify** per established templated-corpus noise pattern.
- **Files modified:** `memory/state/suggest-edges.json`, `memory/logs/2026-08-17.md`.
- **Exit mode:** effectively `SUGGEST_EDGES_NO_PROPOSALS` (post-manual-rejection).

**Follow-up strengthened:** the planner's shared-parent-dir + basename-shape pre-filter for `scripts/suggest-edges.mjs` **must generalize** — a single-cluster hardcoded skip won't stop the now-observed multi-cluster rotation. Needs tokenization-signature dedup across the whole corpus subtree.
