#!/usr/bin/env node
// goal-reconciler.mjs — Spawn goal-driven tasks each fleet cycle.
//
// Reads memory/fleet-goals/backlog.json, picks due goals (round-robin gated by
// cadence), and creates one task per goal via `gl task create`, routed to the
// goal's owner_role with the goal record carried in the payload so executors
// can read objective/next_action_hint/state without re-reading the backlog.
//
// Reuses existing task kinds (research / code-review / deploy / audit) so no
// executor changes are required to land this. Executors that ignore the
// `goal_id` field behave exactly as today; future executors can opt in by
// reading the goal context from the payload.
//
// Outcome reconciliation: each cycle, before picking new goals, walk the
// spawn-log for unresolved entries, find each task's artifact (success path)
// or metrics record (failure path), classify the outcome, and fold it into
// the goal's last_outcome / consecutive_noops. Goals that hit the no-op
// streak limit are auto-paused so the fleet stops re-spawning a broken loop.
//
// Env vars:
//   GITLAWB_NODE              — node URL (default: https://node.gitlawb.com)
//   GITLAWB_REPO_DIR          — repo working directory (default: .)
//   FLEET_GOALS_MAX_PER_CYCLE — max goals to spawn per run (default: 2)
//   FLEET_GOALS_NOOP_LIMIT    — consecutive non-advanced outcomes that trigger
//                               auto-pause (default: 3)
//   FLEET_GOALS_LOST_HOURS    — hours after which an unresolved spawn with
//                               neither artifact nor metrics is "lost" (default: 2)

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import {
  loadBacklog, saveBacklog, pickDueGoals, markAttempted,
  loadSpawns, saveSpawns, appendSpawn, unresolvedSpawns,
  extractTaskId, classifyOutcome, applyOutcome,
} from "./goal-store.mjs";
import { applyGoalUpdate, updateSidecarPath } from "./goal-context.mjs";

const repoDir = process.env.GITLAWB_REPO_DIR || ".";
const node = process.env.GITLAWB_NODE || "https://node.gitlawb.com";
const backlogPath = join(repoDir, "memory/fleet-goals/backlog.json");
const spawnsPath  = join(repoDir, "memory/fleet-goals/spawns.json");
const artifactsDir = join(repoDir, "memory/gitlawb-runner");
const metricsPath  = join(repoDir, "memory/gitlawb-metrics.jsonl");
const maxPerCycle = parseInt(process.env.FLEET_GOALS_MAX_PER_CYCLE || "2", 10);
const noopLimit   = parseInt(process.env.FLEET_GOALS_NOOP_LIMIT || "3", 10);
const lostHours   = parseFloat(process.env.FLEET_GOALS_LOST_HOURS || "2");

// Fleet DIDs — kept in sync with task-generator.mjs. If task-generator moves
// these into a shared module, this should follow.
const ROLE_DIDS = {
  researcher: "did:key:z6MkfnrSDgdDbkvfCCnMyaR4HqoWfWEfGoTFajX1HGkSHRUH",
  reviewer:   "did:key:z6Mks2KSBfbindXsw2SBEGfqdgMJ4HwxJPfPQjkPKHY7U7SZ",
  deployer:   "did:key:z6MknGJBoQsbNL956GNiTJRRWKJqMcprWmdYxJPbVGCwcAuS",
  sentinel:   "did:key:z6MksUuVYyp93QA6pc2qAnXFQZdaoHq46dugXVweeehX4S2M",
};

function run(cmd, args) {
  const proc = spawnSync(cmd, args, { cwd: repoDir, encoding: "utf8" });
  return { ok: proc.status === 0, stdout: (proc.stdout || "").trim(), stderr: (proc.stderr || "").trim() };
}

function getPendingCount(did) {
  const r = run("gl", ["task", "list", "--status", "pending", "--assignee-did", did, "--limit", "5", "--node", node]);
  if (!r.ok) return 0;
  try {
    const data = JSON.parse(r.stdout);
    return (data.tasks || []).length;
  } catch {
    return 0;
  }
}

// `gl task create [OPTIONS] <KIND>` — KIND is positional. See task-generator.mjs
// for the history of the `--kind` regression that masked itself as
// "processed 0 tasks".
export function buildCreateArgs({ kind, assigneeDid, capability, payload }) {
  return [
    "task", "create",
    kind,
    "--assignee-did", assigneeDid,
    "--capability", capability,
    "--payload", JSON.stringify(payload),
    "--node", node,
  ];
}

