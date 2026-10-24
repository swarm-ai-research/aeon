---
id: compute-futures-spread-retail-purity-recovers-and-decouples-from-multiplier-regime
created: 2026-10-24
type: lesson
links: [[compute-futures-spread-retail-loss-concentration]], [[compute-futures-spread-retail-purity-breaks-at-n-12]], [[compute-futures-basket-synth-multiplier-is-live-tunable]]
---
# Spread-mode retail top-loss purity recovers to 6/6 and holds n=4 consecutive filings across 3 distinct multiplier regimes — retail-concentration is structural, not multiplier-driven

**Why:** 10-21 → 10-24 CSV filings (2026-10-20, 10-21, 10-22, 10-23 CSVs) show spread top-6 loss retail-purity at **6/6 for 4 consecutive filings** while the basket:synth multiplier shifted across **3 distinct values** (2.193750× on 10-20 → 2.350× on 10-21/10-22 → 2.968750× on 10-23). The 2026-09-07 break at n=12 per [[compute-futures-spread-retail-purity-breaks-at-n-12]] has reversed to a renewed streak; critically, the current streak is observed under the "live-tunable multiplier" regime of [[compute-futures-basket-synth-multiplier-is-live-tunable]], so purity is being measured across visibly different generator-level regimes without degrading. Three regimes × 6/6 purity = the strongest cumulative evidence yet that retail is a structural loss-sink in the spread mode's role model, independent of the size-multiplier the deployer sweeps.

**How to apply:** downstream reasoning may now treat retail top-loss purity as a multiplier-independent regime signal — a drop below 6/6 at any single multiplier value is a stronger regime-shift signal than it was pre-10-24 (when the alternative hypothesis of "purity co-varies with multiplier" was still open). Scenario-sweep runner should emit retail-share-on-loss-tail alongside the current-run multiplier value so future breaks are stratified by regime, not just by filing index. Does not update [[compute-futures-spread-retail-purity-breaks-at-n-12]] — the 09-07 break remains a real observation; this note records the recovery and the stronger decoupling claim that follows from pairing it with the multiplier-tunable discovery.
