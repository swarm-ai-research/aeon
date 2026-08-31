*Skill Freshness — 2026-08-31*
🔴 FRESHNESS_STALE — 25 of 43 deps flagged across 25 of 43 enabled consumers

Worst:
- run-frequency-guard ← .outputs/run-frequency-guard.md (NEVER, outputs, MISSING)
- ai-framework-watch ← .outputs/ai-framework-watch.md (NEVER, outputs, MISSING)
- memory-structural-dedupe ← .outputs/memory-structural-dedupe.md (123.3h, outputs, STALE)
- batch-health/heartbeat/fleet-control cluster ← 10 daily skills all ~121h (last batch 08-26)

Action: ISS-006 batch-outage root cause; STALE cluster = skills missed 08-27–08-30 batches. Two never-ran skills (run-frequency-guard, ai-framework-watch) = [[enabled-skills-can-never-dispatch]] class.
Full: articles/skill-freshness-2026-08-31.md
