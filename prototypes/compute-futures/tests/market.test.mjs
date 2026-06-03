import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { Contract, expirySchedule } from "../src/contract.mjs";
import { basketPrice, DarkbloomBasketIndex } from "../src/darkbloom.mjs";
import { SurplusSpotIndex, SurplusBasketIndex, referenceModel, SURPLUS_X402, readCachedSurplusPrices } from "../src/surplus.mjs";
import { OrderBook } from "../src/orderbook.mjs";
import { Clearinghouse } from "../src/clearinghouse.mjs";
import { SpreadIndex } from "../src/spread.mjs";
import { SpotIndex } from "../src/spot-index.mjs";
import { WalletBook } from "../src/wallet.mjs";
import { rng } from "../src/util.mjs";

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
// Isolated out dir so parallel test files (conservation.test.mjs etc.) don't
// race on out/last-run.json. Sim respects $COMPUTE_FUTURES_OUT_DIR — same
// pattern conservation.test.mjs uses; without this, `node --test tests/`
// surfaces races where one test reads another test's stale sim output.
const TEST_OUT = mkdtempSync(join(tmpdir(), "cf-market-"));
process.on("exit", () => rmSync(TEST_OUT, { recursive: true, force: true }));
const SIM_ENV = { ...process.env, COMPUTE_FUTURES_OUT_DIR: TEST_OUT };

test("basketPrice normalizes relative weights and rejects bad baskets", () => {
  const { price, components } = basketPrice({ "gemma-4-26b": 3, "minimax-m2.5": 1 });
  assert.equal(components["gemma-4-26b"].weight, 0.75);
  assert.equal(components["minimax-m2.5"].weight, 0.25);
  assert.ok(price > components["gemma-4-26b"].price);
  assert.ok(price < components["minimax-m2.5"].price);
  assert.throws(() => basketPrice({ "gemma-4-26b": 0 }), /positive/);
  assert.throws(() => basketPrice({ missing: 1 }), /unknown model/);
});

test("SpreadIndex derives from legs and records post-step history", () => {
  const next = rng(7);
  const long = new SpotIndex({ symbol: "FRONTIER", underlying: "FRONTIER", price: 0.30, floor: 0.05, next });
  const short = new SpotIndex({ symbol: "COMMODITY", underlying: "LLAMA-INFER", price: 0.10, floor: 0.02, next });
  const spread = new SpreadIndex({ underlying: "FRONTIER-PREMIUM", long, short, next });
  assert.ok(Math.abs(spread.price - 0.20) < 1e-12);
  spread.applyShock(99);
  assert.ok(Math.abs(spread.price - 0.20) < 1e-12);
  long.applyShock(0.5);
  long.step({ reversion: 1, vol: 0 });
  short.step({ reversion: 1, vol: 0 });
  spread.step();
  assert.equal(spread.history.at(-1), spread.price);
  assert.ok(spread.price < 0.20);
});

test("OrderBook respects price-time priority and resting-price execution", () => {
  const contract = new Contract({ underlying: "LLAMA-INFER", expiryRound: 8, tick: 0.0005 });
  const book = new OrderBook(contract);
  book.submit({ did: "seller-a", side: "sell", qty: 2, price: 0.0500 });
  book.submit({ did: "seller-b", side: "sell", qty: 2, price: 0.0495 });
  const trades = book.submit({ did: "buyer", side: "buy", qty: 3, price: 0.0600 });
  assert.deepEqual(
    trades.map((t) => [t.seller, t.qty, t.price]),
    [
      ["seller-b", 2, 0.0495],
      ["seller-a", 1, 0.05],
    ],
  );
  assert.equal(book.bestAsk(), 0.05);
});

test("expirySchedule extends past custom run horizons", () => {
  assert.deepEqual(expirySchedule(12), [8, 16, 24, 30]);
  assert.deepEqual(expirySchedule(30), [8, 16, 24, 30, 38]);
  assert.deepEqual(expirySchedule(60), [8, 16, 24, 30, 38, 46, 54, 62]);
});

test("Clearinghouse settlement is zero-sum across futures P&L", () => {
  const wallets = new WalletBook();
  wallets.open({ did: "long", label: "long", cash: 100 });
  wallets.open({ did: "short", label: "short", cash: 100 });
  const contract = new Contract({ underlying: "LLAMA-INFER", expiryRound: 8, multiplier: 10 });
  const clearing = new Clearinghouse({ wallets });
  clearing.recordTrade(contract, { buyer: "long", seller: "short", qty: 4, price: 0.05 });
  clearing.markToMarket({ [contract.symbol]: 0.06 });
  const settlement = clearing.settle(contract, 0.08);
  const pnl = settlement.legs.reduce((sum, leg) => sum + leg.pnl, 0);
  assert.ok(Math.abs(pnl) < 1e-9);
  assert.equal(clearing.openInterest(contract.symbol), 0);
  assert.equal(wallets.get("long").realized, -wallets.get("short").realized);
});

