---
name: Weekly Reflect
description: Review recent activity, consolidate memory into atomic notes + MOCs, and prune stale entries
var: ""
tags: [meta]
---
> **${var}** — Area to focus on. If empty, reviews everything.

If `${var}` is set, focus the reflection on that specific area.

Today is ${today}. Review the agent's recent activity and maintain long-term memory under the atomic-notes convention:
- **`memory/MEMORY.md`** — short index, ~50 lines, no claims.
- **`memory/topics/*.md`** — MOCs that link to atomic notes for durable claims and keep time-varying snapshots (weekly numbers, point-in-time tables) inline.
- **`memory/notes/${slug}.md`** — one file per claim, frontmatter (id, created, type, links), body ≤3 sentences.
- **`memory/notes/daily/${today}.md`** — date-indexed pointer list, written by `note-taking`.

## Steps

1. **Read state.** `memory/MEMORY.md`, last 7 days of `memory/logs/`, last 7 days of `articles/`, `memory/skill-health/*.json`, and `memory/issues/INDEX.md`.

2. **Consolidate what you learned.**
   - What topics were covered? Note patterns or gaps.
   - What was built or decided? Record durable decisions.
   - Stale entries in `MEMORY.md`? Remove them.
   - Recurring errors? Lift them out as their own atomic notes (type: `lesson`).
   - Skill health trends: declining scores, persistent flags — summarize in the relevant MOC, atomize the durable claim.

3. **Atomicity pass over `memory/notes/`.** For every file under `memory/notes/` (excluding `memory/notes/daily/`):
   - Read it. If the body is >3 sentences excluding the title, OR mentions ≥2 unrelated entities each with its own action, OR contains "and also" / "additionally" / "moreover", it is bundled.
   - **Split it.** Create N new atomic files, one per claim. Each new file's `links:` frontmatter lists the slugs of the others. Delete the original bundled file. Update any `[[old-slug]]` references in MOCs to point at the most specific replacement.
   - Log every split: `RECONCILE_SPLIT old-slug → new-slug-1, new-slug-2, …`.

4. **Reorganize memory under the atomic-notes convention.**
   - **`MEMORY.md`** stays a pure index. Pointers only, no claims.
   - **Topic files** in `memory/topics/` become MOCs: a short framing paragraph, then bulleted `[[slug]]` lists grouped by sub-area, with weekly/snapshot tables kept inline. No multi-sentence claims that should be in a note.
   - **New durable claims** discovered while reading logs/articles → write each as a fresh atomic file under `memory/notes/${slug}.md` (same shape as the `note-taking` skill produces). Add the `[[slug]]` link to the right topic MOC.
   - **Time-varying snapshots** (weekly numbers, dated tables, "as of ${date}" status) stay inline in the MOC — they are NOT atomic claims, they are point-in-time observations that don't belong as graph nodes.

5. **Re-regenerate notegraph** so the consolidation shows up:
   ```bash
   node scripts/notegraph.mjs
   ```
   Record the delta (nodes, edges, orphans) in the log. Any new orphans → those notes need links and probably belong in a topic MOC.

6. **Prune.** Be ruthless. Memory is a living, useful document — not an append-only log.
   - Delete obsolete MEMORY.md bullets.
   - If an atomic note's claim is now contradicted by a newer note, mark `status: superseded` in its frontmatter and add `links: [[newer-slug]]`. Don't delete history — let the graph show the supersession.

7. **Log what you did** to `memory/logs/${today}.md`:
   ```markdown
   ## Reflect
   - **Atomic-pass:** ${SPLIT_COUNT} bundled notes split, ${NEW_COUNT} new atomic notes created
   - **Topic MOCs updated:** ${TOPIC_LIST}
   - **MEMORY.md pruned:** ${PRUNED_COUNT} stale bullets
   - **Notegraph delta:** +${NODE_DELTA} nodes, +${EDGE_DELTA} edges, ${ORPHAN_DELTA:+0} orphans
   - REFLECT_OK
   ```

8. **Notify** via `./notify`:
   ```
   memory consolidated — ${today} · +${NODE_DELTA}n / +${EDGE_DELTA}e
   ```
   If splits or new atomic notes were created, append `(${SPLIT_COUNT} splits, ${NEW_COUNT} new)`.

## Atomicity rules (apply throughout)

A note is atomic if its title states a single claim and the body summarizes in ≤3 coherent sentences without "and also" / "additionally". Bundled notes are linking hazards — every `[[X]]` ends up pointing at a topic dump instead of one idea, and backlinks lose their definitional power.

**When in doubt, split.** A claim with rich detail can stay one note; a bundled note is permanently a hazard. Splitting is cheap, merging later is fine too. See PR #260 for the validated effect — across three topic atomizations, edges grew 5.3× faster than nodes.

## What NOT to atomize

- Weekly cost/heartbeat tables, "as of ${date}" status lines, point-in-time PR queues — these are observations, not claims, and they belong inline in the MOC.
- `memory/issues/ISS-NNN.md` files — already atomic per filename, don't duplicate as notes.
- Soul files (`soul/`) — voice calibration material, not graph content.

## Sandbox Note

- All file operations are inside the sandbox and work without issue.
- `node scripts/notegraph.mjs` runs in-sandbox; if it fails on a sandbox restriction, log `REFLECT_NOTEGRAPH_SKIPPED` and continue — the `notegraph` skill regenerates on its own daily cron.
