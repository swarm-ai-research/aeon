// CapabilityGuard — the bridge / off-switch.
//
// This is the piece the Aeon<->GitLawb integration must supply, because
// GitLawb v0.1 doesn't: it enforces capability attenuation on every event
// (the node won't), caps the lifetime of dangerous capabilities, and gates
// renewal behind a pluggable safety check so that "stop renewing" becomes the
// off-switch revocation can't be.

import { issue, delegate, verify, verifyChain, tokenId, nowSec } from "./ucan.mjs";
import { ceilingFor, isAttenuationOf, isSafetyCritical } from "./caps.mjs";

export class CapabilityGuard {
  constructor({ trustedRoots, revocations, metrics = null }) {
    this.trustedRoots = trustedRoots; // Set<did> of identities we trust as chain roots
    this.revocations = revocations; // RevocationStore
    this.metrics = metrics; // optional MetricsRecorder
  }

  // Enforce the per-capability TTL ceiling. Safety-critical caps
  // (agent/deploy, repo/admin, pr/merge) are clamped hard and short.
  #clampTtl(capabilities, requestedTtl) {
    const ceiling = Math.min(...capabilities.map((c) => ceilingFor(c.can)));
    return Math.min(requestedTtl, ceiling);
  }

  mint({ issuer, audienceDid, capabilities, ttlSeconds }) {
    const ttl = this.#clampTtl(capabilities, ttlSeconds);
    return issue({ issuer, audienceDid, capabilities, ttlSeconds: ttl });
  }

  delegate({ issuer, audienceDid, capabilities, ttlSeconds, proof }) {
    const ttl = this.#clampTtl(capabilities, ttlSeconds);
    return delegate({ issuer, audienceDid, capabilities, ttlSeconds: ttl, proof });
  }

  // Run on EVERY action sourced from a (untrusted) GitLawb node event.
  // Walks the chain, checks the local blocklist, confirms the required cap.
  authorize(token, required, { now = nowSec() } = {}) {
    const res = this.#authorize(token, required, now);
    this.metrics?.record("authorize", {
      allowed: res.allowed,
      reason: res.reason ?? "ok",
      can: required.can,
    });
    return res;
  }

  #authorize(token, required, now) {
    const chain = verifyChain(token, { now, trustedRoots: this.trustedRoots });
    if (!chain.ok) return { allowed: false, reason: chain.reason };

    if (this.revocations.isRevoked(chain.tokenIds, chain.dids)) {
      return { allowed: false, reason: "revoked" };
    }

    const has = chain.capabilities.some(
      (c) => c.can === required.can && matches(c.with, required.with),
    );
    if (!has) return { allowed: false, reason: `missing_cap:${required.can}` };

    return { allowed: true, capabilities: chain.capabilities };
  }

  // Gated renewal — the real off-switch. A safety-critical capability is only
  // re-minted if (a) the prior token is still structurally valid, (b) it isn't
  // revoked, and (c) the safety check passes (e.g. a red-team sub-swarm signs
  // off). Declining to renew lets the capability die at its short expiry.
  async renew(args, safetyCheck) {
    const res = await this.#renew(args, safetyCheck);
    this.metrics?.record("renew", { renewed: res.renewed, reason: res.reason ?? "ok", aud: args.audienceDid });
    return res;
  }

  async #renew({ priorToken, issuer, audienceDid, capabilities, ttlSeconds }, safetyCheck) {
    // The prior token must be an authentic grant — signed and rooted in a
    // trusted issuer — to this exact audience. Expiry is tolerated (renewing a
    // just-lapsed cap is the normal loop case); forgery/escalation is not.
    const prior = verifyChain(priorToken, { trustedRoots: this.trustedRoots, allowExpired: true });
    if (!prior.ok) return { renewed: false, reason: `invalid_prior:${prior.reason}` };
    if (priorToken.payload.aud !== audienceDid) {
      return { renewed: false, reason: "prior_audience_mismatch" };
    }
    if (this.revocations.isRevoked(prior.tokenIds, prior.dids)) {
      return { renewed: false, reason: "revoked" };
    }

    for (const requested of capabilities) {
      const allowed = prior.capabilities.some((held) => isAttenuationOf(requested, held));
      if (!allowed) {
        return {
          renewed: false,
          reason: `renewal_escalation:${requested.can}@${requested.with}`,
        };
      }
    }

    const needsGate = capabilities.some((c) => isSafetyCritical(c.can));
    if (needsGate) {
      const verdict = await safetyCheck({ audienceDid, capabilities });
      if (!verdict.pass) {
        return { renewed: false, reason: `safety_check_failed:${verdict.reason ?? ""}` };
      }
    }

    const token = this.mint({ issuer, audienceDid, capabilities, ttlSeconds });
    return { renewed: true, token, expiresAt: token.payload.exp };
  }
}

function matches(held, required) {
  if (held === "*" || held === required) return true;
  if (held.endsWith("/*")) return required.startsWith(held.slice(0, -1));
  return false;
}

export { verify, tokenId };
