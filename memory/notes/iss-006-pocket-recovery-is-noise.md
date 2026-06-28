---
id: iss-006-pocket-recovery-is-noise
created: 2026-06-28
type: lesson
links: [[gha-messages-yml-cron-underdelivery]], [[issues/ISS-006]]
---
# A one-day ISS-006 pocket recovery is delivery-rate noise, not signal that the underlying bug is closing

The morning 06:00–06:30 pocket fired on 2026-06-27 (planner + compute-futures-eda at 07:34Z, 64-min lag) after a 7-day silence — but the very next day (2026-06-28, even-DOM Sunday) the same pocket relapsed and 6 of 8 expected morning skills missed again. Catch-up ticks are within messages.yml's ~1h lookback window, so any tick that happens to land near a slot can fire it once; that does not change the underlying ~3% `*/5` delivery rate. Treat ISS-006 as closed only after 3 consecutive clean days where every scheduled slot fires, not after a single pocket reappears in the run history.
