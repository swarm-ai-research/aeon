import assert from "node:assert/strict";
import { test } from "node:test";

import { normalizeOpenRouter, OPENROUTER_MODEL_MAP } from "../src/openrouter.mjs";

const SAMPLE = {
  data: [
    { id: "google/gemma-4-26b-a4b-it", pricing: { prompt: "0.00000006", completion: "0.00000033" } },
    { id: "qwen/qwen3.5-9b", pricing: { prompt: 0.00000004, completion: 0.00000015 } },
    { id: "anthropic/claude-opus-4.7-fast", pricing: { prompt: "0.00003", completion: "0.00015" } },
    { id: "some/unmapped-model", pricing: { prompt: "0.001", completion: "0.002" } },
  ],
};

test("normalizeOpenRouter maps catalog ids and converts $/token → $/M", () => {
  const models = normalizeOpenRouter(SAMPLE);
  // gemma: 6e-8 $/token × 1e6 = $0.06/M input, 3.3e-7 × 1e6 = $0.33/M output.
  assert.ok(Math.abs(models["gemma-4-26b"].input - 0.06) < 1e-9);
  assert.ok(Math.abs(models["gemma-4-26b"].output - 0.33) < 1e-9);
  // minimax-m2.5 is mapped to qwen3.5-9b.
  assert.ok(Math.abs(models["minimax-m2.5"].input - 0.04) < 1e-9);
  // frontier: claude-opus → qwen3.5-27b-claude-opus catalog id.
  assert.ok(Math.abs(models["qwen3.5-27b-claude-opus"].input - 30) < 1e-6);
});

test("normalizeOpenRouter omits models absent from the feed (catalog fallback)", () => {
  const models = normalizeOpenRouter(SAMPLE);
  // qwen3.5-122b → openai/gpt-5.4-pro, which isn't in SAMPLE → omitted.
  assert.equal(models["qwen3.5-122b"], undefined);
  // Unmapped feed models never appear.
  assert.equal(models["some/unmapped-model"], undefined);
});

test("normalizeOpenRouter tolerates a bare array and missing pricing", () => {
  const models = normalizeOpenRouter([
    { id: "google/gemma-4-26b-a4b-it", pricing: { prompt: "0.0000001", completion: "0.0000002" } },
    { id: "broken/model" }, // no pricing → skipped, no throw
  ]);
  assert.ok(models["gemma-4-26b"]);
  assert.equal(Object.keys(models).length, 1);
});

test("OPENROUTER_MODEL_MAP covers every catalog model used by baskets", () => {
  for (const id of ["gemma-4-26b", "minimax-m2.5", "qwen3.5-27b-claude-opus", "qwen3.5-122b"]) {
    assert.ok(OPENROUTER_MODEL_MAP[id], `missing mapping for ${id}`);
  }
});
