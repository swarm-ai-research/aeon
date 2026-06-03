// Surplus Intelligence spot source — a second REAL venue for the same underlying
// our futures settle against: AI inference priced in $/M-tokens.
//
// Surplus Intelligence (https://www.surplusintelligence.ai/, built by @mac_eth)
// is an OpenAI-compatible inference marketplace where sellers list *surplus*
// capacity and buyers get many models at MARKET prices — a discounted, dynamic
// clearing price rather than a fixed list. That makes it a sibling to the
// Darkbloom adapter (src/darkbloom.mjs): same deliverable ($/M-tokens of a named
// model), same SpotIndex contract, so the futures layer wires it in unchanged.
//
// Two things make Surplus distinct from Darkbloom as a settlement source:
//
//  1. MARKET-PRICED. Darkbloom publishes a fairly static per-model catalog;
//     Surplus prices clear against live supply of surplus credits. So the
//     headline path here is the LIVE feed (refreshLive); the catalog below is
//     only an indicative, deterministic FALLBACK so seeded/offline runs still
//     reproduce exactly (same discipline as darkbloom.mjs).
//
//  2. A REAL x402 RAIL. Surplus exposes a callable x402 endpoint on Base
//     (USDC), so it is a concrete instance of the settlement rail the
//     prototype's x402.mjs only MODELS (that one is Solana/usepod-flavored).
//     We surface that endpoint's metadata as SURPLUS_X402 so the sim can name
//     the real rail a physical settlement would run over.
//
//   site:     https://www.surplusintelligence.ai/
//   sell:     https://www.surplusintelligence.ai/sell
//   x402 api: https://www.surplusintelligence.ai/x402/api/inference/v1/chat/completions
//
// DESIGN NOTES
//  - A future needs a defined DELIVERABLE. Surplus prices per-model and splits
//    input vs output, so (exactly as for Darkbloom) the deliverable is a fixed
//    blend of a chosen reference model; that single $/M number is what settles.
//  - Determinism: with no --live flag the catalog is the only source. --live
//    does a best-effort fetch and falls back to the catalog on any error.
//  - Caveat: Surplus is a young marketplace and clearing prices move with
//    surplus supply. Good as a feed INPUT; treat it as such, not yet as a
//    standalone settlement AUTHORITY.

import { existsSync, readFileSync } from "node:fs";

import { SpotIndex } from "./spot-index.mjs";
// Reuse the generic blend/basket math from the Darkbloom adapter rather than
// duplicating it — the deliverable definition is venue-independent.
import { blendPrice, DEFAULT_BLEND, normalizeWeights, basketPrice } from "./darkbloom.mjs";

export { blendPrice, DEFAULT_BLEND };

// The real x402 inference endpoint Surplus exposes. A physical-settlement leg
// against Surplus would 402→pay→200 against this resource on Base in USDC —
// the concrete counterpart to the in-memory X402Settlement in src/x402.mjs.
export const SURPLUS_X402 = {
  resource: "https://www.surplusintelligence.ai/x402/api/inference/v1/chat/completions",
  network: "eip155:8453", // Base mainnet
  asset: "USDC",
  scheme: "exact",
  // Observed base price for one inference call at the time of writing
  // (3306 USDC base units; USDC has 6 decimals → $0.003306). Indicative only.
  basePriceUSDC: 0.003306,
  openAICompatible: true,
};

// Indicative Surplus market-clearing prices ($/M-tokens), transcribed as a
// deterministic FALLBACK only — real prices clear lower/higher with surplus
// supply, so use --live for the actual feed. `grade` maps the prototype's two
// conceptual underlyings (commodity vs frontier) onto real models, mirroring
// the Darkbloom catalog so the two venues are directly comparable.
export const SURPLUS_CATALOG = {
  "llama-4-scout": { label: "Llama 4 Scout (surplus market)", input: 0.05, output: 0.16, grade: "commodity" },
  "qwen3.5-32b": { label: "Qwen3.5 32B (surplus market)", input: 0.08, output: 0.4, grade: "commodity" },
  "deepseek-v4": { label: "DeepSeek V4 (surplus market)", input: 0.22, output: 0.85, grade: "frontier" },
  "gpt-oss-120b": { label: "GPT-OSS 120B (surplus market)", input: 0.18, output: 0.72, grade: "frontier" },
};

