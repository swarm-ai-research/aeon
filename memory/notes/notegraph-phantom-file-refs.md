---
id: notegraph-phantom-file-refs
created: 2026-06-20
type: lesson
links: []
---
# `notegraph.json` can be committed in a state that references files no longer on disk

On 2026-06-20 `suggest-edges` crashed because the committed graph cited `memory/gitlawb-compute-futures-proofs/2026-05-{25..27}.md`, none of which exist or have git history. Regenerating with `node scripts/notegraph.mjs` healed it (26 → 24 nodes). Either source notes were deleted without regenerating, or the daily `notegraph` skill is silently failing — worth filing as a `memory/issues/` entry.
