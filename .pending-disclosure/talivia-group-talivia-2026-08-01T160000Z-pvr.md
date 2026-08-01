---
kind: private-vulnerability-report
target_repo: talivia-group/talivia
target_head: 8248ccf3333b9d490712b53a87806abb2e2541cf
detected_at: 2026-08-01T16:00:00Z
detected_by: aeon (semgrep p/security-audit)
disclosure_endpoint: https://github.com/talivia-group/talivia/security/advisories/new
security_md: https://github.com/talivia-group/talivia/blob/main/SECURITY.md
submit_via: gh api -X POST /repos/talivia-group/talivia/security-advisories
severity: low
cwe_ids: ["CWE-354", "CWE-310"]
---

# PVR draft — Weak GCM authentication in `decrypt()` helper accepts truncated tags

**Do not submit as a public issue or public PR.** talivia has a SECURITY.md
that directs vulnerability reports through GitHub Private Vulnerability
Reporting, and the endpoint responds successfully (empty advisory list) so PVR
is enabled on the repo.

## Summary

The shared decryption helper at `src/lib/crypto.ts:33-47` calls
`crypto.createDecipheriv('aes-256-gcm', key, iv)` without an `authTagLength`
option. Node's GCM decipher then accepts any GCM-valid tag length (4, 8, 12,
13, 14, 15, or 16 bytes) via `decipher.setAuthTag(tag)`. Because `tag` is
sliced out of an attacker-controlled base64 blob, a shorter blob produces a
shorter tag, and the decipher will happily authenticate against it. This
reduces the forgery-difficulty exponent from 128 bits down to as little as 32.

## Impact

The helper is reachable from unauthenticated user input through
`parseAuthToken` (`src/lib/jwt.ts:28-36`) → `parseSecureToken` (jwt.ts:20-26)
→ `decrypt(token, secret)` — the token comes straight from the
`Authorization: Bearer` header. Current callers gate the plaintext with an
outer `jwt.verify(...)`, which makes end-to-end exploitation of the current
control flow infeasible (the attacker cannot forge a plaintext that is both a
valid JWT *and* signed with the app secret at 2^32 offline effort).

The report is filed anyway because the primitive itself is broken:
`decrypt()` is a general-purpose helper (also invoked from
`decryptProviderSecret` and cron jobs on server-controlled data). Any future
caller that trusts the plaintext without an outer signature check — a
serialized session cookie, an encrypted redirect target, a config lookup keyed
on the decrypted value — becomes a direct forgery target on the day it
lands, with no other change required. Fixing at the helper closes the class.

Secondary issue in the same function: `decrypt()` does not validate that the
input blob is at least `SALT_LENGTH + IV_LENGTH + TAG_LENGTH + 1` bytes.
`str.subarray(TAG_POSITION, ENC_POSITION)` silently returns a shorter buffer
when `str` is short, and `str.subarray(ENC_POSITION)` returns empty — both are
the mechanism that lets a truncated-tag blob reach `setAuthTag`. A length
guard would also close the class independently of the `authTagLength` option.

## Location

`src/lib/crypto.ts:33-47` — `decrypt()`
- Line 42: `crypto.createDecipheriv(ALGORITHM, key, iv)` — no `authTagLength`.
- Lines 35-38: `str.subarray(...)` slices without length precondition check.

For symmetry the `encrypt()` helper at line 19-31 should also pass
`authTagLength: TAG_LENGTH` to `createCipheriv` — Node currently defaults to
16 for that direction but pinning it prevents drift if someone later swaps in
a different mode.

## Proof of exposure (no working exploit chain)

Constructing a 4-byte GCM tag on the wire is the whole primitive — Node
accepts it:

```js
// Repro only; no attempt to chain into a JWT forgery.
const crypto = require('node:crypto');
const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);
const short = Buffer.alloc(4);         // 4-byte tag
const dec = crypto.createDecipheriv('aes-256-gcm', key, iv);
dec.setAuthTag(short);                 // accepted; no exception
// vs. { authTagLength: 16 }: setAuthTag(short) throws
//   "Invalid authentication tag length: 4"
```

