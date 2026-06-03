// Compute-futures market simulation, driven and traded by the GitLawb fleet.
//
//   node sim.mjs            cash-settled
//   node sim.mjs --x402     physical settlement over the x402 rail (usepod's)
//
// The headline: inject compute-supply/demand events and watch the futures curve
// re-price as the fleet's analyst trades the retail swarm's over-reaction back
// toward fair value. Deterministic (seeded) — every run reproduces.

import { mkdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

import { generateIdentity } from "../gitlawb-safety/src/identity.mjs";
import { CapabilityGuard } from "../gitlawb-safety/src/guard.mjs";
import { RevocationStore } from "../gitlawb-safety/src/revocation.mjs";
import { MetricsRecorder } from "../gitlawb-safety/src/metrics.mjs";
import { SwarmCoordinator } from "../gitlawb-safety/src/coordinator.mjs";

import { rng } from "./src/util.mjs";
import { SpotIndex } from "./src/spot-index.mjs";
import { DarkbloomSpotIndex, DarkbloomBasketIndex } from "./src/darkbloom.mjs";
import { SurplusSpotIndex, SURPLUS_X402 } from "./src/surplus.mjs";
import { marginMultiplier } from "./src/credit.mjs";
import { expirySchedule, termStructure } from "./src/contract.mjs";
import { Trader, ROLE, makeRetail } from "./src/traders.mjs";
import { EventFeed, SPREAD_EVENTS } from "./src/events.mjs";
import { SpreadIndex } from "./src/spread.mjs";
import { WalletBook } from "./src/wallet.mjs";
import { ComputeFuturesMarket } from "./src/market.mjs";
import { X402Settlement, receiptsToMarkdown } from "./src/x402.mjs";
import { termStructureTable, beforeAfter, priceSeries, sparkline } from "./src/curve.mjs";
import { usd } from "./src/util.mjs";

const USE_X402 = process.argv.includes("--x402");
function optionValue(name, fallback) {
  const prefix = `--${name}=`;
  const inline = process.argv.find((a) => a.startsWith(prefix));
  if (inline) return inline.slice(prefix.length);
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

function parseIntOption(name, fallback) {
  const raw = optionValue(name, String(fallback));
  const n = Number.parseInt(raw, 0);
  if (!Number.isFinite(n) || n <= 0) throw new Error(`--${name} must be a positive integer`);
  return n;
}

// Spot source flags (synthetic remains the default so seeded backtests reproduce):
//   --darkbloom        anchor to a single Darkbloom reference model
//   --surplus          anchor to a single Surplus Intelligence reference model
//   --basket[=name]    anchor to a weighted Darkbloom basket index (commodity|frontier|all)
//   --live             additionally pull a live price feed (best effort; falls back)
const USE_SURPLUS = process.argv.includes("--surplus");
const basketArg = process.argv.find((a) => a === "--basket" || a.startsWith("--basket="));
const USE_BASKET = Boolean(basketArg);
const BASKET_NAME = basketArg && basketArg.includes("=") ? basketArg.split("=")[1] : undefined;
const USE_LIVE = process.argv.includes("--live");
// --spread: trade the frontier-vs-commodity premium — a spread between two
// Darkbloom basket indices. Implies basket pricing for both legs.
const USE_SPREAD = process.argv.includes("--spread");
const USE_DARKBLOOM = process.argv.includes("--darkbloom") || USE_BASKET || USE_LIVE || USE_SPREAD;
const SEED = parseIntOption("seed", 0xc0ffee);
const ROUNDS = parseIntOption("rounds", 30);
const UNDERLYING = USE_SPREAD ? "FRONTIER-PREMIUM" : "LLAMA-INFER";

const next = rng(SEED);

// ── Fleet identities (the named GitLawb agents) ──────────────────────────────
const fleet = {
  operator: generateIdentity("operator"), // orchestrates: mints per-round caps
  researcher: generateIdentity("researcher"), // analyst trader
  deployer: generateIdentity("deployer"), // GPU operator (sells capacity forward)
  reviewer: generateIdentity("reviewer"), // clearinghouse / risk (market/settle)
  sentinel: generateIdentity("sentinel"), // surveillance / circuit breaker (market/halt)
};

// ── Capability layer (reused from gitlawb-safety) ────────────────────────────
const metrics = new MetricsRecorder();
const guard = new CapabilityGuard({
  trustedRoots: new Set([fleet.operator.did]), // every chain must root in the operator
  revocations: new RevocationStore(),
  metrics,
});
const coordinator = new SwarmCoordinator({ operator: fleet.operator, guard, metrics });

// ── Wallets (agent-sovereign, usepod-style) ──────────────────────────────────
const wallets = new WalletBook();
wallets.open({ did: fleet.researcher.did, label: "researcher (analyst)", cash: 250_000 });
wallets.open({ did: fleet.deployer.did, label: "deployer (GPU operator)", cash: 250_000 });

const traders = [
  new Trader({ identity: fleet.researcher, role: ROLE.ANALYST, label: "researcher (analyst)" }),
  new Trader({ identity: fleet.deployer, role: ROLE.OPERATOR, label: "deployer (GPU operator)", capacity: 14 }),
  ...makeRetail({ count: 10, makeIdentity: generateIdentity, wallets, startCash: 8_000, next }),
];

// ── Market: pick the index(es) and the event feed ────────────────────────────
// Default: a single underlying (synthetic / single Darkbloom model / basket).
// --spread: two Darkbloom basket legs (commodity + frontier) plus a derived
// FRONTIER-PREMIUM spread index that the fleet trades. All satisfy the same
// SpotIndex-shaped contract the market reads.
let spot; // the headline index used for snapshots/reporting
let spotIndices;
let events;
if (USE_SPREAD) {
  const commodity = new DarkbloomBasketIndex({ underlying: "LLAMA-INFER", next, basket: "commodity" });
  const frontier = new DarkbloomBasketIndex({ underlying: "FRONTIER", next, basket: "frontier" });
  if (USE_LIVE) {
    await commodity.refreshLive();
    await frontier.refreshLive();
  }
  spot = new SpreadIndex({ underlying: UNDERLYING, long: frontier, short: commodity, next });
  spotIndices = [commodity, frontier, spot]; // spread LAST so its history records after the legs step
  events = new EventFeed(SPREAD_EVENTS);
} else {
  if (USE_BASKET) {
    spot = new DarkbloomBasketIndex({ symbol: UNDERLYING, underlying: UNDERLYING, next, basket: BASKET_NAME });
  } else if (USE_SURPLUS) {
    spot = new SurplusSpotIndex({ symbol: UNDERLYING, underlying: UNDERLYING, next });
  } else if (USE_DARKBLOOM) {
    spot = new DarkbloomSpotIndex({ symbol: UNDERLYING, underlying: UNDERLYING, next });
  } else {
    spot = new SpotIndex({
      symbol: UNDERLYING,
      underlying: UNDERLYING,
      price: 0.05, // ~$0.05/M-tokens, commodity open-weight inference (usepod)
      floor: 0.02,
      next,
    });
  }
  // Live re-base for either real venue. Surplus is market-priced, so the live
  // feed is its primary path; Darkbloom falls back to its published catalog.
  if ((USE_SURPLUS || USE_DARKBLOOM) && USE_LIVE && typeof spot.refreshLive === "function") {
    const venue = spot.source; // "surplus" | "darkbloom"
    const envVar = USE_SURPLUS ? "SURPLUS_PRICING_URL" : "DARKBLOOM_PRICING_URL";
    const refreshed = await spot.refreshLive();
    console.log(
      refreshed
        ? `  [${venue}] live anchor: ${spot.modelLabel} → ${usd(spot.price)}/M`
        : `  [${venue}] live feed unavailable — using catalog (set ${envVar})`,
    );
  }
  spotIndices = [spot];
  events = new EventFeed();
}
const EXPIRIES = expirySchedule(ROUNDS);
const contracts = termStructure(UNDERLYING, EXPIRIES, { multiplier: 10, tick: 0.0005 });

// ── Optional x402 physical-settlement rail ───────────────────────────────────
let x402 = null;
if (USE_X402) {
  const escrow = wallets.open({ did: generateIdentity("demand-escrow").did, label: "demand-escrow", cash: 1_000_000 });
  x402 = new X402Settlement({ wallets, escrowDid: escrow.did });
}

const market = new ComputeFuturesMarket({
  fleet,
  traders,
  contracts,
  spotIndices,
  events,
  guard,
  coordinator,
  wallets,
  metrics,
  x402,
  next,
});

// ── Run ──────────────────────────────────────────────────────────────────────
const history = await market.run(ROUNDS);
const dispatchFailures = history.flatMap((h) =>
  h.dispatch.results.filter((r) => !r.ok).map((r) => ({ round: h.round, worker: r.worker, error: r.error })),
);
if (dispatchFailures.length) {
  throw new Error(`dispatch failures: ${JSON.stringify(dispatchFailures.slice(0, 5))}`);
}

// ── Report ────────────────────────────────────────────────────────────────────
const line = (s = "") => console.log(s);
line("═".repeat(72));
line("  COMPUTE FUTURES — simulated & traded by the GitLawb fleet");
const underlyingDesc = USE_SPREAD ? `${UNDERLYING} (frontier − commodity, $/M-tokens)` : `${UNDERLYING} inference compute ($/M-tokens)`;
line(`  underlying: ${underlyingDesc}  ·  settlement: ${USE_X402 ? "x402 physical" : "cash"}`);
line(`  seed: ${SEED}  ·  rounds: ${ROUNDS}`);
line(`  expiries: ${EXPIRIES.join(", ")}`);
const spotKind = USE_SPREAD
  ? "darkbloom spread"
  : USE_BASKET
    ? "darkbloom basket"
    : USE_SURPLUS
      ? "surplus"
      : USE_DARKBLOOM
        ? "darkbloom"
        : "synthetic";
const spotDesc = USE_SPREAD
  ? `${spotKind} (${spot.long.basketLabel} − ${spot.short.basketLabel}${USE_LIVE ? ", live" : ", catalog"})`
  : USE_SURPLUS || USE_DARKBLOOM
    ? `${spotKind} (${spot.modelLabel}${USE_LIVE ? ", live" : ", catalog"})`
    : "synthetic";
line(`  spot source: ${spotDesc}`);
line("═".repeat(72));
line();
if (USE_SPREAD) {
  // Show the t=0 anchors (Σ weightᵢ·blendedᵢ per leg); the spread anchor is the
  // difference of the leg anchors. spot.long/short.price have since drifted.
  const legAnchor = (leg) => Object.values(leg.components).reduce((s, c) => s + c.weight * c.price, 0);
  line("── Spread legs (Darkbloom basket indices, anchor) ".padEnd(72, "─"));
  for (const leg of [spot.long, spot.short]) {
    line(`  ${leg.basketLabel.padEnd(28)} ${leg.underlying.padEnd(16)} ${usd(legAnchor(leg))}/M`);
  }
  line(`  ${"FRONTIER-PREMIUM (spread)".padEnd(28)} ${"".padEnd(16)} ${usd(legAnchor(spot.long) - legAnchor(spot.short))}/M`);
  line();
}
// --spread takes priority over --basket (spot is a SpreadIndex, which has no
// .components); the spread block above already prints its basket-backed legs.
// Without this guard, `--spread --basket` reads spot.components → TypeError.
if (USE_BASKET && !USE_SPREAD) {
  // Components are the t=0 blended prices; the anchor is their weighted sum.
  // (spot.price has since drifted over the run — don't show that here.)
  const anchor = Object.values(spot.components).reduce((s, c) => s + c.weight * c.price, 0);
  line(`── Settlement basket: ${spot.basketLabel} (anchor) `.padEnd(72, "─"));
  for (const [id, c] of Object.entries(spot.components)) {
    line(`  ${id.padEnd(28)} weight ${(c.weight * 100).toFixed(0).padStart(3)}%  blended ${usd(c.price)}/M`);
  }
  line(`  ${"index".padEnd(28)} ${" ".repeat(11)}  =       ${usd(anchor)}/M`);
  line();
}
line("Fleet roles:");
line("  operator   — mints a fresh, scoped market cap to each trader every round");
line("  researcher — analyst: trades the curve back to fair value");
line("  deployer   — GPU operator: sells future capacity forward (the supply)");
line("  reviewer   — clearinghouse: mark-to-market + settlement (market/settle)");
line("  sentinel   — surveillance: circuit breaker on extreme moves (market/halt)");
line();

line(termStructureTable(history[0]));
line();

line("── Curve re-pricing around each event ".padEnd(72, "─"));
for (const e of market.events.fired) {
  line();
  line(beforeAfter(history, e, 3));
}
line();

line("── Price paths (whole run) ".padEnd(72, "─"));
for (const c of contracts) line(priceSeries(history, c.symbol));
line(`  ${"SPOT".padEnd(16)} ${sparkline(history.map((h) => h.spot))}  ${usd(Math.min(...spot.history))}–${usd(Math.max(...spot.history))}`);
line();

line("── Settlements (P&L at expiry) ".padEnd(72, "─"));
for (const s of market.clearing.settlements) {
  line(`  ${s.symbol} settled @ spot ${usd(s.spot)}:`);
  for (const leg of s.legs.sort((a, b) => b.pnl - a.pnl)) {
    line(`    ${(leg.label ?? leg.did).padEnd(24)} qty ${String(leg.qty).padStart(4)} @ ${usd(leg.entry)}  P&L ${usd(leg.pnl)}`);
  }
}
line();

line("── Wallet leaderboard (realized P&L) ".padEnd(72, "─"));
for (const w of wallets.all().sort((a, b) => b.realized - a.realized)) {
  if (w.label === "demand-escrow") continue;
  line(`  ${w.label.padEnd(24)} ${usd(w.realized).padStart(12)}`);
}
line();

// ── Counterparty margin (reputation-scaled) ──────────────────────────────────
// Margin is no longer a flat rate: it scales with each counterparty's Darkbloom
// trust tier + reputation, so weak/unattested sellers post more collateral.
line("── Counterparty margin (Darkbloom-trust-scaled) ".padEnd(72, "─"));
const archetypes = [
  ["researcher (analyst)", fleet.researcher.did],
  ["deployer (GPU operator)", fleet.deployer.did],
  ["retail (each)", traders.find((t) => t.role === ROLE.RETAIL)?.did],
];
line(`  ${"counterparty".padEnd(24)} ${"tier".padEnd(12)} ${"ρ".padStart(5)}  margin ×`);
for (const [label, did] of archetypes) {
  const t = traders.find((x) => x.did === did);
  if (!t) continue;
  line(
    `  ${label.padEnd(24)} ${t.credit.tier.padEnd(12)} ${t.credit.reputation.toFixed(2).padStart(5)}  ${marginMultiplier(t.credit).toFixed(2)}×`,
  );
}
line(`  base margin rate ${(market.clearing.marginRate * 100).toFixed(0)}% of notional · hardware-attested pay the floor, self-attested pay more`);
line(`  peak margin locked: ${usd(market.clearing.peakMarginTotal)} · margin-call flags this run: ${market.clearing.marginCalls.length}`);
line();

if (USE_X402) {
  line("── x402 physical settlement (usepod rail) ".padEnd(72, "─"));
  line(receiptsToMarkdown(x402.receipts));
  line(`  total delivered value: ${usd(x402.total())}  ·  per-tx cost $${0.00025}  ·  ~400ms finality`);
  if (USE_SURPLUS) {
    // The in-memory rail above MODELS settlement; Surplus exposes a callable
    // one. Name the real endpoint a physical Surplus leg would run over.
    line(`  real rail: Surplus x402 ${SURPLUS_X402.resource}`);
    line(`             ${SURPLUS_X402.network} · ${SURPLUS_X402.asset} · base call ${usd(SURPLUS_X402.basePriceUSDC)}`);
  }
  line();
}

// Capability-layer accounting — the orchestration half.
const ev = metrics.all();
const auth = ev.filter((e) => e.type === "authorize");
const denies = auth.filter((e) => !e.allowed);
line("── Capability layer (every order/settlement was authorized) ".padEnd(72, "─"));
line(`  dispatches (per-round caps minted): ${ev.filter((e) => e.type === "dispatch").length}`);
line(`  authorizations: ${auth.length} (allow ${auth.length - denies.length} · deny ${denies.length})`);
line(`  circuit-breaker halts: ${ev.filter((e) => e.type === "halt").length}`);
line(`  ${market.reportTail().split("\n").join("\n  ")}`);
line();

// Persist the run for the dashboard / further analysis.
// Test isolation: $COMPUTE_FUTURES_OUT_DIR lets parallel test files write to
// distinct directories so they don't race on out/last-run.json. Defaults to
// the script-relative out/ that scenario-sweep + the deployer fleet expect.
const outDir = process.env.COMPUTE_FUTURES_OUT_DIR || join(dirname(fileURLToPath(import.meta.url)), "out");
mkdirSync(outDir, { recursive: true });
const outFile = join(outDir, "last-run.json");
writeFileSync(
  outFile,
  JSON.stringify(
    {
      underlying: UNDERLYING,
      settlement: USE_X402 ? "x402" : "cash",
      spotSource: USE_SPREAD
        ? { kind: "darkbloom-spread", long: spot.long.basketId, short: spot.short.basketId, live: USE_LIVE }
        : USE_BASKET
          ? { kind: "darkbloom-basket", basket: spot.basketId, components: spot.components, live: USE_LIVE }
          : USE_SURPLUS
            ? { kind: "surplus", model: spot.modelId, live: USE_LIVE }
            : USE_DARKBLOOM
              ? { kind: "darkbloom", model: spot.modelId, live: USE_LIVE }
              : { kind: "synthetic" },
      seed: SEED,
      events: market.events.fired,
      history,
      wallets: wallets.all().map((w) => w.toJSON()),
      // Clearinghouse settlement-event log — every P&L credit/debit tagged
      // with (round, did, reason, contract). Audit trail for conservation.
      clearinghouse: { events: market.clearing.events },
      x402: x402 ? { receipts: x402.receipts, total: x402.total() } : null,
    },
    null,
    2,
  ),
);
line(`Run written to ${outFile.replace(process.cwd() + "/", "")}`);
