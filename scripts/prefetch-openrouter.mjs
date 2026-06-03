#!/usr/bin/env node
// Prefetch real OpenRouter inference prices for the compute-futures sim.
//
// Runs BEFORE the seeded sim (where network is available — locally and in the
// GitHub Actions fleet runner, which executes plain node, not the Claude bash
// sandbox). Fetches the public OpenRouter model list, maps it onto the futures
// catalog ids, converts $/token → $/M-tokens, and writes a normalized snapshot:
//
//   prototypes/compute-futures/out/live-prices.json
//     { generatedAt, source, models: { "<catalogId>": { input, output } } }
//
// The sim reads this file deterministically via DARKBLOOM_PRICING_FILE, so the
// run stays reproducible within a day. Best-effort: on any failure this logs,
// removes any stale snapshot, and exits 0 so the sim falls back to the static
// catalog (rather than silently reusing an old "live" file).

import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { fetchOpenRouter } from "../prototypes/compute-futures/src/openrouter.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = join(HERE, "..", "prototypes", "compute-futures", "out");
const OUT_FILE = join(OUT_DIR, "live-prices.json");
const SOURCE = process.env.OPENROUTER_PRICING_URL || "https://openrouter.ai/api/v1/models";

const models = await fetchOpenRouter(SOURCE);
if (!models) {
  // Drop any stale snapshot from a previous run so the sweep's existsSync check
  // falls back to the static catalog instead of silently reusing old prices
  // while reporting a "live" run.
  rmSync(OUT_FILE, { force: true });
  console.log(`[prefetch-openrouter] feed unavailable (${SOURCE}) — removed stale snapshot, sim falls back to static catalog`);
  process.exit(0);
}

mkdirSync(OUT_DIR, { recursive: true });
const snapshot = { generatedAt: new Date().toISOString(), source: SOURCE, models };
writeFileSync(OUT_FILE, JSON.stringify(snapshot, null, 2));

const summary = Object.entries(models)
  .map(([id, p]) => `${id}=$${p.input.toFixed(3)}/$${p.output.toFixed(3)}`)
  .join(" · ");
console.log(`[prefetch-openrouter] wrote ${Object.keys(models).length} models → out/live-prices.json (${summary})`);
