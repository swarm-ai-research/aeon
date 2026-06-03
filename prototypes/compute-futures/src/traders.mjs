// Market participants. The GitLawb fleet plays the named institutional roles;
// a generated population of retail agents (the MiroShark-style swarm) supplies
// the noise and the over-reaction that creates mispricing for the fleet to
// trade against.
//
// Each trader exposes quote(ctx) -> orders[]. ctx gives a reference price per
// contract and the *public* fundamental (what an event has revealed about
// marginal cost). Strategies are deterministic given the seeded PRNG, so a run
// reproduces exactly — same discipline as the gitlawb-safety demos.

import { gauss, clamp } from "./util.mjs";
import { TRUST_TIER, reputationScore, DEFAULT_PROFILE } from "./credit.mjs";

const ROLE = {
  ANALYST: "analyst", // researcher — rational value trader (corrects mispricing)
  OPERATOR: "operator-seller", // deployer — GPU operator hedging future capacity (sells)
  RETAIL: "retail", // MiroShark swarm — sentiment / momentum noise traders
};

// Default counterparty credit by role (Darkbloom trust tier + reputation). The
// GPU operator is a hardware-attested provider with a strong delivery record;
// the analyst is an institution; retail is self-attested and average.
const ROLE_CREDIT = {
  [ROLE.ANALYST]: { tier: TRUST_TIER.HARDWARE, reputation: 0.95 },
  [ROLE.OPERATOR]: {
    tier: TRUST_TIER.HARDWARE,
    reputation: reputationScore({ jobSuccess: 0.95, uptime: 0.9, challengeResp: 0.95, responseTime: 0.85 }),
  },
  [ROLE.RETAIL]: { tier: TRUST_TIER.SELF_SIGNED, reputation: 0.5 },
};

export class Trader {
  constructor({ identity, role, label, capacity = 0, credit }) {
    this.identity = identity;
    this.did = identity.did;
    this.role = role;
    this.label = label;
    this.capacity = capacity; // GPU operators: M-token contracts they can sell
    this.sentiment = 0; // retail: drifting belief in [-1, 1]
    this.credit = credit ?? ROLE_CREDIT[role] ?? DEFAULT_PROFILE; // counterparty trust profile
  }

  quote(ctx) {
    if (this.role === ROLE.ANALYST) return this.#analyst(ctx);
    if (this.role === ROLE.OPERATOR) return this.#operator(ctx);
    if (this.role === ROLE.RETAIL) return this.#retail(ctx);
    return [];
  }

  // Researcher: estimate fair value (= public fundamental, no carry) and trade
  // toward it. Takes liquidity when the book is clearly mispriced; otherwise
  // provides a tight two-sided quote around fair.
  #analyst(ctx) {
    const orders = [];
    const edge = 0.03;
    for (const c of ctx.contracts) {
      const fair = ctx.fundamental(c.underlying);
      const ref = ctx.reference(c.symbol) ?? fair;
      const dev = (ref - fair) / fair;
      if (dev < -edge) {
        const qty = clamp(Math.round(Math.abs(dev) * 40), 1, 8);
        orders.push({ did: this.did, contract: c, side: "buy", qty, price: fair * 0.998 });
      } else if (dev > edge) {
        const qty = clamp(Math.round(Math.abs(dev) * 40), 1, 8);
        orders.push({ did: this.did, contract: c, side: "sell", qty, price: fair * 1.002 });
      } else {
        orders.push({ did: this.did, contract: c, side: "buy", qty: 1, price: fair * 0.985 });
        orders.push({ did: this.did, contract: c, side: "sell", qty: 1, price: fair * 1.015 });
      }
    }
    return orders;
  }

  // GPU operator: hedge future capacity by selling forward — persistent ask
  // supply a touch above the reference, sized by available capacity. Sells more
  // willingly when prices are rich relative to its cost (the fundamental).
  #operator(ctx) {
    const orders = [];
    for (const c of ctx.contracts) {
      const fair = ctx.fundamental(c.underlying); // the operator's marginal cost
      const ref = ctx.reference(c.symbol) ?? fair;
      const rich = ref > fair ? 1.4 : 0.8; // sell more when the curve is rich
      const qty = clamp(Math.round((this.capacity / ctx.contracts.length) * rich), 1, this.capacity);
      // Offers are anchored to cost (a touch above), not to a stale last price,
      // so supply re-prices the moment an event moves the operator's cost.
      orders.push({ did: this.did, contract: c, side: "sell", qty, price: fair * 1.01 });
    }
    return orders;
  }

  // Retail swarm: sentiment drifts, over-reacts to events (momentum), and
  // quotes around the reference biased by belief. This is the inefficiency the
  // fleet's analyst arbitrages.
  #retail(ctx) {
    this.sentiment = clamp(
      this.sentiment * 0.7 + gauss(ctx.next, 0, 0.3) + ctx.eventImpulse,
      -1,
      1,
    );
    const orders = [];
    const picks = ctx.contracts.filter(() => ctx.next() < 0.6);
    for (const c of picks.length ? picks : [ctx.contracts[0]]) {
      const ref = ctx.reference(c.symbol) ?? ctx.fundamental(c.underlying);
      const bias = 1 + this.sentiment * 0.08 + gauss(ctx.next, 0, 0.012);
      const side = this.sentiment >= 0 ? "buy" : "sell";
      const qty = 1 + Math.floor(ctx.next() * 3);
      orders.push({ did: this.did, contract: c, side, qty, price: ref * bias });
    }
    return orders;
  }
}

export { ROLE };

// Build the retail population (MiroShark-style swarm).
export function makeRetail({ count, makeIdentity, wallets, startCash, next }) {
  const traders = [];
  for (let i = 0; i < count; i++) {
    const identity = makeIdentity(`retail-${i + 1}`);
    wallets.open({ did: identity.did, label: `retail-${i + 1}`, cash: startCash });
    const t = new Trader({ identity, role: ROLE.RETAIL, label: `retail-${i + 1}` });
    t.sentiment = gauss(next, 0, 0.2);
    traders.push(t);
  }
  return traders;
}
