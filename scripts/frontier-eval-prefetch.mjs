#!/usr/bin/env node
// Prefetch: fan out the frontier-eval task corpus across all configured
// frontier models via OpenRouter, write raw responses to disk for the
// Claude-side skill to score.
//
// Runs BEFORE the skill (sandbox can't expand env vars in curl headers — the
// standard Aeon pattern). Best-effort: any single (model, task) failure
// drops to null in the output; the skill handles partial coverage.
//
// Inputs:
//   memory/topics/frontier-eval/tasks.yaml          (private task corpus)
//   env OPENROUTER_API_KEY                          (required; skips cleanly if absent)
//   env FRONTIER_EVAL_MODELS                        (optional CSV override)
//
// Output:
//   .frontier-eval-cache/YYYY-MM-DD.json
//     { generatedAt, models: [...], runs: [ { model, taskId, response, latencyMs, error } ] }

import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const TASKS_FILE = join(ROOT, "memory/topics/frontier-eval/tasks.yaml");
const CACHE_DIR = join(ROOT, ".frontier-eval-cache");

const KEY = process.env.OPENROUTER_API_KEY;
if (!KEY) {
  console.log("[prefetch-frontier-eval] OPENROUTER_API_KEY not set — skipping");
  process.exit(0);
}
if (!existsSync(TASKS_FILE)) {
  console.log(`[prefetch-frontier-eval] no corpus at ${TASKS_FILE} — skipping`);
  process.exit(0);
}

// Frontier model slate. Edit here OR override at runtime via FRONTIER_EVAL_MODELS.
// Keep ~6 models — coverage across labs, not exhaustive. Cost per full pass at
// 50 tasks × 6 models × ~800 output tokens ≈ a few USD.
const DEFAULT_MODELS = [
  "anthropic/claude-opus-4.7",
  "anthropic/claude-sonnet-4.6",
  "openai/gpt-5",
  "google/gemini-2.5-pro",
  "deepseek/deepseek-v3.5",
  "x-ai/grok-4",
];
const MODELS = (process.env.FRONTIER_EVAL_MODELS || "").split(",").map(s => s.trim()).filter(Boolean);
const SLATE = MODELS.length ? MODELS : DEFAULT_MODELS;

// Minimal YAML reader — corpus uses a flat shape (no anchors/refs), so a tiny
// hand-rolled parser is enough and avoids pulling in a dep. If the corpus
// grows into needing real YAML, switch to `yaml` from npm.
function parseTasks(yaml) {
  const tasks = [];
  let cur = null;
  let inPrompt = false;
  let inRubric = false;
  let promptLines = [];
  let activeSection = false;

  for (const rawLine of yaml.split("\n")) {
    const line = rawLine.replace(/\r$/, "");
    if (/^active:\s*$/.test(line)) { activeSection = true; continue; }
    if (/^retired:/.test(line)) { activeSection = false; continue; }
    if (!activeSection) continue;

    const idMatch = line.match(/^\s*-\s*id:\s*(\S+)/);
    if (idMatch) {
      if (cur) finalize(cur, promptLines, tasks);
      cur = { id: idMatch[1], prompt: "", rubric: [], max_score: null };
      promptLines = [];
      inPrompt = false;
      inRubric = false;
      continue;
    }
    if (!cur) continue;

    if (/^\s+prompt:\s*\|/.test(line)) { inPrompt = true; inRubric = false; continue; }
    if (/^\s+rubric:\s*$/.test(line)) { inPrompt = false; inRubric = true; continue; }
    const maxMatch = line.match(/^\s+max_score:\s*(\d+)/);
    if (maxMatch) { cur.max_score = Number(maxMatch[1]); inPrompt = false; inRubric = false; continue; }

    if (inPrompt) {
      // YAML block scalars are dedented relative to the indentation of the
      // first non-blank line; we use 6 spaces in the corpus consistently.
      promptLines.push(line.replace(/^ {6}/, ""));
      continue;
    }
    if (inRubric) {
      const m = line.match(/^\s+-\s*(.*)$/);
      if (m) cur.rubric.push(m[1]);
      continue;
    }
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
    const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${KEY}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/rsavitt/aeon",
        "X-Title": "aeon-frontier-eval",
      },
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content: prompt }],
        max_tokens: 1024,
        temperature: 0.0,
      }),
    });
    const body = await res.json();
    if (!res.ok) {
      return { response: null, latencyMs: Date.now() - start, error: body?.error?.message || `HTTP ${res.status}` };
    }
    const content = body?.choices?.[0]?.message?.content ?? null;
    return { response: content, latencyMs: Date.now() - start, error: content ? null : "empty response" };
  } catch (e) {
    return { response: null, latencyMs: Date.now() - start, error: String(e.message || e) };
  }
}

const tasks = parseTasks(readFileSync(TASKS_FILE, "utf8"));
if (!tasks.length) {
  console.log("[prefetch-frontier-eval] corpus parsed to 0 tasks — check tasks.yaml format");
  process.exit(0);
}

console.log(`[prefetch-frontier-eval] ${tasks.length} tasks × ${SLATE.length} models = ${tasks.length * SLATE.length} calls`);

// Run all (model, task) pairs concurrently. OpenRouter handles rate limiting;
// at this volume (~300 calls max) it's a non-issue.
const jobs = [];
for (const model of SLATE) {
  for (const task of tasks) {
    jobs.push(callModel(model, task.prompt).then(r => ({ model, taskId: task.id, ...r })));
  }
}
const runs = await Promise.all(jobs);

mkdirSync(CACHE_DIR, { recursive: true });
const stamp = new Date().toISOString().slice(0, 10);
const outFile = join(CACHE_DIR, `${stamp}.json`);
writeFileSync(outFile, JSON.stringify({
  generatedAt: new Date().toISOString(),
  models: SLATE,
  taskIds: tasks.map(t => t.id),
  runs,
}, null, 2));

const ok = runs.filter(r => r.response).length;
const errs = runs.length - ok;
console.log(`[prefetch-frontier-eval] wrote ${outFile} — ${ok} ok, ${errs} errors`);
