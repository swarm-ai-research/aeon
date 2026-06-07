#!/usr/bin/env node
// Local-models track for frontier-eval. Mirrors frontier-eval-prefetch.mjs but
// hits a local Ollama server instead of OpenRouter. Output lands in a sibling
// cache file (-local.json) so the skill can score both tracks in one pass and
// emit a per-track row to timeseries.jsonl.
//
// The point of running this in parallel with the OpenRouter track is the
// *gap* between the two — closed-frontier minus open-weights, on identical
// tasks, scored by the same judge. Narrowing gap → commoditization signal.
// Widening gap → closed-source moat reasserting.
//
// Inputs:
//   memory/topics/frontier-eval/tasks.yaml          (shared corpus)
//   env OLLAMA_HOST                                 (optional; default http://localhost:11434)
//   env FRONTIER_EVAL_LOCAL_MODELS                  (optional CSV override)
//
// Output:
//   .frontier-eval-cache/YYYY-MM-DD-local.json
//     { generatedAt, host, models: [...], runs: [...] }

import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const TASKS_FILE = join(ROOT, "memory/topics/frontier-eval/tasks.yaml");
const CACHE_DIR = join(ROOT, ".frontier-eval-cache");

const HOST = (process.env.OLLAMA_HOST || "http://localhost:11434").replace(/\/$/, "");

if (!existsSync(TASKS_FILE)) {
  console.log(`[frontier-eval-local] no corpus at ${TASKS_FILE} — skipping`);
  process.exit(0);
}

// Best-effort connectivity probe. If Ollama isn't running, skip cleanly — the
// skill handles missing-cache for either track.
let installed;
try {
  const tagsRes = await fetch(`${HOST}/api/tags`, { signal: AbortSignal.timeout(2000) });
  if (!tagsRes.ok) throw new Error(`HTTP ${tagsRes.status}`);
  const body = await tagsRes.json();
  installed = new Set((body?.models ?? []).map(m => m.name));
} catch (e) {
  console.log(`[frontier-eval-local] Ollama unreachable at ${HOST} (${e.message || e}) — skipping`);
  process.exit(0);
}

// Open-weights slate. Edit here OR override at runtime via FRONTIER_EVAL_LOCAL_MODELS.
// Default picks span sizes (small/mid/large) and source labs (Alibaba, Meta,
// DeepSeek, Google, Mistral) so the time series captures the open frontier,
// not just one family's trajectory.
const DEFAULT_MODELS = [
  "qwen3:32b",
  "llama3.3:70b",
  "deepseek-r1:32b",
  "gemma3:27b",
  "mistral-nemo:12b",
  "phi4:14b",
];
const SLATE_RAW = (process.env.FRONTIER_EVAL_LOCAL_MODELS || "").split(",").map(s => s.trim()).filter(Boolean);
const REQUESTED = SLATE_RAW.length ? SLATE_RAW : DEFAULT_MODELS;

// Only run models actually pulled locally. Anything missing logs and is skipped
// — we don't want to silently inflate "errors" when the user just hasn't pulled
// a model yet. They can `ollama pull <name>` and rerun.
const SLATE = REQUESTED.filter(m => installed.has(m));
const SKIPPED = REQUESTED.filter(m => !installed.has(m));
if (SKIPPED.length) {
  console.log(`[frontier-eval-local] not installed (skipping): ${SKIPPED.join(", ")}`);
}
if (!SLATE.length) {
  console.log(`[frontier-eval-local] no requested models are pulled locally — skipping`);
  process.exit(0);
}

