// FleetStore — persistence split along the trust boundary:
//
//   • public registry  (memory/gitlawb-fleet.json) — DIDs, capability token
//     ids, expiries, status. Safe to commit; this is what fleet-control reads.
//   • key vault        (.gitlawb-vault/keys.json)   — Ed25519 private keys.
//     SECRET. gitignored, never committed. A real deployment swaps this for a
//     KMS / sealed secret; the interface stays the same.

import { readFileSync, writeFileSync, existsSync, mkdirSync, chmodSync } from "node:fs";
import { dirname } from "node:path";
import { exportPrivateKey, importIdentity } from "./identity.mjs";

const EMPTY = { meta: {}, instances: [], updated: null };

export class FleetStore {
  constructor({ registryPath, vaultPath }) {
    this.registryPath = registryPath;
    this.vaultPath = vaultPath;
    this.registry = existsSync(registryPath)
      ? JSON.parse(readFileSync(registryPath, "utf8"))
      : structuredClone(EMPTY);
    if (!this.registry.meta) this.registry.meta = {};
    this.vault = existsSync(vaultPath) ? JSON.parse(readFileSync(vaultPath, "utf8")) : {};
  }

  getMeta() {
    return this.registry.meta;
  }

  setMeta(patch) {
    this.registry.meta = { ...this.registry.meta, ...patch };
    this.#writeRegistry();
  }

  // ── identities (vault) ───────────────────────────────────────────────
  saveIdentity(identity) {
    this.vault[identity.did] = { label: identity.label, pem: exportPrivateKey(identity) };
    this.#writeVault();
  }

  loadIdentity(did) {
    const entry = this.vault[did];
    if (!entry) return null;
    return importIdentity(entry.pem, entry.label);
  }

  // ── instances (public registry) ──────────────────────────────────────
  upsertInstance(entry) {
    const i = this.registry.instances.findIndex((x) => x.did === entry.did);
    if (i === -1) this.registry.instances.push(entry);
    else this.registry.instances[i] = { ...this.registry.instances[i], ...entry };
    this.#writeRegistry();
  }

  getInstance(did) {
    return this.registry.instances.find((x) => x.did === did) ?? null;
  }

  listInstances() {
    return this.registry.instances;
  }

  #writeRegistry() {
    this.registry.updated = new Date().toISOString();
    mkdirSync(dirname(this.registryPath), { recursive: true });
    writeFileSync(this.registryPath, JSON.stringify(this.registry, null, 2));
  }

  #writeVault() {
    // The vault holds private keys — keep it owner-only (0600), enforced even
    // if the file already existed with looser permissions.
    mkdirSync(dirname(this.vaultPath), { recursive: true });
    writeFileSync(this.vaultPath, JSON.stringify(this.vault, null, 2), { mode: 0o600 });
    chmodSync(this.vaultPath, 0o600);
  }
}
