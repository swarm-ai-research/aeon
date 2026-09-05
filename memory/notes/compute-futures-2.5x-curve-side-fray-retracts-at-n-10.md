---
id: compute-futures-2.5x-curve-side-fray-retracts-at-n-10
created: 2026-09-05
type: pattern
links: [[compute-futures-2.5x-curve-side-frays-at-n-9]], [[compute-futures-basket-synth-2.5x-multiplier]], [[compute-futures-12-seed-sample-too-small]]
---
# The 08-31 curve-side fray in the 2.5× multiplier fully retracts at n=10 filings — one-day anomaly confirmed, not per-column deployer drift

At the 2026-09-04 CSV (10th filing of the 2.5× regime), the `maxCurve` std dropped 5.4× from 08-31's 2.82e-02 to 5.18e-03 — recovering the pre-fray tight-dispersion baseline. The 09-01 and 09-02 intermediate reads (recovered in the 4-day CSV backlog analyzed 09-04) show the retraction was monotonic, not a bounce. The [[compute-futures-2.5x-curve-side-frays-at-n-9]] hypothesis had two forks (per-column randomization drift vs one-day artifact); the artifact fork is now confirmed, and the 2.5× multiplier's durability claim extends to both spot and curve columns again. Practical: don't split spot-tight/curve-loose annotations on the 2.5× anchor; treat 08-31's single-day widening as scenario-sweep sample noise consistent with [[compute-futures-12-seed-sample-too-small]].
