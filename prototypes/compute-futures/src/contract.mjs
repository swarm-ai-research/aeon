// A compute-futures contract: an agreement to settle a quantity of inference
// compute (priced in $/M-tokens) at a future round. Cash-settled by default
// against the SpotIndex at expiry; optionally physically settled — the short
// (a GPU operator) delivers inference and is paid per-M-token via x402.

export class Contract {
  constructor({ underlying, expiryRound, multiplier = 1, tick = 0.0005 }) {
    this.underlying = underlying; // "LLAMA-INFER"
    this.expiryRound = expiryRound; // round at which it settles
    this.multiplier = multiplier; // M-tokens of compute per contract
    this.tick = tick; // minimum price increment ($/M-tokens)
    this.symbol = `${underlying}-R${expiryRound}`;
  }

  roundToTick(price) {
    return Math.round(price / this.tick) * this.tick;
  }

  // Notional value of one contract at a given price.
  notional(price) {
    return price * this.multiplier;
  }
}

// Build a term structure: the same underlying at several expiries. A real desk
// trades the whole curve; the demo watches it pivot when an event lands.
export function termStructure(underlying, expiries, opts = {}) {
  return expiries.map((expiryRound) => new Contract({ underlying, expiryRound, ...opts }));
}

// Default demo expiries preserve the original curve. Longer simulations extend
// the ladder by 8-round tenors until at least one contract remains active after
// the final requested round; otherwise retail quote fallback sees no contracts.
export function expirySchedule(rounds, { base = [8, 16, 24, 30], step = 8 } = {}) {
  if (!Number.isFinite(rounds) || rounds <= 0) throw new Error("rounds must be a positive number");
  const expiries = [...base].sort((a, b) => a - b);
  while (expiries.at(-1) <= rounds) expiries.push(expiries.at(-1) + step);
  return expiries;
}