// Codex review on PR #120 flagged that goal payloads only carried generic
// objective/next_action_hint fields, while command executors (reviewer.mjs,
// deployer.mjs, sentinel.mjs, researcher.mjs) actually read executor-specific
// fields (target/focus, action/component, topic/scope, …). Without translation,
// a goal-spawned reviewer task fell back to reviewing this repo's recent commits
// instead of the swarm PR queue. We let each goal declare an `executor_payload`
// block with exactly the fields its target executor reads; goal metadata
// (goal_id/title/objective/state) overlays on top so attribution and the
// goal-context writeback still work.
export function buildPayload(goal) {
  return {
    ...(goal.executor_payload || {}),
    goal_id: goal.id,
    title: `[goal:${goal.id}] ${goal.title}`,
    objective: goal.objective || goal.title,
    success_criteria: goal.success_criteria || null,
    next_action_hint: goal.next_action_hint || null,
    state: goal.state || {},
  };
}

// createFn must return {ok, taskId|null}. taskId lets us record the spawn so
// outcomeReconcile can later link the completed task back to the goal.
export function reconcile({ backlog, spawns, now, maxPerCycle: max, pendingFn, createFn, log }) {
  const due = pickDueGoals(backlog, now, max);
  log(`[goal-reconciler] ${due.length} goal(s) due (max ${max})`);

  const spawned = [];
  for (const goal of due) {
    const did = ROLE_DIDS[goal.owner_role];
    if (!did) {
      log(`  skip ${goal.id}: unknown owner_role ${goal.owner_role}`);
      continue;
    }
    const pending = pendingFn(did);
    if (pending >= (goal.max_concurrent ?? 1)) {
      log(`  skip ${goal.id}: ${pending} pending task(s) for ${goal.owner_role}`);
      continue;
    }
    const args = buildCreateArgs({
      kind: goal.kind,
      assigneeDid: did,
      capability: goal.capability,
      payload: buildPayload(goal),
    });
    const result = createFn(args);
    if (result && result.ok) {
      markAttempted(backlog, goal.id, now.toISOString());
      spawned.push(goal.id);
      if (result.taskId) {
        appendSpawn(spawns, { spawned_at: now.toISOString(), goal_id: goal.id, task_id: result.taskId });
        log(`  spawned ${goal.id} → ${goal.owner_role} (${goal.kind}) task=${result.taskId}`);
      } else {
        log(`  spawned ${goal.id} → ${goal.owner_role} (${goal.kind}) — WARN no task id parsed; outcome cannot be reconciled`);
      }
    } else {
      log(`  FAILED ${goal.id} → ${goal.owner_role}`);
    }
  }
  return { spawned };
}

// ── Outcome reconciliation ───────────────────────────────────────────────
//
// readArtifactFn(taskId) → object | null  (loads memory/gitlawb-runner/{taskId}.json)
// readMetricsFn()        → array of {event, taskId, ok, reason} from metrics.jsonl
//
// For each unresolved spawn:
//   1. classify outcome from (artifact, metricsEvent)
//   2. if classified: applyOutcome to goal, mark spawn resolved
//   3. if null (still pending), leave as-is
//
// Returns {resolved: [{goal_id, task_id, outcome, autoPaused}], pending: n}.
// readUpdateFn(taskId) → object | null  (loads the goal-update sidecar, if any)
// consumeUpdateFn(taskId)                (removes the sidecar after applying)
export function reconcileOutcomes({
  backlog, spawns, readArtifactFn, readMetricsFn, readUpdateFn, consumeUpdateFn,
  now, noopLimit, lostHours, log,
}) {
  const open = unresolvedSpawns(spawns);
  if (open.length === 0) return { resolved: [], pending: 0, patched: 0 };

  const metricsByTaskId = new Map();
  for (const ev of readMetricsFn()) {
    // MetricsRecorder.record(type, fields) writes {ts, type, ...fields} — so
    // task events use `type: "task"`, not `event: "task"`. Codex review on
    // PR #121 caught that this predicate had the wrong field; failed goal
    // tasks fell through to the lost-timeout path instead of being marked
    // "blocked" promptly.
    if (ev && ev.type === "task" && ev.taskId) metricsByTaskId.set(String(ev.taskId), ev);
  }

  const resolved = [];
  let pending = 0;
  let patched = 0;
  for (const spawn of open) {
    const artifact = readArtifactFn(spawn.task_id);
    const metricsEvent = metricsByTaskId.get(spawn.task_id) || null;
    const outcome = classifyOutcome({ artifact, metricsEvent, spawnedAt: spawn.spawned_at, now, lostAfterHours: lostHours });
    if (outcome === null) { pending++; continue; }

    const goal = backlog.goals.find((g) => g.id === spawn.goal_id);
    let autoPaused = false;
    let goalPatched = false;
    if (goal) {
      const r = applyOutcome(goal, outcome, now, noopLimit);
      autoPaused = r.autoPaused;

      // Apply the executor's goal-update sidecar AFTER applyOutcome so a
      // freshly auto-paused goal still gets its hint refreshed for when
      // the operator unpauses it.
      if (readUpdateFn) {
        const update = readUpdateFn(spawn.task_id);
        if (update) {
          goalPatched = applyGoalUpdate(goal, update);
          if (goalPatched) patched++;
          if (consumeUpdateFn) consumeUpdateFn(spawn.task_id);
        }
      }
    } else {
      log(`  resolved orphan spawn task=${spawn.task_id} (goal ${spawn.goal_id} no longer in backlog)`);
      // Orphan: still consume the sidecar so it doesn't pile up forever.
      if (consumeUpdateFn) consumeUpdateFn(spawn.task_id);
    }

    spawn.resolved_at = now.toISOString();
    spawn.outcome = outcome;
    resolved.push({ goal_id: spawn.goal_id, task_id: spawn.task_id, outcome, autoPaused, patched: goalPatched });
    const tags = [autoPaused ? "AUTO-PAUSED" : null, goalPatched ? "patched" : null].filter(Boolean).join(" ");
    log(`  resolved ${spawn.goal_id} task=${spawn.task_id} → ${outcome}${tags ? " " + tags : ""}`);
  }
  return { resolved, pending, patched };
}

