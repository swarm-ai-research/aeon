# Compute Pulse Tracker

*Last run: 2026-07-04*

## Durable claims
- [[inference-cost-1000x-collapse]] — ~1,000× cost collapse since 2022; Gartner forecasts 90%+ further drop by 2030
- [[anthropic-xai-1-25b-month-lease]] — $1.25B/month Colossus lease through May 2029, largest publicly disclosed AI compute deal

## Inference Pricing Baseline

Current prices ($/1M tokens in/out) as of 2026-07-04:

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Claude Fable 5 | $10.00 | $50.00 | Flagship; cache write $12.50 (5m)/$20 (1h) |
| Claude Opus 4.8 | $5.00 | $25.00 | Fast Mode $10/$50; launched May 28, 2026. 67% cut vs Opus 4.1 |
| Claude Sonnet 5 | $2.00 | $10.00 | Introductory pricing through Aug 31, 2026; then $3/$15 |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Prior mid-tier (superseded) |
| Claude Haiku 4.5 | $1.00 | $5.00 | Budget tier |
| GPT-5.6 Sol | $5.00 | $30.00 | New family flagship |
| GPT-5.6 Terra | $2.50 | $15.00 | Mid-tier; replaces GPT-5.5 in practice |
| GPT-5.6 Luna | $1.00 | $6.00 | New budget frontier — 80% input cut vs 5.5 |
| GPT-5.5 | $5.00 | $30.00 | Superseded by 5.6 family |
| GPT-4.1 nano | $0.10 | $0.40 | Budget |
| Gemini 3.5 Flash | $1.50 | $9.00 | Launched May 19, 2026 |
| Gemini 3.1 Flash-Lite | $0.25 | $1.50 | Budget tier |
| Grok 4.3 | $1.25 | $2.50 | Flagship |
| Grok 4.1 Fast | $0.20 | $0.50 | New budget tier — among cheapest frontier APIs |
| DeepSeek V4-Pro | ~$0.27 | $0.89 | Permanent 75% price cut effective April 26, 2026 |

*Structural signal: 1,000× aggregate cost collapse documented since late 2022. Token prices fell 280× over two years; enterprise total spend up 320% (volume outpacing unit cost). Gartner (March 2026): inference on 1T-param models will cost 90%+ less by 2030 than in 2025. Inference now accounts for ~85% of enterprise AI budget. AWS EC2 Capacity Block GPU prices rose 20% effective July 1, 2026 — second increase this year (first +15% in January); centralized spot supply constrained.*

## Decentralized Compute Tokens

Prices as of 2026-07-04:

| Symbol | Project | Price | Signal |
|--------|---------|-------|--------|
| RENDER | Render Network | ~$1.61 | Flat; mcap ~$835M; -88% from ATH $13.53 |
| TAO | Bittensor | ~$215–275 | Inconsistent data; broadly flat; subnet economy active |
| IO | io.net | ~$0.18 | Flat; token unlock July 11 (13.29M IO = 1.7% supply) |
| AKT | Akash Network | ~$0.64 | Down ~15% vs Jun 20; 428% YoY usage growth reported |

*DePIN narrative: AWS GPU price hike (+20% Jul 1) widens the cost-advantage window for decentralized compute (60-80% cheaper for latency-tolerant workloads). But real-time inference at scale remains elusive for DePIN — most volume still in training/batch. Neoclouds on track for $20B revenue in 2026 (tripling YoY). Token prices underperforming vs narrative strength.*

## Hardware Signal Log

- 2026-06-20: Stargate Phase 2 (1.2 GW, 6 buildings, ~400k B200s) targeting mid-2026 / xAI Colossus at 555k GPUs / 2 GW — largest single AI site / Meta-NVIDIA multiyear deal for millions of Blackwell+Rubin GPUs / Blackwell wide deployment underway / momentum: breakout
- 2026-06-20 (run 2): Anthropic → xAI $1.25B/month for 300 MW / 220k+ NVIDIA GPUs on Colossus through May 2029 — largest publicly disclosed compute lease in AI / Vera Rubin ramping full production (Computex May 2026): 5× Blackwell perf, 10× lower cost/token / momentum: breakout
- 2026-06-27: Vera Rubin Q3 launch confirmed, Q4 volume ramp — 10x lower cost/token vs Blackwell; first deployments at AWS/GCP/Azure/CoreWeave / Google Cloud Next '26: Virgo Network enables up to 960k GPU cross-site clusters / Baseten $1.5B at $13B valuation (inference infra operator) / $1.8B into inference+world-model startups in 48h (Jun 21-22) / momentum: building
- 2026-07-04: Stargate Phase 2 — OpenAI + Oracle agreement for 4.5 GW additional capacity (>$300B, 5yr; >5 GW total, >2M chips across all sites; Abilene TX site up with first GB200 racks delivering) / HUMAIN + NVIDIA Saudi Arabia AI factory: first phase 18k GB300 GPUs, 500 MW total plan / Stargate UAE: 1 GW Abu Dhabi cluster, 200 MW live in 2026 / Vera Rubin full production — H2 2026 deployments at AWS/GCP/Azure/OCI/CoreWeave/Lambda/Nebius/Nscale / AWS EC2 Capacity Blocks +20% from July 1 (second hike this year) / momentum: breakout

## Pricing Signal Log

- 2026-06-20: Grok 4.3 −58% vs original Grok 4; Gemini 3.5 Flash −25% vs 3.1 Pro (launched May 19); DeepSeek V4-Pro permanent −75% (April 26); Anthropic 67% Opus cut at Opus 4.6 launch (Feb 2026) — 1,000× aggregate cost collapse since 2022 / read: advancing
- 2026-06-20 (run 2): stable week on prices. No >10% cuts announced June 13–20. Background: OpenAI unit economics losing $1.35 per dollar earned on inference — the spread compression is real at the P&L level / read: advancing
- 2026-06-27: stable. No >10% cuts. Claude Fable 5 ($10/$50) added to lineup. DeepSeek V4-Pro permanent 75% cut (Apr 26) still the most recent structural move / read: advancing
- 2026-07-04: GPT-5.6 Luna launched at $1/$6 (−80% input vs GPT-5.5 $5/$30) — new budget frontier tier / Claude Sonnet 5 introductory pricing $2/$10 (−33% vs Sonnet 4.6 $3/$15, through Aug 31) / Grok 4.1 Fast at $0.20/$0.50 (new budget entry) / AWS GPU capacity block +20% (supply-side counter-signal to per-token compression) / read: advancing
