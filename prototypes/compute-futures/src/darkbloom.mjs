// Darkbloom spot source — a REAL venue for the same underlying our futures
// settle against: AI inference priced in $/M-tokens.
//
// Where SpotIndex (spot-index.mjs) anchors to a hand-set "fundamental", this
// anchors to Darkbloom's published per-model prices. Darkbloom (Eigen Labs) is
// a decentralized, OpenAI-compatible inference market running on idle Apple
// Silicon — exactly the kind of spot venue usepod is, so we can treat it as a
// settlement index and build the futures layer on top unchanged.
//
//   docs:  https://www.darkbloom.dev/
//   api:   https://api.darkbloom.dev/v1  (OpenAI-compatible)
//
// DESIGN NOTES
//  - A future needs a defined DELIVERABLE. Darkbloom prices per-model and splits
//    input vs output, so we define the deliverable as a fixed blend (see
//    blendPrice) of a chosen reference model. That single $/M number is what the
//    contract settles against.
//  - Determinism is preserved: with no --live flag the catalog below is the only
//    source, so seeded runs still reproduce exactly. --live does a best-effort
//    fetch and falls back to the catalog on any error (offline, no endpoint).
//  - Caveat: Darkbloom is an unaudited research preview. Good as a feed INPUT;
//    not yet a trustworthy settlement AUTHORITY. This adapter treats it as the
//    former.

import { readFileSync } from "node:fs";

import { SpotIndex } from "./spot-index.mjs";

// Published Darkbloom catalog ($/M-tokens), transcribed from darkbloom.dev /
// the d-inference README on 2026-05-25. `grade` lets us map the prototype's two
// conceptual underlyings (commodity vs frontier) onto real models.
export const DARKBLOOM_CATALOG = {
  "gemma-4-26b": { label: "Gemma 4 26B (MoE, 4B active)", input: 0.065, output: 0.2, grade: "commodity" },
  "qwen3.5-27b-claude-opus": { label: "Qwen3.5 27B (dense, Opus-distilled)", input: 0.1, output: 0.78, grade: "frontier" },
  "qwen3.5-122b": { label: "Qwen3.5 122B (MoE, 10B active)", input: 0.13, output: 1.04, grade: "frontier" },
  "minimax-m2.5": { label: "MiniMax M2.5 (MoE, 11B active)", input: 0.06, output: 0.5, grade: "commodity" },
};

// Map the prototype's underlying symbols to a reference model in the catalog.
export const GRADE_REFERENCE = {
  "LLAMA-INFER": "gemma-4-26b", // commodity open-weight MoE
  FRONTIER: "qwen3.5-27b-claude-opus", // frontier-quality reasoning
};

// The deliverable blend: 1M tokens delivered at this input:output mix. Inference
// workloads are input-heavy, so we default to 3:1. This ratio IS the contract
// spec — change it and you've defined a different deliverable.
export const DEFAULT_BLEND = { inWeight: 3, outWeight: 1 };

// Blend a model's split pricing into a single $/M settlement price.
export function blendPrice(model, { inWeight, outWeight } = DEFAULT_BLEND) {
  const w = inWeight + outWeight;
  return (model.input * inWeight + model.output * outWeight) / w;
}

// Resolve a reference model from an underlying symbol (or an explicit model id).
export function referenceModel(underlying) {
  const id = DARKBLOOM_CATALOG[underlying] ? underlying : GRADE_REFERENCE[underlying];
  const model = DARKBLOOM_CATALOG[id];
  if (!model) throw new Error(`darkbloom: no reference model for "${underlying}"`);
  return { id, model };
}

