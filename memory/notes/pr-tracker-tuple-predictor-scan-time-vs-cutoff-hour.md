---
id: pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour
created: 2026-08-02
type: lesson
links: [[pr-tracker-tuple-predictor-calendar-day-boundary-bug]], [[pr-tracker-notify-repeats-with-no-state-change]], [[pr-status]]
---
# pr-tracker's category-tuple predictor over-counts today's rolloffs when the anniversary hour is later than the scan hour on the same date

2026-08-02 pr-tracker predicted closed_no_merge=4 assuming kage#66 would roll off its 30d window today, but the scan fired at 11:16Z and kage's anniversary hour is 12:20Z — the item was still in the bucket at scan time and the actual tuple came in at closed_no_merge=5. This is a distinct failure axis from [[pr-tracker-tuple-predictor-calendar-day-boundary-bug]]: the 07-30 fix reframed deadlines against "next scheduled scan time" instead of calendar-day midnight, but treats the scheduled dispatch hour as satisfying every same-day anniversary — it doesn't. Fix: the predictor must compare `anniversary_datetime` against the actual expected scan `datetime` (both same-day hours), and only count the rolloff when `anniversary_datetime ≤ scan_datetime`.