Applied to the shipped `decrypt()`: with `SALT_LENGTH=64, IV_LENGTH=16,
TAG_LENGTH=16`, submit a 84-byte base64 blob (salt + IV + 4-byte tag + 0-byte
ciphertext); the slice returns a 4-byte `tag`, `setAuthTag` accepts it, and
forgery probability drops from 2^-128 to 2^-32 per attempt. The rest of the
chain (turning that forged plaintext into a valid signed JWT) is not
demonstrated because it isn't necessary to establish the crypto flaw itself.

## Suggested fix

```ts
// src/lib/crypto.ts

export function encrypt(value: any, secret: any) {
  const iv = crypto.randomBytes(IV_LENGTH);
  const salt = crypto.randomBytes(SALT_LENGTH);
  const key = getKey(secret, salt);

  const cipher = crypto.createCipheriv(ALGORITHM, key, iv, {
    authTagLength: TAG_LENGTH,          // pin, don't rely on default
  });
  // ...unchanged
}

export function decrypt(value: any, secret: any) {
  const str = Buffer.from(String(value), 'base64');
  if (str.length < ENC_POSITION) {
    throw new Error('decrypt: input too short');   // (a) length precondition
  }
  const salt = str.subarray(0, SALT_LENGTH);
  const iv = str.subarray(SALT_LENGTH, TAG_POSITION);
  const tag = str.subarray(TAG_POSITION, ENC_POSITION);
  const encrypted = str.subarray(ENC_POSITION);

  const key = getKey(secret, salt);

  const decipher = crypto.createDecipheriv(ALGORITHM, key, iv, {
    authTagLength: TAG_LENGTH,          // (b) reject any tag != 16 bytes
  });

  decipher.setAuthTag(tag);

  return decipher.update(encrypted) + decipher.final('utf8');
}
```

Either fix independently closes the class; both together are cheap and
mutually reinforcing.

## Severity

**Low.** No current end-to-end exploit chain in shipping code — the sole
user-reachable caller (JWT parseSecureToken) has an outer `jwt.verify` that
rejects forged plaintexts. Filed as defense-in-depth against a shared
primitive whose exploitability today is one commit away for any new caller.
Suggested CVSS: `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N` (3.1 Low).

## Detected by

Aeon + Semgrep OSS rule `javascript.node-crypto.security.gcm-no-tag-length`
(`p/security-audit`). Fired on `src/lib/crypto.ts:42`. Verified reachable
from unauthenticated input via manual call-graph walk. Contextual dampening
(outer `jwt.verify`) confirmed by reading `src/lib/jwt.ts` and every other
`decrypt(` call site in the repo.

## Suggested advisory metadata

- **Title:** `decrypt() helper accepts truncated GCM authentication tags`
- **Severity:** Low
- **CVSS:** 3.1
- **CWE:** CWE-354, CWE-310
- **Affected:** `<= HEAD 8248ccf3333b9d490712b53a87806abb2e2541cf` (as of
  2026-08-01). If tagged releases exist, apply to all releases carrying
  `src/lib/crypto.ts` in this shape.
- **Credit:** Aeon (https://github.com/aeonframework/aeon) — attribution
  optional at the reporter's discretion.

## Operator submission command (copy/paste when ready)

```bash
gh api -X POST /repos/talivia-group/talivia/security-advisories \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  -f summary="decrypt() helper accepts truncated GCM authentication tags" \
  -F cwe_ids='["CWE-354","CWE-310"]' \
  -f severity="low" \
  -f description="$(cat .pending-disclosure/talivia-group-talivia-2026-08-01T160000Z-pvr.md \
                    | awk '/^## Summary/,/^## Detected by/' \
                    | head -n -1)"
```

(Or paste the Summary → Impact → Location → Proof → Suggested fix sections
into the web UI at the disclosure endpoint URL above — same result.)

**Do not open a public issue or PR for this finding.** The `decrypt()` code
is unpatched.
