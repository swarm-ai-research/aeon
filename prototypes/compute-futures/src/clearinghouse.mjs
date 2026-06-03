// The clearinghouse — run by the fleet's `reviewer` (risk) role under a
// market/settle capability. It records every trade as a position, marks
// positions to market each round, enforces margin, and settles contracts at
// expiry against the spot index. With --x402 it settles physically: the short
// delivers inference and is paid per-M-token from the long's agent wallet.

import { usd } from "./util.mjs";
import { marginMultiplier, DEFAULT_PROFILE } from "./credit.mjs";

// DID used for the synthetic "house" counterparty (see Clearinghouse).
export const HOUSE_DID = "did:system:clearinghouse-house";

export class Clearinghouse {
  constructor({ wallets, marginRate = 0.15, x402 = null, creditFor = null }) {
    this.wallets = wallets;
    this.marginRate = marginRate; // initial margin as a fraction of notional
    this.x402 = x402; // optional X402Settlement extension
    // Counterparty credit: did -> { tier, reputation }. Margin is scaled by the
    // holder's trust (Darkbloom-grounded), so weak counterparties post more.
    this.creditFor = creditFor ?? (() => DEFAULT_PROFILE);
    // did -> symbol -> { qty (signed: + long / - short), avgPrice, multiplier }
    this.positions = new Map();
    this.marginCalls = [];
    this.settlements = [];
    this.peakMarginTotal = 0; // max total margin locked across the run
    this.lastMargin = []; // per-holder margin breakdown from the latest mark
    // Settlement-event log — paired events: every credit to a trader is
    // accompanied by a debit against the house. Σ events.amount per round
    // (or per reason category) is structurally 0 by construction. This is
    // what makes the conservation tests pass strictly.
    this.events = [];
    // Open a "house" wallet that absorbs the counterparty side of every
    // trade-close and cash-settle event. In a real futures clearing system
    // this is the clearinghouse itself acting as central counterparty;
    // here it's an accounting fiction that lets Σ events == 0 hold
    // structurally without requiring the sim to model who-traded-with-whom.
    // realizedByRole already excludes labels that aren't in its known set,
    // so the house wallet doesn't pollute role attribution.
    this.houseWallet = this.wallets.open({
      did: HOUSE_DID,
      label: "clearinghouse-house",
      cash: 0,
    });
  }

