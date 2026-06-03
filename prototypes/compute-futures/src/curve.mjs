// Rendering the thing the demo is about: the futures curve and how it moves.
//
//  • term structure  — futures mid per expiry at a point in time
//  • price series     — a contract's mid over rounds, as an ASCII sparkline
//  • a before/after table around an event, so the pivot is legible in a terminal

import { usd } from "./util.mjs";

const SPARK = "▁▂▃▄▅▆▇█";

export function sparkline(values) {
  const nums = values.filter((v) => v != null);
  if (!nums.length) return "";
  const lo = Math.min(...nums);
  const hi = Math.max(...nums);
  const span = hi - lo || 1;
  return values
    .map((v) => (v == null ? " " : SPARK[Math.round(((v - lo) / span) * (SPARK.length - 1))]))
    .join("");
}

// One row per expiry: the futures mid right now.
export function termStructureTable(snapshot) {
  const rows = snapshot.curve
    .map((c) => `  R${String(c.expiry).padEnd(3)} ${usd(c.price).padStart(9)}`)
    .join("\n");
  return `Term structure @ round ${snapshot.round} (spot ${usd(snapshot.spot)}):\n${rows}`;
}

// Compare the curve immediately before vs a few rounds after an event.
export function beforeAfter(history, event, lag = 3) {
  const before = history.find((h) => h.round === event.round - 1) ?? history[0];
  const after =
    history.find((h) => h.round === event.round + lag) ?? history[history.length - 1];
  const byExpiry = new Map(before.curve.map((c) => [c.expiry, c.price]));
  const rows = after.curve.map((c) => {
    const b = byExpiry.get(c.expiry);
    const chg = b ? ((c.price - b) / b) * 100 : 0;
    const arrow = chg > 0.5 ? "▲" : chg < -0.5 ? "▼" : "→";
    return `  R${String(c.expiry).padEnd(3)} ${usd(b).padStart(9)} ${arrow} ${usd(c.price).padStart(9)}  (${chg >= 0 ? "+" : ""}${chg.toFixed(1)}%)`;
  });
  return [
    `Event @ round ${event.round}: ${event.label}`,
    `  expiry   before        after     change`,
    ...rows,
  ].join("\n");
}

// Per-contract price path as a sparkline, for the whole run.
export function priceSeries(history, symbol) {
  const series = history.map((h) => h.curve.find((c) => c.symbol === symbol)?.price ?? null);
  const vals = series.filter((v) => v != null);
  const lo = vals.length ? Math.min(...vals) : 0;
  const hi = vals.length ? Math.max(...vals) : 0;
  return `  ${symbol.padEnd(16)} ${sparkline(series)}  ${usd(lo)}–${usd(hi)}`;
}
