// OpenRouter live-price adapter.
//
// OpenRouter publishes a public, no-auth model list at
// https://openrouter.ai/api/v1/models with the shape:
//   { data: [ { id, pricing: { prompt, completion } }, ... ] }
// where `prompt`/`completion` are quoted in $/token (often as strings).
//
// Our futures catalog (src/darkbloom.mjs) prices in $/M-tokens and keys models
// by the catalog ids below. This adapter maps real OpenRouter models onto those
// catalog ids and converts $/token → $/M-tokens (× 1e6), producing exactly the
// { <catalogId>: { input, output } } shape that fetchLivePrices() already
// consumes. Any model that isn't found is simply omitted, so the caller merges
// what it can over the static catalog and the run never breaks.

const PER_TOKEN_TO_PER_M = 1_000_000;

// Catalog id → OpenRouter id. The catalog's ids are research-preview names; we
// stand in real, currently-listed OpenRouter models of the same grade so the
// live feed tracks a real venue. Resolved best-effort against the live list.
export const OPENROUTER_MODEL_MAP = {
  "gemma-4-26b": "google/gemma-4-26b-a4b-it", // commodity open-weight MoE
  "minimax-m2.5": "qwen/qwen3.5-9b", // commodity small dense
  "qwen3.5-27b-claude-opus": "anthropic/claude-opus-4.7-fast", // frontier, Opus-distilled analog
  "qwen3.5-122b": "openai/gpt-5.4-pro", // frontier large
};

function toNumber(x) {
  const n = typeof x === "string" ? Number.parseFloat(x) : Number(x);
  return Number.isFinite(n) ? n : NaN;
}

// Build a lookup of OpenRouter id → { input, output } in $/M-tokens from a raw
// API body. Tolerates both { data: [...] } and a bare array.
function indexByOpenRouterId(body) {
  const list = Array.isArray(body) ? body : body?.data ?? body?.models ?? [];
  const out = new Map();
  for (const m of Array.isArray(list) ? list : []) {
    const id = m?.id ?? m?.model;
    const pricing = m?.pricing ?? m;
    if (!id || !pricing) continue;
    const promptPer = toNumber(pricing.prompt ?? pricing.input);
    const completionPer = toNumber(pricing.completion ?? pricing.output);
    if (!Number.isFinite(promptPer) || !Number.isFinite(completionPer)) continue;
    out.set(id, {
      input: promptPer * PER_TOKEN_TO_PER_M,
      output: completionPer * PER_TOKEN_TO_PER_M,
    });
  }
  return out;
}

// Normalize an OpenRouter API body into the catalog-keyed live-price shape:
//   { "<catalogId>": { input, output } }  ($/M-tokens)
// `map` overrides the default catalog→OpenRouter mapping (handy for tests).
export function normalizeOpenRouter(body, map = OPENROUTER_MODEL_MAP) {
  const byId = indexByOpenRouterId(body);
  const models = {};
  for (const [catalogId, openrouterId] of Object.entries(map)) {
    const priced = byId.get(openrouterId);
    if (priced) models[catalogId] = priced;
  }
  return models;
}

// Best-effort fetch of the OpenRouter model list. Returns the normalized
// catalog-keyed map, or null on any failure (offline, non-200, empty). Never
// throws — callers fall back to the static catalog.
export async function fetchOpenRouter(url = "https://openrouter.ai/api/v1/models", map = OPENROUTER_MODEL_MAP) {
  if (typeof fetch !== "function") return null;
  try {
    const res = await fetch(url, { headers: { accept: "application/json" } });
    if (!res.ok) return null;
    const body = await res.json();
    const models = normalizeOpenRouter(body, map);
    return Object.keys(models).length ? models : null;
  } catch {
    return null;
  }
}
