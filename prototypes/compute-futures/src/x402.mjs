// OPTIONAL extension — x402 settlement, the actual usepod payment rail.
//
// usepod settles inference per-call over x402 (the HTTP 402 "Payment Required"
// flow) and batches sessions via MPP, paying directly from agent-sovereign
// wallets on Solana (~$0.00025 / tx, ~400ms finality, no API keys, no human in
// the loop). This module models that rail so the futures market can settle
// PHYSICALLY: at expiry a GPU operator (the short) delivers compute and is paid
// per-M-token from a demand-side escrow, wallet→wallet, with x402 receipts.
//
// It's deliberately separable: the market runs fully without it (cash
// settlement). Pass --x402 to wire it in, or run x402-demo.mjs to see the rail
// on its own.

export const SOLANA_TX_COST_USDC = 0.00025;
export const SOLANA_FINALITY_MS = 400;

let RECEIPT_SEQ = 0;

export class X402Settlement {
  constructor({ wallets, escrowDid }) {
    this.wallets = wallets;
    this.escrowDid = escrowDid; // demand-side escrow funding physical delivery
    this.receipts = [];
  }

  // One x402-settled payment: 402 challenge → wallet-signed payment → 200.
  #pay({ fromDid, toDid, mTokens, pricePerM, model, kind }) {
    const amount = mTokens * pricePerM;
    const from = this.wallets.get(fromDid);
    const to = this.wallets.get(toDid);
    if (from) from.cash -= amount;
    if (to) to.cash += amount;
    const receipt = {
      id: ++RECEIPT_SEQ,
      scheme: "x402",
      kind, // "deliver" | "call" | "mpp-session"
      model,
      mTokens,
      pricePerM,
      amount,
      from: from?.label ?? fromDid,
      to: to?.label ?? toDid,
      txCostUSDC: SOLANA_TX_COST_USDC,
      finalityMs: SOLANA_FINALITY_MS,
      flow: ["HTTP 402", "X-PAYMENT (wallet sig)", "HTTP 200"],
    };
    this.receipts.push(receipt);
    return receipt;
  }

  // Physical-delivery leg of a settled future: escrow pays the operator for the
  // compute it delivers at the settlement price.
  deliver({ sellerDid, mTokens, pricePerM, model }) {
    return this.#pay({
      fromDid: this.escrowDid,
      toDid: sellerDid,
      mTokens,
      pricePerM,
      model,
      kind: "deliver",
    });
  }

  // A live inference session billed per call (used by x402-demo.mjs).
  call({ buyerDid, sellerDid, mTokens, pricePerM, model }) {
    return this.#pay({ fromDid: buyerDid, toDid: sellerDid, mTokens, pricePerM, model, kind: "call" });
  }

  // MPP: instead of N on-chain txns, meter N calls off-chain and settle the sum
  // in one transaction — the saving is (N-1) × tx cost.
  settleSession({ buyerDid, sellerDid, calls, model }) {
    const mTokens = calls.reduce((s, c) => s + c.mTokens, 0);
    const amount = calls.reduce((s, c) => s + c.mTokens * c.pricePerM, 0);
    const pricePerM = mTokens ? amount / mTokens : 0;
    const r = this.#pay({ fromDid: buyerDid, toDid: sellerDid, mTokens, pricePerM, model, kind: "mpp-session" });
    r.calls = calls.length;
    r.onChainTxnsSaved = Math.max(0, calls.length - 1);
    r.txCostSavedUSDC = r.onChainTxnsSaved * SOLANA_TX_COST_USDC;
    return r;
  }

  total() {
    return this.receipts.reduce((s, r) => s + r.amount, 0);
  }
}

export function receiptsToMarkdown(receipts) {
  if (!receipts.length) return "No x402 settlements.";
  const lines = receipts.map(
    (r) =>
      `  #${r.id} ${r.kind.padEnd(12)} ${r.from} → ${r.to}  ${r.mTokens.toFixed(1)}M @ $${r.pricePerM.toFixed(4)}/M = $${r.amount.toFixed(4)} (tx $${r.txCostUSDC}, ${r.finalityMs}ms)`,
  );
  return lines.join("\n");
}
