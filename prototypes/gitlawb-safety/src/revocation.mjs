// Local revocation blocklist.
//
// GitLawb has NO protocol-level revocation: "Issued UCAN tokens cannot be
// revoked before expiry. Compromised keypairs remain valid for 30 days." The
// only documented workaround is to regenerate identity and blocklist old DIDs
// by hand. So we maintain that blocklist ourselves, at the trust boundary we
// control, and consult it on every authorization.
//
// This is a non-authoritative stop on a public mesh — other nodes won't honor
// it — which is exactly why short TTLs + gated renewal (see guard.mjs) are the
// primary control and this is the emergency brake.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

export class RevocationStore {
  constructor(path = null) {
    this.path = path;
    this.dids = new Set();
    this.tokens = new Set();
    if (path && existsSync(path)) {
      const data = JSON.parse(readFileSync(path, "utf8"));
      this.dids = new Set(data.dids ?? []);
      this.tokens = new Set(data.tokens ?? []);
    }
  }

  revokeDid(did, reason = "") {
    this.dids.add(did);
    this.#persist();
    return { did, reason, at: new Date().toISOString() };
  }

  revokeToken(id, reason = "") {
    this.tokens.add(id);
    this.#persist();
    return { token: id, reason, at: new Date().toISOString() };
  }

  // A token is revoked if ANY token id in its delegation chain is listed
  // (so revoking a parent kills its descendants), or ANY identity in the
  // chain (issuer/audience) has been blocklisted.
  isRevoked(chainTokenIds = [], chainDids = []) {
    if (chainTokenIds.some((id) => this.tokens.has(id))) return true;
    return chainDids.some((d) => this.dids.has(d));
  }

  #persist() {
    if (!this.path) return;
    mkdirSync(dirname(this.path), { recursive: true });
    writeFileSync(
      this.path,
      JSON.stringify({ dids: [...this.dids], tokens: [...this.tokens] }, null, 2),
    );
  }
}
