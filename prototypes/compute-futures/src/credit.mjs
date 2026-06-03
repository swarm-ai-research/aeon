// Counterparty credit model — grounds futures margin in Darkbloom's provider
// trust. A short (a GPU operator) that is hardware-attested with a strong track
// record is a safer delivery counterparty than an unverified one, so it should
// post LESS collateral. We reuse Darkbloom's two trust tiers and its actual
// reputation formula, then map (tier, reputation) → a margin multiplier.
//
// This is the credit layer the prototype's clearinghouse was missing: margin
// scales with how trustworthy each counterparty is, not a flat rate for all.

export const TRUST_TIER = { HARDWARE: "hardware", SELF_SIGNED: "self_signed", NONE: "none" };

// Darkbloom's provider reputation score (coordinator/registry/reputation.go):
//   ρ = 0.4·jobSuccess + 0.3·uptime + 0.2·challengeResp + 0.1·responseTime
// All inputs in [0,1]; new providers default to 0.5.
export function reputationScore({ jobSuccess = 0.5, uptime = 0.5, challengeResp = 0.5, responseTime = 0.5 } = {}) {
  return 0.4 * jobSuccess + 0.3 * uptime + 0.2 * challengeResp + 0.1 * responseTime;
}

// Tier base multiplier: an unattested counterparty posts far more margin than a
// hardware-attested one (Apple MDA certificate chain) for the same notional.
const TIER_BASE = { hardware: 1.0, self_signed: 1.6, none: 3.0 };
const REP_WEIGHT = 1.0; // reputation 1 → ×1, reputation 0 → ×2 on top of tier base
const MIN_MULT = 1.0;
const MAX_MULT = 5.0;

// Default profile for any did without an explicit one (e.g. the x402 escrow):
// self-attested, average reputation — Darkbloom's new-provider baseline.
export const DEFAULT_PROFILE = { tier: TRUST_TIER.SELF_SIGNED, reputation: 0.5 };

function clamp01(x) {
  return Math.max(0, Math.min(1, Number.isFinite(x) ? x : 0));
}

// Margin multiplier for a counterparty: lower trust / lower reputation ⇒ more
// collateral. Bounded to [1, 5]× the base margin rate.
export function marginMultiplier(profile = DEFAULT_PROFILE) {
  const p = profile ?? DEFAULT_PROFILE;
  const base = TIER_BASE[p.tier] ?? TIER_BASE.none;
  const mult = base * (1 + (1 - clamp01(p.reputation)) * REP_WEIGHT);
  return Math.max(MIN_MULT, Math.min(MAX_MULT, mult));
}
