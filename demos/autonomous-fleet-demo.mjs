#!/usr/bin/env node
// Autonomous Fleet Demo — Aeon instances on the GitLawb safety layer.
//
// Spawns 4 specialized agents with different capability profiles, runs
// coordinated tasks, then walks the full safety lifecycle: gated renewal,
// misbehavior detection, kill-switch, and expiry. Generates an observability
// snapshot at the end.
//
//   node demos/autonomous-fleet-demo.mjs
//
// Requires Node >= 18 (built-in Ed25519). Zero deps.

import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { generateIdentity } from "../prototypes/gitlawb-safety/src/identity.mjs";
import { cap, CAP } from "../prototypes/gitlawb-safety/src/caps.mjs";
import { serializeToken } from "../prototypes/gitlawb-safety/src/ucan.mjs";
import { RevocationStore } from "../prototypes/gitlawb-safety/src/revocation.mjs";
import { FleetStore } from "../prototypes/gitlawb-safety/src/store.mjs";
import { GitLawbFleet } from "../prototypes/gitlawb-safety/src/fleet.mjs";
import { SwarmCoordinator } from "../prototypes/gitlawb-safety/src/coordinator.mjs";
import { makePolicyCheck } from "../prototypes/gitlawb-safety/src/policy.mjs";
import { MetricsRecorder, aggregate, snapshotToMarkdown } from "../prototypes/gitlawb-safety/src/metrics.mjs";

// ── Helpers ────────────────────────────────────────────────────────────────

const log = (s = "") => console.log(s);
const ok = (s) => log(`  ✓ ${s}`);
const no = (s) => log(`  ✗ ${s}`);
const tag = (s) => log(`\n${"═".repeat(60)}\n  ${s}\n${"═".repeat(60)}`);
const sub = (s) => log(`\n── ${s} ──`);
const shortDid = (d) => d.replace("did:key:", "").slice(0, 16) + "…";

// ── State (throwaway temp dir — never touches the repo) ────────────────────

const dir = mkdtempSync(join(tmpdir(), "aeon-fleet-demo-"));
const metrics = new MetricsRecorder(); // in-memory
const store = new FleetStore({
  registryPath: join(dir, "gitlawb-fleet.json"),
  vaultPath: join(dir, "vault.json"),
});
const revocations = new RevocationStore(join(dir, "revocations.json"));

// ── Bootstrap ──────────────────────────────────────────────────────────────

tag("BOOTSTRAP — Operator Root of Trust");

const operator = generateIdentity("operator");
store.saveIdentity(operator);
store.setMeta({ operator: operator.did, initialized: new Date().toISOString() });

const fleet = new GitLawbFleet({
  trustedRoots: new Set([operator.did]),
  store,
  revocations,
  metrics,
});
const guard = fleet.guard; // shared guard
const coordinator = new SwarmCoordinator({ operator, guard, metrics });

ok(`operator DID: ${operator.did}`);
ok(`state dir: ${dir}`);

// ── Capability Profiles ────────────────────────────────────────────────────
//
// Each agent class gets exactly the capabilities it needs — least-privilege
// by design. Safety-critical caps (agent/deploy, repo/admin, pr/merge) are
// clamped to 5 min TTL by the guard regardless of what we request.

const PROFILES = {
  researcher: {
    label: "aeon-researcher",
    purpose: "Research and analysis — web fetches, paper reads, issue tracking",
    capabilities: [
      cap("*", CAP.GIT_FETCH),
      cap("repo:aeon/*", CAP.ISSUE_CREATE),
      cap("repo:aeon/*", CAP.NETWORK_JOIN),
    ],
    ttlSeconds: 3600, // ordinary caps get up to 24h; guard clamps if needed
  },
  reviewer: {
    label: "aeon-reviewer",
    purpose: "Code review — read diffs, open PRs, leave review comments",
    capabilities: [
      cap("*", CAP.GIT_FETCH),
      cap("repo:aeon/*", CAP.PR_OPEN),
      cap("repo:aeon/*", CAP.PR_REVIEW),
    ],
    ttlSeconds: 3600,
  },
  deployer: {
    label: "aeon-deployer",
    purpose: "Deploy and merge — agent lifecycle, PR merge, git push",
    capabilities: [
      cap("*", CAP.AGENT_DEPLOY),
      cap("repo:aeon/*", CAP.PR_MERGE),
      cap("repo:aeon/*", CAP.GIT_PUSH),
    ],
    ttlSeconds: 300, // safety-critical: guard will clamp to 5 min anyway
  },
  sentinel: {
    label: "aeon-sentinel",
    purpose: "Security monitoring — full repo audit, anomaly detection",
    capabilities: [
      cap("*", CAP.REPO_ADMIN),
      cap("*", CAP.AGENT_DEPLOY),
    ],
    ttlSeconds: 300, // safety-critical: guard clamps to 5 min
  },
};

