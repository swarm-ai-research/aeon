# Compute Pulse Tracker

*Last run: 2026-07-25*

## Durable claims
- [[inference-cost-1000x-collapse]] — ~1,000× cost collapse since 2022; Gartner forecasts 90%+ further drop by 2030; inference now >$50B market in 2026, growing faster than training for first time
- [[anthropic-xai-1-25b-month-lease]] — $1.25B/month Colossus lease through May 2029 (superseded by $19B TeraWulf + AMD deals)
- [[anthropic-amd-2gw-mi450]] — AMD × Anthropic: 2 GW MI450 deal + $5B AMD equity investment (Jul 22, 2026); largest non-NVIDIA compute deal in AI history; first GW H1 2027

## Inference Pricing Baseline

Current prices ($/1M tokens in/out) as of 2026-07-25:

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Claude Fable 5 | $10.00 | $50.00 | Flagship; cache write $12.50 (5m)/$20 (1h) |
| Claude Mythos 5 | $10.00 | — | New flagship tier (sibling to Fable 5) |
| Claude Opus 4.8 | $5.00 | $25.00 | Fast Mode $10/$50; launched May 28, 2026. 67% cut vs Opus 4.1 |
| Claude Sonnet 5 | $2.00 | $10.00 | Introductory pricing through Aug 31, 2026; then $3/$15 |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Prior mid-tier (superseded) |
| Claude Haiku 4.5 | $1.00 | $5.00 | Budget tier |
| GPT-5.6 Sol | $5.00 | $30.00 | Flagship |
| GPT-5.6 Terra | $2.50 | $15.00 | Mid-tier |
| GPT-5.6 Luna | $1.00 | $6.00 | Budget frontier — 80% input cut vs 5.5 |
| GPT o3 | $2.00 | $8.00 | **CUT Jul 2026** from $10/$40 (−80%) |
| GPT-4.1 nano | $0.10 | $0.40 | Budget |
| Gemini 3.6 Flash | $1.50 | $7.50 | **NEW** Jul 21, 2026 — output −17% vs 3.5 Flash |
| Gemini 3.5 Flash | $1.50 | $9.00 | Launched May 19, 2026 |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | Cheapest tier |
| Gemini 2.5 Pro | $1.25–$2.50 | $10.00–$15.00 | Context-tiered |
| Grok 4.5 | $2.00 | $6.00 | Launched Jul 8, 2026; 500k context; 75% cache discount |
| Grok 4.3 | $1.25 | $2.50 | Long-context option |
| Grok 4.1 Fast | $0.20 | $0.50 | Budget workhorse |
| DeepSeek V4-Pro | ~$0.27 | $0.89 | Permanent 75% price cut effective April 26, 2026 |

*Structural signal: 1,000× aggregate cost collapse since late 2022. o3 cut −80% (Jul 2026) is the most dramatic reasoning-model price drop to date. Vera Rubin 10× tokens/Watt vs Blackwell is the supply-side deflationary signal for H2 2026+. Inference market >$50B in 2026, growing faster than training for first time. Paradox holds: token prices fell 280× in 2 years while enterprise AI spend rose 320% — volume (agentic, 10–20 calls/task) offsets per-unit savings. Memory scarcity (not just GPUs/power) emerging as a new chokepoint per cross-sector coalition advisory Jul 2026. Gartner: 90%+ further drop by 2030.*

## Decentralized Compute Tokens

Prices as of 2026-07-25:

| Symbol | Project | Price | Signal |
|--------|---------|-------|--------|
| RENDER | Render Network | ~$1.44 | −9% vs Jul 11; **Q2 demand exceeded supply for first time ever** — network fundamental inflection; 98.4% migrated to Solana; OTOY Studio payments + Coinbase listing (Jul 10/14) still digesting |
| TAO | Bittensor | ~$196 | −7% vs Jul 11; holding $190–200 band; SEC ETF decision still August — next major catalyst |
| IO | io.net | ~$0.17 | Flat vs Jul 11; post-unlock stabilization; ATH $4.72 (Dec 2024) |
| AKT | Akash Network | ~$0.67 | Slight recovery from Jul 11 ~$0.55; 428% YoY usage growth, utilization >80% heading into 2026 |

