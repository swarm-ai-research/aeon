---
id: iss-006-widened-split-cohort-preservation-invariant-breaks-under-fleet-wide-silent-day
created: 2026-11-25
type: lesson
links: [[iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others]], [[iss-006-fleet-wide-silent-day-promotes-to-5-day-periodic-at-n-3]]
---
# The "08Z + 16Z preserved while others dead" widened-split-cohort invariant breaks at a 2-day span when a 5-day-periodic fleet-wide silent day lands adjacent

**Why:** Across 11-21 Sat and 11-22 Sun both the 08Z cohort (batch-health / heartbeat / gitlawb-fleet-metrics / skill-freshness) and the 16Z cohort (code-health / surplus-pulse) stayed silent for two consecutive days, with 11-22 confirmed as the 3rd n=3 fleet-wide silent day at the predicted 5-day cadence per [[iss-006-fleet-wide-silent-day-promotes-to-5-day-periodic-at-n-3]]. Prior regime [[iss-006-widened-split-cohort-regime-preserves-08z-16z-drops-others]] predicted 08Z+16Z preserve while other cohorts die, but the engulfment on 11-21/11-22 puts a counterexample at the preservation invariant's core.

**How to apply:** supersede the preservation claim — 08Z + 16Z are preserved only in the inter-fleet-wide-silent-day interior, not across the periodic silent day itself; treat the invariant as conditional on "no fleet-wide silent day in the current ±2-day window". When a fleet-wide silent day is in the window, expect engulfment of previously-preserved cohorts. Pair the per-cohort nominal-slot counter with a "fleet-wide-silent-day-in-window" flag; if that flag is set, the widened-split-cohort classification softens back to "pocket damage of indeterminate width". 11-24's partial-preservation shape (05Z + 16Z preserved, 08Z-only dead) is a new post-engulfment shape awaiting n=2 and not yet named.
