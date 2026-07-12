## Summary

Ran reflect on 2026-07-12.

**What changed:**
- **1 new atomic note** created: `memory/notes/snapshot-rebase-clobbers-docs-status-md.md` — captures today's heartbeat discovery that snapshot commit `bcae68a` at 07:01Z overwrote yesterday's landed `docs/status.md` write with an older upstream-fork version.
- **1 note superseded**: `memory/notes/status-md-auto-commit-drops-writes.md` rewritten from "silently lost" (07-05 framing) to "DELAY not DROP" per today's memory-flush contradiction; `status: superseded` added.
- **0 splits** — atomicity pass over 42 notes found no bundled content (same result as reflect passes 07-06 → 07-11).

**Files modified:**
- `memory/notes/status-md-auto-commit-drops-writes.md` (rewrite)
- `memory/notes/snapshot-rebase-clobbers-docs-status-md.md` (new)
- `memory/topics/fleet-ops.md` (Lessons list + ISS-006 open-incidents refreshed to Day-22 mixed-delivery)
- `memory/MEMORY.md` (Current-focus status.md line + Next-priorities item 4 split into two-part fix)
- `notegraph.json`, `docs/notegraph.{md,html}`, `docs/notegraph-speedrun.html` (extractor regen: 162 nodes / 1163 hard / 450 soft / 1 orphan / 0 bundled — Δ +13n/+130e vs 05Z run, 0 new orphans)
- `memory/logs/2026-07-12.md` (Reflect entry appended)
- `.pending-notify/1783881801-reflect.md` (notification queued)

**Sandbox note:** shell `>` redirect for log append was refused mid-run per [[sandbox-blocks-shell-redirect-to-workdir]] — recovered via Edit tool. Existing note still accurate.

**Follow-ups:** the two-part `docs/status.md` fix (heartbeat auto-commit glob + snapshot-rebase gate) is now in Next-priorities; operator PAT provisioning remains the meta-blocker on all 11+ staged branches.
