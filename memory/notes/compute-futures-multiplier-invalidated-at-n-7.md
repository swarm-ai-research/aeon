---
id: compute-futures-multiplier-invalidated-at-n-7
created: 2026-08-19
type: lesson
links: [[compute-futures-basket-synth-3025x-multiplier]], [[compute-futures-12-seed-sample-too-small]], [[compute-futures-seed-padding-bug]]
---
# A compute-futures multiplier promoted at n≥3 can invalidate at n=7 when an upstream deployer parameter changes

The basket/synth 3.0250× spot multiplier promoted on 2026-08-14 (n=4) and cemented at n=7 by 08-17 broke on 08-18 to 2.5000×, then held at 2.5000× n=2 on 08-19 — an upstream deployer config change reset the constant without touching schema. Promotion criteria that treat n=3–7 as terminal miss this class; promoted deterministic patterns need a re-validation cadence (each new filed run) or an upstream config-hash pin, otherwise the promoted lesson silently misinforms downstream `x × synth` collapse shortcuts.
