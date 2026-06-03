#!/usr/bin/env node
// fleet-cli — thin command line over GitLawbFleet, for the gitlawb-fleet skill.
//
//   node fleet-cli.mjs init
//   node fleet-cli.mjs spawn <label> [--node <id>] [--caps agent/deploy,pr/merge@repo:aeon/bot] [--ttl 300]
//   node fleet-cli.mjs renew [--activity <file.json>]
//   node fleet-cli.mjs kill <did> [reason]
//   node fleet-cli.mjs list
//   node fleet-cli.mjs sync
//
// Paths (overridable via env):
//   GITLAWB_REGISTRY   memory/gitlawb-fleet.json     (public, committable)
//   GITLAWB_REVOCATIONS memory/gitlawb-revocations.json (public, committable)
//   GITLAWB_VAULT      .gitlawb-vault/keys.json       (SECRET, gitignored)
//   GITLAWB_INSTANCES  memory/instances.json          (Aeon fleet registry)

import { readFileSync } from "node:fs";
import { generateIdentity } from "./src/identity.mjs";
import { cap } from "./src/caps.mjs";
import { RevocationStore } from "./src/revocation.mjs";
import { FleetStore } from "./src/store.mjs";
import { GitLawbFleet } from "./src/fleet.mjs";
import { makePolicyCheck } from "./src/policy.mjs";
import { makeReviewerGate } from "./src/reviewer-gate.mjs";
import { MetricsRecorder, aggregate, snapshotToMarkdown } from "./src/metrics.mjs";

const P = {
  registry: process.env.GITLAWB_REGISTRY ?? "memory/gitlawb-fleet.json",
  revocations: process.env.GITLAWB_REVOCATIONS ?? "memory/gitlawb-revocations.json",
  vault: process.env.GITLAWB_VAULT ?? ".gitlawb-vault/keys.json",
  instances: process.env.GITLAWB_INSTANCES ?? "memory/instances.json",
  metrics: process.env.GITLAWB_METRICS ?? "memory/gitlawb-metrics.jsonl",
  artifacts: process.env.GITLAWB_ARTIFACTS ?? "memory/gitlawb-runner",
};

// Look up an instance DID by name in the instances registry (used to route the
// renewal red-team to the reviewer agent). Returns null if absent/unreadable.
function findInstanceDid(instancesPath, name) {
  try {
    const raw = JSON.parse(readFileSync(instancesPath, "utf8"));
    const all = Array.isArray(raw.instances) ? raw.instances : [];
    return all.find((i) => i.name === name)?.did ?? null;
  } catch {
    return null;
  }
}

const OPERATOR_LABEL = "operator";
const WILDCARD_SAFE = new Set(["agent/deploy", "network/join"]);

function load() {
  const store = new FleetStore({ registryPath: P.registry, vaultPath: P.vault });
  const revocations = new RevocationStore(P.revocations);
  const metrics = new MetricsRecorder({ path: P.metrics });
  const operatorDid = store.getMeta().operator ?? null;
  const trustedRoots = new Set(operatorDid ? [operatorDid] : []);
  const fleet = new GitLawbFleet({ trustedRoots, store, revocations, metrics });
  return { store, revocations, metrics, fleet, operatorDid };
}