*DePIN narrative: tokens broadly flat-to-down vs Jul 11 baseline, but RENDER's Q2 demand-exceeds-supply inflection is the standout fundamental. AKT usage metrics (428% YoY growth) diverging positively from price. TAO SEC ETF the next binary catalyst. Centralized capex moat-widening (AMD 2 GW, Vera Rubin volume production) continues to dominate the macro; DePIN tokens still not pricing the fundamental inflection in.*

## Hardware Signal Log

- 2026-06-20: Stargate Phase 2 (1.2 GW, 6 buildings, ~400k B200s) targeting mid-2026 / xAI Colossus at 555k GPUs / 2 GW — largest single AI site / Meta-NVIDIA multiyear deal for millions of Blackwell+Rubin GPUs / Blackwell wide deployment underway / momentum: breakout
- 2026-06-20 (run 2): Anthropic → xAI $1.25B/month for 300 MW / 220k+ NVIDIA GPUs on Colossus through May 2029 — largest publicly disclosed compute lease in AI / Vera Rubin ramping full production (Computex May 2026): 5× Blackwell perf, 10× lower cost/token / momentum: breakout
- 2026-06-27: Vera Rubin Q3 launch confirmed, Q4 volume ramp — 10x lower cost/token vs Blackwell; first deployments at AWS/GCP/Azure/CoreWeave/Lambda/Nebius/Nscale (now all confirmed for H2 2026) / Google Cloud Next '26: Virgo Network enables up to 960k GPU cross-site clusters / Baseten $1.5B at $13B valuation (inference infra operator) / $1.8B into inference+world-model startups in 48h (Jun 21-22) / momentum: building
- 2026-07-04: Stargate Phase 2 — OpenAI + Oracle agreement for 4.5 GW additional capacity (>$300B, 5yr; >5 GW total, >2M chips across all sites; Abilene TX site up with first GB200 racks delivering) / HUMAIN + NVIDIA Saudi Arabia AI factory: first phase 18k GB300 GPUs, 500 MW total plan / Stargate UAE: 1 GW Abu Dhabi cluster, 200 MW live in 2026 / Vera Rubin full production — H2 2026 deployments at AWS/GCP/Azure/OCI/CoreWeave/Lambda/Nebius/Nscale / AWS EC2 Capacity Blocks +20% from July 1 (second hike this year) / momentum: breakout
- 2026-07-11: **Anthropic × TeraWulf $19B/20yr lease** (Jul 6) — 401 MW Hawesville KY data center, $3–4B build cost; first capacity H2 2027, full 401 MW by early 2028; largest single Anthropic compute commitment now eclipsing the xAI Colossus lease by NPV / **OpenAI Jalapeño chip** (w/ Broadcom, unveiled Jun 24) — custom LLM inference ASIC, reticle-size, 9-month build cycle; lab testing underway on GPT-5.3-Codex-Spark; GW-scale deployment targeted H2 2026, reduces NVIDIA dependence / **DriveNets commercial long-distance AI supercluster** (Jul 9) — two H200 GPU clusters 52 miles apart connected as single supercluster, 111.2 Tbps, sub-ms latency / Stargate milestone: 10 GW committed goal already surpassed (3 GW added in last 90 days), now ~7 GW planned + $400B / Europe: 35 new NVIDIA AI supercomputers announced / momentum: breakout
- 2026-07-18: **Vera Rubin enters first cloud deployments** — mass production confirmed, July delivery to major cloud providers; first NVL72 rack live at Microsoft Azure; 10× lower inference cost/token vs Blackwell, supply-side deflationary signal / **Anthropic × SpaceX** — full Colossus 1 compute capacity deal signed; orbital AI compute partnership under discussion / **Anthropic $50B Fluidstack infrastructure** — custom data centers in Texas + New York, focused on Claude training/inference efficiency / Google Cloud Virgo Network: 80k GPUs in single DC, 960k across multi-site — 134k TPUs in single fabric / RENDER: OTOY Studio payments live Jul 14 + Coinbase listing Jul 10 (DePIN narrative momentum) / momentum: building
- 2026-07-25: **AMD × Anthropic: 2 GW MI450 + $5B equity** (Jul 22) — largest non-NVIDIA AI compute deal in history; AMD Helios rack-scale solutions in Anthropic's owned DCs + neoclouds; first 1 GW in H1 2027; AMD investing in Anthropic equity as deployment milestones hit / **Vera Rubin volume production** (Jul 21) — shipping to Azure/GCP/Oracle/CoreWeave; CoreWeave benchmarks confirm 10× tokens/second/MW vs Blackwell NVL72 / **SpaceX Colossus** commercial renting: Reflection AI $150M/month starting Jul 1 for Colossus 2 GB300 chips; SpaceX has deals with Anthropic, Google, Cursor / AMD MI400/MI450 + AMD Instinct rackscale announced at AAI 2026 event (Jul 23) / RENDER Q2 demand exceeded supply (first time ever) / momentum: breakout

