// GitLawbFleet — Phase 2 lifecycle manager.
//
// Spawns Aeon instances as GitLawb identities, hands each a short-lived
// capability via the guard, keeps them alive only through gated renewal, and
// kills them via the blocklist. State lives in FleetStore; the GitHub-side
// fleet registry (memory/instances.json) is mirrored so fleet-control sees
// GitLawb-hosted instances alongside fork instances.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { CapabilityGuard } from "./guard.mjs";
import { generateIdentity } from "./identity.mjs";
import { tokenId, serializeToken, deserializeToken, nowSec } from "./ucan.mjs";
import { isSafetyCritical } from "./caps.mjs";

const iso = () => new Date().toISOString();

export class GitLawbFleet {
  constructor({ trustedRoots, store, revocations, metrics = null }) {
    this.store = store;
    this.revocations = revocations;
    this.metrics = metrics;
    this.guard = new CapabilityGuard({ trustedRoots, revocations, metrics });
  }

  // Spawn a new instance: fresh identity + a short-lived capability minted by
  // the operator (root). The private key goes to the vault; the public
  // registry records only the DID, token, and expiry.
  spawn({ operator, label, node, capabilities, ttlSeconds }) {
    const identity = generateIdentity(label);
    this.store.saveIdentity(identity);

    const token = this.guard.mint({
      issuer: operator,
      audienceDid: identity.did,
      capabilities,
      ttlSeconds,
    });

    const entry = {
      name: label,
      did: identity.did,
      host: "gitlawb",
      node,
      purpose: `GitLawb-hosted Aeon instance (${label})`,
      caps: capabilities,
      cap_token: serializeToken(token),
      cap_token_id: tokenId(token),
      cap_expires_at: token.payload.exp,
      cap_status: "active",
      created: iso(),
      last_renewed: iso(),
      issued_by: operator.did,
    };
    this.store.upsertInstance(entry);
    this.metrics?.record("spawn", { did: identity.did, label, node });
    return { identity, token, entry };
  }

  // The renewal loop — the actual off-switch. For every live instance, attempt
  // a gated renewal. Safety-critical caps require the safetyCheck to pass;
  // failure (or revocation) means we simply stop renewing and the capability
  // dies at its existing short expiry.
  async renewAll({ operator, ttlSeconds, activityFor }, safetyCheck) {
    const results = { renewed: [], denied: [] };

    for (const inst of this.store.listInstances()) {
      if (inst.host !== "gitlawb") continue;
      if (inst.cap_status === "revoked") {
        results.denied.push({ did: inst.did, reason: "revoked" });
        continue;
      }

      const activity = activityFor ? activityFor(inst.did) : undefined;
      const gatedCheck = (ctx) => safetyCheck({ ...ctx, activity });

      const res = await this.guard.renew(
        {
          priorToken: deserializeToken(inst.cap_token),
          issuer: operator,
          audienceDid: inst.did,
          capabilities: inst.caps,
          ttlSeconds,
        },
        gatedCheck,
      );

      if (res.renewed) {
        this.store.upsertInstance({
          did: inst.did,
          cap_token: serializeToken(res.token),
          cap_token_id: tokenId(res.token),
          cap_expires_at: res.token.payload.exp,
          cap_status: "active",
          last_renewed: iso(),
          last_renew_reason: "ok",
        });
        results.renewed.push({ did: inst.did, expiresAt: res.expiresAt });
      } else {
        this.store.upsertInstance({
          did: inst.did,
          cap_status: res.reason.startsWith("revoked") ? "revoked" : "not_renewed",
          last_renew_reason: res.reason,
        });
        results.denied.push({ did: inst.did, reason: res.reason });
      }
    }
    return results;
  }

  // Emergency brake: blocklist the identity and stop renewing it.
  kill(did, reason = "operator_kill") {
    this.revocations.revokeDid(did, reason);
    if (this.store.getInstance(did)) {
      this.store.upsertInstance({ did, cap_status: "revoked", last_renew_reason: reason });
    }
    this.metrics?.record("kill", { did, reason });
    return { did, reason };
  }

  // Run on every action sourced from a (untrusted) node event.
  authorize(serializedToken, requiredCap, { now = nowSec() } = {}) {
    return this.guard.authorize(deserializeToken(serializedToken), requiredCap, { now });
  }

  // Effective, time-aware status for reporting.
  statusOf(inst, now = nowSec()) {
    if (inst.cap_status === "revoked") return "revoked";
    if (now > inst.cap_expires_at) return "expired";
    if (inst.cap_status === "not_renewed") return "expiring";
    const soon = inst.caps.some((c) => isSafetyCritical(c.can));
    return soon && inst.cap_expires_at - now < 60 ? "expiring-soon" : "active";
  }

  // Mirror GitLawb instances into Aeon's memory/instances.json, preserving all
  // existing (GitHub/fork) entries. fleet-control branches on host:"gitlawb".
  syncToInstancesRegistry(instancesPath, now = nowSec()) {
    const reg = existsSync(instancesPath)
      ? JSON.parse(readFileSync(instancesPath, "utf8"))
      : { instances: [] };
    if (!Array.isArray(reg.instances)) reg.instances = [];

    for (const inst of this.store.listInstances()) {
      if (inst.host !== "gitlawb") continue;
      const mirror = {
        name: inst.name,
        repo: null,
        host: "gitlawb",
        node: inst.node,
        did: inst.did,
        purpose: inst.purpose,
        created: inst.created,
        health: this.statusOf(inst, now),
        cap_status: inst.cap_status,
        cap_expires_at: inst.cap_expires_at,
        archived: false,
      };
      const i = reg.instances.findIndex((x) => x.did === inst.did);
      if (i === -1) reg.instances.push(mirror);
      else reg.instances[i] = { ...reg.instances[i], ...mirror };
    }

    mkdirSync(dirname(instancesPath), { recursive: true });
    writeFileSync(instancesPath, JSON.stringify(reg, null, 2));
    return reg;
  }
}
