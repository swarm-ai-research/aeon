import assert from "node:assert/strict";
import { test } from "node:test";

import { ci95, mean, median, realizedByRole, roleOf, stddev, winRate } from "../src/stats.mjs";

test("mean / median / stddev", () => {
  assert.equal(mean([2, 4, 6]), 4);
  assert.equal(median([3, 1, 2]), 2);
  assert.equal(median([1, 2, 3, 4]), 2.5);
  assert.ok(Math.abs(stddev([2, 4, 6]) - 2) < 1e-12); // sample stddev
  assert.equal(stddev([5]), 0);
});

test("ci95 returns a symmetric band around the mean", () => {
  const { mean: m, lo, hi, margin, n } = ci95([10, 12, 14, 16]);
  assert.equal(m, 13);
  assert.equal(n, 4);
  assert.ok(margin > 0);
  assert.ok(Math.abs((hi - lo) / 2 - margin) < 1e-12);
  assert.ok(lo < m && m < hi);
});

test("winRate counts strictly positive samples", () => {
  assert.equal(winRate([1, -1, 2, 0]), 0.5); // 0 does not count as a win
  assert.equal(winRate([-1, -2]), 0);
});

test("roleOf classifies sim wallet labels", () => {
  assert.equal(roleOf("researcher (analyst)"), "analyst");
  assert.equal(roleOf("deployer (GPU operator)"), "operator");
  assert.equal(roleOf("retail-7"), "retail");
  assert.equal(roleOf("demand-escrow"), "escrow");
});

test("realizedByRole sums per role and excludes escrow", () => {
  const by = realizedByRole([
    { label: "researcher (analyst)", realized: 5 },
    { label: "deployer (GPU operator)", realized: -8 },
    { label: "retail-1", realized: 1 },
    { label: "retail-2", realized: 2 },
    { label: "demand-escrow", realized: 999 },
  ]);
  assert.deepEqual(by, { analyst: 5, operator: -8, retail: 3 });
});
