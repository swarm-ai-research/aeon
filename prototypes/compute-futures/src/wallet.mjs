// Agent-sovereign wallet — usepod's model: each participant is an Ed25519
// did:key (no accounts, no custodian) holding a stablecoin balance it controls
// directly. Futures margin is locked here; settlement P&L and x402 inference
// payments move between these wallets.

import { usd } from "./util.mjs";

export class Wallet {
  constructor({ did, label, cash = 0 }) {
    this.did = did;
    this.label = label;
    this.cash = cash; // free balance (USDC units)
    this.margin = 0; // locked as futures margin
    this.realized = 0; // realized P&L over the run
  }

  get equity() {
    return this.cash + this.margin;
  }

  lockMargin(amount) {
    // Margin can exceed free cash in this PoC (we flag it as a margin call in
    // the clearinghouse rather than blocking the trade) — model it honestly.
    this.cash -= amount;
    this.margin += amount;
  }

  releaseMargin(amount) {
    const m = Math.min(amount, this.margin);
    this.margin -= m;
    this.cash += m;
  }

  // Move realized P&L (positive = credit, negative = debit) at settlement.
  credit(amount) {
    this.cash += amount;
    this.realized += amount;
  }

  toJSON() {
    return {
      did: this.did,
      label: this.label,
      cash: this.cash,
      margin: this.margin,
      equity: this.equity,
      realized: this.realized,
    };
  }

  summary() {
    return `${this.label}: equity ${usd(this.equity)} (cash ${usd(this.cash)}, margin ${usd(
      this.margin,
    )}, realized ${usd(this.realized)})`;
  }
}

export class WalletBook {
  constructor() {
    this.byDid = new Map();
  }

  open({ did, label, cash }) {
    const w = new Wallet({ did, label, cash });
    this.byDid.set(did, w);
    return w;
  }

  get(did) {
    return this.byDid.get(did);
  }

  all() {
    return [...this.byDid.values()];
  }
}