// Same YAML reader as the closed-track prefetch. Kept in-file so the two
// scripts have no cross-import; the corpus parser is small enough that
// duplicating it is cheaper than wiring a shared module.
function parseTasks(yaml) {
  const tasks = [];
  let cur = null, inPrompt = false, inRubric = false, promptLines = [], activeSection = false;
  for (const rawLine of yaml.split("\n")) {
    const line = rawLine.replace(/\r$/, "");
    if (/^active:\s*$/.test(line)) { activeSection = true; continue; }
    if (/^retired:/.test(line)) { activeSection = false; continue; }
    if (!activeSection) continue;
    const idMatch = line.match(/^\s*-\s*id:\s*(\S+)/);
    if (idMatch) {
      if (cur) finalize(cur, promptLines, tasks);
      cur = { id: idMatch[1], prompt: "", rubric: [], max_score: null };
      promptLines = []; inPrompt = false; inRubric = false; continue;
    }
    if (!cur) continue;
    if (/^\s+prompt:\s*\|/.test(line)) { inPrompt = true; inRubric = false; continue; }
    if (/^\s+rubric:\s*$/.test(line)) { inPrompt = false; inRubric = true; continue; }
    const maxMatch = line.match(/^\s+max_score:\s*(\d+)/);
    if (maxMatch) { cur.max_score = Number(maxMatch[1]); inPrompt = false; inRubric = false; continue; }
    if (inPrompt) { promptLines.push(line.replace(/^ {6}/, "")); continue; }
    if (inRubric) { const m = line.match(/^\s+-\s*(.*)$/); if (m) cur.rubric.push(m[1]); continue; }
  }
  if (cur) finalize(cur, promptLines, tasks);
  return tasks;
}
function finalize(cur, promptLines, tasks) {
  cur.prompt = promptLines.join("\n").replace(/\n+$/, "");
  if (cur.id && cur.prompt) tasks.push(cur);
}

async function callModel(model, prompt) {
  const start = Date.now();
  try {
    // Ollama's /api/chat is OpenAI-shaped at the messages level. We use it
    // rather than /api/generate because the chat endpoint applies the model's
    // own chat template, which matters for instruct/RL-tuned variants.
    const res = await fetch(`${HOST}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content: prompt }],
        stream: false,
        options: { temperature: 0.0, num_predict: 1024 },
      }),
      // Local-model inference can be slow on a laptop; give each call generous
      // headroom but cap so a single hung model doesn't block the whole run.
      signal: AbortSignal.timeout(180_000),
    });
    const body = await res.json();
    if (!res.ok) {
      return { response: null, latencyMs: Date.now() - start, error: body?.error || `HTTP ${res.status}` };
    }
    const content = body?.message?.content ?? null;
    return { response: content, latencyMs: Date.now() - start, error: content ? null : "empty response" };
  } catch (e) {
    return { response: null, latencyMs: Date.now() - start, error: String(e.message || e) };
  }
}

const tasks = parseTasks(readFileSync(TASKS_FILE, "utf8"));
if (!tasks.length) {
  console.log("[frontier-eval-local] corpus parsed to 0 tasks — check tasks.yaml format");
  process.exit(0);
}

console.log(`[frontier-eval-local] ${tasks.length} tasks × ${SLATE.length} models = ${tasks.length * SLATE.length} calls @ ${HOST}`);

// Run each (model, task) pair sequentially per model — local Ollama serves
// requests one-at-a-time per model anyway (KV cache + GPU memory), so
// concurrent calls to the same model just queue. Across models we'd benefit
// from concurrency, but only if Ollama is hosting multiple models in VRAM
// simultaneously, which is rare on a single-GPU box. Sequential is the
// honest default; users on multi-GPU rigs can wrap this in xargs -P.
const runs = [];
for (const model of SLATE) {
  for (const task of tasks) {
    const r = await callModel(model, task.prompt);
    runs.push({ model, taskId: task.id, ...r });
  }
}

mkdirSync(CACHE_DIR, { recursive: true });
const stamp = new Date().toISOString().slice(0, 10);
const outFile = join(CACHE_DIR, `${stamp}-local.json`);
writeFileSync(outFile, JSON.stringify({
  generatedAt: new Date().toISOString(),
  host: HOST,
  models: SLATE,
  taskIds: tasks.map(t => t.id),
  runs,
}, null, 2));

const ok = runs.filter(r => r.response).length;
const errs = runs.length - ok;
console.log(`[frontier-eval-local] wrote ${outFile} — ${ok} ok, ${errs} errors`);
