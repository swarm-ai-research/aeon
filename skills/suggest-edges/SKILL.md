---
name: Suggest Edges
description: Densify the note graph by proposing wikilinks for high-similarity pairs that aren't yet hard-linked; opens a PR with up to 3 edge proposals per run
var: ""
tags: [meta, docs]
---

Today is ${today}. Find pairs of notes that the TF-IDF similarity says should be linked but aren't, and propose adding `[[wikilinks]]`. **Skip notify and PR when nothing new is proposed** — silence on a well-connected graph is the expected outcome.

## Steps

### 1. Run the suggester

```bash
node scripts/suggest-edges.mjs
```

The script:

- Reads `notegraph.json` (refreshes via `scripts/notegraph.mjs` if missing).
- Finds pairs with similarity ≥ 0.40 that have no existing hard edge in either direction.
- Filters out pairs already accepted or rejected in `memory/state/suggest-edges.json`.
- Skips source notes already well-connected (≥ 5 outgoing hard edges) — the goal is densifying the thin parts of the graph.
- Takes the top 3 by score, appends a `## Related notes` section to each source note with the matching wikilink.
- Updates `memory/state/suggest-edges.json` with what was applied.

If stdout reports `no new high-similarity unlinked pairs above threshold`, **exit silently. No notify. No PR.**

### 2. Detect change and stage edits

```bash
git diff --quiet docs/ memory/ memory/state/suggest-edges.json || echo "changes detected"
```

If no diff, exit silently (shouldn't happen if step 1 printed proposals, but defensive).

Collect from `memory/state/suggest-edges.json`'s tail `applied` entries (those with `appliedAt` from this run): list of `{source, target, score, shared}`.

Build `verdict_one_line`:

- 1 proposal → `1 missing link: ${source.basename} ↔ ${target.basename}`
- ≥2 → `${N} missing links proposed (top: ${first.source.basename})`

### 3. Open PR

```bash
git checkout -b suggest-edges/${today} 2>/dev/null || git checkout suggest-edges/${today}
git add docs/ memory/ memory/state/suggest-edges.json
git commit -m "suggest-edges: ${verdict_one_line}"
git push -u origin suggest-edges/${today}
gh pr create \
  --title "suggest-edges: ${verdict_one_line}" \
  --body "Auto-proposed by the \`suggest-edges\` skill on ${today}. Each entry below is a TF-IDF cosine match ≥ 0.40 between two notes that have no existing hard link.

## Proposals

$( for each applied entry: echo \"- **\${source}** → **\${target}** (similarity \${score}) shared terms: \${shared.join(', ')}\" )

## How to review

Each proposal added a \`## Related notes\` section (or appended to one) on the source note. Look at the diff — keep the suggestions you find useful, delete the ones that aren't, and merge. Rejected suggestions can be moved to the \`rejected\` array in \`memory/state/suggest-edges.json\` so they don't recur, otherwise this skill will re-propose them next time the corpus shifts.

The footer comment \`<!-- suggested by scripts/suggest-edges.mjs — edit or remove freely -->\` is a marker — leave it if you keep the section, delete it freely otherwise."
```

### 4. Notify

```bash
./notify "*Suggest-edges* — ${verdict_one_line}. Review PR: ${pr_url}"
```

Always notify when a PR opens — these are corpus mutations, not silent cleanup, and the operator should see them.

## Spam prevention (built into the script, not the skill)

- **State file** records every applied or rejected pair. The next run skips them.
- **Hard cap of 3 proposals per run** — even if the corpus suddenly has 20 unlinked high-similarity pairs (e.g. after a big import), only the top 3 by score get proposed today.
- **Source out-degree cap** — already-hubbed notes are skipped as sources so the suggester densifies edges, doesn't pile more onto MEMORY.md.
- **Threshold of 0.40** is conservative — earlier in this corpus, scores ≥ 0.5 were always genuine (ISS-001↔ISS-002, gitlawb-demo pair), and 0.40 is the practical floor for "obviously about the same thing."

## How operators reject a proposal

If a PR proposal isn't useful, instead of just deleting the bullet, edit `memory/state/suggest-edges.json` and move the entry from `applied` to `rejected`. The script reads both arrays and skips known pairs.

## Sandbox note

Pure local work — no outbound network. The script reads tracked notes via the existing `notegraph.json` (already a tracked artifact) and writes only inside `docs/`, `memory/`, and `memory/state/`.

## Exit modes

- `SUGGEST_EDGES_NO_PROPOSALS` — no new high-similarity unlinked pairs; silent exit (the expected path on a stable, well-connected graph)
- `SUGGEST_EDGES_OK` — proposals applied + PR opened + notify sent
- `SUGGEST_EDGES_ERROR` — script crashed or git op failed; notify with the error and exit non-zero
