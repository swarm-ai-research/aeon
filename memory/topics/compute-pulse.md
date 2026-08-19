# Compute Pulse Tracker

*Last run: 2026-08-15*

## Durable claims
- [[inference-cost-1000x-collapse]] — ~1,000× cost collapse since 2022; Gartner forecasts 90%+ further drop by 2030; inference now >$50B market in 2026, growing faster than training for first time
- [[anthropic-xai-1-25b-month-lease]] — $1.25B/month Colossus lease through May 2029 (superseded by $19B TeraWulf + AMD deals)
- [[anthropic-amd-2gw-mi450]] — AMD × Anthropic: 2 GW MI450 deal + $5B AMD equity investment (Jul 22, 2026); largest non-NVIDIA compute deal in AI history; first GW H1 2027
- [[compute-futures-basket-synth-3025x-multiplier]] — **INVALIDATED 2026-08-18** — the basket/synth 3.0250× multiplier promoted on 08-14 and cemented n=7 by 08-17 broke to 2.5000× on 08-18 via upstream deployer config change; see [[compute-futures-multiplier-invalidated-at-n-7]] for the promotion-criterion lesson

## Inference Pricing Baseline

Current prices ($/1M tokens in/out) as of 2026-08-15 (stable week — no >10% cuts; see Pricing Signal Log):

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| Claude Fable 5 | $10.00 | $50.00 | Flagship; cache write $12.50 (5m)/$20 (1h) |
| Claude Mythos 5 | $10.00 | — | New flagship tier (sibling to Fable 5) |
| Claude Opus 5 | $5.00 | $25.00 | **NEW** Jul 24, 2026; Fast Mode $10/$50; 1M context; closest to Fable 5 at half price |
| Claude Opus 4.8 | $5.00 | $25.00 | Fast Mode $10/$50; launched May 28, 2026 (superseded by Opus 5) |
| Claude Sonnet 5 | $2.00 | $10.00 | Introductory pricing through **Aug 31, 2026**; then $3/$15 — expiry imminent |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Prior mid-tier (superseded) |
| Claude Haiku 4.5 | $1.00 | $5.00 | Budget tier |
| GPT-5.6 Sol | $5.00 | $30.00 | Flagship; unchanged |
| GPT-5.6 Terra | $2.00 | $12.00 | **CUT Jul 30** from $2.50/$15 (−20%) |
| GPT-5.6 Luna | $0.20 | $1.20 | **CUT Jul 30** from $1.00/$6.00 (−80%) — fastest frontier-tier repricing on record |
| GPT o3 | $2.00 | $8.00 | CUT Jul 2026 from $10/$40 (−80%) |
| GPT-4.1 nano | $0.10 | $0.40 | Budget |
| Gemini 3.6 Flash | $1.50 | $7.50 | Launched Jul 21, 2026 — output −17% vs 3.5 Flash |
| Gemini 3.5 Flash | $1.50 | $9.00 | Launched May 19, 2026 |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | Cheapest tier |
| Gemini 2.5 Pro | $1.25–$2.50 | $10.00–$15.00 | Context-tiered |
| Grok 4.6 | $2.00 | $6.00 | **NEW** Aug 12, 2026; 1.5T-param, 1753 ELO, 500k context; price flat vs 4.5 |
| Grok 4.5 | $2.00 | $6.00 | Prior flagship (superseded by 4.6); same pricing |
| Grok 4.3 | $1.25 | $2.50 | Long-context option |
| Grok 4.1 Fast | $0.20 | $0.50 | Budget workhorse |
| DeepSeek V4-Pro | ~$0.27 | $0.89 | Permanent 75% price cut (Apr 26, 2026); **price increase announced — no date set; watch** |

*Structural signal: 1,000× aggregate cost collapse since late 2022. GPT-4-class fell from $30/1M tokens (2023) to <$0.50 (2026) — 95% drop in 2 years. GPT-5.6 Luna −80% (Jul 30) remains sharpest recent single-tier pricing move. Vera Rubin 10× tokens/Watt in full production (H2 2026 cloud deployments live) is the supply-side deflationary signal. Inference market >$50B in 2026, now 67% of total AI compute spend (was 33% in 2023). OpenAI 20% internal cost reduction via SW optimization (Jul 29 post) not yet passed through as list-price cut — watch. Jevons paradox active: per-token costs −67% YoY but enterprise AI bills tripled (volume growth outpaces compression). Anthropic in-house chip team forming (Aug 5) — co-design silicon + Claude, Samsung manufacturing target, ~50% inference cost reduction goal. Claude Sonnet 5 introductory rate expires Aug 31 → then $3/$15 (pending increase). DeepSeek price increase announced (no date). Memory scarcity emerging as next chokepoint. Gartner: 90%+ further drop by 2030.*

