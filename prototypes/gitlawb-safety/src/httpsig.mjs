// Minimal RFC 9421 HTTP Message Signatures over Ed25519.
//
// GitLawb signs "every write via HTTP Signatures" — this is request-level
// auth: it proves *this specific request* was sent by the holder of a key,
// which complements UCAN (UCAN says what you MAY do; the HTTP sig proves WHO
// is asking right now, defeating token replay by a party who lacks the key).
//
// Faithful to the RFC's structure (signature base, @method / @target-uri
// derived components, content-digest, signature-input params) without aiming
// for full spec coverage. keyid is the sender's did:key; alg is ed25519.

import { createHash } from "node:crypto";
import { didToPublicKey, signBytes, verifyBytes } from "./identity.mjs";

const LABEL = "sig1";
const COVERED = ["@method", "@target-uri", "content-digest"];

function contentDigest(body) {
  const hash = createHash("sha256").update(body ?? "").digest("base64");
  return `sha-256=:${hash}:`;
}

function paramsString(created, keyid) {
  const list = COVERED.map((c) => `"${c}"`).join(" ");
  return `(${list});created=${created};keyid="${keyid}";alg="ed25519"`;
}

function signatureBase({ method, url, digest, created, keyid }) {
  const lines = [
    `"@method": ${method.toUpperCase()}`,
    `"@target-uri": ${url}`,
    `"content-digest": ${digest}`,
    `"@signature-params": ${paramsString(created, keyid)}`,
  ];
  return lines.join("\n");
}

// Sign a request; returns the headers a sender attaches.
export function signRequest({ method, url, did, privateKey, body, created = Math.floor(Date.now() / 1000) }) {
  const digest = contentDigest(body);
  const base = signatureBase({ method, url, digest, created, keyid: did });
  const sig = signBytes(privateKey, base).toString("base64");
  return {
    "Content-Digest": digest,
    "Signature-Input": `${LABEL}=${paramsString(created, did)}`,
    "Signature": `${LABEL}=:${sig}:`,
  };
}

// HTTP header names are case-insensitive; real stacks (Node, fetch, proxies)
// often lowercase them. Look up tolerantly.
function getHeader(headers, name) {
  if (headers[name] != null) return headers[name];
  const lower = name.toLowerCase();
  for (const key of Object.keys(headers)) {
    if (key.toLowerCase() === lower) return headers[key];
  }
  return undefined;
}

function parseSignatureInput(value) {
  // sig1=("@method" "@target-uri" "content-digest");created=..;keyid="..";alg=".."
  const inner = value.slice(value.indexOf("(") + 1, value.indexOf(")"));
  const covered = inner.split(/\s+/).map((s) => s.replace(/"/g, "")).filter(Boolean);
  const tail = value.slice(value.indexOf(")") + 1);
  const created = Number((tail.match(/created=(\d+)/) ?? [])[1]);
  const keyid = (tail.match(/keyid="([^"]+)"/) ?? [])[1];
  const alg = (tail.match(/alg="([^"]+)"/) ?? [])[1];
  return { covered, created, keyid, alg };
}

// Verify a request signature. Returns { ok, keyid, reason }.
export function verifyRequest({ method, url, headers, body, maxAgeSeconds = 300, now = Math.floor(Date.now() / 1000) }) {
  const sigInput = getHeader(headers, "Signature-Input");
  const sigHeader = getHeader(headers, "Signature");
  const contentDigestHeader = getHeader(headers, "Content-Digest");
  if (!sigInput || !sigHeader) return { ok: false, reason: "missing_signature_headers" };

  const { covered, created, keyid, alg } = parseSignatureInput(sigInput);
  if (alg !== "ed25519") return { ok: false, reason: `unsupported_alg:${alg}` };
  if (!keyid) return { ok: false, reason: "missing_keyid" };
  if (covered.join(",") !== COVERED.join(",")) {
    return { ok: false, keyid, reason: "unexpected_covered_components" };
  }

  // Replay window: reject signatures that are too old (or from the future).
  if (!Number.isFinite(created) || now - created > maxAgeSeconds || created - now > 60) {
    return { ok: false, keyid, reason: "stale_or_future_signature" };
  }

  // Content-Digest must match the body actually delivered (tamper detection).
  if (contentDigestHeader !== contentDigest(body)) {
    return { ok: false, keyid, reason: "content_digest_mismatch" };
  }

  const expectedSig = sigHeader.slice(sigHeader.indexOf(":") + 1, sigHeader.lastIndexOf(":"));
  const base = signatureBase({ method, url, digest: contentDigestHeader, created, keyid });

  let pub;
  try {
    pub = didToPublicKey(keyid);
  } catch {
    return { ok: false, keyid, reason: "bad_keyid" };
  }
  void pub;

  if (!verifyBytes(keyid, base, Buffer.from(expectedSig, "base64"))) {
    return { ok: false, keyid, reason: "bad_signature" };
  }
  return { ok: true, keyid };
}
