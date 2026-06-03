#!/usr/bin/env node
// fleet-heal — Self-healing loop for the GitLawb fleet.
//
//   node prototypes/gitlawb-safety/fleet-heal.mjs [--dry-run]
//
// Reads fleet health from memory/instances.json, detects degraded/expired/killed
// instances, and takes corrective action:
//   1. Reconstructs activity from task runner logs (synthetic activity feed)
//   2. Adjusts trust scores based on task completion rates
//   3. Attempts renewal with synthetic activity for degraded instances
//   4. Respawns expired instances with fresh identities
//   5. Escalates safety violations to the operator

import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { spawnSync } from "node:child_process";
import { makePolicyCheck } from "./src/policy.mjs";
import { makeReviewerGate } from "./src/reviewer-gate.mjs";

// ── Config ──────────────────────────────────────────────────────────────────

const INSTANCES_PATH = join(process.cwd(), "memory/instances.json");
const RUNNER_ARTIFACTS = join(process.cwd(), "memory/gitlawb-runner");
const HEAL_LOG = join(process.cwd(), "memory/fleet-heal-log.json");
const FLEET_DIR = join(homedir(), ".gitlawb", "fleet");
const OPERATOR_DIR = join(homedir(), ".gitlawb"); // operator identity (issues renewal UCANs)
const NODE = "https://node.gitlawb.com";

// Renewal is operator-granted: after the safety gate passes, the operator
// re-delegates each capability with a fresh expiry via `gl ucan delegate`. The
// resource the caps are scoped to (the fleet's repo namespace).
const REPO_RESOURCE =
  process.env.GITLAWB_REPO_URL ??
  "gitlawb://did:key:z6MkpiXbCJzXGLw9bQXw5t8ja734YsrhYWEQMqsicwUcjHbH/aeon";
const RENEW_EXPIRY_HOURS = Number(process.env.GITLAWB_RENEW_HOURS || 168); // 7d default

const DRY_RUN = process.argv.includes("--dry-run");

// ── Helpers ─────────────────────────────────────────────────────────────────

const log = (msg) => console.log(`[fleet-heal] ${msg}`);
const now = () => new Date().toISOString();
const nowSec = () => Math.floor(Date.now() / 1000);

function loadJSON(path) {
  try { return JSON.parse(readFileSync(path, "utf8")); } catch { return null; }
}

function saveJSON(path, data) {
  writeFileSync(path, JSON.stringify(data, null, 2) + "\n");
}

// `args` is an array — passed to gl WITHOUT a shell, so values like DIDs,
// labels, or reasons can't break out into shell interpretation (no injection
// via interpolation). Returns trimmed stdout, or null on non-zero exit.
const gl = (args, dir) => {
  const proc = spawnSync("gl", args, {
    encoding: "utf8",
    cwd: dir || process.cwd(),
    env: { ...process.env, GITLAWB_NODE: NODE },
  });
  return proc.status === 0 ? (proc.stdout || "").trim() : null;
};

// ── Activity Reconstruction ─────────────────────────────────────────────────
// Build synthetic activity map from task runner artifacts.
// The policy check needs {changedFiles, changedLines} per agent.

function reconstructActivity() {
  const activity = {};
  if (!existsSync(RUNNER_ARTIFACTS)) return activity;

  const files = readdirSync(RUNNER_ARTIFACTS).filter(f => f.endsWith(".json"));
  const cutoff = Date.now() - 24 * 60 * 60 * 1000; // last 24h

  for (const file of files) {
    const artifact = loadJSON(join(RUNNER_ARTIFACTS, file));
    if (!artifact || !artifact.task || !artifact.instance) continue;

    const ts = new Date(artifact.processed_at || artifact.timestamp || 0).getTime();
    if (ts < cutoff) continue;

    const did = artifact.instance.did;
    if (!activity[did]) {
      activity[did] = { changedFiles: [], changedLines: 0, tasks: 0, successes: 0 };
    }

    activity[did].tasks++;
    if (artifact.task.status === "completed") {
      activity[did].successes++;
    }

    // Infer changed files from task kind and result
    const kind = artifact.task.kind;
    if (kind === "research") {
      activity[did].changedFiles.push("memory/issues/");
      activity[did].changedLines += 50;
    } else if (kind === "code-review") {
      activity[did].changedFiles.push("memory/issues/");
      activity[did].changedLines += 30;
    } else if (kind === "deploy") {
      activity[did].changedFiles.push("demos/", "memory/gitlawb-runner/");
      activity[did].changedLines += 100;
    } else if (kind === "audit") {
      activity[did].changedFiles.push("memory/issues/");
      activity[did].changedLines += 40;
    }
  }

  // Deduplicate files
  for (const did of Object.keys(activity)) {
    activity[did].changedFiles = [...new Set(activity[did].changedFiles)];
  }

  return activity;
}

