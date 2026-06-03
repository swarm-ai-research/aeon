// Market capability vocabulary, layered on the GitLawb capability model
// (../gitlawb-safety/src/caps.mjs). The fleet doesn't get blanket market
// access: the operator mints each participant a short-lived, scoped capability
// per round, and the guard authorizes every order/settlement against it.
//
// Resource URIs are scoped per underlying symbol so a trader cap for
// "market:LLAMA-INFER/*" can't be replayed to act on "market:FRONTIER/*".

import { cap } from "../../gitlawb-safety/src/caps.mjs";

export const MARKET_CAP = {
  QUOTE: "market/quote", // post a limit order (bid/ask)
  TRADE: "market/trade", // cross the book / take liquidity
  SETTLE: "market/settle", // mark-to-market + cash/physical settlement (clearinghouse)
  HALT: "market/halt", // trip a circuit breaker (surveillance)
  DELIVER: "compute/deliver", // a GPU operator delivers inference against a contract
};

// Like SAFETY_CRITICAL in gitlawb-safety: clearing and halting move money and
// stop the market, so in a real deployment they'd carry the short mandatory
// TTL + gated renewal. We surface the set here; the guard clamps TTLs and the
// operator mints these only to the clearing/surveillance roles.
export const MARKET_SAFETY_CRITICAL = new Set([MARKET_CAP.SETTLE, MARKET_CAP.HALT]);

export function marketResource(symbol) {
  return `market:${symbol}`;
}

// Capability scoped to one underlying (e.g. "market:LLAMA-INFER/*"), so the
// guard's prefix matching lets it act on any expiry of that underlying.
export function marketCap(underlying, ability, constraints) {
  return cap(`${marketResource(underlying)}/*`, ability, constraints);
}

// What the guard requires to act on a specific contract (e.g. one expiry).
export function requiredFor(contract, ability) {
  return cap(`${marketResource(contract.underlying)}/${contract.expiryRound}`, ability);
}
