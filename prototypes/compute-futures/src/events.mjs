// The event feed — the headline-driven side MiroShark is built for. Each event
// lands at a round, shifts the marginal cost of compute (so the futures curve
// has a new fair value), and hands the retail swarm a sentiment impulse so it
// over-reacts. The fleet's analyst trades the gap back toward fair.
//
// `factor` multiplies the spot fundamental: > 1 = supply crunch / demand surge
// (price up), < 1 = supply glut / efficiency gain (price down). `impulse` is
// the same-signed sentiment kick to retail (over-reaction).

export const DEFAULT_EVENTS = [
  {
    round: 6,
    label: "Hyperscaler reserves H100 capacity — spot supply tightens",
    factor: 1.8,
    impulse: 0.5,
  },
  {
    round: 13,
    label: "DeepSeek V3.2 open-weights drop — efficient inference floods supply",
    factor: 0.55,
    impulse: -0.6,
  },
  {
    round: 20,
    label: "Agent platform onboards 10k agents — inference demand surges",
    factor: 1.5,
    impulse: 0.45,
  },
];

// Spread-mode events shock the two basket legs DIFFERENTLY (via `factors` keyed
// by underlying), so the frontier premium moves — the whole point of the spread.
// A leg with no entry in `factors` is left unshocked (factor 1).
export const SPREAD_EVENTS = [
  {
    round: 6,
    label: "Frontier price war (Opus-distilled undercut) — premium compresses",
    factors: { FRONTIER: 0.7 },
    impulse: -0.4,
  },
  {
    round: 13,
    label: "Open-weights commodity glut — commodity leg craters, premium widens",
    factors: { "LLAMA-INFER": 0.55 },
    impulse: 0.5,
  },
  {
    round: 20,
    label: "Agents demand frontier quality — frontier bid up, premium widens",
    factors: { FRONTIER: 1.45 },
    impulse: 0.45,
  },
  // Balance the widener/compressor mix: without this, 2 wideners + 1 compressor
  // give the spread net positive drift over the run, and a mean-reversion strategy
  // (the analyst) loses systematically. Round 26 leaves ~4 rounds for the legs
  // to mean-revert before the last expiry, matching the round-6 pattern.
  {
    round: 26,
    label: "Open-source frontier breakthrough — frontier leg cracks, premium compresses",
    factors: { FRONTIER: 0.75 },
    impulse: -0.35,
  },
];

export class EventFeed {
  constructor(events = DEFAULT_EVENTS) {
    this.byRound = new Map(events.map((e) => [e.round, e]));
    this.fired = [];
  }

  // Returns the event firing this round (or null). Applies its shock to the
  // matching spot indices; the caller propagates the sentiment impulse. Supports
  // a per-underlying `factors` map (spread mode) falling back to a single
  // `factor` (default mode), and 1 (no shock) if neither is present.
  fire(round, spotIndices) {
    const e = this.byRound.get(round);
    if (!e) return null;
    for (const idx of spotIndices) {
      const f = e.factors && e.factors[idx.underlying] !== undefined ? e.factors[idx.underlying] : e.factor ?? 1;
      idx.applyShock(f);
    }
    this.fired.push({ round, ...e });
    return e;
  }
}
