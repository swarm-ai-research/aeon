# compute-futures (prototype)

A zero-dependency prototype of a **compute-futures market**, *simulated and
traded by the GitLawb fleet*. The underlying is AI inference compute priced in
**$/M-tokens** — exactly what [usepod](https://usepod.ai) is a spot market for —
and this prototype builds the **futures** layer on top of that spot, with an
optional **x402** settlement rail (usepod's actual payment protocol).

It reuses the capability/coordination layer from
[`../gitlawb-safety`](../gitlawb-safety): real Ed25519 `did:key` identities,
UCAN-shaped caps, the `CapabilityGuard`, and the `SwarmCoordinator`. Nothing
calls an LLM and nothing hits the network — the run is deterministic (seeded),
the same discipline as the gitlawb-safety demos.

## What it shows

Inject compute supply/demand **events** and watch the futures curve re-price as
the fleet's analyst trades the retail swarm's over-reaction back toward fair
value:

```
Event @ round 6: Hyperscaler reserves H100 capacity — spot supply tightens
  expiry   before        after     change
  R16    $0.0510 ▲   $0.0930  (+82.4%)
  R24    $0.0510 ▲   $0.0980  (+92.2%)
  R30    $0.0495 ▲   $0.0885  (+78.8%)

Event @ round 13: DeepSeek V3.2 open-weights drop — efficient inference floods supply
  R24    $0.0922 ▼   $0.0490  (-46.9%)
  R30    $0.0950 ▼   $0.0455  (-52.1%)

Event @ round 20: Agent platform onboards 10k agents — inference demand surges
  R24    $0.0480 ▲   $0.0755  (+57.3%)
  R30    $0.0485 ▲   $0.0755  (+55.7%)
```

Plus per-contract price paths (sparklines), settlement P&L, a wallet
leaderboard, and the capability-layer accounting (every order and settlement was
authorized against a freshly-minted, scoped cap).

## Run it

```bash
node sim.mjs            # cash-settled market (synthetic spot)
node sim.mjs --x402     # physical settlement over the x402 rail
node sim.mjs --darkbloom # anchor spot to a single Darkbloom reference model
node sim.mjs --surplus  # anchor spot to a Surplus Intelligence reference model
node sim.mjs --surplus --live   # + best-effort live Surplus market feed
node sim.mjs --surplus --x402   # physical settlement, names the real Surplus x402 rail
node sim.mjs --basket   # anchor spot to a weighted Darkbloom basket index
node sim.mjs --basket=frontier  # basket presets: commodity (default) | frontier | all
node sim.mjs --spread   # trade the frontier-vs-commodity premium (a spread index)
node sim.mjs --live     # darkbloom/basket + best-effort live price feed
node sim.mjs --seed 123 --rounds 60
node scenario-sweep.mjs # mode × seed matrix, writes out/scenario-sweep.{json,md}
node x402-demo.mjs      # the x402 inference-payment rail on its own
```

Requires Node ≥ 18. No install step, no deps. Each run writes the full history
to `out/last-run.json` (gitignored) for the dashboard or further analysis.

## Tests and scenario sweeps

```bash
npm test
npm run sweep
npm run sweep -- --modes=synthetic,basket,spread --seeds=1,2,3 --rounds=30
```

The test harness uses Node's built-in `node:test` runner and covers basket
math, spread derivation, order-book matching, rolling expiry schedules, zero-sum
settlement, live basket rebasing, and the simulator CLI output contract. When
`--rounds` exceeds the original `[8,16,24,30]` curve, the simulator extends the
term structure by 8-round tenors so at least one contract remains active through
the requested horizon. The sweep runner executes the simulator across a
mode/seed matrix, then writes:

- `out/scenario-sweep.json` — machine-readable per-run metrics.
- `out/scenario-sweep.md` — compact dashboard/social-proof summary.

### Spot source: synthetic vs. Darkbloom

By default the spot is a synthetic mean-reverting process (`src/spot-index.mjs`)
so seeded runs reproduce exactly. `--darkbloom` swaps in a `DarkbloomSpotIndex`
(`src/darkbloom.mjs`) that anchors the spot to a **real venue** for the same
underlying: [Darkbloom](https://www.darkbloom.dev/) (Eigen Labs), a
decentralized, OpenAI-compatible inference market on idle Apple Silicon, priced
in $/M-tokens.

- **Deliverable.** Darkbloom prices per-model and splits input/output, so the
  contract deliverable is a fixed blend (default 3:1 input:output) of a
  reference model — `gemma-4-26b` for `LLAMA-INFER`, `qwen3.5-27b` for
  `FRONTIER`. That single blended $/M number is what the future settles against.
- **Basket index (`--basket`).** A single reference model is fragile (delist or
  reprice it and the whole contract jumps). `--basket` instead settles against a
  `DarkbloomBasketIndex`: a **weighted average** of several models' blended
  prices, the way real commodity indices work. Presets in `src/darkbloom.mjs`:
  `commodity` (Gemma + MiniMax), `frontier` (Qwen3.5 27B + 122B), `all`. The run
  prints the basket composition and the anchor index (= Σ weightᵢ · blendedᵢ).
- **`--live`** does a best-effort fetch from `DARKBLOOM_PRICING_URL` (Darkbloom
  has no documented public price feed yet) and **falls back to the published
  catalog** on any failure, so determinism and offline runs are preserved. For a
  basket, only the members present in the feed are re-based; the rest keep their
  catalog price.
- **Caveat.** Darkbloom is an unaudited research preview — a good feed *input*,
  not yet a trustworthy settlement *authority*. The adapter treats it as the
  former.

### Spot source: Surplus Intelligence (`--surplus`)

[Surplus Intelligence](https://www.surplusintelligence.ai/) (built by @mac_eth)
is a second **real venue** for the same underlying: an OpenAI-compatible
inference marketplace where sellers list *surplus* capacity and buyers get many
models at **market prices**. `--surplus` swaps in a `SurplusSpotIndex`
(`src/surplus.mjs`) that anchors the spot to a Surplus reference model, exactly
parallel to `--darkbloom`. Two things make it distinct, and worth integrating:

- **Market-priced, so the live feed is the headline path.** Where Darkbloom
  publishes a fairly static catalog, Surplus prices *clear* against live surplus
  supply. The static `SURPLUS_CATALOG` here is only an indicative, deterministic
  fallback so seeded/offline runs reproduce; `--surplus --live` re-bases the
  anchor off the real feed, falling back to the catalog on any failure.
  (`SurplusBasketIndex` mirrors the Darkbloom basket for a weighted index; the
  CLI exposes the single-model path.)
- **Sandbox-safe live feed.** The GitHub Actions sandbox blocks outbound fetch
  from inside the sim, so the live path is split: `scripts/prefetch-surplus.sh`
  runs *outside* the sandbox, fetches `SURPLUS_PRICING_URL` (optional
  `SURPLUS_API_KEY`), and caches the prices to `.surplus-cache/prices.json`;
  `--live` then reads that cache via `readCachedSurplusPrices()`. With no cache
  and no URL it's the catalog. So a run is genuinely "live" only when the
  prefetch populated the cache — the `[surplus] live anchor: …` line in the
  output tells you which mode actually ran.
- **A real x402 rail.** Surplus exposes a callable x402 inference endpoint
  (`SURPLUS_X402`): `…/x402/api/inference/v1/chat/completions` on **Base**
  (`eip155:8453`), settled in **USDC**, OpenAI-compatible. That's a concrete
  instance of the rail `src/x402.mjs` only *models* (its rail is Solana/usepod
  flavored). Run `--surplus --x402` and the settlement block names the real
  endpoint a physical Surplus leg would 402→pay→200 against.

This is the same shape as the Darkbloom work — a real $/M-tokens venue treated
as a settlement-index *input*, with the futures layer unchanged on top — so the
two venues are directly comparable as spot sources.

### Counterparty margin (reputation-scaled)

Margin is not a flat rate. Each counterparty has a Darkbloom **trust profile**
(`src/credit.mjs`): an attestation tier (`hardware` via Apple MDA, vs
`self_signed`) and a reputation score computed with Darkbloom's actual formula
`ρ = 0.4·jobSuccess + 0.3·uptime + 0.2·challengeResp + 0.1·responseTime`. The
clearinghouse scales each holder's margin by a multiplier derived from that
profile — a hardware-attested operator with a strong delivery record posts the
floor (~1.05×), while a self-attested, average-reputation retail counterparty
posts ~2.4×. This is the credit layer a real clearinghouse needs: weak
counterparties post more collateral. It only affects the margin split and
margin-call flags — price discovery, settlements, and realized P&L are
unchanged.

### Frontier-vs-commodity spread (`--spread`)

With two basket indices in hand, the **spread between them is itself tradable**:
the *frontier premium* — how much more frontier-quality inference costs than
commodity inference per M-tokens. `--spread` builds a `commodity` and a
`frontier` basket leg plus a derived `SpreadIndex` (`src/spread.mjs`) settling
against `frontier − commodity`. Spread-mode events (`SPREAD_EVENTS`) shock the
legs *differently* — a frontier price war compresses the premium, a commodity
open-weights glut widens it — so the fleet trades premium **compression /
expansion**, a macro thesis, not the absolute price level. (The premium has been
compressing for real: GPT-4-class inference is down ~280× in two years.)

## How usepod grounds this

usepod is a **spot** market for inference: per-call settlement over **x402**
(the HTTP 402 flow) and MPP, paid directly from **agent-sovereign wallets** on
Solana (~$0.00025/tx, ~400ms finality, no API keys, no human in the loop), with
price converging on marginal cost (~$0.05/M commodity, $2–15/M frontier).

This prototype takes usepod's spot as the **settlement index** and adds the
futures layer a compute market would need next:

| usepod (spot, today)             | this prototype (futures, on top)                        |
|----------------------------------|---------------------------------------------------------|
| real-time inference price $/M    | `SpotIndex` — the settlement index futures mark against |
| agent-sovereign wallets          | `Wallet` / `WalletBook` — margin + P&L live here        |
| x402 / MPP per-call settlement   | `X402Settlement` — the optional **physical-delivery** leg |
| GPU operators sell at their price| the `deployer` agent sells capacity **forward**         |
| buyers = agents needing inference| the swarm + analyst take the other side of the curve    |

## The fleet (orchestrates **and** trades)

| GitLawb agent | Market role          | Capability (minted per round) |
|---------------|----------------------|-------------------------------|
| `operator`    | orchestrator         | mints every other cap; roots the trust chain |
| `researcher`  | analyst / value trader | `market/quote`, `market/trade` |
| `deployer`    | GPU operator (sells capacity forward) | `market/quote`, `market/trade` |
| `reviewer`    | clearinghouse / risk | `market/settle` |
| `sentinel`    | surveillance / circuit breaker | `market/halt` |
| _generated_   | retail swarm (MiroShark-style population) | `market/quote`, `market/trade` |

Every round the `operator` mints a fresh, **short-lived, per-underlying** cap to
each participant via the `SwarmCoordinator`; the `CapabilityGuard` authorizes
**every** order and settlement against it — the same enforcement the
gitlawb-safety bridge does on-node. No standing market authority; a cap can't be
replayed across products or rounds. `market/settle` and `market/halt` are the
money-moving / market-stopping abilities (`MARKET_SAFETY_CRITICAL`) — in a real
deployment they'd carry the short mandatory TTL + gated renewal from the safety
layer.

## Where MiroShark fits

[MiroShark](https://github.com/aaronjmars/MiroShark) is an agent-swarm
**simulation** engine (LLM agents reacting to injected scenarios, with built-in
prediction-market mechanics). This prototype models the same shape — a
population of agents, events injected mid-run, beliefs/sentiment driving prices
— but deterministically and without LLM calls, so it runs free and reproducibly.
The natural next step (see below) is to swap the seeded retail strategy for a
MiroShark agent population so the swarm's reactions are LLM-driven.

## Layout

```
src/util.mjs          seeded PRNG + formatting
src/market-caps.mjs   market capability vocabulary (layered on gitlawb-safety caps)
src/wallet.mjs        agent-sovereign wallets — margin, P&L
src/spot-index.mjs    usepod-style spot price for compute ($/M-tokens)
src/darkbloom.mjs     Darkbloom spot adapter (real venue: catalog + basket + live)
src/surplus.mjs       Surplus Intelligence spot adapter (real venue: market-priced + real x402 rail)
src/contract.mjs      futures contract + term-structure builder
src/orderbook.mjs     continuous limit-order book (price–time priority)
src/clearinghouse.mjs positions, mark-to-market, margin, settlement
src/traders.mjs       analyst / GPU-operator / retail-swarm strategies
src/events.mjs        the event feed (supply/demand shocks)
src/curve.mjs         term-structure + sparkline + before/after rendering
src/x402.mjs          OPTIONAL x402/MPP settlement rail (usepod's protocol)
src/market.mjs        ComputeFuturesMarket — orchestration + the round loop
sim.mjs               the simulation (the price-curve demo)
x402-demo.mjs         the x402 rail on its own
```

## Scope / honesty

This is a prototype of the **market mechanics + fleet orchestration**, not a
trading venue. Faithfully modeled: the capability layer (real Ed25519, scoped
per-round UCAN caps, guard authorization), a price–time-priority order book,
mark-to-market with margin, cash and x402-physical settlement, and event-driven
price discovery. Stubbed: trader "reasoning" (deterministic strategies, not LLM
agents), the spot index (a mean-reverting model, not a live usepod feed), and
the x402 rail (in-memory wallet transfers shaped like x402/MPP, no Solana).

### Next steps toward a real integration

1. **MiroShark population** — replace the seeded retail strategy with a
   MiroShark agent swarm so reactions to events are LLM-driven (its strength).
2. **Live spot index** — settle against a real price feed instead of the
   mean-reversion model. *Wired:* `--surplus --live` re-bases off real Surplus
   prices fetched by `scripts/prefetch-surplus.sh` into `.surplus-cache/`. It
   runs daily two ways — the standalone `surplus-pulse` skill (with a `./notify`
   summary) and the GitLawb fleet's `compute-futures-sim-surplus` task (records
   a curve proof). Remaining: an authenticated, documented Surplus price
   endpoint, and a feed the contract can trust as a settlement *authority*.
3. **Real x402** — swap `X402Settlement` for on-chain x402/MPP. *Concrete target
   identified:* Surplus exposes a callable x402 inference endpoint on Base/USDC
   (`SURPLUS_X402` in `src/surplus.mjs`); `--surplus --x402` already names it.
   Remaining: actually drive 402→pay→200 against it from a funded Base wallet
   (needs a wallet/private-key secret — deliberately not added; real spend).
4. **Safety-critical TTLs** — promote `market/settle` / `market/halt` to the
   short mandatory-TTL + gated-renewal path from gitlawb-safety.
