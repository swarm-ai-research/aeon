// Ed25519 identity + did:key encoding, using Node's built-in crypto (zero deps).
//
// Mirrors GitLawb's model: each actor (human or agent) is an Ed25519 keypair
// whose public key encodes to a `did:key:z6Mk...` identifier. No accounts,
// no passwords — identity is purely cryptographic.

import {
  generateKeyPairSync,
  sign as edSign,
  verify as edVerify,
  createPublicKey,
  createPrivateKey,
} from "node:crypto";

const BASE58_ALPHABET =
  "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";

// multicodec prefix for ed25519-pub (0xed 0x01)
const ED25519_MULTICODEC = Uint8Array.from([0xed, 0x01]);

// Standard SPKI DER header for an Ed25519 public key (12 bytes), so we can
// rebuild a verifiable KeyObject from nothing but the 32-byte raw key.
const SPKI_ED25519_PREFIX = Buffer.from("302a300506032b6570032100", "hex");

function base58encode(bytes) {
  let zeros = 0;
  while (zeros < bytes.length && bytes[zeros] === 0) zeros++;

  const digits = [0];
  for (let i = zeros; i < bytes.length; i++) {
    let carry = bytes[i];
    for (let j = 0; j < digits.length; j++) {
      carry += digits[j] << 8;
      digits[j] = carry % 58;
      carry = (carry / 58) | 0;
    }
    while (carry > 0) {
      digits.push(carry % 58);
      carry = (carry / 58) | 0;
    }
  }

  let out = "1".repeat(zeros);
  for (let i = digits.length - 1; i >= 0; i--) out += BASE58_ALPHABET[digits[i]];
  return out;
}

function base58decode(str) {
  let zeros = 0;
  while (zeros < str.length && str[zeros] === "1") zeros++;

  const bytes = [0];
  for (let i = zeros; i < str.length; i++) {
    const value = BASE58_ALPHABET.indexOf(str[i]);
    if (value === -1) throw new Error(`invalid base58 char: ${str[i]}`);
    let carry = value;
    for (let j = 0; j < bytes.length; j++) {
      carry += bytes[j] * 58;
      bytes[j] = carry & 0xff;
      carry >>= 8;
    }
    while (carry > 0) {
      bytes.push(carry & 0xff);
      carry >>= 8;
    }
  }

  const out = new Uint8Array(zeros + bytes.length);
  for (let i = 0; i < bytes.length; i++) out[zeros + i] = bytes[bytes.length - 1 - i];
  return Buffer.from(out);
}

function rawPubKeyToDid(rawKey) {
  const payload = Buffer.concat([ED25519_MULTICODEC, rawKey]);
  return "did:key:z" + base58encode(payload);
}

// Recover a verifiable public KeyObject straight from a did:key string.
// Verification needs only the DID — never the private key.
export function didToPublicKey(did) {
  if (!did.startsWith("did:key:z")) throw new Error(`unsupported DID: ${did}`);
  const decoded = base58decode(did.slice("did:key:z".length));
  if (decoded[0] !== 0xed || decoded[1] !== 0x01) {
    throw new Error("DID is not an ed25519-pub key");
  }
  const rawKey = decoded.subarray(2);
  const der = Buffer.concat([SPKI_ED25519_PREFIX, rawKey]);
  return createPublicKey({ key: der, format: "der", type: "spki" });
}

// Create a fresh actor identity.
export function generateIdentity(label = "actor") {
  const { publicKey, privateKey } = generateKeyPairSync("ed25519");
  const rawKey = publicKey.export({ format: "der", type: "spki" }).subarray(-32);
  const did = rawPubKeyToDid(rawKey);
  return { label, did, publicKey, privateKey };
}

// Persist/restore an identity via its PKCS#8 private key. The private key is a
// secret — store it in a vault, never in the public registry or git.
export function exportPrivateKey(identity) {
  return identity.privateKey.export({ format: "pem", type: "pkcs8" }).toString();
}

export function importIdentity(pem, label = "actor") {
  const privateKey = createPrivateKey(pem);
  const publicKey = createPublicKey(privateKey);
  const rawKey = publicKey.export({ format: "der", type: "spki" }).subarray(-32);
  return { label, did: rawPubKeyToDid(rawKey), publicKey, privateKey };
}

export function signBytes(privateKey, data) {
  return edSign(null, Buffer.from(data), privateKey);
}

export function verifyBytes(did, data, signature) {
  try {
    return edVerify(null, Buffer.from(data), didToPublicKey(did), signature);
  } catch {
    return false;
  }
}