test("DarkbloomBasketIndex can partially rebase from a live feed", async () => {
  const idx = new DarkbloomBasketIndex({ underlying: "LLAMA-INFER", next: rng(9), basket: "commodity" });
  const before = idx.price;
  const floorBefore = idx.floor;
  const dataUrl = `data:application/json,${encodeURIComponent(JSON.stringify({ models: { "gemma-4-26b": { input: 0.2, output: 0.4 } } }))}`;
  const refreshed = await idx.refreshLive(dataUrl);
  assert.equal(refreshed, true);
  assert.notEqual(idx.price, before);
  assert.equal(idx.history.length, 1);
  // refreshLive must keep the floor consistent with the live catalog (a
  // partial rebase may leave floor unchanged if the cheapest basket member
  // wasn't in the live feed, but the floor must never exceed the live price).
  assert.ok(idx.floor <= idx.price, `floor (${idx.floor}) should not exceed live price (${idx.price})`);
  assert.ok(Number.isFinite(idx.floor) && idx.floor > 0, `floor ${idx.floor} (was ${floorBefore}) must be finite`);
});

test("DarkbloomBasketIndex floor tracks a frontier rebase (no static-catalog lag)", async () => {
  const idx = new DarkbloomBasketIndex({ underlying: "FRONTIER", next: rng(11), basket: "frontier" });
  const fundamentalBefore = idx.fundamental;
  const floorBefore = idx.floor;
  // Simulate OpenRouter live anchors ~$30/M input across all frontier members —
  // the exact scenario PR #105 noted as making the static ~$0.10 floor stale.
  const liveModels = Object.fromEntries(Object.keys(idx.weights).map((id) => [id, { input: 30, output: 60 }]));
  const dataUrl = `data:application/json,${encodeURIComponent(JSON.stringify({ models: liveModels }))}`;
  const refreshed = await idx.refreshLive(dataUrl);
  assert.equal(refreshed, true);
  assert.ok(idx.fundamental > fundamentalBefore * 10, "fundamental should jump on live rebase");
  assert.ok(idx.floor > floorBefore * 10, `floor should rebase too, got ${idx.floor} (was ${floorBefore})`);
  // Sanity invariant: after live rebase, floor/fundamental ratio is bounded —
  // catches future drift where one moves and the other doesn't.
  assert.ok(idx.fundamental < idx.floor * 100, `floor (${idx.floor}) should stay within 100× of fundamental (${idx.fundamental})`);
});

test("DarkbloomSpotIndex refreshLive rebases the marginal-cost floor", async () => {
  const { DarkbloomSpotIndex } = await import("../src/darkbloom.mjs");
  const idx = new DarkbloomSpotIndex({ underlying: "FRONTIER", next: rng(13) });
  const floorBefore = idx.floor;
  const dataUrl = `data:application/json,${encodeURIComponent(JSON.stringify({ models: { [idx.modelId]: { input: 30, output: 60 } } }))}`;
  const refreshed = await idx.refreshLive(dataUrl);
  assert.equal(refreshed, true);
  assert.ok(idx.floor > floorBefore * 10, `floor should rebase on live update, got ${idx.floor} (was ${floorBefore})`);
});

test("sim CLI accepts seed and emits stable run history", () => {
  const res = spawnSync(process.execPath, ["sim.mjs", "--basket", "--seed", "123", "--rounds", "12"], {
    cwd: ROOT,
    encoding: "utf8",
    timeout: 20_000,
    env: SIM_ENV,
  });
  assert.equal(res.status, 0, res.stderr);
  assert.match(res.stdout, /seed: 123/);
  const run = JSON.parse(readFileSync(join(TEST_OUT, "last-run.json"), "utf8"));
  assert.equal(run.seed, 123);
  assert.equal(run.history.length, 12);
  assert.equal(run.spotSource.kind, "darkbloom-basket");
  assert.equal(run.history.flatMap((h) => h.dispatch.results.filter((r) => !r.ok)).length, 0);
  assert.ok(run.history.some((h) => h.settlements.length));
});