// Map the prototype's underlying symbols to a reference model in the catalog.
export const GRADE_REFERENCE = {
  "LLAMA-INFER": "llama-4-scout", // commodity open-weight
  FRONTIER: "deepseek-v4", // frontier-quality reasoning
};

// Resolve a reference model from an underlying symbol (or an explicit model id).
export function referenceModel(underlying) {
  const id = SURPLUS_CATALOG[underlying] ? underlying : GRADE_REFERENCE[underlying];
  const model = SURPLUS_CATALOG[id];
  if (!model) throw new Error(`surplus: no reference model for "${underlying}"`);
  return { id, model };
}

// ── Settlement baskets ───────────────────────────────────────────────────────
// Same rationale as the Darkbloom baskets: a single reference model is fragile,
// so a basket settles against a weighted average of several models' blended
// prices. Weights are relative and normalized at use.
export const BASKETS = {
  commodity: {
    label: "Surplus commodity basket",
    weights: { "llama-4-scout": 1, "qwen3.5-32b": 1 },
  },
  frontier: {
    label: "Surplus frontier basket",
    weights: { "deepseek-v4": 1, "gpt-oss-120b": 1 },
  },
  all: {
    label: "Surplus all-catalog basket",
    weights: { "llama-4-scout": 1, "qwen3.5-32b": 1, "deepseek-v4": 1, "gpt-oss-120b": 1 },
  },
};

export const UNDERLYING_BASKET = {
  "LLAMA-INFER": "commodity",
  FRONTIER: "frontier",
};

export function resolveBasket(nameOrUnderlying) {
  const id = BASKETS[nameOrUnderlying] ? nameOrUnderlying : UNDERLYING_BASKET[nameOrUnderlying];
  const basket = BASKETS[id];
  if (!basket) throw new Error(`surplus: no basket for "${nameOrUnderlying}"`);
  return { id, ...basket };
}

// Where the prefetch script (scripts/prefetch-surplus.sh) caches the live feed.
// The GitHub Actions sandbox blocks outbound fetch from INSIDE the sim, so the
// workflow fetches Surplus OUTSIDE the sandbox and writes this file; the sim
// then reads it instead of hitting the network itself.
export const SURPLUS_CACHE_FILE = process.env.SURPLUS_CACHE || ".surplus-cache/prices.json";

// Parse a price body into a { id: { input, output } } map. Accepts an object
// map ({ "<id>": {...} }), a `{ models|data: ... }` wrapper, or an OpenAI-style
// list ([{ id, input, output }]).
function parsePriceMap(body) {
  const models = body?.models ?? body?.data ?? body ?? {};
  const entries = Array.isArray(models)
    ? models.map((m) => [m?.id ?? m?.model, m])
    : Object.entries(models);
  const out = {};
  for (const [id, m] of entries) {
    if (!id || typeof m !== "object") continue;
    const input = Number(m.input ?? m.input_price ?? m.prompt);
    const output = Number(m.output ?? m.output_price ?? m.completion);
    if (Number.isFinite(input) && Number.isFinite(output)) out[id] = { input, output };
  }
  return out;
}

// Read prices the prefetch script cached to disk. Never throws.
export function readCachedSurplusPrices(path = SURPLUS_CACHE_FILE) {
  try {
    if (!path || !existsSync(path)) return null;
    const out = parsePriceMap(JSON.parse(readFileSync(path, "utf8")));
    return Object.keys(out).length ? out : null;
  } catch {
    return null;
  }
}

// Best-effort live price fetch from Surplus. The marketplace is OpenAI-compatible
// so a /models or pricing endpoint typically returns either { models: { <id>:
// { input, output } } } or an OpenAI-style list. Any failure → null. Never throws.
export async function fetchLiveSurplusPrices(url = process.env.SURPLUS_PRICING_URL) {
  if (!url || typeof fetch !== "function") return null;
  try {
    const res = await fetch(url, { headers: { accept: "application/json" } });
    if (!res.ok) return null;
    const out = parsePriceMap(await res.json());
    return Object.keys(out).length ? out : null;
  } catch {
    return null;
  }
}