## Decentralized Compute Tokens

Prices as of 2026-08-15:

| Symbol | Project | Price | Signal |
|--------|---------|-------|--------|
| RENDER | Render Network | ~$1.27 | **−7% vs Aug 8** — bid soft; demand>supply inflection still unpriced; 5,600+ GPU nodes, 68M+ frames cumulative |
| TAO | Bittensor | ~$189 | −2% vs Aug 8; holding ~$189 support; SEC ETF window still open — binary catalyst |
| IO | io.net | ~$0.17 | **+13% vs Aug 8** — slight recovery; unlock-digest easing; IDE burn mechanism live (Jun 11) |
| AKT | Akash Network | ~$0.53 | +6% vs Aug 8 — recovering from −25% last week; Mainnet 18 usage gains slow to price in; 428% YoY usage growth, >80% utilization |

*DePIN narrative: AKT recovering from last week's −25% slide; Mainnet 18 usage improvements starting to hold partial bid. IO unlock digestion easing (mild positive). RENDER and TAO giving back slight ground. Akash network usage 428% YoY growth with >80% utilization is the actual DePIN compute signal — token price lagging. Centralized capex mega-deals (Anthropic in-house chips + AMD 2 GW + Amazon 5 GW + Google/Broadcom 3.5 GW) still dominating market perception. TAO SEC ETF window remains sector's key binary catalyst. No DePIN token outperforming — centralized moat winning in market perception.*

## Hardware Signal Log