test("sim CLI extends term structure for long custom horizons", () => {
  const res = spawnSync(process.execPath, ["sim.mjs", "--seed", "123", "--rounds", "60"], {
    cwd: ROOT,
    encoding: "utf8",
    timeout: 20_000,
    env: SIM_ENV,
  });
  assert.equal(res.status, 0, res.stderr);
  assert.match(res.stdout, /expiries: 8, 16, 24, 30, 38, 46, 54, 62/);
  const run = JSON.parse(readFileSync(join(TEST_OUT, "last-run.json"), "utf8"));
  assert.equal(run.history.length, 60);
  assert.equal(run.history.flatMap((h) => h.dispatch.results.filter((r) => !r.ok)).length, 0);
  assert.ok(run.history.at(-1).curve.length > 0);
});

test("SurplusSpotIndex anchors to the reference model and re-bases from a live feed", async () => {
  const idx = new SurplusSpotIndex({ underlying: "LLAMA-INFER", next: rng(7) });
  const { id, model } = referenceModel("LLAMA-INFER");
  assert.equal(idx.modelId, id);
  // Anchor = the default 3:1 input:output blend of the reference model.
  const expected = (model.input * 3 + model.output * 1) / 4;
  assert.ok(Math.abs(idx.price - expected) < 1e-12);

  const before = idx.price;
  const dataUrl = `data:application/json,${encodeURIComponent(JSON.stringify({ models: { [id]: { input: 0.5, output: 1.5 } } }))}`;
  const refreshed = await idx.refreshLive(dataUrl);
  assert.equal(refreshed, true);
  assert.notEqual(idx.price, before);
  assert.equal(idx.history.length, 1);
  // A live feed that doesn't mention our model leaves the index untouched.
  const miss = await idx.refreshLive(`data:application/json,${encodeURIComponent(JSON.stringify({ models: { "other-model": { input: 1, output: 2 } } }))}`);
  assert.equal(miss, false);
});

test("SurplusBasketIndex partially re-bases from a live feed and SURPLUS_X402 is on Base/USDC", async () => {
  const idx = new SurplusBasketIndex({ underlying: "LLAMA-INFER", next: rng(11), basket: "commodity" });
  const before = idx.price;
  const dataUrl = `data:application/json,${encodeURIComponent(JSON.stringify({ models: { "llama-4-scout": { input: 0.3, output: 0.6 } } }))}`;
  const refreshed = await idx.refreshLive(dataUrl);
  assert.equal(refreshed, true);
  assert.notEqual(idx.price, before);
  // The real x402 rail metadata: Base mainnet, USDC, OpenAI-compatible endpoint.
  assert.equal(SURPLUS_X402.network, "eip155:8453");
  assert.equal(SURPLUS_X402.asset, "USDC");
  assert.match(SURPLUS_X402.resource, /surplusintelligence\.ai\/x402\//);
});

test("readCachedSurplusPrices parses the prefetch cache file and ignores junk", () => {
  const dir = mkdtempSync(join(tmpdir(), "surplus-cache-"));
  try {
    const file = join(dir, "prices.json");
    writeFileSync(
      file,
      JSON.stringify({ models: { "llama-4-scout": { input: 0.1, output: 0.3 }, bad: { input: "x", output: 1 } } }),
    );
    assert.deepEqual(readCachedSurplusPrices(file), { "llama-4-scout": { input: 0.1, output: 0.3 } });
    // OpenAI-style list form is also accepted.
    const listFile = join(dir, "list.json");
    writeFileSync(listFile, JSON.stringify({ data: [{ id: "deepseek-v4", input: 0.2, output: 0.8 }] }));
    assert.deepEqual(readCachedSurplusPrices(listFile), { "deepseek-v4": { input: 0.2, output: 0.8 } });
    // Missing file → null, never throws.
    assert.equal(readCachedSurplusPrices(join(dir, "nope.json")), null);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("sim CLI accepts --surplus and records the surplus spot source", () => {
  const res = spawnSync(process.execPath, ["sim.mjs", "--surplus", "--seed", "321", "--rounds", "12"], {
    cwd: ROOT,
    encoding: "utf8",
    timeout: 20_000,
    env: SIM_ENV,
  });
  assert.equal(res.status, 0, res.stderr);
  assert.match(res.stdout, /spot source: surplus/);
  const run = JSON.parse(readFileSync(join(TEST_OUT, "last-run.json"), "utf8"));
  assert.equal(run.spotSource.kind, "surplus");
  assert.equal(run.history.length, 12);
  assert.equal(run.history.flatMap((h) => h.dispatch.results.filter((r) => !r.ok)).length, 0);
});
