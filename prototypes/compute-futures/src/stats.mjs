// Small statistics helpers for the scenario sweep — enough to turn a handful of
// seeded runs into a distribution we can reason about (mean, dispersion, a
// confidence band, and a win-rate) plus per-role P&L attribution.

export function mean(xs) {
  if (!xs.length) return NaN;
  return xs.reduce((a, b) => a + b, 0) / xs.length;
}

// Sample standard deviation (n-1). Returns 0 for n < 2.
export function stddev(xs) {
  if (xs.length < 2) return 0;
  const m = mean(xs);
  const variance = xs.reduce((a, b) => a + (b - m) ** 2, 0) / (xs.length - 1);
  return Math.sqrt(variance);
}

export function median(xs) {
  if (!xs.length) return NaN;
  const s = [...xs].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}

// 95% confidence interval on the mean (normal approximation: mean ± 1.96·SE).
// Approximate for small n — the sweep labels it as such. Returns the half-width
// (margin) alongside lo/hi so callers can render "mean ± margin".
export function ci95(xs) {
  const m = mean(xs);
  const se = xs.length ? stddev(xs) / Math.sqrt(xs.length) : NaN;
  const margin = 1.96 * se;
  return { mean: m, margin, lo: m - margin, hi: m + margin, n: xs.length };
}

// Fraction of samples strictly greater than 0.
export function winRate(xs) {
  if (!xs.length) return NaN;
  return xs.filter((x) => x > 0).length / xs.length;
}

// Map a wallet's label to a market role. Labels come from sim.mjs:
//   "researcher (analyst)", "deployer (GPU operator)", "retail-N", "demand-escrow".
export function roleOf(label = "") {
  if (label.includes("(analyst)")) return "analyst";
  if (label.includes("GPU operator")) return "operator";
  if (label.startsWith("retail")) return "retail";
  if (label.includes("escrow")) return "escrow";
  return "other";
}

// Sum realized P&L per role for one run's wallets. Escrow is excluded from the
// totals (it's the x402 demand-side float, not a market participant).
export function realizedByRole(wallets = []) {
  const by = { analyst: 0, operator: 0, retail: 0 };
  for (const w of wallets) {
    const role = roleOf(w.label);
    if (role === "escrow" || role === "other") continue;
    by[role] += w.realized ?? 0;
  }
  return by;
}
