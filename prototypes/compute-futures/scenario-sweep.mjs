// Scenario sweep runner for the compute-futures prototype.
//
// Runs the simulator across mode × seed combinations, extracts market-quality
// metrics from out/last-run.json, and writes compact JSON/Markdown reports.
//
// Beyond the per-run table it now reports a DISTRIBUTION per mode (mean, 95% CI,
// win-rate), per-ROLE P&L attribution (analyst / operator / retail — who makes
// or loses money), a P&L-conservation check, and an optional paired
// synthetic-vs-basket diff (--pair) that isolates the basket effect from seed
// noise. With --live, the darkbloom-backed modes (basket, spread) read the
// prefetched OpenRouter snapshot at out/live-prices.json.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { ci95, mean, median, realizedByRole, stddev, winRate } from "./src/stats.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "out");
const LIVE_FILE = join(OUT, "live-prices.json");

const MODE_ARGS = {
  synthetic: [],
  basket: ["--basket"],
  spread: ["--spread"],
  x402: ["--x402"],
};

// Modes whose spot source is darkbloom-backed and therefore benefit from a live
// feed. synthetic/x402 use the synthetic spot index (deterministic baseline);
// passing --live to them would flip USE_DARKBLOOM and change the spot source, so
// we never do.
const LIVE_MODES = new Set(["basket", "spread"]);