- 2026-06-20: Stargate Phase 2 (1.2 GW, 6 buildings, ~400k B200s) targeting mid-2026 / xAI Colossus at 555k GPUs / 2 GW — largest single AI site / Meta-NVIDIA multiyear deal for millions of Blackwell+Rubin GPUs / Blackwell wide deployment underway / momentum: breakout
- 2026-06-20 (run 2): Anthropic → xAI $1.25B/month for 300 MW / 220k+ NVIDIA GPUs on Colossus through May 2029 — largest publicly disclosed compute lease in AI / Vera Rubin ramping full production (Computex May 2026): 5× Blackwell perf, 10× lower cost/token / momentum: breakout
- 2026-06-27: Vera Rubin Q3 launch confirmed, Q4 volume ramp — 10x lower cost/token vs Blackwell; first deployments at AWS/GCP/Azure/CoreWeave/Lambda/Nebius/Nscale (now all confirmed for H2 2026) / Google Cloud Next '26: Virgo Network enables up to 960k GPU cross-site clusters / Baseten $1.5B at $13B valuation (inference infra operator) / $1.8B into inference+world-model startups in 48h (Jun 21-22) / momentum: building
- 2026-07-04: Stargate Phase 2 — OpenAI + Oracle agreement for 4.5 GW additional capacity (>$300B, 5yr; >5 GW total, >2M chips across all sites; Abilene TX site up with first GB200 racks delivering) / HUMAIN + NVIDIA Saudi Arabia AI factory: first phase 18k GB300 GPUs, 500 MW total plan / Stargate UAE: 1 GW Abu Dhabi cluster, 200 MW live in 2026 / Vera Rubin full production — H2 2026 deployments at AWS/GCP/Azure/OCI/CoreWeave/Lambda/Nebius/Nscale / AWS EC2 Capacity Blocks +20% from July 1 (second hike this year) / momentum: breakout
- 2026-07-11: **Anthropic × TeraWulf $19B/20yr lease** (Jul 6) — 401 MW Hawesville KY data center, $3–4B build cost; first capacity H2 2027, full 401 MW by early 2028; largest single Anthropic compute commitment now eclipsing the xAI Colossus lease by NPV / **OpenAI Jalapeño chip** (w/ Broadcom, unveiled Jun 24) — custom LLM inference ASIC, reticle-size, 9-month build cycle; lab testing underway on GPT-5.3-Codex-Spark; GW-scale deployment targeted H2 2026, reduces NVIDIA dependence / **DriveNets commercial long-distance AI supercluster** (Jul 9) — two H200 GPU clusters 52 miles apart connected as single supercluster, 111.2 Tbps, sub-ms latency / Stargate milestone: 10 GW committed goal already surpassed (3 GW added in last 90 days), now ~7 GW planned + $400B / Europe: 35 new NVIDIA AI supercomputers announced / momentum: breakout
- 2026-07-18: **Vera Rubin enters first cloud deployments** — mass production confirmed, July delivery to major cloud providers; first NVL72 rack live at Microsoft Azure; 10× lower inference cost/token vs Blackwell, supply-side deflationary signal / **Anthropic × SpaceX** — full Colossus 1 compute capacity deal signed; orbital AI compute partnership under discussion / **Anthropic $50B Fluidstack infrastructure** — custom data centers in Texas + New York, focused on Claude training/inference efficiency / Google Cloud Virgo Network: 80k GPUs in single DC, 960k across multi-site — 134k TPUs in single fabric / RENDER: OTOY Studio payments live Jul 14 + Coinbase listing Jul 10 (DePIN narrative momentum) / momentum: building
- 2026-07-25: **AMD × Anthropic: 2 GW MI450 + $5B equity** (Jul 22) — largest non-NVIDIA AI compute deal in history; AMD Helios rack-scale solutions in Anthropic's owned DCs + neoclouds; first 1 GW in H1 2027; AMD investing in Anthropic equity as deployment milestones hit / **Vera Rubin volume production** (Jul 21) — shipping to Azure/GCP/Oracle/CoreWeave; CoreWeave benchmarks confirm 10× tokens/second/MW vs Blackwell NVL72 / **SpaceX Colossus** commercial renting: Reflection AI $150M/month starting Jul 1 for Colossus 2 GB300 chips; SpaceX has deals with Anthropic, Google, Cursor / AMD MI400/MI450 + AMD Instinct rackscale announced at AAI 2026 event (Jul 23) / RENDER Q2 demand exceeded supply (first time ever) / momentum: breakout
- 2026-08-01: **Meta Prometheus 1 GW AI cluster** (New Albany, OH) — first gigawatt-capable DC targeting 2026 online; backed by 6.6 GW nuclear offtake (Oklo + TerraPower + Vistra through 2035) / **Anthropic × Google + Broadcom 3.5 GW TPU deal** (Apr 7, confirmed) — $46B deal, capacity from 2027; Anthropic $30B annual revenue run-rate / **Fireworks AI $1.5B Series D at $17.5B** (Jul 2026) — inference infra operator-layer, 4.4× valuation in 9 months / **Vera Rubin cloud deployments live** — first NVL72 racks at Azure; H2 2026 allocations at AWS/GCP/OCI/CoreWeave/Lambda/Nebius/Nscale underway / NVIDIA Data Center Q1 FY2027: $75.2B (+92% YoY) / global DC capex on pace for $1T in 2026 / momentum: breakout
- 2026-08-08: quiet hardware week; Vera Rubin hyperscaler ramp continuing (volume production, multi-cloud allocations live) / Alpha Compute ALPHA-03 (~1,000 B200s, Canada) targets August online (small/medium signal) / no new >10k-GPU cluster or >$1B deal announced / AKT −25% (notable DePIN slide) / momentum: quiet (1 pt)
- 2026-08-15: **Anthropic in-house chip team confirmed** (Aug 5, Forbes Aug 6) — co-design silicon + Claude, Samsung manufacturing target, ~50% inference cost reduction goal; structural NVIDIA hedge (medium signal) / **Amazon × Anthropic**: up to 5 GW capacity confirmed incl Trainium2+3, ~1 GW by end-2026 / **Grok 4.6** launched Aug 12 (1.5T-param, 1753 ELO, $2/$6 flat vs 4.5, agentic focus) / Vera Rubin hyperscaler ramp continuing / no new >10k-GPU cluster announced this week / DePIN: IO +13%, AKT +6%, RENDER −7%, TAO −2% / momentum: quiet (1 pt)

## Pricing Signal Log