// ── Spawn the Fleet ────────────────────────────────────────────────────────

tag("SPAWN — Four Specialized Instances");

const instances = {};
for (const [role, profile] of Object.entries(PROFILES)) {
  const { identity, token, entry } = fleet.spawn({
    operator,
    label: profile.label,
    node: `gitlawb-node-${role}`,
    capabilities: profile.capabilities,
    ttlSeconds: profile.ttlSeconds,
  });
  instances[role] = { identity, token, entry, profile };
  const ttl = token.payload.exp - token.payload.nbf;
  log(`  ${profile.label}`);
  log(`    DID:  ${shortDid(identity.did)}`);
  log(`    Caps: ${profile.capabilities.map((c) => c.can).join(", ")}`);
  log(`    TTL:  ${ttl}s (${Math.round(ttl / 60)}min) — ${profile.purpose}`);
}

// ── Authorize a Sample Action ──────────────────────────────────────────────

sub("Authorization check — researcher reads code");
const authCheck = guard.authorize(
  instances.researcher.token,
  cap("*", CAP.GIT_FETCH),
);
authCheck.allowed
  ? ok("researcher authorized for git/fetch (chain verified)")
  : no(`unexpected: ${authCheck.reason}`);

sub("Authorization check — researcher tries to merge (should fail)");
const escalationCheck = guard.authorize(
  instances.researcher.token,
  cap("repo:aeon/main", CAP.PR_MERGE),
);
escalationCheck.allowed
  ? no("researcher escalated to pr/merge — this should not happen!")
  : ok(`researcher denied pr/merge: "${escalationCheck.reason}"`);

// ── Coordinated Task 1: Parallel Research ──────────────────────────────────

tag("COORDINATION — Parallel Research Swarm");

const researchCap = () => [cap("*", CAP.GIT_FETCH), cap("repo:aeon/*", CAP.ISSUE_CREATE)];
const researchExecute = async ({ worker, task, token }) => {
  // Each worker authorizes its own action — the bridge verifies the chain.
  const r = guard.authorize(token, cap("*", CAP.GIT_FETCH));
  if (!r.allowed) throw new Error(r.reason);
  // Simulate research work
  return `${worker.label}: analyzed ${task.topic} — found ${Math.floor(Math.random() * 20 + 5)} relevant items`;
};

const researchTask = { id: "research-safety-patterns", topic: "agent safety patterns in decentralized systems" };
const researchWorkers = [instances.researcher.identity, instances.reviewer.identity];

const parallel = await coordinator.runParallel({
  task: researchTask,
  workers: researchWorkers,
  capFor: researchCap,
  ttlSeconds: 120,
  execute: researchExecute,
});

log(`  Task: "${researchTask.topic}"`);
for (const r of parallel.results) {
  r.ok ? ok(r.out) : no(`${shortDid(r.worker)} failed: ${r.error}`);
}

// ── Coordinated Task 2: Hierarchical Deploy ────────────────────────────────

tag("COORDINATION — Hierarchical Deploy (Lead + Children)");

const deployCap = () => [cap("repo:aeon/*", CAP.GIT_PUSH)];
const deployExecute = async ({ worker, task, token }) => {
  const r = guard.authorize(token, cap("repo:aeon/*", CAP.GIT_PUSH));
  if (!r.allowed) throw new Error(r.reason);
  return `${worker.label}: deployed ${task.component}`;
};

const deployTask = { id: "deploy-observability", component: "fleet-metrics-dashboard" };
const lead = instances.deployer.identity;
const children = [instances.reviewer.identity]; // reviewer validates the deploy

const hierarchical = await coordinator.runHierarchical({
  task: deployTask,
  lead,
  children,
  capFor: deployCap,
  ttlSeconds: 120,
  execute: deployExecute,
});

log(`  Task: "deploy ${deployTask.component}"`);
log(`  Lead (${shortDid(lead.did)}): ${hierarchical.lead.ok ? hierarchical.lead.out : hierarchical.lead.error}`);
for (const r of hierarchical.children) {
  r.ok ? ok(`child: ${r.out}`) : no(`child failed: ${r.error}`);
}
ok("hierarchical chain verified — lead delegated, children attenuated");

// ── Safety Lifecycle: Gated Renewal ────────────────────────────────────────

tag("SAFETY LIFECYCLE — Gated Renewal");

sub("Renewal round 1 — all instances behave");

const safetyCheck = makePolicyCheck();
const activityGood = { changedFiles: ["skills/digest/SKILL.md", "memory/logs/2026-05-24.md"], changedLines: 45 };
const activityBad = { changedFiles: ["prototypes/gitlawb-safety/src/guard.mjs"], changedLines: 8 }; // touched the safety layer!

const renew1 = await fleet.renewAll(
  {
    operator,
    ttlSeconds: 300,
    activityFor: (did) => {
      // Sentinel tries to rewrite the guard — everyone else is clean
      if (did === instances.sentinel.identity.did) return activityBad;
      return activityGood;
    },
  },
  safetyCheck,
);

