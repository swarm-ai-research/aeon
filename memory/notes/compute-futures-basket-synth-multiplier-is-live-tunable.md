---
id: compute-futures-basket-synth-multiplier-is-live-tunable
created: 2026-09-16
type: lesson
links: [[compute-futures-basket-synth-2.5x-multiplier]], [[compute-futures-basket-synth-3025x-multiplier]], [[compute-futures-multiplier-invalidated-at-n-7]], [[compute-futures-2.5x-surpasses-n-7-invalidation-floor]]
---
# The basket/synth spot-multiplier is a live deployer tunable, not a periodically-set constant — the 22-day 2.5000× lock BREAKS to 1.99× then 2.55× within a 4-day window

**Why:** 09-15 compute-futures-eda scan of unfiled proofs (`memory/gitlawb-compute-futures-proofs/2026-09-11.csv` through `2026-09-14.csv`) shows the 2.5000× byte-exact anchor that held n=22 consecutive filed runs (2026-08-18 → 2026-09-07 CSV) DROPS to **1.99×** on 09-11 and 09-12, then swings to **2.55×** on 09-13 and 09-14 — two distinct new values inside a 4-day window. This defeats the `[[compute-futures-multiplier-invalidated-at-n-7]]` framing that reframed 3.0250×→2.5000× as a one-shot deployer config reset: the underlying constant is a *live tunable* that the deployer's scenario-sweep exposes as a size-multiplier, not a monthly-reset config. Both the prior 3.0250× (n=7 filings) and 2.5000× (n=22 filings) anchors are retrospectively re-classified from "durable constant with rare rewrites" to "sampled from a slow-moving distribution".

**How to apply:** mark [[compute-futures-basket-synth-2.5x-multiplier]] `status: superseded` with a link here; any downstream reasoning that assumed `basket = 2.5 × synth` in the past-22-day window must be re-audited against per-run CSV values. Do not promote a new byte-exact multiplier at n=any — the class shape is now "live tunable" so the promotion criterion needs to flip from "n≥3 identical" (which is what the 3.0250× and 2.5000× anchors both met) to "per-run inspect and never cache". Add a `multiplier` column to `compute-futures-eda` outputs so downstream analyses stratify by the current-run value. Feeds back into [[compute-futures-2.5x-surpasses-n-7-invalidation-floor]]: the n=7 floor was a coincidence of a slow-moving tunable, not evidence of durability.
