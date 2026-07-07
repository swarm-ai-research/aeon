---
id: notegraph-extractor-generatedat-nondeterministic
created: 2026-07-07
type: lesson
links: [[notegraph-phantom-file-refs]]
---
# The notegraph extractor writes a fresh `generatedAt` timestamp into every output, so `git diff` sees churn on stable corpora

`node scripts/notegraph.mjs` emits `generatedAt` into all four output files (`notegraph.json`, `docs/notegraph.md`, `docs/notegraph.html`, `docs/notegraph-speedrun.html`); when the corpus fingerprint moves but the resulting graph is identical, `git diff --quiet` still reports HAS_DIFF purely from those four timestamp lines — the skill's silent-exit heuristic must inspect each file's diff for topology/stats content before deciding to skip, and revert the timestamp-only churn (`git checkout --`) to keep the tree clean. On 2026-07-07 the extractor produced 128n/1163e identical to HEAD's stored graph despite a fingerprint drift, and the correct verdict `NOTEGRAPH_NO_CHANGE` required this per-file inspection; a naive HAS_DIFF gate would have opened a fresh PR carrying only bumped timestamps. Fix shape: either make the extractor omit `generatedAt` when writing (or write it to a sidecar), or teach the skill to diff-mask the `generatedAt` line before its silent-exit decision.
