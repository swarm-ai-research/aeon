---
name: Memory Flush
description: Promote important recent log entries into MEMORY.md, resolve contradictions, and decay stale detail
var: ""
tags: [meta]
---
> **${var}** — Topic to focus on. If empty, flushes all recent activity.

If `${var}` is set, only flush entries related to that topic.

## Design note

This skill applies a few **cognitive-memory** ideas (decay, contradiction
resolution, importance-weighted recall) as plain git-native passes over the
markdown store — no external service or API key. The store stays diffable and
reviewable in git; the passes below just decide *what* to keep, *how much
detail* to keep, and *how to make it findable later*.

Recall in Aeon is grep-over-markdown ranked by four signals — **keywords**
(the words in the entry), **meaning** (the topic file it lives in),
**relationships** (`[[wikilinks]]` between MEMORY.md and `topics/`), and
**timing** (log dates). The passes below keep all four signals healthy so
future reads surface the right context, not just more context.

Read `memory/MEMORY.md` for current memory state.
Read the last 3 days of `memory/logs/` for recent activity.

## Steps

### 1. Scan recent logs for entries worth promoting to long-term memory
- New lessons learned (errors encountered, workarounds found)
- Topics covered (articles, digests) — add to the recent articles/digests tables
- Features built or tools created
- Important findings from monitors (on-chain, GitHub, papers)
- Ideas captured that are still relevant
- Goals completed or progress milestones

### 2. Check each candidate against existing MEMORY.md content
Skip if already recorded. If a candidate **updates** an existing entry rather
than adding a net-new fact, treat it as a contradiction (step 3), not an addition.

### 3. Contradiction resolution (newest grounded fact wins)
Before adding anything, reconcile candidates against what MEMORY.md already
asserts. When a recent log entry **contradicts or supersedes** an existing
fact — a status flipped (`fixing` → `resolved`), a count changed (open PRs
4 → 1), a workaround replaced, a goal completed, a number revised — do **not**
let both versions coexist:

1. Keep the **newer, log-grounded** value.
2. **Delete** the stale assertion in the same edit (don't append a correction
   below it — that's how single-canonical sections drift; see
   `memory-structural-dedupe`).
3. If the *fact that it changed* is itself a lesson (e.g. an assumption proved
   wrong), fold that into Lessons Learned as one line; otherwise just replace.

When two recent log entries disagree with each other, prefer the one with the
later timestamp; if still ambiguous, verify against current repo state (`gh`,
file contents) rather than guessing.

### 4. Graded decay (keep the fact, shed the detail)
Old entries lose **detail**, not the **fact/entity**. Importance and recency
set how aggressively to compress — frequently-referenced, still-active topics
stay verbatim; old or one-off entries get compressed or dropped:

| Age / status | Action |
|---|---|
| Recent **or** still-referenced by an active goal/priority | Keep verbatim. |
| Older (~2+ weeks) and no longer actively referenced | Compress to a one-line fact, pushing any narrative detail down into the matching `topics/<topic>.md`. Preserve the entity name + the outcome; drop the play-by-play. |
| Fully resolved / superseded / one-off with no future signal value | Remove from MEMORY.md (the daily log still holds the full record). |

Importance signals (treat as "keep sharper"): referenced by a current entry in
**Goals** or **Next Priorities**, linked from multiple topic files, or a
**Lesson Learned** that still constrains future behaviour. Decay is
compression toward the canonical fact — never invent or alter the fact while
compressing.

Apply decay to the existing maintenance targets specifically:
   a. **Open Improvement PRs section**: Run `gh pr list --state open --search "improve:" --json number,title,url` and compare against any "Open Improvement PRs" section in MEMORY.md. If all listed PRs are merged/closed, remove the section; if some merged, trim to current open ones.
   b. **Next Priorities section**: Cross-check each priority against recent logs and current repo state. Remove ones already done (e.g. "Merge open PRs" when 0 are open). Add any newly urgent priorities surfaced by recent logs.
   c. **Lessons Learned**: Remove lessons now outdated or resolved (a workaround for a bug later fixed). Compress still-valid-but-old lessons to one line.
   d. **Skills Built table**: If grown beyond the last 10–15 entries, archive the oldest rows to `memory/topics/skills-history.md` to keep MEMORY.md under ~50 lines.

### 5. Recall-readiness (make kept entries findable)
For every entry you add or rewrite, make sure it carries the four recall
signals so future reads rank it correctly:
- **Relationships:** link to the relevant topic file with `[[wikilink]]` (or move detail there and leave a pointer) instead of stranding detail in MEMORY.md.
- **Keywords:** keep the concrete nouns in the line (repo names, PR numbers, skill names, error strings) — that's what a future grep matches on.
- **Timing:** date-stamp anything time-sensitive (`as of YYYY-MM-DD`) so staleness is self-evident on the next pass.
- **Meaning:** put the entry under the section/topic it actually belongs to, not wherever it was easiest to append.

### 6. Update memory
- Add brief entries to MEMORY.md (keep it under ~50 lines as an index).
- If a topic needs more detail, write to `memory/topics/<topic>.md` instead.
- Update tables (recent articles, recent digests) with new rows.
- Make targeted additions, replacements, and removals — do **NOT** rewrite the whole file.

### 7. Log what changed
Append to `memory/logs/${today}.md` a brief note covering: promoted entries,
contradictions resolved (old → new), and entries decayed/compressed/removed.

If nothing was worth promoting, no contradiction was found, and nothing needed
decaying, log `MEMORY_FLUSH_OK` and end.

## Sandbox Note

Reads and writes only local files (`memory/MEMORY.md`, `memory/topics/`,
`memory/logs/`) and runs one `gh pr list` call (uses `gh`'s own auth, not curl —
sandbox-safe). No external network calls, no API keys, no prefetch/postprocess.
