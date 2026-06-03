// Phase 5 demo — observability + coordination on the capability layer.
//   node phase5.mjs
//
// Exit criterion: a multi-agent GitLawb fleet is observable (a metrics snapshot
// fit for Aeon's dashboard) and steerable (coordinated runs where every
// sub-task gets a least-privilege, self-expiring capability).

import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { generateIdentity } from "./src/identity.mjs";
import { cap, CAP } from "./src/caps.mjs";
import { RevocationStore } from "./src/revocation.mjs";
import { FleetStore } from "./src/store.mjs";
import { GitLawbFleet } from "./src/fleet.mjs";
import { SelfEvolutionGate } from "./src/evolution.mjs";
import { SwarmCoordinator } from "./src/coordinator.mjs";
import { MetricsRecorder, aggregate, snapshotToMarkdown } from "./src/metrics.mjs";

const log = (s = "") => console.log(s);
const hh = (s) => log(`\n── ${s} ──`);

const dir = mkdtempSync(join(tmpdir(), "gitlawb-p5-"));
const metrics = new MetricsRecorder(); // in-memory for the demo
const store = new FleetStore({ registryPath: join(dir, "fleet.json"), vaultPath: join(dir, "vault.json") });
const revocations = new RevocationStore(join(dir, "rev.json"));

const operator = generateIdentity("operator");
const fleet = new GitLawbFleet({ trustedRoots: new Set([operator.did]), store, revocations, metrics });
const guard = fleet.guard; // shared guard (same metrics, roots, revocations)
const gate = new SelfEvolutionGate({ operator, guard, redTeam: async () => ({ pass: true }), metrics });
const coordinator = new SwarmCoordinator({ operator, guard, metrics });

const baseCaps = [cap("*", CAP.AGENT_DEPLOY), cap("repo:aeon/*", CAP.PR_MERGE), cap("repo:aeon/*", CAP.GIT_PUSH)];

// ── Generate fleet activity ────────────────────────────────────────────────
hh("Driving the fleet (spawn · renew · kill · review · merge)");
const a = fleet.spawn({ operator, label: "aeon-a", node: "n1", capabilities: baseCaps, ttlSeconds: 300 });
const b = fleet.spawn({ operator, label: "aeon-b", node: "n2", capabilities: baseCaps, ttlSeconds: 300 });
const c = fleet.spawn({ operator, label: "aeon-c", node: "n3", capabilities: baseCaps, ttlSeconds: 300 });

await fleet.renewAll(
  {
    operator,
    ttlSeconds: 300,
    activityFor: (did) =>
      did === b.identity.did
        ? { changedFiles: ["prototypes/gitlawb-safety/src/guard.mjs"], changedLines: 2 } // will be refused
        : { changedFiles: ["skills/digest/SKILL.md"], changedLines: 20 },
  },
  (await import("./src/policy.mjs")).makePolicyCheck(),
);

fleet.kill(c.identity.did, "anomaly_detected");

const proposal = { repo: "aeon/bot", ref: "refs/heads/main", agentDid: a.identity.did, changedFiles: ["skills/digest/SKILL.md"], changedLines: 20, diffDigest: "sha256:aa" };
const review = await gate.review(proposal);
gate.authorizeMerge({ token: review.mergeToken, proposal }); // allow
gate.authorizeMerge({ token: review.mergeToken, proposal: { ...proposal, diffDigest: "sha256:bb" } }); // reuse → deny
await gate.review({ ...proposal, changedFiles: ["prototypes/gitlawb-safety/src/guard.mjs"] }); // refused at policy
log("  fleet exercised — events recorded");

// ── Coordination on the capability layer ────────────────────────────────────
hh("Coordinated runs — each sub-task gets a scoped, self-expiring cap");
const pushCap = () => [cap("repo:aeon/bot", CAP.GIT_PUSH)];
const execute = async ({ token }) => {
  const r = guard.authorize(token, cap("repo:aeon/bot", CAP.GIT_PUSH));
  if (!r.allowed) throw new Error(r.reason);
  return "ok";
};

const par = await coordinator.runParallel({ task: { id: "reindex" }, workers: [a.identity, b.identity], capFor: pushCap, execute });
log(`  parallel "reindex": ${par.results.filter((r) => r.ok).length}/${par.results.length} workers succeeded`);

const hier = await coordinator.runHierarchical({ task: { id: "migrate" }, lead: a.identity, children: [b.identity], capFor: pushCap, execute });
log(`  hierarchical "migrate": lead ${hier.lead.ok ? "ok" : "fail"}, children ${hier.children.filter((r) => r.ok).length}/${hier.children.length} (delegated chain verified)`);

// ── Observability snapshot (what the gitlawb-fleet-metrics skill emits) ──────
hh("Observability snapshot → ./notify → dashboard");
const instances = store.listInstances().map((i) => ({ ...i, status: fleet.statusOf(i) }));
const snapshot = aggregate(metrics.all(), { instances });
log("");
log(snapshotToMarkdown(snapshot));
log(`\n  (state under ${dir})`);
