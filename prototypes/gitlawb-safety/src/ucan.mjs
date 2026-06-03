// UCAN-shaped capability tokens, faithful to gitlawb-core/src/ucan.rs:
//   payload = { iss, aud, att (caps), exp, nbf?, prf (proof chain), nonce }
//   signature = Ed25519 over the canonical payload.
//
// Two deliberate divergences from GitLawb v0.1 — these ARE the safety layer:
//   1. `exp` is MANDATORY. GitLawb makes it optional, so a token minted
//      without `exp` never expires — a permanent, un-revocable grant. We
//      refuse to mint one.
//   2. `verifyChain()` walks the full delegation chain and enforces
//      attenuation. GitLawb v0.1 "does not yet walk the full UCAN delegation
//      chain" — any signed agent can push regardless of capability. We do the
//      walk ourselves, at the bridge, treating the node as untrusted.

import { randomBytes } from "node:crypto";
import { signBytes, verifyBytes } from "./identity.mjs";
import { isAttenuationOf } from "./caps.mjs";

function nowSec() {
  return Math.floor(Date.now() / 1000);
}

// Stable, sorted serialization so signatures are deterministic.
function canonical(value) {
  if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
  if (value && typeof value === "object") {
    return (
      "{" +
      Object.keys(value)
        .sort()
        .map((k) => JSON.stringify(k) + ":" + canonical(value[k]))
        .join(",") +
      "}"
    );
  }
  return JSON.stringify(value ?? null);
}

function b64url(buf) {
  return Buffer.from(buf).toString("base64url");
}

// A unique, stable id for a token (stand-in for GitLawb's CID), used by the
// revocation blocklist to name a specific token.
export function tokenId(token) {
  return "tok_" + b64url(token.s).slice(0, 16);
}

function buildPayload({ issuer, audienceDid, capabilities, ttlSeconds, proofs }) {
  if (typeof ttlSeconds !== "number" || !Number.isFinite(ttlSeconds)) {
    throw new Error("REFUSED: ttlSeconds is required (no never-expiring tokens)");
  }
  if (ttlSeconds <= 0) throw new Error("REFUSED: ttlSeconds must be > 0");

  const iat = nowSec();
  return {
    iss: issuer.did,
    aud: audienceDid,
    att: capabilities,
    nbf: iat,
    exp: iat + ttlSeconds,
    prf: (proofs ?? []).map(encodeProof),
    nonce: randomBytes(9).toString("base64url"),
  };
}

// Proofs embed the full parent token (payload + raw signature) so a verifier
// holding only the leaf can reconstruct and re-check the whole chain.
function encodeProof(token) {
  return b64url(JSON.stringify({ payload: token.payload, s: b64url(token.s) }));
}

function decodeProof(encoded) {
  const obj = JSON.parse(Buffer.from(encoded, "base64url").toString("utf8"));
  return { payload: obj.payload, s: Buffer.from(obj.s, "base64url") };
}

function sealed(issuer, payload) {
  const s = signBytes(issuer.privateKey, canonical(payload));
  return { payload, s };
}

// Root issuance: an actor grants capabilities to an audience.
export function issue({ issuer, audienceDid, capabilities, ttlSeconds }) {
  return sealed(issuer, buildPayload({ issuer, audienceDid, capabilities, ttlSeconds }));
}

// Delegation: re-grant capabilities you already hold, attenuated, to someone
// else. The parent token rides along in `prf` so the chain can be walked.
export function delegate({ issuer, audienceDid, capabilities, ttlSeconds, proof }) {
  return sealed(
    issuer,
    buildPayload({ issuer, audienceDid, capabilities, ttlSeconds, proofs: [proof] }),
  );
}

// Single-hop checks: signature, not-before, not-expired.
// `allowExpired` skips only the expiry check (used by renewal, which must
// confirm a prior grant's authenticity even as it lapses) — signature and
// presence-of-expiry are always enforced.
export function verify(token, { now = nowSec(), allowExpired = false } = {}) {
  if (!verifyBytes(token.payload.iss, canonical(token.payload), token.s)) {
    return { ok: false, reason: "bad_signature" };
  }
  if (token.payload.nbf != null && now < token.payload.nbf) {
    return { ok: false, reason: "not_yet_valid" };
  }
  if (token.payload.exp == null) {
    return { ok: false, reason: "no_expiry" }; // never trust a no-exp token
  }
  if (!allowExpired && now > token.payload.exp) return { ok: false, reason: "expired" };
  return { ok: true };
}

// Full chain walk. Returns the EFFECTIVE capability set authorized by an
// unbroken, attenuated, in-date chain rooted in a trusted issuer, plus the
// DIDs and token ids of every link (so revocation can target any ancestor).
//
// At each link we check:
//   - the link itself verifies (sig + in-date)
//   - the parent's audience == this link's issuer (delegation continuity)
//   - every capability claimed here is an attenuation of one the parent held
//   - the root issuer is in `trustedRoots`
export function verifyChain(token, { now = nowSec(), trustedRoots, allowExpired = false }) {
  const self = verify(token, { now, allowExpired });
  if (!self.ok) return { ok: false, reason: `link:${self.reason}` };

  const proofs = token.payload.prf ?? [];
  const id = tokenId(token);

  // Root link: no proofs. Must be signed by a trusted root identity.
  if (proofs.length === 0) {
    if (!trustedRoots.has(token.payload.iss)) {
      return { ok: false, reason: "untrusted_root" };
    }
    return {
      ok: true,
      capabilities: token.payload.att,
      dids: [token.payload.iss, token.payload.aud],
      tokenIds: [id],
    };
  }

  // Delegated link: decode the parent, recurse, then enforce continuity +
  // attenuation against the parent's effective capabilities.
  let parent;
  try {
    parent = decodeProof(proofs[0]);
  } catch {
    return { ok: false, reason: "unparseable_proof" };
  }

  if (parent.payload.aud !== token.payload.iss) {
    return { ok: false, reason: "broken_delegation_chain" };
  }

  const upstream = verifyChain(parent, { now, trustedRoots, allowExpired });
  if (!upstream.ok) return { ok: false, reason: `parent:${upstream.reason}` };

  for (const claimed of token.payload.att) {
    const allowed = upstream.capabilities.some((p) => isAttenuationOf(claimed, p));
    if (!allowed) {
      return { ok: false, reason: `escalation:${claimed.can}@${claimed.with}` };
    }
  }
  return {
    ok: true,
    capabilities: token.payload.att,
    dids: [...upstream.dids, token.payload.iss, token.payload.aud],
    tokenIds: [...upstream.tokenIds, id],
  };
}

// Serialize a token for storage/transport (signature is a Buffer).
export function serializeToken(token) {
  return { payload: token.payload, s: Buffer.from(token.s).toString("base64url") };
}

export function deserializeToken(obj) {
  return { payload: obj.payload, s: Buffer.from(obj.s, "base64url") };
}

export { canonical, nowSec };
