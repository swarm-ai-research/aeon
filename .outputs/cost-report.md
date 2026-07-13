*Cost Report — 2026-07-13 (last 7 days)*

Spent $208.06 across 41 runs (↓0.18% WoW); 3 skill-level spikes flagged; projected monthly burn ~$891.68 ⚠

Top 3 by cost:
1. reflect — $87.11 (6 runs)
2. compute-futures-eda — $27.25 (4 runs)
3. notegraph — $20.80 (3 runs)

No optimization levers found this week (cache already used heavily; output/input ratios too high for model-downgrade filter).

⚠ 3 skill-level spikes — see report:
• notegraph 4.2× ($4.95→$20.80) — 07-08 cache_read blowup (5.84M tokens)
• memory-flush 3.1× ($4.55→$14.23) — 07-12 cache_read blowup (5.89M tokens)
• skill-freshness 2.1× ($3.78→$7.83) — elevated output on 07-06 + 07-12

30-day projection: $891.68 (cache-read = 58% of spend; driven by MEMORY.md growth)
Full: articles/cost-report-2026-07-13.md