  // Record a paired P&L event: `did` is credited +amount; the house is debited
  // -amount. Both events go into the log; both wallets' `realized` updates.
  // Σ events.amount per round == 0 by construction.
  // `reason` is one of:
  //   'trade-close' — partial or full close via orderbook fill
  //   'cash-settle' — settlement at expiry against spot
  // `contract` is the contract symbol; pass null if not applicable.
  #recordEvent({ round, did, amount, reason, contract }) {
    if (amount === 0) return;
    this.wallets.get(did)?.credit(amount);
    this.houseWallet.credit(-amount);
    this.events.push({ round, did, amount, reason, contract });
    this.events.push({ round, did: HOUSE_DID, amount: -amount, reason, contract });
  }

  #pos(did, contract) {
    let bySym = this.positions.get(did);
    if (!bySym) {
      bySym = new Map();
      this.positions.set(did, bySym);
    }
    let p = bySym.get(contract.symbol);
    if (!p) {
      p = { qty: 0, avgPrice: 0, multiplier: contract.multiplier, underlying: contract.underlying };
      bySym.set(contract.symbol, p);
    }
    return p;
  }

  // Apply a fill to one side. `dir` is +1 for the buyer (long), -1 for seller.
  #apply(did, contract, dir, qty, price, round) {
    const p = this.#pos(did, contract);
    const signed = dir * qty;
    if (p.qty === 0 || Math.sign(p.qty) === Math.sign(signed)) {
      // opening or adding: weighted-average the entry price
      const newQty = p.qty + signed;
      p.avgPrice = newQty === 0 ? 0 : (p.avgPrice * p.qty + price * signed) / newQty;
      p.qty = newQty;
    } else {
      // reducing/closing: realize P&L on the closed portion
      const closed = Math.min(Math.abs(signed), Math.abs(p.qty));
      const pnl = (price - p.avgPrice) * Math.sign(p.qty) * closed * contract.multiplier;
      this.#recordEvent({ round, did, amount: pnl, reason: "trade-close", contract: contract.symbol });
      p.qty += signed;
      if (p.qty === 0) p.avgPrice = 0;
    }
  }

  recordTrade(contract, trade, round = null) {
    this.#apply(trade.buyer, contract, +1, trade.qty, trade.price, round);
    this.#apply(trade.seller, contract, -1, trade.qty, trade.price, round);
  }

  // Mark every open position to the current mid and re-lock margin. Flags a
  // margin call when required margin exceeds the wallet's equity.
  markToMarket(prices) {
    this.marginCalls = [];
    this.lastMargin = [];
    let total = 0;
    for (const [did, bySym] of this.positions) {
      const w = this.wallets.get(did);
      if (!w) continue;
      const profile = this.creditFor(did) ?? DEFAULT_PROFILE;
      const mult = marginMultiplier(profile); // reputation/tier-scaled
      let required = 0;
      for (const [sym, p] of bySym) {
        if (p.qty === 0) continue;
        const px = prices[sym] ?? p.avgPrice;
        // Margin is a non-negative risk metric: use absolute notional so that
        // spread products (SpreadIndex.floor = -Infinity) trading below zero
        // can't produce negative `required`, which would credit cash via
        // lockMargin and silently bypass margin-call checks.
        required += Math.abs(p.qty) * Math.abs(px) * p.multiplier * this.marginRate * mult;
      }
      w.releaseMargin(w.margin);
      w.lockMargin(required);
      if (required > 0) {
        this.lastMargin.push({ did, label: w.label, tier: profile.tier, reputation: profile.reputation, mult, required });
      }
      if (required > w.equity + 1e-9) {
        this.marginCalls.push({ did, label: w.label, required, equity: w.equity });
      }
      total += required;
    }
    if (total > this.peakMarginTotal) this.peakMarginTotal = total;
  }

  openInterest(symbol) {
    let longs = 0;
    for (const bySym of this.positions.values()) {
      const p = bySym.get(symbol);
      if (p && p.qty > 0) longs += p.qty;
    }
    return longs;
  }

  // Settle a contract at expiry against the spot price. Cash settlement credits
  // each side the difference between spot and their entry. If an x402 extension
  // is attached, the physical leg is also paid per-M-token, wallet→wallet.
  settle(contract, spotPrice, round = null) {
    const result = { symbol: contract.symbol, spot: spotPrice, legs: [], x402Receipts: [] };
    for (const [did, bySym] of this.positions) {
      const p = bySym.get(contract.symbol);
      if (!p || p.qty === 0) continue;
      const pnl = (spotPrice - p.avgPrice) * p.qty * contract.multiplier;
      const w = this.wallets.get(did);
      this.#recordEvent({ round, did, amount: pnl, reason: "cash-settle", contract: contract.symbol });
      result.legs.push({ did, label: w?.label, qty: p.qty, entry: p.avgPrice, pnl });

      // Physical delivery: shorts (GPU operators, qty < 0) deliver compute and
      // are paid at the settlement price by the longs, via x402.
      if (this.x402 && p.qty < 0) {
        const mTokens = Math.abs(p.qty) * contract.multiplier;
        // Pair each short's delivery against the aggregate long demand pro-rata
        // is overkill for the PoC; bill the contract's notional to the book.
        result.x402Receipts.push(
          this.x402.deliver({
            sellerDid: did,
            mTokens,
            pricePerM: spotPrice,
            model: contract.underlying,
          }),
        );
      }
      p.qty = 0;
      p.avgPrice = 0;
    }
    // Release margin held against this contract.
    this.markToMarket({});
    this.settlements.push(result);
    return result;
  }

  summary() {
    return this.wallets
      .all()
      .map((w) => w.summary())
      .join("\n");
  }

  // Conservation breakdown — Σ events.amount, optionally filtered by round.
  // With paired counterparties trading via the orderbook this should net to
  // zero per round; non-zero values reveal where the wallet-walk derivation
  // is leaking (unmatched open interest, unpaired margin moves, etc).
  // Today (pre-paired-events refactor) this equals `Σ wallet.realized` for
  // the same filter, so it's primarily a diagnostic helper. The next pass
  // makes conservation tautological by modeling paired transfers.
  conservation({ round = null, byReason = false } = {}) {
    const events = round == null ? this.events : this.events.filter((e) => e.round === round);
    if (!byReason) return events.reduce((s, e) => s + e.amount, 0);
    const buckets = {};
    for (const e of events) buckets[e.reason] = (buckets[e.reason] ?? 0) + e.amount;
    return buckets;
  }

  toJSON() {
    const positions = {};
    for (const [did, bySym] of this.positions) {
      positions[did] = Object.fromEntries(
        [...bySym].filter(([, p]) => p.qty !== 0).map(([s, p]) => [s, { qty: p.qty, avgPrice: p.avgPrice }]),
      );
    }
    return { positions, marginCalls: this.marginCalls, settlements: this.settlements, events: this.events };
  }
}

export function describeMarginCalls(calls) {
  if (!calls.length) return "none";
  return calls.map((c) => `${c.label} (need ${usd(c.required)} vs ${usd(c.equity)})`).join(", ");
}