// ── Trust Score Adjustment ──────────────────────────────────────────────────
// Increment on success, decrement on failure. Auto-kill below threshold.

function adjustTrust(inst, activity) {
  const did = inst.did;
  const agentActivity = activity[did];
  const oldTrust = inst.trust || 0.05;
  let newTrust = oldTrust;
  let action = null;

  if (agentActivity) {
    const rate = agentActivity.tasks > 0 ? agentActivity.successes / agentActivity.tasks : 0;

    if (rate >= 0.8 && agentActivity.tasks >= 3) {
      // Successful agent — increment trust
      newTrust = Math.min(1.0, oldTrust + 0.01);
      if (newTrust > oldTrust) action = "trust_increased";
    } else if (rate < 0.5 && agentActivity.tasks >= 3) {
      // Failing agent — decrement trust
      newTrust = Math.max(0.0, oldTrust - 0.05);
      if (newTrust < 0.01) {
        action = "trust_critical_will_kill";
      } else if (newTrust < oldTrust) {
        action = "trust_decreased";
      }
    }
  }

  // Check renewal history
  const consecutiveFailures = inst.consecutive_renewal_failures || 0;
  if (consecutiveFailures >= 3 && newTrust > 0.01) {
    newTrust = Math.max(0.01, newTrust - 0.10);
    action = "trust_decreased_renewal_failures";
  }

  return { oldTrust, newTrust, action };
}

// ── Health Classification ───────────────────────────────────────────────────

function classifyHealth(inst) {
  const capStatus = inst.cap_status || "unknown";
  const expiresAt = inst.cap_expires_at ? new Date(inst.cap_expires_at).getTime() / 1000 : 0;
  const now = nowSec();

  if (capStatus === "revoked") return "killed";
  if (capStatus === "expired" || (expiresAt > 0 && now > expiresAt)) return "expired";
  if (capStatus === "not_renewed") return "degraded";
  if (capStatus === "expiring" || (expiresAt > 0 && expiresAt - now < 120)) return "expiring";
  if (capStatus === "active" && inst.health === "active") return "healthy";
  if (inst.trust && inst.trust < 0.02) return "untrusted";
  return "healthy";
}

// ── Recovery Actions ────────────────────────────────────────────────────────

// "x:y" capability → "x/y" form the gate + gl expect.
const capToCan = (cap) => String(cap).replace(":", "/");

