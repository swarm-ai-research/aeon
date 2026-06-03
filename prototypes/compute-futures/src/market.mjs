// ComputeFuturesMarket — where the GitLawb fleet orchestrates AND trades.
//
// Orchestration (the capability layer from ../gitlawb-safety):
//   • operator   — each round mints short-lived, scoped market caps to every
//                  participant via the SwarmCoordinator. No standing authority.
//   • reviewer   — holds market/settle; runs mark-to-market and clears expiries.
//   • sentinel   — holds market/halt; trips a circuit breaker on extreme moves.
// Every order and settlement is authorized by the CapabilityGuard against the
// cap minted for that round — the same enforcement the bridge does on-node.
//
// Trading: the researcher is the analyst, the deployer is a GPU operator
// selling capacity forward, plus the retail swarm. Price discovery happens in
// the order book; events move the fundamental and the curve re-prices.

import { OrderBook } from "./orderbook.mjs";
import { Clearinghouse, describeMarginCalls } from "./clearinghouse.mjs";
import { marketCap, requiredFor, MARKET_CAP } from "./market-caps.mjs";
import { usd } from "./util.mjs";

const HALT_THRESHOLD = 0.6; // single-round |Δmid| that trips the breaker (truly extreme only)

export class ComputeFuturesMarket {
  constructor({ fleet, traders, contracts, spotIndices, events, guard, coordinator, wallets, metrics, x402 = null, next }) {
    this.fleet = fleet; // { operator, reviewer, sentinel } identities
    this.traders = traders;
    this.contracts = contracts;
    this.spotIndices = new Map(spotIndices.map((s) => [s.underlying, s]));
    this.events = events;
    this.guard = guard;
    this.coordinator = coordinator;
    this.wallets = wallets;
    this.metrics = metrics;
    this.next = next;
    // Counterparty credit map: each trader's Darkbloom trust profile drives its
    // margin multiplier in the clearinghouse (unknown dids fall back to default).
    const creditByDid = new Map(traders.map((t) => [t.did, t.credit]));
    this.clearing = new Clearinghouse({ wallets, x402, creditFor: (did) => creditByDid.get(did) });
    this.books = new Map(contracts.map((c) => [c.symbol, new OrderBook(c)]));
    this.history = [];
    this.haltsThisRun = [];
    this.underlyings = [...new Set(contracts.map((c) => c.underlying))];
  }

