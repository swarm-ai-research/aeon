// Conservation regression — every settled round must produce a wallet P&L sum
// at or near zero across all modes. Net non-zero is "the dollars went somewhere
// we didn't account for", which is the class of bug B was designed to make
// structurally impossible.
//
// Today (pre-Proposal B) this test fails: the wallet-walk derivation of P&L
// leaves ~10-19% of |realizedAbs| as residual across every mode. Once the
// Settlement-primitives refactor lands (Proposal B from
// `autoresearch-goal` run on `improve compute-futures prototype`), every
// credit/debit is recorded as an explicit SettlementEvent and Σ events == 0
// per round becomes structural. At that point this test passes and the skip
// flag below comes off.
//
// Why TDD on this: the test is what we're trying to make true. Writing it
// strict-and-skipped is the canary for the refactor — when it passes
// unmodified, the refactor's done its job.

import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
// Isolated out dir per test file so parallel test files (market.test.mjs etc.)
// don't race on out/last-run.json. Sim respects $COMPUTE_FUTURES_OUT_DIR.
const TEST_OUT = mkdtempSync(join(tmpdir(), "cf-conservation-"));
process.on("exit", () => rmSync(TEST_OUT, { recursive: true, force: true }));

const MODES = [
  { name: "synthetic", args: [] },
  { name: "basket", args: ["--basket"] },
  { name: "spread", args: ["--spread"] },
  { name: "x402", args: ["--x402"] },
];

const TOLERANCE_USD = 1.0; // ~$1 across the full run, not per round

function runSim(extraArgs, seed = 101) {
  const res = spawnSync(
    process.execPath,
    ["sim.mjs", ...extraArgs, "--seed", String(seed), "--rounds", "20"],
    {
      cwd: ROOT,
      encoding: "utf8",
      timeout: 30_000,
      env: { ...process.env, COMPUTE_FUTURES_OUT_DIR: TEST_OUT },
    },
  );
  assert.equal(res.status, 0, `sim exited ${res.status}: ${(res.stderr || res.stdout).slice(0, 400)}`);
  return JSON.parse(readFileSync(join(TEST_OUT, "last-run.json"), "utf8"));
}

function walletSum(run) {
  return run.wallets.reduce((s, w) => s + (w.realized ?? 0), 0);
}

// Strict conservation across all wallets (including the house). With the
// paired-event refactor every credit is balanced by an offsetting house
// debit, so Σ realized is structurally 0 modulo float precision.
for (const mode of MODES) {
  test(`conservation: Σ wallet.realized ≈ 0 in ${mode.name} mode`, () => {
    const run = runSim(mode.args);
    const sum = walletSum(run);
    const realizedAbs = run.wallets.reduce((s, w) => s + Math.abs(w.realized ?? 0), 0);
    assert.ok(
      Math.abs(sum) <= TOLERANCE_USD,
      `${mode.name}: Σ realized = ${sum.toFixed(4)} (|realizedAbs|=${realizedAbs.toFixed(2)}, tolerance=±$${TOLERANCE_USD})`,
    );
  });
}

// Structural conservation on the event log itself: Σ events.amount == 0
// per run, by construction (every event is paired with a house offset).
for (const mode of MODES) {
  test(`conservation: Σ clearinghouse.events == 0 in ${mode.name} mode`, () => {
    const run = runSim(mode.args);
    const eventSum = (run.clearinghouse?.events ?? []).reduce((s, e) => s + e.amount, 0);
    assert.ok(
      Math.abs(eventSum) < 1e-9,
      `${mode.name}: Σ events.amount = ${eventSum} — should be 0 by construction. A code path is creating unpaired events.`,
    );
  });
}

// Non-house wallet drift — Σ realized across the TRADERS (analyst, operator,
// retail, escrow) excluding the house. This is what wallet_sum_pnl in the
// scenario-sweep CSV reports today. Pre-refactor, drift bands were ±$50 to
// ±$3000 by mode; post-refactor the house absorbs the imbalance, so non-house
// drift equals the (negated) house realized. The band here only catches
// catastrophic regressions — for sub-cent precision, use the strict tests above.
const NONHOUSE_TOLERANCE = {
  synthetic: 50,
  basket: 100,
  spread: 3000,
  x402: 50,
};

for (const mode of MODES) {
  test(`baseline: non-house drift in ${mode.name} stays within known band`, () => {
    const run = runSim(mode.args);
    const nonHouseSum = run.wallets
      .filter((w) => w.label !== "clearinghouse-house")
      .reduce((s, w) => s + (w.realized ?? 0), 0);
    const bound = NONHOUSE_TOLERANCE[mode.name];
    assert.ok(
      Math.abs(nonHouseSum) <= bound,
      `${mode.name}: non-house Σ realized = ${nonHouseSum.toFixed(4)}, exceeds known band ±$${bound}.`,
    );
  });
}

// Event log round-trip: Σ events.amount == Σ wallet.realized. With paired
// events this is two ways of saying the same thing (both are structurally 0),
// but keep the test so a future code path that bypasses #recordEvent and
// directly mutates `wallet.realized` would be caught.
for (const mode of MODES) {
  test(`event log: Σ clearinghouse.events == Σ wallet.realized in ${mode.name} mode`, () => {
    const run = runSim(mode.args);
    const eventSum = (run.clearinghouse?.events ?? []).reduce((s, e) => s + e.amount, 0);
    const walletRealized = walletSum(run);
    assert.ok(
      Math.abs(eventSum - walletRealized) < 1e-6,
      `${mode.name}: event log Σ=${eventSum.toFixed(4)} vs wallet Σ realized=${walletRealized.toFixed(4)} — a P&L path is bypassing the event log`,
    );
  });
}
