// SpreadIndex — a DERIVED index whose value is the difference between two base
// spot indices. With two Darkbloom basket indices (frontier and commodity), the
// spread IS the "frontier premium": how much more frontier-quality inference
// costs than commodity inference per M-tokens.
//
// Trading the spread trades a thesis — premium COMPRESSION or EXPANSION — rather
// than the absolute price level. The prototype's own Compute Pulse logs track
// this premium compressing (GPT-4-class down ~280x in 2y as open weights catch
// up), which is exactly what a short-the-premium position expresses.
//
// It is derived: events shock the BASE indices directly; the spread just reads
// `long.price - short.price`. So it exposes the same fields the market reads
// (price, fundamental, history, applyShock, step) but applyShock is a no-op and
// step only records history. Construct it AFTER its bases and list it LAST in
// the spotIndices array so its history is recorded after the bases have stepped.

export class SpreadIndex {
  constructor({ symbol, underlying, long, short, next }) {
    this.symbol = symbol ?? underlying;
    this.underlying = underlying; // e.g. "FRONTIER-PREMIUM"
    this.long = long; // the dearer leg (frontier basket)
    this.short = short; // the cheaper leg (commodity basket)
    this.next = next;
    this.floor = -Infinity; // a spread may legitimately go negative
    this.history = [this.price];
  }

  // Live difference of the two legs — recomputed on read, so it always reflects
  // the current (possibly shocked, possibly stepped) base prices.
  get price() {
    return this.long.price - this.short.price;
  }

  // Fair value of the spread = difference of the legs' marginal-cost anchors.
  get fundamental() {
    return this.long.fundamental - this.short.fundamental;
  }

  // Derived: shocks are applied to the base indices, never to the spread.
  applyShock() {}

  // No stochastic process of its own — just record the post-step spread so the
  // sparkline/price path can be drawn.
  step() {
    this.history.push(this.price);
    return this.price;
  }
}