function flag(args, name, def) {
  const i = args.indexOf(`--${name}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
}

function parseCaps(spec) {
  // Capabilities are comma-separated. Abilities that can affect repo state
  // must be explicitly scoped as ability@resource, e.g.
  // "pr/merge@repo:aeon/bot,git/push@repo:aeon/docs".
  return spec
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean)
    .map((entry) => {
      const [ability, resource] = entry.split("@");
      if (resource) return cap(resource, ability);
      if (WILDCARD_SAFE.has(ability)) return cap("*", ability);
      throw new Error(`capability ${ability} requires an explicit @resource scope`);
    });
}

async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  const { store, fleet, metrics, operatorDid } = load();

  switch (cmd) {
    case "init": {
      if (operatorDid) {
        console.log(`OPERATOR_EXISTS ${operatorDid}`);
        return;
      }
      const op = generateIdentity(OPERATOR_LABEL);
      store.saveIdentity(op);
      store.setMeta({ operator: op.did, initialized: new Date().toISOString() });
      console.log(`OPERATOR_CREATED ${op.did}`);
      return;
    }

    case "spawn": {
      const label = args[0];
      if (!label) return fail("spawn requires a <label>");
      const operator = requireOperator(store, operatorDid);
      let capabilities;
      try {
        capabilities = parseCaps(flag(args, "caps", "agent/deploy"));
      } catch (e) {
        return fail(e.message);
      }
      const ttl = Number(flag(args, "ttl", "300"));
      const node = flag(args, "node", "unassigned");
      const { identity, entry } = fleet.spawn({ operator, label, node, capabilities, ttlSeconds: ttl });
      fleet.syncToInstancesRegistry(P.instances);
      console.log(`SPAWNED ${label} ${identity.did} cap_exp=${entry.cap_expires_at}`);
      return;
    }

    case "renew": {
      const operator = requireOperator(store, operatorDid);
      const activityFile = flag(args, "activity", null);
      const activityMap = activityFile ? JSON.parse(readFileSync(activityFile, "utf8")) : {};
      const activityFor = (did) => activityMap[did];
      // Renewal gate: cheap rule checks + an adversarial red-team routed to the
      // aeon-reviewer agent (true sub-swarm). The gate is fail-closed: a cap is
      // renewed only once a fresh reviewer verdict approves the activity; with
      // no reviewer in the registry it falls back to rules-only.
      const reviewerDid = findInstanceDid(P.instances, "aeon-reviewer");
      const redTeam = makeReviewerGate({ reviewerDid, artifactsDir: P.artifacts });
      if (redTeam) console.log(`REDTEAM enabled (routed to ${reviewerDid})`);
      const res = await fleet.renewAll({ operator, ttlSeconds: 300, activityFor }, makePolicyCheck({ redTeam }));
      fleet.syncToInstancesRegistry(P.instances);
      console.log(`RENEWED ${res.renewed.length} DENIED ${res.denied.length}`);
      for (const d of res.denied) console.log(`  denied ${d.did} ${d.reason}`);
      return;
    }

    case "kill": {
      const did = args[0];
      if (!did) return fail("kill requires a <did>");
      fleet.kill(did, args[1] ?? "operator_kill");
      fleet.syncToInstancesRegistry(P.instances);
      console.log(`KILLED ${did}`);
      return;
    }

    case "list": {
      for (const inst of store.listInstances()) {
        console.log(`${fleet.statusOf(inst).padEnd(14)} ${inst.name.padEnd(16)} ${inst.did}`);
      }
      return;
    }

    case "sync": {
      const reg = fleet.syncToInstancesRegistry(P.instances);
      console.log(`SYNCED ${reg.instances.filter((x) => x.host === "gitlawb").length} gitlawb instances`);
      return;
    }

    case "metrics": {
      // Emit a dashboard-ready snapshot. The gitlawb-fleet-metrics skill pipes
      // this markdown to ./notify (which fans out + renders via notify-jsonrender).
      const windowHours = Number(flag(args, "hours", "24"));
      const instances = store.listInstances().map((i) => ({ ...i, status: fleet.statusOf(i) }));
      const snapshot = aggregate(metrics.all(), { windowSeconds: windowHours * 3600, instances });
      console.log(snapshotToMarkdown(snapshot));
      return;
    }

    default:
      return fail(`unknown command: ${cmd ?? "(none)"}`);
  }
}

function requireOperator(store, operatorDid) {
  if (!operatorDid) {
    fail("no operator — run `node fleet-cli.mjs init` first");
    process.exit(1);
  }
  const op = store.loadIdentity(operatorDid);
  if (!op) {
    fail("operator key missing from vault");
    process.exit(1);
  }
  return op;
}

function fail(msg) {
  console.error(`ERROR: ${msg}`);
  process.exitCode = 1;
}

main();
