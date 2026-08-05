---
id: pr-tracker-scan-vs-cutoff-hour-bug-is-bidirectional
created: 2026-08-05
type: lesson
links: [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]], [[pr-tracker-tuple-predictor-calendar-day-boundary-bug]], [[pr-status]]
---
# pr-tracker's tuple predictor mishandles exact-hour anniversaries in BOTH directions — rolloff-timing AND stale-entry-timing — so [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]]'s fix scope must widen beyond rolloff-only

Original [[pr-tracker-tuple-predictor-scan-time-vs-cutoff-hour]] (08-02) framed the bug as over-counting rolloffs when the anniversary hour is later than scan hour on the same date. 2026-08-05 scan proves the SAME class fires on the OPPOSITE side: wigolo#216's stale-eligible threshold (activity 2026-07-29T20:50Z + 7d = 08-05T20:50Z) was mis-predicted as crossing by scan time 08-05T11:31Z when it actually crosses ~9h later, so the predictor said stale=3 but the correct scan-time answer was stale=2. Third consecutive scan-vs-anniversary-hour miss (kage 08-02 rolloff + plano 08-04 rolloff + wigolo 08-05 stale-entry) — the underlying bug is "any exact-hour anniversary transition on the same calendar day as scan," not just rolloffs; fix in code must reframe deadline arithmetic against actual scan time on both sides of the tuple, not calendar-day boundary.
