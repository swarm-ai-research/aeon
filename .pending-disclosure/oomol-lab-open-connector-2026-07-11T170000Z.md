---
repo: oomol-lab/open-connector
head: 62796b0d9390df49ed7644692ed75ba576bac9e9
scanned_at: 2026-07-11T17:00:00Z
channel_intent: private-vulnerability-report
preferred_submit_url: https://github.com/oomol-lab/open-connector/security/advisories/new
fallback_email: support@oomol.com
fallback_subject: "[security] AES-GCM: missing authTagLength in local secret codec"
severity_suggested: medium
cwe_ids: [CWE-327, CWE-354]
scanners: semgrep=ok, trufflehog-fs=ok, trufflehog-git=ok, osv=ok
---

# Private Vulnerability Report — oomol-lab/open-connector

**Do not publish this draft as a public issue or PR.** The operator should submit
it through the preferred private channel (GitHub advisories UI, above) or, as a
fallback, email `support@oomol.com`. The maintainer's `SECURITY.md` requests
private reporting and coordinated disclosure.

---

## Summary

`src/server/secrets/secret-codec.ts` — the Node.js local-deployment implementation
of `AesGcmSecretCodec` — decrypts stored credentials with AES-256-GCM but calls
`createDecipheriv("aes-256-gcm", key, iv)` without the `authTagLength` option and
then hands the caller-controlled tag to `decipher.setAuthTag(...)` with no length
check. Node.js's default behaviour for GCM is to accept any tag length permitted
by NIST SP 800-38D (4, 8, 12, 13, 14, 15, or 16 bytes). An attacker who can
write to the encrypted credential store can substitute a payload with a
4-byte tag, reducing the effort to forge a ciphertext that decrypts to a chosen
plaintext from ~2^128 to ~2^32.

## Impact

Concrete threat model against a local (SQLite) or Cloudflare (D1) deployment
running with `OOMOL_CONNECT_ENCRYPTION_KEY` set:

1. An attacker who obtains **write** access to the encrypted credential store
   (e.g. via a database backup restored to an untrusted host, an unrelated
   file-system vulnerability, or an operator-side data-store leak) but does
   **not** know the encryption key can attempt to substitute a stored OAuth
   refresh token or provider API key with a value they control.
2. With a full 16-byte GCM tag (the encoder path already uses 16 bytes), a
   forgery attempt has ~2^-128 success probability — effectively impossible.
3. With the decoder accepting a 4-byte tag, the same forgery becomes ~2^-32.
   Roughly 4 × 10^9 candidate ciphertexts can be prepared offline, and only one
   needs to decrypt to an attacker-useful plaintext (for example, a valid-looking
   provider access token, or an empty string that would break authentication for
   a specific credential and force re-linking to an attacker-controlled account).
4. Once the forged record is persisted, any legitimate use of the affected
   credential by the gateway (`/v1/actions`, MCP tool call, OpenAPI runtime)
   silently uses the attacker's substituted value.

This is a defence-in-depth failure in exactly the module the SECURITY.md scope
calls out first: *"Credential storage and at-rest encryption
(`src/server/secrets/*`), key handling, and token management."* The Cloudflare
Worker variant (`src/server/secrets/worker-secret-codec.ts`) is **not** affected
— it uses `crypto.subtle.decrypt` with the WebCrypto default `tagLength` of 128
bits and validates tag length as part of ciphertext parsing.

## Location

- File: `src/server/secrets/secret-codec.ts`
- Line: 48 (`createDecipheriv` call) — and line 49 (`setAuthTag`) which trusts
  the caller-supplied buffer length.
- Commit at time of report: `8d87cab8248dd78d4e592a687b8588f4d9b983f7`
  (2026-07-02, latest touching this file).
- HEAD at time of scan: `62796b0d9390df49ed7644692ed75ba576bac9e9` on `main`.

## Proof of exploitability (no working forgery included)

Rather than a live forgery PoC (which would require a database write oracle
against a running instance), the following short Node script demonstrates that
the current codec **accepts a 4-byte tag** without complaint, which is the
underlying weakness. No real credentials are used; the plaintext and key are
throw-away values.

```js
import { createCipheriv, createDecipheriv, scryptSync, randomBytes } from "node:crypto";
const key = scryptSync("test-passphrase", "oomol-connect-local-secret-store-v1", 32);
const iv = randomBytes(12);
const cipher = createCipheriv("aes-256-gcm", key, iv);
const ct = Buffer.concat([cipher.update("hello", "utf8"), cipher.final()]);
const fullTag = cipher.getAuthTag(); // 16 bytes

// Truncate to 4 bytes — well below the 12-byte NIST recommendation.
const shortTag = fullTag.subarray(0, 4);

const decipher = createDecipheriv("aes-256-gcm", key, iv);
decipher.setAuthTag(shortTag);        // succeeds silently — no length check
const pt = Buffer.concat([decipher.update(ct), decipher.final()]).toString("utf8");
console.log("decrypted:", pt);        // "hello" — a 4-byte tag was accepted
```

The vulnerability is not that legitimately-encoded records use 4-byte tags —
they use 16. The vulnerability is that the decoder *accepts* whatever length an
attacker chooses to place in the stored `<tag>` segment.

## Suggested fix

Pin the authentication tag to exactly 16 bytes at both the API call and the
buffer that reaches `setAuthTag`:

```ts
async decode(stored: string): Promise<string> {
  if (!stored.startsWith(encryptedPrefix)) return stored;

  const [ivText, tagText, encryptedText] = stored.slice(encryptedPrefix.length).split(".");
  if (!ivText || !tagText || !encryptedText) {
    throw new Error("Encrypted local secret payload is malformed.");
  }

  const tag = Buffer.from(tagText, "base64url");
  if (tag.length !== 16) {
    throw new Error("Encrypted local secret payload has an invalid authentication tag length.");
  }

  const decipher = createDecipheriv(
    "aes-256-gcm",
    this.key,
    Buffer.from(ivText, "base64url"),
    { authTagLength: 16 },
  );
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(Buffer.from(encryptedText, "base64url")), decipher.final()]).toString("utf8");
}
```

Two independent hardenings: the `{ authTagLength: 16 }` option makes Node
reject any tag not of exactly 16 bytes at `setAuthTag`, and the explicit
`tag.length !== 16` check documents the invariant and gives a clear error path
for legacy or corrupted records (there should be none — the encoder has always
written 16-byte tags).

The `encode` path already uses the default 16-byte tag length, so pinning
`authTagLength` on the decoder is fully backwards-compatible for records
produced by any prior version of the codec. A schema-version bump is not
required.

## Severity rationale

Suggested CVSS 4.0 vector: `AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N`
— roughly **medium** (attack complexity high, requires DB-write privilege, but
compromise of a stored credential yields full read/impersonation of the linked
provider account). Adjust as your triage sees fit.

## Detection

Detected by [Semgrep](https://semgrep.dev/) rule
`javascript.node-crypto.security.gcm-no-tag-length.gcm-no-tag-length` in a routine
scan (`p/security-audit` + `p/owasp-top-ten` + `p/secrets` rulesets). All other
scanners (`trufflehog` filesystem + git history for verified secrets,
`osv-scanner` for dependency CVEs) reported no findings; the audit is otherwise
clean at this commit.

## Reporter

Filed by [Aeon](https://github.com/aeonframework/aeon), an autonomous
security-audit bot. Draft prepared 2026-07-11 by the `vuln-scanner` skill;
the operator submits the report through the private channels above. Happy to
coordinate on the fix or a CVE request through the same channel.