// ── Settlement baskets ───────────────────────────────────────────────────────
// A single reference model is fragile: if it's delisted or repriced, the whole
// contract moves. A basket settles against a WEIGHTED AVERAGE of several models'
// blended $/M prices — a representative index, the way real commodity indices
// work. Weights are relative and normalized at use.
export const BASKETS = {
  commodity: {
    label: "Commodity-MoE basket",
    weights: { "gemma-4-26b": 1, "minimax-m2.5": 1 },
  },
  frontier: {
    label: "Frontier basket",
    weights: { "qwen3.5-27b-claude-opus": 1, "qwen3.5-122b": 1 },
  },
  all: {
    label: "All-catalog basket",
    weights: { "gemma-4-26b": 1, "minimax-m2.5": 1, "qwen3.5-27b-claude-opus": 1, "qwen3.5-122b": 1 },
  },
};

// Map the prototype's underlying symbols to a default basket.
export const UNDERLYING_BASKET = {
  "LLAMA-INFER": "commodity",
  FRONTIER: "frontier",
};

// Normalize a {modelId: weight} map so the weights sum to 1.
export function normalizeWeights(weights) {
  const total = Object.values(weights).reduce((a, b) => a + b, 0);
  if (!(total > 0)) throw new Error("darkbloom: basket weights must sum to a positive number");
  return Object.fromEntries(Object.entries(weights).map(([id, w]) => [id, w / total]));
}

// Weighted-average blended price across a basket's members. Returns the index
// price plus the per-component breakdown (weight + that model's blended price)
// for transparency in reports/output. `catalog` is injectable so a live feed
// can be merged over the static catalog.
export function basketPrice(weights, { blend = DEFAULT_BLEND, catalog = DARKBLOOM_CATALOG } = {}) {
  const norm = normalizeWeights(weights);
  const components = {};
  let price = 0;
  for (const [id, w] of Object.entries(norm)) {
    const model = catalog[id];
    if (!model) throw new Error(`darkbloom: basket references unknown model "${id}"`);
    const p = blendPrice(model, blend);
    components[id] = { weight: w, price: p };
    price += w * p;
  }
  return { price, components };
}

// Resolve a basket's weight map from a preset name or underlying symbol.
export function resolveBasket(nameOrUnderlying) {
  const id = BASKETS[nameOrUnderlying] ? nameOrUnderlying : UNDERLYING_BASKET[nameOrUnderlying];
  const basket = BASKETS[id];
  if (!basket) throw new Error(`darkbloom: no basket for "${nameOrUnderlying}"`);
  return { id, ...basket };
}

// Best-effort live price fetch. Two sources, file takes precedence:
//   - DARKBLOOM_PRICING_FILE: a local JSON snapshot (e.g. written by
//     scripts/prefetch-openrouter.mjs). Preferred in the sandbox, since Node's
//     fetch can't read file:// and prefetch keeps the seeded run network-free.
//   - DARKBLOOM_PRICING_URL: an operator-supplied HTTP endpoint.
// Both are expected to return { models: { <id>: { input, output } } } (or an
// OpenAI-style list). Any failure → null, and the caller keeps the static
// catalog. Never throws.
export async function fetchLivePrices(url = process.env.DARKBLOOM_PRICING_URL, file = process.env.DARKBLOOM_PRICING_FILE) {
  try {
    let body;
    if (file) {
      body = JSON.parse(readFileSync(file, "utf8"));
    } else {
      if (!url || typeof fetch !== "function") return null;
      const res = await fetch(url, { headers: { accept: "application/json" } });
      if (!res.ok) return null;
      body = await res.json();
    }
    const models = body.models ?? body.data ?? body;
    // Object-map ({ "<id>": {...} }) or OpenAI-style list ([{ id, ... }]). For a
    // list, key by the model's own id, not its array index.
    const entries = Array.isArray(models)
      ? models.map((m) => [m.id ?? m.model, m])
      : Object.entries(models);
    const out = {};
    for (const [id, m] of entries) {
      if (!id) continue;
      const input = Number(m.input ?? m.input_price ?? m.prompt);
      const output = Number(m.output ?? m.output_price ?? m.completion);
      if (Number.isFinite(input) && Number.isFinite(output)) out[id] = { input, output };
    }
    return Object.keys(out).length ? out : null;
  } catch {
    return null;
  }
}