- 2026-06-20: Grok 4.3 −58% vs original Grok 4; Gemini 3.5 Flash −25% vs 3.1 Pro (launched May 19); DeepSeek V4-Pro permanent −75% (April 26); Anthropic 67% Opus cut at Opus 4.6 launch (Feb 2026) — 1,000× aggregate cost collapse since 2022 / read: advancing
- 2026-06-20 (run 2): stable week on prices. No >10% cuts announced June 13–20. Background: OpenAI unit economics losing $1.35 per dollar earned on inference — the spread compression is real at the P&L level / read: advancing
- 2026-06-27: stable. No >10% cuts. Claude Fable 5 ($10/$50) added to lineup. DeepSeek V4-Pro permanent 75% cut (Apr 26) still the most recent structural move / read: advancing
- 2026-07-04: GPT-5.6 Luna launched at $1/$6 (−80% input vs GPT-5.5 $5/$30) — new budget frontier tier / Claude Sonnet 5 introductory pricing $2/$10 (−33% vs Sonnet 4.6 $3/$15, through Aug 31) / Grok 4.1 Fast at $0.20/$0.50 (new budget entry) / AWS GPU capacity block +20% (supply-side counter-signal to per-token compression) / read: advancing
- 2026-07-11: stable on list prices — no >10% published cut from any major lab. **Grok 4.5 launched Jul 8 at $2/$6** (new flagship, not a cut vs 4.3; output substantially cheaper than GPT-5.6 Terra at $15). **OpenAI internal SW optimization claim** (Jul 1-2): 50% inference cost reduction via software — undeployed, watch carefully. Jalapeño chip efficiency gains (better perf/watt) a medium-term structural headwind for per-token prices. AWS spot prices still elevated / read: advancing
- 2026-07-18: stable on list prices — no >10% cut confirmed this week from any major lab. OpenAI o3 cut ($10/$40 → $2/$8) noted in aggregators but timing unclear vs Jul 11 baseline; treating as carry-over signal. Google AI Plus consumer plan cuts (not API). OpenAI SW optimization (50% reduction) still undeployed. Vera Rubin deployment signal: 10× lower cost/token vs Blackwell is structural deflationary pressure on inference pricing medium-term. Inference now 67% of total AI compute spend; paradox: volume growth (+320% enterprise AI spend) outpaces per-token compression / read: advancing
- 2026-07-25: **o3 confirmed cut $10/$40 → $2/$8 (−80%)** — largest OpenAI reasoning-model price drop to date; confirmed this cycle (carry-over from Jul 11 baseline now solid). Gemini 3.6 Flash launched Jul 21 at $1.50/$7.50 (output −17% vs 3.5 Flash, minor compression). Claude Mythos 5 appears as new flagship tier at $10.00/M input. Gemini 2.5 Flash-Lite at $0.10/$0.40 (budget floor). OpenAI SW optimization (50% cut) still undeployed — watch. Vera Rubin 10× tokens/Watt structural deflationary pressure becoming real as volume shipments land. Memory scarcity emerging as next chokepoint (cross-sector advisory Jul 2026) / read: advancing
- 2026-08-01: **GPT-5.6 Luna −80%** ($1.00/$6.00 → $0.20/$1.20, Jul 30) + **GPT-5.6 Terra −20%** ($2.50/$15.00 → $2.00/$12.00, Jul 30) — repriced <3 weeks after Jul 9 launch; OpenAI cited model-assisted inference optimization + open-model competition pressure; fastest frontier-tier repricing on record. **Claude Opus 5** launched Jul 24 at $5/$25 (same tier as Opus 4.8, new frontier capability; 1M context). **OpenAI SW optimization 20% cost reduction** (Jul 29 engineering post) — structural, not yet list-price cut; watch for pass-through. No cuts from Anthropic, Google, xAI, or DeepSeek this cycle / read: advancing
- 2026-08-08: stable — no >10% cuts from any major lab. xAI grok-voice-latest alias → grok-voice-think-fast-2.0 on Aug 5 (voice API only; text model prices unchanged). Google deprecating Imagen 4 Aug 17 (not a price signal — sunset). Market bifurcation intensifying: frontier API tier +36.4% YoY vs mid-tier −35.8% (Axis Intelligence); inference now 67% of total AI compute spend (vs 33% in 2023). OpenAI SW optimization 20% reduction still undeployed as list-price cut — watch / read: holding
- 2026-08-15: stable — no >10% list-price cuts from any major lab. Grok 4.6 at same price as 4.5 ($2/$6, no cut). Claude Sonnet 5 introductory rate ($2/$10) expires **Aug 31 → then $3/$15** (pending increase). DeepSeek price increase announced (no date attached) — first counter-signal in the compression narrative. OpenAI 20% cost-reduction still not passed through as list-price cut. Vera Rubin structural deflationary pressure ongoing in production. GPT-4-class: $30/1M (2023) → <$0.50 (2026), 95% drop in 2 years. Jevons paradox: costs −67% YoY, enterprise AI bills tripled. / read: holding