// Resolve the live price map for a refresh. An explicit URL wins (tests, manual
// runs); otherwise prefer the prefetch CACHE FILE (the sandbox-safe path), then
// fall back to a configured SURPLUS_PRICING_URL. Never throws.
export async function loadSurplusPrices(url) {
  if (url) return fetchLiveSurplusPrices(url);
  return (
    readCachedSurplusPrices() ??
    (process.env.SURPLUS_PRICING_URL ? fetchLiveSurplusPrices(process.env.SURPLUS_PRICING_URL) : null)
  );
}

// A SpotIndex anchored to Surplus's market price for a reference model. It IS a
// SpotIndex (same applyShock/step/history contract), so the market wires it in
// with zero changes. With surplus being market-priced, the live feed is the
// headline path — call refreshLive() before the run to re-base the anchor.
export class SurplusSpotIndex extends SpotIndex {
  constructor({ symbol, underlying, next, blend = DEFAULT_BLEND, modelId } = {}) {
    const { id, model } = referenceModel(modelId ?? underlying);
    const anchor = blendPrice(model, blend);
    super({
      symbol: symbol ?? underlying,
      underlying,
      price: anchor,
      // Marginal-cost floor = the cheapest the deliverable can plausibly trade:
      // an input-only mix. A surplus seller can't sell below the rate it quotes.
      floor: Math.min(model.input, blendPrice(model, { inWeight: 9, outWeight: 1 })),
      next,
    });
    this.source = "surplus";
    this.modelId = id;
    this.modelLabel = model.label;
    this.blend = blend;
  }

  async refreshLive(url) {
    const live = await loadSurplusPrices(url);
    if (!live || !live[this.modelId]) return false;
    const model = { ...SURPLUS_CATALOG[this.modelId], ...live[this.modelId] };
    this.fundamental = blendPrice(model, this.blend);
    this.price = this.fundamental;
    this.floor = Math.min(model.input, blendPrice(model, { inWeight: 9, outWeight: 1 }));
    this.history = [this.price];
    return true;
  }
}

// A SpotIndex anchored to a weighted BASKET of Surplus catalog models — a
// settlement index. Identical contract to DarkbloomBasketIndex; the basket only
// sets the anchor and is re-based by a live feed.
export class SurplusBasketIndex extends SpotIndex {
  constructor({ symbol, underlying, next, blend = DEFAULT_BLEND, basket, weights } = {}) {
    const resolved = weights ? { id: "custom", label: "Custom basket", weights } : resolveBasket(basket ?? underlying);
    const norm = normalizeWeights(resolved.weights);
    const { price, components } = basketPrice(norm, { blend, catalog: SURPLUS_CATALOG });
    super({
      symbol: symbol ?? underlying,
      underlying,
      price,
      floor: Math.min(...Object.keys(norm).map((id) => SURPLUS_CATALOG[id].input)),
      next,
    });
    this.source = "surplus-basket";
    this.basketId = resolved.id;
    this.basketLabel = resolved.label;
    this.modelLabel = resolved.label;
    this.weights = norm;
    this.components = components;
    this.blend = blend;
  }

  async refreshLive(url) {
    const live = await loadSurplusPrices(url);
    if (!live) return false;
    const catalog = { ...SURPLUS_CATALOG };
    let updated = false;
    for (const id of Object.keys(this.weights)) {
      if (live[id]) {
        catalog[id] = { ...catalog[id], ...live[id] };
        updated = true;
      }
    }
    if (!updated) return false;
    const { price, components } = basketPrice(this.weights, { blend: this.blend, catalog });
    this.fundamental = price;
    this.price = price;
    this.components = components;
    this.floor = Math.min(...Object.keys(this.weights).map((id) => catalog[id].input));
    this.history = [price];
    return true;
  }
}