function option(name, fallback) {
  const prefix = `--${name}=`;
  const inline = process.argv.find((a) => a.startsWith(prefix));
  if (inline) return inline.slice(prefix.length);
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

function listOption(name, fallback) {
  return option(name, fallback).split(",").map((s) => s.trim()).filter(Boolean);
}

const seeds = listOption("seeds", "12648430,12648431,12648432").map((s) => Number.parseInt(s, 0));
const modes = listOption("modes", "synthetic,basket,spread,x402");
const rounds = Number.parseInt(option("rounds", "30"), 0);
const USE_LIVE = process.argv.includes("--live");
const USE_PAIR = process.argv.includes("--pair");

if (!Number.isFinite(rounds) || rounds <= 0) throw new Error("--rounds must be a positive integer");
for (const seed of seeds) if (!Number.isFinite(seed) || seed <= 0) throw new Error(`invalid seed: ${seed}`);
for (const mode of modes) if (!MODE_ARGS[mode]) throw new Error(`unknown mode "${mode}"`);

const liveAvailable = USE_LIVE && existsSync(LIVE_FILE);

function runOne({ mode, seed }) {
  // Gate on liveAvailable (not just USE_LIVE): if the prefetch snapshot is
  // absent the sim falls back to the static catalog anyway, so we must not pass
  // --live or label the run live — that would let JSON consumers read a catalog
  // run as live while the top-level report says the feed was unavailable.
  const live = liveAvailable && LIVE_MODES.has(mode);
  const args = ["sim.mjs", ...MODE_ARGS[mode], "--seed", String(seed), "--rounds", String(rounds)];
  if (live) args.push("--live");
  // Darkbloom modes read the prefetched snapshot deterministically via the file
  // env var; synthetic/x402 spawns get a clean env so they stay reproducible.
  const env = live ? { ...process.env, DARKBLOOM_PRICING_FILE: LIVE_FILE } : process.env;
  const res = spawnSync(process.execPath, args, { cwd: HERE, encoding: "utf8", timeout: 30_000, env });
  if (res.status !== 0) {
    throw new Error(`sim failed for ${mode}/${seed}\n${res.stderr || res.stdout}`);
  }
  const runFile = join(OUT, "last-run.json");
  if (!existsSync(runFile)) throw new Error(`missing run output for ${mode}/${seed}`);
  const run = JSON.parse(readFileSync(runFile, "utf8"));
  const failedDispatches = run.history.flatMap((h) => h.dispatch.results.filter((r) => !r.ok));
  if (failedDispatches.length) {
    throw new Error(`sim produced ${failedDispatches.length} failed dispatches for ${mode}/${seed}`);
  }
  return summarize(run, { mode, seed, live });
}

function summarize(run, { mode, seed, live }) {
  const spots = run.history.map((h) => h.spot).filter(Number.isFinite);
  const curvePrices = run.history.flatMap((h) => h.curve.map((c) => c.price).filter(Number.isFinite));
  const realized = run.wallets.map((w) => w.realized ?? 0);
  const settlementLegs = run.history.flatMap((h) => h.settlements.flatMap((s) => s.legs));
  const eventRounds = run.events.map((e) => e.round);
  const deniedWorkers = run.history.reduce((n, h) => n + h.dispatch.results.filter((r) => r.out?.denied > 0).length, 0);
  // Per-contract notional anchor for cross-mode comparison. Spread mode anchors
  // ~600× higher than synthetic in live runs (frontier ~$30 vs synthetic ~$0.05),
  // so raw $ P&Ls aren't comparable. multiplier is hardcoded to match sim.mjs.
  const CONTRACT_MULTIPLIER = 10;
  const anchorSpot = spots[0] ?? 0;
  const notionalPerContract = anchorSpot * CONTRACT_MULTIPLIER;
  return {
    mode,
    seed,
    live: Boolean(live),
    settlement: run.settlement,
    spotSource: run.spotSource.kind,
    rounds: run.history.length,
    events: eventRounds,
    minSpot: Math.min(...spots),
    maxSpot: Math.max(...spots),
    minCurve: Math.min(...curvePrices),
    maxCurve: Math.max(...curvePrices),
    anchorSpot,
    notionalPerContract,
    realizedSum: realized.reduce((a, b) => a + b, 0),
    realizedAbs: realized.reduce((a, b) => a + Math.abs(b), 0),
    byRole: realizedByRole(run.wallets),
    settlementLegs: settlementLegs.length,
    x402Total: run.x402?.total ?? 0,
    deniedWorkers,
  };
}

function fmt(x) {
  return Number.isFinite(x) ? x.toFixed(4) : "n/a";
}
function pct(x) {
  return Number.isFinite(x) ? `${(x * 100).toFixed(0)}%` : "n/a";
}

mkdirSync(OUT, { recursive: true });
const results = [];
for (const mode of modes) {
  for (const seed of seeds) {
    results.push(runOne({ mode, seed }));
  }
}

const byMode = (m) => results.filter((r) => r.mode === m);

const grouped = modes.map((mode) => {
  const runs = byMode(mode);
  return {
    mode,
    runs: runs.length,
    minSpot: Math.min(...runs.map((r) => r.minSpot)),
    maxSpot: Math.max(...runs.map((r) => r.maxSpot)),
    realizedAbsAvg: mean(runs.map((r) => r.realizedAbs)),
    x402Total: runs.reduce((a, r) => a + r.x402Total, 0),
  };
});

// Per-mode distribution of the ANALYST's realized P&L (the value strategy we
// care about), plus role means and a P&L-conservation figure. This is the
// diagnostic layer: it tells us not just that a mode loses, but who loses and
// whether it's a redistribution (sum≈0) or real leakage (sum≠0).
const stats = modes.map((mode) => {
  const runs = byMode(mode);
  const analyst = runs.map((r) => r.byRole.analyst);
  const operator = runs.map((r) => r.byRole.operator);
  const retail = runs.map((r) => r.byRole.retail);
  const conservation = runs.map((r) => r.realizedSum);
  // Analyst P&L in bps of per-contract notional — normalizes across modes whose
  // underlying anchor differs by orders of magnitude (live spread vs synthetic).
  const analystBps = runs
    .map((r) => (r.notionalPerContract > 0 ? (r.byRole.analyst / r.notionalPerContract) * 10_000 : null))
    .filter((x) => x !== null && Number.isFinite(x));
  const anchorMean = mean(runs.map((r) => r.anchorSpot));
  return {
    mode,
    n: runs.length,
    live: runs.some((r) => r.live),
    analyst: { ...ci95(analyst), median: median(analyst), stddev: stddev(analyst), winRate: winRate(analyst) },
    analystBps: analystBps.length ? { ...ci95(analystBps), median: median(analystBps) } : null,
    anchorMean,
    operatorMean: mean(operator),
    retailMean: mean(retail),
    conservationMean: mean(conservation),
  };
});

// Paired synthetic-vs-basket: same seed in both modes, so the per-seed analyst
// difference isolates the basket effect from seed noise. Only when both ran.
let paired = null;
if (USE_PAIR && modes.includes("synthetic") && modes.includes("basket")) {
  const synBySeed = new Map(byMode("synthetic").map((r) => [r.seed, r.byRole.analyst]));
  const diffs = byMode("basket")
    .filter((r) => synBySeed.has(r.seed))
    .map((r) => ({ seed: r.seed, synthetic: synBySeed.get(r.seed), basket: r.byRole.analyst, diff: r.byRole.analyst - synBySeed.get(r.seed) }));
  const dxs = diffs.map((d) => d.diff);
  paired = { pairs: diffs, ...ci95(dxs), winRate: winRate(dxs.map((d) => -d)) };
}

const report = {
  generatedAt: new Date().toISOString(),
  rounds,
  seeds,
  modes,
  live: liveAvailable,
  results,
  grouped,
  stats,
  paired,
};

writeFileSync(join(OUT, "scenario-sweep.json"), JSON.stringify(report, null, 2));

// Long-format CSV: one row per (seed × mode × role). Drop-in input for
// programmatic-eda and any tabular tool. `wallet_sum_pnl` is the renamed
// `realizedSum` — Σ across ALL wallets, NOT the strategy P&L (see
// memory/aeon-compute-futures-experiments).
const CSV_COLS = [
  "seed", "mode", "live", "settlement", "spotSource", "role", "role_pnl",
  "wallet_sum_pnl", "realizedAbs", "minSpot", "maxSpot", "minCurve", "maxCurve",
  "rounds", "settlementLegs", "x402Total", "deniedWorkers",
];
const csvCell = (v) => {
  if (v === null || v === undefined) return "";
  if (typeof v === "string") return `"${v.replace(/"/g, '""')}"`;
  if (typeof v === "boolean") return v ? "true" : "false";
  return String(v);
};
const csvLines = [CSV_COLS.join(",")];
for (const r of results) {
  for (const [role, role_pnl] of Object.entries(r.byRole ?? {})) {
    csvLines.push([
      r.seed, r.mode, r.live, r.settlement, r.spotSource, role, role_pnl,
      r.realizedSum, r.realizedAbs, r.minSpot, r.maxSpot, r.minCurve, r.maxCurve,
      r.rounds, r.settlementLegs, r.x402Total, r.deniedWorkers,
    ].map(csvCell).join(","));
  }
}
writeFileSync(join(OUT, "scenario-sweep.csv"), csvLines.join("\n") + "\n");

const liveSuffix = (mode) => (USE_LIVE && LIVE_MODES.has(mode) && liveAvailable ? " *(live)*" : "");

const md = [
  "# Compute-Futures Scenario Sweep",
  "",
  `Generated: ${report.generatedAt}`,
  `Rounds: ${rounds}`,
  `Seeds (${seeds.length}): ${seeds.join(", ")}`,
  `Live feed: ${liveAvailable ? "OpenRouter snapshot (out/live-prices.json)" : "off — static catalog"}`,
  "",
  "| Mode | Runs | Spot range | Avg abs realized P&L | x402 delivered |",
  "|------|------|------------|----------------------|---------------|",
  ...grouped.map(
    (g) => `| ${g.mode} | ${g.runs} | $${fmt(g.minSpot)}-$${fmt(g.maxSpot)} | $${fmt(g.realizedAbsAvg)} | $${fmt(g.x402Total)} |`,
  ),
  "",
  "## Analyst P&L distribution (the value strategy)",
  "",
  "Mean ± 95% CI (normal approx) of the analyst's realized P&L across seeds; win-rate = share of seeds with analyst P&L > 0.",
  "",
  "| Mode | n | Mean | 95% CI | Median | Stddev | Win-rate |",
  "|------|---|------|--------|--------|--------|----------|",
  ...stats.map(
    (s) =>
      `| ${s.mode}${liveSuffix(s.mode)} | ${s.n} | $${fmt(s.analyst.mean)} | [$${fmt(s.analyst.lo)}, $${fmt(s.analyst.hi)}] | $${fmt(s.analyst.median)} | $${fmt(s.analyst.stddev)} | ${pct(s.analyst.winRate)} |`,
  ),
  "",
  "### Analyst P&L normalized (bps of per-contract notional)",
  "",
  "Raw $ P&L isn't comparable across modes: live spread anchors ~$30/M vs synthetic ~$0.05/M, a ~600× notional gap. The bps figure divides analyst P&L by `anchor_spot × contract_multiplier` so modes can be compared on skill rather than scale. The win-rate column above is already scale-free — use it as the primary signal; bps is the magnitude in comparable units.",
  "",
  "| Mode | Anchor spot | Notional/contract | Analyst (bps) | 95% CI (bps) |",
  "|------|-------------|-------------------|---------------|--------------|",
  ...stats.map((s) => {
    const notional = s.anchorMean * 10;
    const bps = s.analystBps;
    return `| ${s.mode}${liveSuffix(s.mode)} | $${fmt(s.anchorMean)} | $${fmt(notional)} | ${bps ? fmt(bps.mean) : "n/a"} | ${bps ? `[${fmt(bps.lo)}, ${fmt(bps.hi)}]` : "n/a"} |`;
  }),
  "",
  "## Role attribution (mean realized P&L per role)",
  "",
  "Who makes or loses money in each mode. `Σ all` is the sum across all wallets — if it is ~0 the mode is a zero-sum redistribution; a persistent non-zero indicates leakage (e.g. floor-clamp / tick rounding).",
  "",
  "| Mode | Analyst | Operator | Retail | Σ all (conservation) |",
  "|------|---------|----------|--------|----------------------|",
  ...stats.map(
    (s) => `| ${s.mode} | $${fmt(s.analyst.mean)} | $${fmt(s.operatorMean)} | $${fmt(s.retailMean)} | $${fmt(s.conservationMean)} |`,
  ),
  "",
];

if (paired) {
  md.push(
    "## Paired synthetic vs basket (same seeds)",
    "",
    "Per-seed analyst P&L difference (basket − synthetic). Pairing on the seed removes seed noise, so a CI that excludes 0 means the basket spot source itself drives the effect. Win-rate = share of seeds where basket *under*performs synthetic.",
    "",
    `Mean diff (basket − synthetic): **$${fmt(paired.mean)}**  ·  95% CI [$${fmt(paired.lo)}, $${fmt(paired.hi)}]  ·  basket-worse rate ${pct(paired.winRate)}`,
    "",
    "| Seed | Synthetic | Basket | Diff |",
    "|------|-----------|--------|------|",
    ...paired.pairs.map((p) => `| ${p.seed} | $${fmt(p.synthetic)} | $${fmt(p.basket)} | $${fmt(p.diff)} |`),
    "",
  );
}

md.push(
  "## Runs",
  "",
  "| Mode | Seed | Settlement | Spot source | Spot range | Curve range | Legs | Realized sum |",
  "|------|------|------------|-------------|------------|-------------|------|--------------|",
  ...results.map(
    (r) =>
      `| ${r.mode} | ${r.seed} | ${r.settlement} | ${r.spotSource} | $${fmt(r.minSpot)}-$${fmt(r.maxSpot)} | $${fmt(r.minCurve)}-$${fmt(r.maxCurve)} | ${r.settlementLegs} | $${fmt(r.realizedSum)} |`,
  ),
  "",
);

writeFileSync(join(OUT, "scenario-sweep.md"), md.join("\n"));

console.log(`SCENARIO_SWEEP_OK runs=${results.length} live=${liveAvailable} pair=${Boolean(paired)} report=out/scenario-sweep.md csv=out/scenario-sweep.csv`);
