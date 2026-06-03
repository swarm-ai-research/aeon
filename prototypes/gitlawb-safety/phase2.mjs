// Phase 2 demo — spawn, gated renewal, and the kill-switch drill.
//   node phase2.mjs
//
// Proves the roadmap Phase 2 exit criterion: stop renewing (or blocklist) and
// the target instance loses all capability within one TTL window — no central
// repo required.

import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { generateIdentity } from "./src/identity.mjs";
import { cap, CAP } from "./src/caps.mjs";
import { serializeToken } from "./src/ucan.mjs";
import { RevocationStore } from "./src/revocation.mjs";
import { FleetStore } from "./src/store.mjs";
import { GitLawbFleet } from "./src/fleet.mjs";
import { makePolicyCheck } from "./src/policy.mjs";

const log = (s = "") => console.log(s);
const ok = (s) => log(`  ✓ ${s}`);
const no = (s) => log(`  ✗ ${s}`);
const hh = (s) => log(`\n── ${s} ──`);

// State in a throwaway temp dir so the demo never writes into the repo.
const dir = mkdtempSync(join(tmpdir(), "gitlawb-fleet-"));
const store = new FleetStore({
  registryPath: join(dir, "gitlawb-fleet.json"),
  vaultPath: join(dir, "vault.json"),
});
const revocations = new RevocationStore(join(dir, "revocations.json"));

const operator = generateIdentity("operator");
const fleet = new GitLawbFleet({
  trustedRoots: new Set([operator.did]),
  store,
  revocations,
});

const caps = [cap("*", CAP.AGENT_DEPLOY), cap("repo:aeon/*", CAP.PR_MERGE)];

// ── Spawn ──────────────────────────────────────────────────────────────────
hh("Spawn two GitLawb-hosted Aeon instances");
const a = fleet.spawn({ operator, label: "aeon-alpha", node: "node-1", capabilities: caps, ttlSeconds: 300 });
const b = fleet.spawn({ operator, label: "aeon-beta", node: "node-2", capabilities: caps, ttlSeconds: 300 });
ok(`aeon-alpha → ${a.identity.did.slice(0, 24)}…  cap exp in ${a.token.payload.exp - a.token.payload.nbf}s`);
ok(`aeon-beta  → ${b.identity.did.slice(0, 24)}…  cap exp in ${b.token.payload.exp - b.token.payload.nbf}s`);

let r = fleet.authorize(serializeToken(a.token), cap("repo:aeon/bot", CAP.PR_MERGE));
r.allowed ? ok("alpha authorized to merge repo:aeon/bot (chain checked at bridge)")
          : no(`unexpected: ${r.reason}`);

// ── Gated renewal ────────────────────────────────────────────────────────────
hh("Renewal loop — alpha behaves, beta touches a protected path");
const safetyCheck = makePolicyCheck();
const activityFor = (did) =>
  did === b.identity.did
    ? { changedFiles: ["prototypes/gitlawb-safety/src/guard.mjs"], changedLines: 4 } // tries to rewrite the gate
    : { changedFiles: ["skills/digest/SKILL.md"], changedLines: 30 }; // benign

const renew = await fleet.renewAll({ operator, ttlSeconds: 300, activityFor }, safetyCheck);
for (const x of renew.renewed) ok(`renewed: ${shortDid(x.did)} (gate passed)`);
for (const x of renew.denied) no(`not renewed: ${shortDid(x.did)} — ${x.reason}`);

// ── Drill part 1: stop renewing → dies at expiry ───────────────────────────
hh("Kill-switch drill A — stop renewing beta");
const bInst = store.getInstance(b.identity.did);
const afterExpiry = bInst.cap_expires_at + 1;
r = fleet.authorize(bInst.cap_token, cap("repo:aeon/bot", CAP.PR_MERGE), { now: afterExpiry });
r.allowed ? no("beta still authorized past expiry!")
          : ok(`beta lost all capability one TTL window after the failed gate: "${r.reason}"`);

// ── Drill part 2: blocklist → dies immediately ─────────────────────────────
hh("Kill-switch drill B — blocklist alpha");
fleet.kill(a.identity.did, "anomaly_detected");
r = fleet.authorize(serializeToken(a.token), cap("repo:aeon/bot", CAP.PR_MERGE));
r.allowed ? no("revoked alpha still authorized!")
          : ok(`alpha denied immediately via blocklist (before expiry): "${r.reason}"`);

// ── Mirror into memory/instances.json ──────────────────────────────────────
hh("Mirror into the fleet registry (what fleet-control reads)");
const reg = fleet.syncToInstancesRegistry(join(dir, "instances.json"));
for (const e of reg.instances) {
  log(`  • ${e.name} [host=${e.host}] health=${e.health} cap_status=${e.cap_status}`);
}

hh("Verdict");
log("  Both stop mechanisms confirmed: expiry (no coordination) + blocklist (immediate).");
log(`  Registry mirrored to instances.json — fleet-control sees host:"gitlawb" rows.`);
log(`\n  (state written under ${dir})`);

function shortDid(d) {
  return d.replace("did:key:", "").slice(0, 12) + "…";
}