  #active(round) {
    return this.contracts.filter((c) => c.expiryRound > round);
  }

  #ref(symbol) {
    return this.books.get(symbol)?.mid() ?? null;
  }

  // Capabilities a trader needs this round: market/quote + market/trade on each
  // underlying it may touch. Scoped per underlying so a cap can't be replayed
  // across products.
  #capFor() {
    return this.underlyings.flatMap((u) => [
      marketCap(u, MARKET_CAP.QUOTE),
      marketCap(u, MARKET_CAP.TRADE),
    ]);
  }

  async runRound(round) {
    const active = this.#active(round);
    for (const c of active) this.books.get(c.symbol).clearResting();

    // 1. News. The event moves the marginal cost; retail gets a sentiment kick.
    const event = this.events.fire(round, [...this.spotIndices.values()]);
    const eventImpulse = event ? event.impulse : 0;

    // 2. Operator mints a per-round, per-trader capability and fans out trading.
    const ctx = {
      contracts: active,
      reference: (s) => this.#ref(s),
      fundamental: (u) => this.spotIndices.get(u).fundamental,
      round,
      next: this.next,
      eventImpulse,
    };

    const dispatch = await this.coordinator.runParallel({
      task: { id: `round-${round}` },
      workers: this.traders,
      capFor: () => this.#capFor(),
      ttlSeconds: 60,
      execute: ({ worker, token }) => {
        const trader = this.traders.find((t) => t.did === worker.did);
        let placed = 0;
        let denied = 0;
        for (const o of trader.quote(ctx)) {
          // Enforce the capability on every order, exactly like the bridge.
          const ok = this.guard.authorize(token, requiredFor(o.contract, MARKET_CAP.TRADE));
          if (!ok.allowed) {
            denied++;
            continue;
          }
          const book = this.books.get(o.contract.symbol);
          if (book.halted) continue;
          const trades = book.submit(o);
          for (const t of trades) this.clearing.recordTrade(o.contract, t, round);
          placed++;
        }
        return { placed, denied };
      },
    });

    // 3. Spot advances toward the (possibly shocked) fundamental.
    for (const s of this.spotIndices.values()) s.step();

    // 4. Reviewer marks to market under market/settle.
    const prices = {};
    for (const c of active) prices[c.symbol] = this.#ref(c.symbol) ?? this.spotIndices.get(c.underlying).price;
    this.#asReviewer(round, () => this.clearing.markToMarket(prices));

    // 5. Sentinel surveillance under market/halt — trip the breaker on extremes.
    this.#asSentinel(round, () => {
      const prev = this.history[this.history.length - 1];
      for (const c of active) {
        const book = this.books.get(c.symbol);
        book.halted = false; // breakers are one round; re-evaluate fresh
        const now = this.#ref(c.symbol);
        const was = prev?.curve.find((x) => x.symbol === c.symbol)?.price;
        if (was && now && Math.abs(now - was) / was > HALT_THRESHOLD) {
          book.halted = true;
          this.haltsThisRun.push({ round, symbol: c.symbol, move: (now - was) / was });
          this.metrics?.record("halt", { round, symbol: c.symbol });
        }
      }
    });

    // 6. Settle anything expiring this round (physical via x402 if attached).
    const settlements = [];
    for (const c of this.contracts.filter((x) => x.expiryRound === round)) {
      const spot = this.spotIndices.get(c.underlying).price;
      const res = this.#asReviewer(round, () => this.clearing.settle(c, spot, round));
      settlements.push(res);
    }

    // 7. Snapshot the curve.
    const snapshot = {
      round,
      event: event ? event.label : null,
      spot: this.spotIndices.get(this.underlyings[0]).price,
      curve: this.#active(round).map((c) => ({
        symbol: c.symbol,
        expiry: c.expiryRound,
        price: this.#ref(c.symbol) ?? this.spotIndices.get(c.underlying).price,
        oi: this.clearing.openInterest(c.symbol),
      })),
      marginCalls: this.clearing.marginCalls.length,
      settlements,
      dispatch,
    };
    this.history.push(snapshot);
    this.metrics?.record("curve", { round, spot: snapshot.spot });
    return snapshot;
  }

  // Mint a settle capability to the reviewer, authorize, then act. This is the
  // "clearing is a capability, not a role you simply are" model.
  #asReviewer(round, fn) {
    const token = this.guard.mint({
      issuer: this.fleet.operator,
      audienceDid: this.fleet.reviewer.did,
      capabilities: [marketCap(this.underlyings[0], MARKET_CAP.SETTLE)],
      ttlSeconds: 60,
    });
    const ok = this.guard.authorize(token, marketCap(this.underlyings[0], MARKET_CAP.SETTLE));
    if (!ok.allowed) throw new Error(`reviewer settle denied: ${ok.reason}`);
    return fn();
  }

  #asSentinel(round, fn) {
    const token = this.guard.mint({
      issuer: this.fleet.operator,
      audienceDid: this.fleet.sentinel.did,
      capabilities: [marketCap(this.underlyings[0], MARKET_CAP.HALT)],
      ttlSeconds: 60,
    });
    const ok = this.guard.authorize(token, marketCap(this.underlyings[0], MARKET_CAP.HALT));
    if (!ok.allowed) throw new Error(`sentinel halt denied: ${ok.reason}`);
    return fn();
  }

  run(rounds) {
    return (async () => {
      for (let r = 1; r <= rounds; r++) await this.runRound(r);
      return this.history;
    })();
  }

  reportTail() {
    const mc = describeMarginCalls(this.clearing.marginCalls);
    return `Open margin calls: ${mc}\nLast spot: ${usd(this.spotIndices.get(this.underlyings[0]).price)}`;
  }
}
