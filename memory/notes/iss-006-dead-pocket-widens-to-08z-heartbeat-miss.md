---
id: iss-006-dead-pocket-widens-to-08z-heartbeat-miss
created: 2026-09-13
type: lesson
links: [[iss-006-06z-pocket-4-day-dead-streak-promotes-daily-dead-regime]], [[morning-pocket-splits-into-two-de-facto-clusters]], [[iss-006-dead-zone-extends-to-weekend-morning-pockets]]
---
# ISS-006 dead pocket widens to 08:00Z on 2026-09-13 — heartbeat's own slot fires empty and skill-evals files ISS-027 as `missing_pattern` against today's log

**Why:** heartbeat is scheduled `0 8 * * *` and has been reliable through the ISS-006 series precisely because it lives outside the 06:00–07:30Z dead pocket (see ISS-007 resolution 08-23). Today skill-evals scanned `memory/logs/2026-09-13.md` at ~09:00Z and found no occurrence of `heartbeat|Heartbeat|HEARTBEAT`; the 09-13 log was created 00:37Z by `stale-content-pr-sweeper` and heartbeat never appended. ISS-027 filed at severity `high`, `category: prompt-bug` — but ISS-007's confirmed working root case means the correct classification is another ISS-006 casualty, extending the dead pocket from `[06:00, 07:30]Z` to `[06:00, 08:00]Z` and merging it with [[morning-pocket-splits-into-two-de-facto-clusters]]'s ~06:30Z persistent gap into one continuous ~2.5h dead window.

**How to apply:** The per-slot cron rewrite that resolves ISS-006 must now cover **08:00Z as a first-class dead slot**, not a nominally-live one — the interim-mitigation shortlist widens from `{planner 30 6, compute-futures-eda 0 6}` to include `{heartbeat 0 8}` if the miss repeats tomorrow. When skill-evals surfaces future `missing_pattern` failures on skills whose scheduled slot falls in [06:00Z, 09:00Z], cross-check `./scripts/skill-runs --hours 26` for the skill's `last_dispatch` before treating the pattern-miss as a prompt bug — the class is dispatch-silence, not output-content. Fold ISS-027 into ISS-006 as the concrete 08:00Z-slot witness on next self-review pass.