async function attemptRenewal(inst, operator, activityData, reviewerDid) {
  log(`Attempting renewal for ${inst.name} (${inst.did.slice(0, 25)}...)`);

  // ── 1. DECIDE — run the safety gate in-process (no vault/operator store) ──
  // Cheap rule checks first, then the reviewer-routed red-team. Same gate as
  // before, but called directly so renewal no longer depends on fleet-cli's
  // separate FleetStore (which is never populated in CI → always exit(1)).
  const ctx = {
    audienceDid: inst.did,
    purpose: inst.purpose,
    capabilities: (inst.capabilities || []).map((c) => ({ can: capToCan(c) })),
    activity: {
      changedFiles: activityData.changedFiles || [],
      changedLines: activityData.changedLines || 0,
    },
  };
  // In dry-run, skip the red-team (it dispatches a real review task via gl) and
  // exercise only the side-effect-free rule checks.
  const redTeam = DRY_RUN ? null : makeReviewerGate({ reviewerDid, artifactsDir: RUNNER_ARTIFACTS, node: NODE });
  const verdict = await makePolicyCheck({ redTeam })(ctx);
  if (!verdict.pass) {
    log(`  Renewal gate DENIED: ${verdict.reason}${verdict.findings ? ` (${verdict.findings})` : ""}`);
    return { renewed: false, reason: verdict.reason };
  }
  log(`  Renewal gate PASSED${verdict.reason ? ` (${verdict.reason})` : ""}`);

  if (DRY_RUN) {
    log(`  [dry-run] Would re-delegate ${(inst.capabilities || []).length} caps via gl`);
    return { renewed: true, dryRun: true };
  }

  // ── 2. ACT — operator re-grants each capability with a fresh expiry ──
  for (const cap of inst.capabilities || []) {
    const out = gl(
      ["ucan", "delegate", "--to", inst.did, "--cap", REPO_RESOURCE, "--can", capToCan(cap),
       "--expiry", String(RENEW_EXPIRY_HOURS), "--dir", OPERATOR_DIR],
    );
    if (out === null) {
      log(`  Delegate FAILED for ${cap}`);
      return { renewed: false, reason: `delegate_failed:${cap}` };
    }
  }
  const newExpiry = new Date(Date.now() + RENEW_EXPIRY_HOURS * 3600 * 1000).toISOString();
  log(`  Renewed ${inst.capabilities.length} caps via gl (expiry → ${newExpiry})`);
  return { renewed: true, capExpiresAt: newExpiry };
}

function respawnAgent(inst, operator) {
  log(`Respawning ${inst.name} (old DID: ${inst.did.slice(0, 25)}...)`);

  if (DRY_RUN) {
    log(`  [dry-run] Would kill old DID and spawn new identity for ${inst.name}`);
    return { respawned: true, dryRun: true };
  }

  // Kill old identity
  gl(["agent", "kill", inst.did, "--reason", "self-heal: respawn", "--yes"], FLEET_DIR);

  // Spawn new identity with same capabilities
  const caps = (inst.capabilities || []).join(",");
  const spawnResult = gl(["agent", "spawn", inst.name, "--capabilities", caps], FLEET_DIR);

  if (!spawnResult) {
    log(`  Respawn failed`);
    return { respawned: false, error: "spawn failed" };
  }

  // Register the new agent
  const regResult = gl(["register", "--dir", join(FLEET_DIR, inst.name), "--capabilities", caps], FLEET_DIR);

  log(`  Respawned: new identity registered`);
  return { respawned: true, result: regResult };
}

// ── Main Healing Loop ───────────────────────────────────────────────────────