// I/O helpers used by main(); exported only so tests can swap them without
// touching disk.
export function defaultReadArtifact(taskId) {
  const p = join(artifactsDir, `${taskId}.json`);
  if (!existsSync(p)) return null;
  try { return JSON.parse(readFileSync(p, "utf8")); } catch { return null; }
}

export function defaultReadMetrics() {
  if (!existsSync(metricsPath)) return [];
  const out = [];
  for (const line of readFileSync(metricsPath, "utf8").split("\n")) {
    if (!line.trim()) continue;
    try { out.push(JSON.parse(line)); } catch { /* skip malformed */ }
  }
  return out;
}

export function defaultReadUpdate(taskId) {
  const p = updateSidecarPath(taskId, repoDir);
  if (!existsSync(p)) return null;
  try { return JSON.parse(readFileSync(p, "utf8")); } catch { return null; }
}

export function defaultConsumeUpdate(taskId) {
  const p = updateSidecarPath(taskId, repoDir);
  if (!existsSync(p)) return;
  try { unlinkSync(p); } catch { /* best-effort */ }
}

async function main() {
  const backlog = loadBacklog(backlogPath);
  const spawns = loadSpawns(spawnsPath);
  if (backlog.goals.length === 0 && spawns.length === 0) {
    console.log("[goal-reconciler] no goals in backlog, nothing to do");
    console.log("0 goal(s) resolved, 0 goal(s) spawned");
    return;
  }
  const now = new Date();

  // 1. Close the loop on prior spawns BEFORE picking new work — that way
  // auto-pause kicks in before we'd otherwise re-spawn a stuck goal.
  const { resolved, pending, patched } = reconcileOutcomes({
    backlog, spawns, now, noopLimit, lostHours,
    readArtifactFn: defaultReadArtifact,
    readMetricsFn: defaultReadMetrics,
    readUpdateFn: defaultReadUpdate,
    consumeUpdateFn: defaultConsumeUpdate,
    log: console.log,
  });
  console.log(`[goal-reconciler] outcomes: ${resolved.length} resolved (${patched} patched), ${pending} still pending`);

  // 2. Pick + spawn new goal-driven tasks.
  const { spawned } = reconcile({
    backlog, spawns, now, maxPerCycle,
    pendingFn: getPendingCount,
    createFn: (args) => {
      const r = run("gl", args);
      return { ok: r.ok, taskId: r.ok ? extractTaskId(r.stdout) : null };
    },
    log: console.log,
  });

  // 3. Persist both ledgers if either changed.
  if (resolved.length > 0 || spawned.length > 0) {
    saveBacklog(backlogPath, backlog);
    saveSpawns(spawnsPath, spawns, now);
  }
  const autoPaused = resolved.filter((r) => r.autoPaused).map((r) => r.goal_id);
  if (autoPaused.length > 0) {
    console.log(`[goal-reconciler] AUTO-PAUSED: ${autoPaused.join(", ")}`);
  }
  console.log(`${resolved.length} goal(s) resolved, ${spawned.length} goal(s) spawned`);
}

// Allow tests to import without running main.
const isEntry = import.meta.url === `file://${process.argv[1]}`;
if (isEntry) {
  main().catch((err) => {
    console.error("[goal-reconciler] fatal:", err);
    process.exit(1);
  });
}
