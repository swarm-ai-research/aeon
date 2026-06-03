// x402-demo — the usepod settlement rail on its own, no market.
//
// An autonomous buyer agent runs an inference session against a GPU operator,
// paying per call over x402 (HTTP 402 → wallet-signed payment → 200) directly
// from its agent-sovereign wallet. Then the same session is settled once via
// MPP, showing the on-chain saving. No accounts, no API keys, no human in the
// loop — machine-speed micropayments.
//
//   node x402-demo.mjs

import { generateIdentity } from "../gitlawb-safety/src/identity.mjs";
import { WalletBook } from "./src/wallet.mjs";
import { X402Settlement, receiptsToMarkdown, SOLANA_TX_COST_USDC } from "./src/x402.mjs";
import { rng } from "./src/util.mjs";
import { usd } from "./src/util.mjs";

const next = rng(0x402402);
const buyer = generateIdentity("buyer-agent");
const seller = generateIdentity("gpu-operator");

const wallets = new WalletBook();
wallets.open({ did: buyer.did, label: "buyer-agent", cash: 50 });
wallets.open({ did: seller.did, label: "gpu-operator", cash: 0 });

const x402 = new X402Settlement({ wallets, escrowDid: buyer.did });

const MODEL = "LLAMA-INFER";
const PRICE_PER_M = 0.05; // commodity open-weight, usepod marginal-cost zone

const line = (s = "") => console.log(s);
line("═".repeat(64));
line("  x402 inference settlement — agent-sovereign micropayments");
line("═".repeat(64));
line();
line(`  buyer  ${buyer.did.slice(0, 32)}…`);
line(`  seller ${seller.did.slice(0, 32)}…`);
line(`  model  ${MODEL} @ ${usd(PRICE_PER_M)}/M-tokens`);
line();

// 1. Per-call settlement — one x402 transaction per inference call.
line("── Per-call x402 (one on-chain tx per call) ".padEnd(64, "─"));
const calls = [];
for (let i = 0; i < 12; i++) {
  const mTokens = 0.05 + next() * 0.4; // small bursts of tokens per call
  calls.push({ mTokens, pricePerM: PRICE_PER_M });
  x402.call({ buyerDid: buyer.did, sellerDid: seller.did, mTokens, pricePerM: PRICE_PER_M, model: MODEL });
}
const perCall = x402.receipts.filter((r) => r.kind === "call");
line(`  ${perCall.length} calls settled per-call`);
line(`  inference paid: ${usd(perCall.reduce((s, r) => s + r.amount, 0))}`);
line(`  on-chain tx cost: ${usd(perCall.length * SOLANA_TX_COST_USDC)} (${perCall.length} txns)`);
line();

// 2. Same session via MPP — meter off-chain, settle once.
line("── Same session via MPP (settle once) ".padEnd(64, "─"));
const mpp = x402.settleSession({ buyerDid: buyer.did, sellerDid: seller.did, calls, model: MODEL });
line(`  ${mpp.calls} calls → 1 settlement of ${usd(mpp.amount)}`);
line(`  on-chain txns saved: ${mpp.onChainTxnsSaved}  ·  tx cost saved: ${usd(mpp.txCostSavedUSDC)}`);
line();

line("── Receipts ".padEnd(64, "─"));
line(receiptsToMarkdown(x402.receipts.slice(-4)));
line(`  …(${x402.receipts.length} total)`);
line();
line(`  buyer wallet:  ${wallets.get(buyer.did).summary()}`);
line(`  seller wallet: ${wallets.get(seller.did).summary()}`);
line();
line("  x402 flow per payment: HTTP 402 → X-PAYMENT (wallet sig) → HTTP 200");
line("  no API key, no account, no human authorization — settled from the agent's wallet.");
