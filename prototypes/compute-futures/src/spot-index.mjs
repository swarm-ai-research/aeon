// The spot price of inference compute, $/M-tokens — the underlying our futures
// settle against. This is exactly what usepod is: a real-time SPOT market for
// inference, where price converges toward marginal cost (~$0.05/M for commodity
// open-weight models, ~$2–15/M for frontier). We don't reinvent that; we treat
// usepod's spot as the settlement index and build the FUTURES layer on top.
//
// Price tracks a "fundamental" (marginal cost given supply/demand) with mean
// reversion plus noise. Events move the fundamental — that's what the agents
// trade on, and what makes the futures curve shift.

import { gauss, clamp } from "./util.mjs";

export class SpotIndex {
  constructor({ symbol, underlying, price, floor, next }) {
    this.symbol = symbol;
    this.underlying = underlying; // "LLAMA-INFER" | "FRONTIER"
    this.price = price; // current spot, $/M-tokens
    this.fundamental = price; // marginal-cost anchor it reverts toward
    this.floor = floor; // hard marginal-cost floor (can't go negative/near-zero)
    this.next = next; // seeded PRNG
    this.history = [price];
  }

  // An event shifts the marginal cost: factor > 1 = supply crunch / demand
  // surge (price up), factor < 1 = supply glut / efficiency gain (price down).
  applyShock(factor) {
    this.fundamental = Math.max(this.floor, this.fundamental * factor);
  }

  // Advance one round: revert toward fundamental, add multiplicative noise.
  step({ reversion = 0.2, vol = 0.035 } = {}) {
    const drift = reversion * (this.fundamental - this.price);
    const shock = this.price * gauss(this.next, 0, vol);
    this.price = clamp(this.price + drift + shock, this.floor, this.fundamental * 8);
    this.history.push(this.price);
    return this.price;
  }
}
