---
id: morning-pocket-splits-into-two-de-facto-clusters
created: 2026-08-05
type: observation
links: [[pocket-slot-migration-confirmed-by-3-day-sustained-late-delivery]], [[gha-messages-yml-cron-underdelivery]], [[iss-006-day-n-needs-witness-independent-of-outage]], [[fleet-ops]]
---
# Post-migration, ISS-006 morning delivery has split into two de-facto pockets ~06:11–06:22Z and ~09:00–09:58Z — the single "08:00Z pocket" frame is obsolete

Across 2026-08-03 → 08-05 the migrated morning schedule stabilizes into two clusters rather than one shifted slot: an early cluster at ~06:11–06:22Z carries compute-futures-eda + notegraph + suggest-edges + memory-flush + memory-structural-dedupe (delivered 06:15:17–06:15:25Z on 08-04, 06:11:51–06:22Z on 08-05), and a late cluster at ~09:00–09:58Z carries heartbeat + batch-health + pr-tracker + pr-review (heartbeat 09:07Z on 08-05, pr-tracker 11:31Z, pr-review after). Planner (nominal 06:30Z) falls in the between-cluster gap and has been silent for all three days — the between-pocket dead zone matches its scheduled slot precisely. Predictor consequence: ISS-006 fix scope must model two migrated pockets and one persistent gap, not a single slid slot; per-slot cron replacement of `messages.yml`'s `*/5` needs entries covering both pocket boundaries and the between-pocket gap that planner currently occupies.