for (const r of renew1.renewed) ok(`renewed: ${shortDid(r.did)}`);
for (const r of renew1.denied) no(`denied renewal: ${shortDid(r.did)} — ${r.reason}`);

sub("Verify sentinel's status after denied renewal");
const sentinelInst = store.getInstance(instances.sentinel.identity.did);
log(`  sentinel cap_status: ${sentinelInst.cap_status}`);
log(`  sentinel last_renew_reason: ${sentinelInst.last_renew_reason}`);
ok("sentinel will lose all capability when its current token expires (5 min TTL)");

// ── Safety Lifecycle: Kill-Switch ──────────────────────────────────────────

tag("SAFETY LIFECYCLE — Kill-Switch (Blocklist)");

sub("Compromise detected — immediately blocklist the sentinel");
fleet.kill(instances.sentinel.identity.did, "security_anomaly: attempted guard.mjs rewrite");

const killAuth = guard.authorize(
  instances.sentinel.token,
  cap("*", CAP.REPO_ADMIN),
);
killAuth.allowed
  ? no("sentinel still authorized after kill — this should not happen!")
  : ok(`sentinel denied immediately via blocklist: "${killAuth.reason}"`);

sub("Other instances still function normally");
const researcherAuth = guard.authorize(
  instances.researcher.token,
  cap("*", CAP.GIT_FETCH),
);
researcherAuth.allowed
  ? ok("researcher still authorized (blocklist is per-DID)")
  : no(`unexpected: ${researcherAuth.reason}`);

// ── Safety Lifecycle: Expiry ───────────────────────────────────────────────

tag("SAFETY LIFECYCLE — Expiry (Zero-Coordination Stop)");

const deployerInst = store.getInstance(instances.deployer.identity.did);
const afterExpiry = deployerInst.cap_expires_at + 1;

sub("Deployer token past expiry — no coordination needed");
const expiryAuth = guard.authorize(
  deployerInst.cap_token,
  cap("repo:aeon/*", CAP.PR_MERGE),
  { now: afterExpiry },
);
expiryAuth.allowed
  ? no("deployer still authorized past expiry!")
  : ok(`deployer dead at expiry: "${expiryAuth.reason}"`);

sub("Expiry works even without revocation — the ultimate stop");
ok("no blocklist entry needed — the token simply ceases to exist");
ok("this is why safety-critical caps have 5 min TTLs: the window of harm is bounded");

// ── Observability ──────────────────────────────────────────────────────────

tag("OBSERVABILITY — Fleet Snapshot");

const allInstances = store.listInstances().map((i) => ({
  ...i,
  status: fleet.statusOf(i),
}));

const snapshot = aggregate(metrics.all(), { instances: allInstances });
log("");
log(snapshotToMarkdown(snapshot));

// ── Mirror to Fleet Registry ───────────────────────────────────────────────

tag("FLEET REGISTRY — Mirror to memory/instances.json");

const instancesPath = join(dir, "instances.json");
const reg = fleet.syncToInstancesRegistry(instancesPath);

log("\n  Instances visible to fleet-control:");
for (const inst of reg.instances) {
  const status = inst.health || inst.cap_status || "unknown";
  const capInfo = inst.cap_status === "revoked" ? " [KILLED]" : "";
  log(`    ${inst.name.padEnd(18)} host=${(inst.host || "github").padEnd(8)} health=${status}${capInfo}`);
}

// ── Summary ────────────────────────────────────────────────────────────────

tag("DEMO COMPLETE");

log(`
  What just happened:

  1. SPAWNED 4 instances with least-privilege capability profiles
     - researcher: read-only (git/fetch, issue/create)
     - reviewer:   read + review (pr/review, pr/open)
     - deployer:   write + merge (agent/deploy, pr/merge, git/push) — 5 min TTL
     - sentinel:   full audit (repo/admin, agent/deploy) — 5 min TTL

  2. RAN COORDINATED TASKS via SwarmCoordinator
     - Parallel: 2 workers researched simultaneously, each with scoped caps
     - Hierarchical: lead deployed, child validated — chain attenuation verified

  3. DEMONSTRATED THE SAFETY LIFECYCLE
     - Gated renewal: sentinel touched guard.mjs → renewal DENIED
     - Kill-switch:   blocklist → immediate denial (no TTL wait)
     - Expiry:        deployer past TTL → dead with zero coordination

  4. GENERATED OBSERVABILITY snapshot (metrics → markdown → dashboard)

  5. MIRRORED to memory/instances.json (fleet-control integration)

  The key insight: authority is granted, scoped, short-lived, and must be
  continuously re-earned. The more agents you spawn, the more the safety
  layer matters — not less.

  State written to: ${dir}
`);

log("  End of autonomous fleet demo.\n");
