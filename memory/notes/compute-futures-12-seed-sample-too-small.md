---
id: compute-futures-12-seed-sample-too-small
created: 2026-06-29
type: lesson
links: [[compute-futures-seed-padding-bug]]
---
# At n=12 seeds, compute-futures-eda outlier flags are IQR-fence artifacts, not regime changes

Two consecutive runs flagged degenerate IQR outliers driven by tie-clustering at small n: 2026-06-26 spread `minCurve` outlier_pct=25% (3 of 12 seeds at the fence) and 2026-06-29 spread `settlementLegs` outlier_pct=33% (18 of 36 rows at exactly 80 legs, q1=79.5/q3=80.25). Both were normal jitter, not regime shifts — IQR ceases to be a stable dispersion estimator when N is this small and ties dominate. Either widen the seed sweep in `scenario-sweep.mjs` or switch outlier detection to a rule that's robust to ties (MAD-based, or absolute-deviation against catalog spec) before treating new outlier flags as actionable signals.