// A SpotIndex whose anchor comes from Darkbloom's real catalog instead of a
// hand-set fundamental. It IS a SpotIndex (same applyShock/step/history
// contract), so the market wires it in with zero changes — events still shock
// the fundamental, the curve still reprices, runs stay deterministic.
export class DarkbloomSpotIndex extends SpotIndex {
  constructor({ symbol, underlying, next, blend = DEFAULT_BLEND, modelId } = {}) {
    const { id, model } = referenceModel(modelId ?? underlying);
    const anchor = blendPrice(model, blend);
    super({
      symbol: symbol ?? underlying,
      underlying,
      price: anchor,
      // Marginal-cost floor = the cheapest the deliverable can plausibly trade:
      // an input-only mix. The provider can't sell below the rate it's quoted.
      floor: Math.min(model.input, blendPrice(model, { inWeight: 9, outWeight: 1 })),
      next,
    });
    this.source = "darkbloom";
    this.modelId = id;
    this.modelLabel = model.label;
    this.blend = blend;
  }

  // Pull a fresh anchor from a live feed (if configured) and re-base the
  // fundamental on it. Best-effort: leaves the index untouched on any failure.
  // Call BEFORE the run starts so seeded stepping stays reproducible per-feed.
  async refreshLive(url) {
    const live = await fetchLivePrices(url);
    if (!live || !live[this.modelId]) return false;
    const model = { ...DARKBLOOM_CATALOG[this.modelId], ...live[this.modelId] };
    this.fundamental = blendPrice(model, this.blend);
    this.price = this.fundamental;
    this.floor = Math.min(model.input, blendPrice(model, { inWeight: 9, outWeight: 1 }));
    this.history = [this.price];
    return true;
  }
}

// A SpotIndex anchored to a weighted BASKET of catalog models rather than a
// single reference model — a settlement index. Once constructed it evolves as a
// single price series (you trade the index, not the components), so the
// applyShock/step contract and determinism are identical to SpotIndex; the
// basket only sets the anchor and is re-based by a live feed.
export class DarkbloomBasketIndex extends SpotIndex {
  constructor({ symbol, underlying, next, blend = DEFAULT_BLEND, basket, weights } = {}) {
    const resolved = weights ? { id: "custom", label: "Custom basket", weights } : resolveBasket(basket ?? underlying);
    const norm = normalizeWeights(resolved.weights);
    const { price, components } = basketPrice(norm, { blend });
    super({
      symbol: symbol ?? underlying,
      underlying,
      price,
      // Floor = cheapest member's input-only rate; the index can't trade below
      // the marginal cost of its cheapest constituent.
      floor: Math.min(...Object.keys(norm).map((id) => DARKBLOOM_CATALOG[id].input)),
      next,
    });
    this.source = "darkbloom-basket";
    this.basketId = resolved.id;
    this.basketLabel = resolved.label;
    this.modelLabel = resolved.label; // so the sim header/JSON treat it like the single-model index
    this.weights = norm;
    this.components = components;
    this.blend = blend;
  }

  // Re-base the index on live prices: merge the live feed over the static
  // catalog for the basket's members and recompute. Best-effort — returns false
  // (index untouched) unless at least one member was updated.
  async refreshLive(url) {
    const live = await fetchLivePrices(url);
    if (!live) return false;
    const catalog = { ...DARKBLOOM_CATALOG };
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
    // Re-anchor the marginal-cost floor against the LIVE catalog. Without this,
    // a frozen-catalog floor (e.g. ~$0.10) lingers under a live fundamental
    // (~$30), making the "compression to marginal cost" regime unreachable.
    this.floor = Math.min(...Object.keys(this.weights).map((id) => catalog[id].input));
    this.history = [price];
    return true;
  }
}