async function heal() {
  log("Starting fleet health check...");

  const instances = loadJSON(INSTANCES_PATH);
  if (!instances || !instances.instances || instances.instances.length === 0) {
    log("No instances found. Nothing to heal.");
    return { healed: 0, actions: [], total: 0 };
  }

  // The renewal red-team routes to the reviewer agent; find its DID once.
  const reviewerDid = instances.instances.find((i) => i.name === "aeon-reviewer")?.did ?? null;

  const activity = reconstructActivity();
  const actions = [];
  let healed = 0;

  for (const inst of instances.instances) {
    const health = classifyHealth(inst);
    const { oldTrust, newTrust, action: trustAction } = adjustTrust(inst, activity);

    // Update trust
    if (trustAction) {
      inst.trust = newTrust;
      actions.push({ name: inst.name, action: trustAction, oldTrust, newTrust });
    }

    // Take action based on health
    switch (health) {
      case "healthy":
        // Update task stats from activity
        const agentActivity = activity[inst.did];
        if (agentActivity) {
          inst.tasks_completed = (inst.tasks_completed || 0) + agentActivity.successes;
          inst.tasks_failed = (inst.tasks_failed || 0) + (agentActivity.tasks - agentActivity.successes);
        }
        inst.health = "active";
        inst.last_checked = now();
        break;

      case "expiring":
        // Attempt renewal with synthetic activity
        const renewResult = await attemptRenewal(inst, instances.operator, activity[inst.did] || {}, reviewerDid);
        if (renewResult.renewed) {
          inst.health = "active";
          inst.cap_status = "active";
          if (renewResult.capExpiresAt) inst.cap_expires_at = renewResult.capExpiresAt;
          inst.consecutive_renewal_failures = 0;
          actions.push({ name: inst.name, action: "renewed" });
          healed++;
        } else {
          inst.consecutive_renewal_failures = (inst.consecutive_renewal_failures || 0) + 1;
          actions.push({ name: inst.name, action: "renewal_failed", reason: renewResult.reason });
        }
        inst.last_checked = now();
        break;

      case "degraded":
        // Try renewal, escalate if repeated
        const failures = inst.consecutive_renewal_failures || 0;
        if (failures < 3) {
          const degResult = await attemptRenewal(inst, instances.operator, activity[inst.did] || {}, reviewerDid);
          if (degResult.renewed) {
            inst.health = "active";
            inst.cap_status = "active";
            if (degResult.capExpiresAt) inst.cap_expires_at = degResult.capExpiresAt;
            inst.consecutive_renewal_failures = 0;
            actions.push({ name: inst.name, action: "recovered" });
            healed++;
          } else {
            inst.consecutive_renewal_failures = failures + 1;
            actions.push({ name: inst.name, action: "renewal_failed", reason: degResult.reason, failures: failures + 1 });
          }
        } else {
          // 3+ consecutive failures — escalate to operator
          inst.health = "degraded";
          inst.next_action = "operator_intervention_required";
          actions.push({ name: inst.name, action: "escalated", failures });
        }
        inst.last_checked = now();
        break;

      case "expired":
        // Respawn with fresh identity
        const respResult = respawnAgent(inst, instances.operator);
        if (respResult.respawned) {
          inst.health = "active";
          inst.cap_status = "active";
          inst.consecutive_renewal_failures = 0;
          inst.trust = 0.05; // reset trust on respawn
          actions.push({ name: inst.name, action: "respawned" });
          healed++;
        } else {
          inst.health = "unreachable";
          inst.next_action = "manual_respawn_required";
          actions.push({ name: inst.name, action: "respawn_failed" });
        }
        inst.last_checked = now();
        break;

      case "killed":
        // Already dead — nothing to do, log it
        actions.push({ name: inst.name, action: "dead", reason: "revoked" });
        inst.last_checked = now();
        break;

      case "untrusted":
        // Trust too low — auto-kill
        if (!DRY_RUN) {
          gl(["agent", "kill", inst.did, "--reason", `self-heal: trust below threshold (${newTrust})`, "--yes"], FLEET_DIR);
        }
        inst.cap_status = "revoked";
        inst.health = "killed";
        actions.push({ name: inst.name, action: "auto_killed_low_trust", trust: newTrust });
        healed++;
        inst.last_checked = now();
        break;
    }
  }

  // Save updated instances
  if (!DRY_RUN) {
    saveJSON(INSTANCES_PATH, instances);
  }

  // Append to heal log
  const logEntry = { timestamp: now(), actions, healed, dryRun: DRY_RUN };
  const healLog = loadJSON(HEAL_LOG) || [];
  healLog.push(logEntry);
  if (healLog.length > 100) healLog.splice(0, healLog.length - 100); // keep last 100
  if (!DRY_RUN) {
    saveJSON(HEAL_LOG, healLog);
  }

  // Summary
  log(`Healing complete: ${healed} instances healed, ${actions.length} actions taken`);
  for (const a of actions) {
    log(`  ${a.name}: ${a.action}${a.reason ? ` (${a.reason})` : ""}${a.trust !== undefined ? ` trust=${a.trust}` : ""}`);
  }

  return { healed, actions, total: instances.instances.length };
}

// ── Run ─────────────────────────────────────────────────────────────────────

const result = await heal();

// Output for fleet-runner integration. Distinguish "no instances in the
// registry" from "instances exist and are all healthy" — previously a healthy
// fleet with nothing to do (healed=0, actions=0) was mislabelled no_instances.
if (result.total === 0) {
  console.log(`FLEET_HEAL no_instances`);
} else if (result.healed > 0) {
  console.log(`FLEET_HEAL healed=${result.healed} actions=${result.actions.length}`);
} else {
  console.log(`FLEET_HEAL checked=${result.total} no_healing_needed actions=${result.actions.length}`);
}