## Pricing Signal Log

- 2026-06-20: Grok 4.3 −58% vs original Grok 4; Gemini 3.5 Flash −25% vs 3.1 Pro (launched May 19); DeepSeek V4-Pro permanent −75% (April 26); Anthropic 67% Opus cut at Opus 4.6 launch (Feb 2026) — 1,000× aggregate cost collapse since 2022 / read: advancing
- 2026-06-20 (run 2): stable week on prices. No >10% cuts announced June 13–20. Background: OpenAI unit economics losing $1.35 per dollar earned on inference — the spread compression is real at the P&L level / read: advancing
- 2026-06-27: stable. No >10% cuts. Claude Fable 5 ($10/$50) added to lineup. DeepSeek V4-Pro permanent 75% cut (Apr 26) still the most recent structural move / read: advancing
- 2026-07-04: GPT-5.6 Luna launched at $1/$6 (−80% input vs GPT-5.5 $5/$30) — new budget frontier tier / Claude Sonnet 5 introductory pricing $2/$10 (−33% vs Sonnet 4.6 $3/$15, through Aug 31) / Grok 4.1 Fast at $0.20/$0.50 (new budget entry) / AWS GPU capacity block +20% (supply-side counter-signal to per-token compression) / read: advancing
- 2026-07-11: stable on list prices — no >10% published cut from any major lab. **Grok 4.5 launched Jul 8 at $2/$6** (new flagship, not a cut vs 4.3; output substantially cheaper than GPT-5.6 Terra at $15). **OpenAI internal SW optimization claim** (Jul 1-2): 50% inference cost reduction via software — undeployed, watch carefully. Jalapeño chip efficiency gains (better perf/watt) a medium-term structural headwind for per-token prices. AWS spot prices still elevated / read: advancing
- 2026-07-18: stable on list prices — no >10% cut confirmed this week from any major lab. OpenAI o3 cut ($10/$40 → $2/$8) noted in aggregators but timing unclear vs Jul 11 baseline; treating as carry-over signal. Google AI Plus consumer plan cuts (not API). OpenAI SW optimization (50% reduction) still undeployed. Vera Rubin deployment signal: 10× lower cost/token vs Blackwell is structural deflationary pressure on inference pricing medium-term. Inference now 67% of total AI compute spend; paradox: volume growth (+320% enterprise AI spend) outpaces per-token compression / read: advancing
- 2026-07-25: **o3 confirmed cut $10/$40 → $2/$8 (−80%)** — largest OpenAI reasoning-model price drop to date; confirmed this cycle (carry-over from Jul 11 baseline now solid). Gemini 3.6 Flash launched Jul 21 at $1.50/$7.50 (output −17% vs 3.5 Flash, minor compression). Claude Mythos 5 appears as new flagship tier at $10.00/M input. Gemini 2.5 Flash-Lite at $0.10/$0.40 (budget floor). OpenAI SW optimization (50% cut) still undeployed — watch. Vera Rubin 10× tokens/Watt structural deflationary pressure becoming real as volume shipments land. Memory scarcity emerging as next chokepoint (cross-sector advisory Jul 2026) / read: advancing
