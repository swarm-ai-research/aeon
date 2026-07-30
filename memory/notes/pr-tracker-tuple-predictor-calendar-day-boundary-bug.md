---
id: pr-tracker-tuple-predictor-calendar-day-boundary-bug
created: 2026-07-30
type: lesson
links: [[pr-tracker-notify-repeats-with-no-state-change]], [[pr-tracker-step-5-misses-fresh-bot-prs]], [[pr-status]]
---
# pr-tracker's category-tuple predictor mis-frames stale-roll deadlines against calendar-day, but the scan fires ~11:22Z — 7d anniversaries after that time land in the NEXT scan's window, not today's

2026-07-30 pr-tracker predicted `(2, 5, 3, 4)` from three 7d anniversaries expected today (worldmonitor#5518 at 16:03Z, voicebox#958 at 16:34Z, RuView#1409 at 23:41Z) but scan fired at ~11:22Z and observed `(3, 1, 4, 6)` — 0 stale rolls today, all three anniversaries land AFTER the scan clock. The predictor should compute deadlines relative to the next scheduled dispatch (~10:00Z tomorrow), not the calendar-day boundary; the same-day stale-clock prediction on buzz#2248 hit to the minute (18:08:42Z on 07-29) because it happened to fall before the reflect scan clock, not because the calendar-day framing was correct. Fix: switch the tuple-predictor deadline math from `< today+1d 00:00Z` to `< next scheduled scan time`.
