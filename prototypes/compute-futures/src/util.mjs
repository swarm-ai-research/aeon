// Tiny shared helpers: a seeded PRNG (so every run is reproducible, like the
// gitlawb-safety demos) and number/format utilities.

// mulberry32 — deterministic, seedable, good enough for a simulation.
export function rng(seed = 0x9e3779b9) {
  let a = seed >>> 0;
  return function next() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Box–Muller normal from a uniform generator.
export function gauss(next, mean = 0, sd = 1) {
  let u = 0;
  let v = 0;
  while (u === 0) u = next();
  while (v === 0) v = next();
  return mean + sd * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

export function clamp(x, lo, hi) {
  return Math.max(lo, Math.min(hi, x));
}

// $/M-tokens are small; show enough precision to see the curve move.
export function usd(x) {
  if (x == null || Number.isNaN(x)) return "—";
  if (Math.abs(x) >= 1) return `$${x.toFixed(2)}`;
  return `$${x.toFixed(4)}`;
}

export function round2(x) {
  return Math.round(x * 100) / 100;
}
