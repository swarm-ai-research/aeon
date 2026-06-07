// goal-store.test.mjs — Tests for the goal backlog store + picker.
//
// Run: node scripts/fleet-executors/goal-store.test.mjs

import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  BACKLOG_VERSION,
  loadBacklog,
  saveBacklog,
  validateGoal,
  pickDueGoals,
  markAttempted,
  loadSpawns,
  saveSpawns,
  appendSpawn,
  unresolvedSpawns,
  extractTaskId,
  classifyOutcome,
  applyOutcome,
} from "./goal-store.mjs";

let passed = 0;
let failed = 0;

function assert(cond, label) {
  if (cond) { passed++; console.log(`  ✓ ${label}`); }
  else { failed++; console.error(`  ✗ ${label}`); }
}

const tmp = mkdtempSync(join(tmpdir(), "goal-store-test-"));

// ── load / save round-trip ───────────────────────────────────
console.log("load/save:");
{
  const path = join(tmp, "backlog.json");
  const empty = loadBacklog(path);
  assert(empty.version === BACKLOG_VERSION, "missing file → default version");
  assert(empty.goals.length === 0, "missing file → empty goals");

  const seeded = {
    version: BACKLOG_VERSION,
    goals: [{ id: "x", title: "X", owner_role: "researcher", kind: "research", capability: "issue:create", status: "active" }],
  };
  saveBacklog(path, seeded);
  const reloaded = loadBacklog(path);
  assert(reloaded.goals.length === 1, "round-trip preserves goals");
  assert(reloaded.goals[0].id === "x", "round-trip preserves id");
}

// ── validateGoal ─────────────────────────────────────────────
console.log("validateGoal:");
{
  const ok = validateGoal({ id: "a", title: "t", owner_role: "researcher", kind: "research", capability: "issue:create" });
  assert(ok.length === 0, "valid goal → no errors");

  const bad = validateGoal({ id: "", title: "t", owner_role: "wat", kind: "research", capability: "x" });
  assert(bad.length >= 2, "invalid goal → multiple errors");

  const negCadence = validateGoal({ id: "a", title: "t", owner_role: "researcher", kind: "research", capability: "x", cadence_hours: -1 });
  assert(negCadence.some((e) => e.includes("cadence_hours")), "negative cadence flagged");
}

// ── pickDueGoals ─────────────────────────────────────────────
console.log("pickDueGoals:");
{
  const now = new Date("2026-06-02T12:00:00Z");
  const backlog = {
    version: BACKLOG_VERSION,
    goals: [
      // never attempted, cadence 0 → always due
      { id: "g1", title: "g1", owner_role: "researcher", kind: "research", capability: "x", status: "active", cadence_hours: 0, last_attempted_at: null },
      // attempted 2h ago, cadence 1h → due
      { id: "g2", title: "g2", owner_role: "reviewer",   kind: "code-review", capability: "x", status: "active", cadence_hours: 1, last_attempted_at: "2026-06-02T10:00:00Z" },
      // attempted 30min ago, cadence 6h → NOT due
      { id: "g3", title: "g3", owner_role: "deployer",   kind: "deploy",   capability: "x", status: "active", cadence_hours: 6, last_attempted_at: "2026-06-02T11:30:00Z" },
      // paused
      { id: "g4", title: "g4", owner_role: "sentinel",   kind: "audit",    capability: "x", status: "paused" },
      // attempted 24h ago, cadence 1h → due, oldest
      { id: "g5", title: "g5", owner_role: "researcher", kind: "research", capability: "x", status: "active", cadence_hours: 1, last_attempted_at: "2026-06-01T12:00:00Z" },
    ],
  };

  const picked = pickDueGoals(backlog, now, 10);
  const ids = picked.map((g) => g.id);
  assert(!ids.includes("g3"), "cadence-gated goal excluded");
  assert(!ids.includes("g4"), "paused goal excluded");
  assert(ids.includes("g1") && ids.includes("g2") && ids.includes("g5"), "due goals included");

  // Round-robin order: oldest-attempted first (null = epoch = oldest).
  assert(ids[0] === "g1", "never-attempted goal picked first");
  assert(ids[1] === "g5", "next is the oldest real attempt");

  const capped = pickDueGoals(backlog, now, 2);
  assert(capped.length === 2, "maxPerCycle caps the result");
}

// ── markAttempted ────────────────────────────────────────────
console.log("markAttempted:");
{
  const backlog = {
    version: BACKLOG_VERSION,
    goals: [{ id: "g1", title: "g1", owner_role: "researcher", kind: "research", capability: "x", status: "active" }],
  };
  const ok = markAttempted(backlog, "g1", "2026-06-02T12:00:00Z");
  assert(ok === true, "returns true on hit");
  assert(backlog.goals[0].last_attempted_at === "2026-06-02T12:00:00Z", "writes timestamp");

  const miss = markAttempted(backlog, "nope", "2026-06-02T12:00:00Z");
  assert(miss === false, "returns false on miss");
}

// ── spawn log ────────────────────────────────────────────────
console.log("spawns load/save/prune:");
{
  const path = join(tmp, "spawns.json");
  assert(loadSpawns(path).length === 0, "missing → empty");

  const now = new Date("2026-06-02T12:00:00Z");
  const spawns = [];
  appendSpawn(spawns, { spawned_at: "2026-06-02T11:00:00Z", goal_id: "g1", task_id: "t1" });
  appendSpawn(spawns, { spawned_at: "2026-05-20T11:00:00Z", goal_id: "g0", task_id: "t-old" });
  spawns[1].resolved_at = "2026-05-20T11:30:00Z"; // > 7d old, should be pruned on save
  spawns[1].outcome = "advanced";
  saveSpawns(path, spawns, now);

  const reloaded = loadSpawns(path);
  assert(reloaded.length === 1, "resolved spawn older than TTL pruned");
  assert(reloaded[0].task_id === "t1", "unresolved spawn kept");
}

console.log("unresolvedSpawns:");
{
  const spawns = [
    { task_id: "a", goal_id: "g", spawned_at: "x" },
    { task_id: "b", goal_id: "g", spawned_at: "x", resolved_at: "y", outcome: "advanced" },
  ];
  const open = unresolvedSpawns(spawns);
  assert(open.length === 1 && open[0].task_id === "a", "filters to open spawns only");
}

// ── extractTaskId ────────────────────────────────────────────
console.log("extractTaskId:");
{
  const uuid = "12345678-1234-1234-1234-123456789012";
  assert(extractTaskId(uuid) === uuid, "bare UUID extracted");
  assert(extractTaskId(`Task created: ${uuid}`) === uuid, "UUID inside human prefix");
  assert(extractTaskId(`{"task_id": "${uuid}"}`) === uuid, "JSON envelope with task_id");
  assert(extractTaskId(`{"id": "${uuid}"}`) === uuid, "JSON envelope with id");
  assert(extractTaskId("") === null, "empty input");
  assert(extractTaskId("nothing to see") === null, "no UUID in output");
}

// ── classifyOutcome ──────────────────────────────────────────
console.log("classifyOutcome:");
{
  const now = new Date("2026-06-02T12:00:00Z");
  const recent = "2026-06-02T11:45:00Z";   // 15min old
  const stale  = "2026-06-02T09:00:00Z";   // 3h old

  assert(classifyOutcome({ artifact: { result: { summary: "Did the thing" } }, metricsEvent: null, spawnedAt: recent, now }) === "advanced", "artifact summary → advanced");
  assert(classifyOutcome({ artifact: { result: { summary: "no-op cycle" } }, metricsEvent: null, spawnedAt: recent, now }) === "noop", "noop summary classified noop");
  assert(classifyOutcome({ artifact: { result: { summary: "Skipped: nothing to do" } }, metricsEvent: null, spawnedAt: recent, now }) === "noop", "skip + nothing-to-do → noop");
  assert(classifyOutcome({ artifact: null, metricsEvent: { ok: false, reason: "boom" }, spawnedAt: recent, now }) === "blocked", "metrics ok=false → blocked");
  assert(classifyOutcome({ artifact: null, metricsEvent: null, spawnedAt: stale, now, lostAfterHours: 2 }) === "lost", "stale unresolved → lost");
  assert(classifyOutcome({ artifact: null, metricsEvent: null, spawnedAt: recent, now, lostAfterHours: 2 }) === null, "recent unresolved → pending");
}

// ── applyOutcome ─────────────────────────────────────────────
console.log("applyOutcome:");
{
  const now = new Date("2026-06-02T12:00:00Z");

  const g = { id: "g", status: "active", consecutive_noops: 2 };
  const r1 = applyOutcome(g, "advanced", now, 3);
  assert(r1.autoPaused === false, "advance does not pause");
  assert(g.consecutive_noops === 0, "advance resets streak");
  assert(g.last_outcome === "advanced" && g.last_outcome_at === now.toISOString(), "outcome stamped");

  const h = { id: "h", status: "active", consecutive_noops: 2 };
  const r2 = applyOutcome(h, "noop", now, 3);
  assert(r2.autoPaused === true, "3rd consecutive noop auto-pauses");
  assert(h.status === "paused", "status flipped");
  assert(h.consecutive_noops === 3, "streak incremented");
  assert(h.paused_reason && h.paused_at, "pause metadata set");

  // Re-applying outcome to already-paused goal does NOT re-emit auto-pause.
  const r3 = applyOutcome(h, "noop", now, 3);
  assert(r3.autoPaused === false, "subsequent noop on paused goal does not re-pause");
}

rmSync(tmp, { recursive: true, force: true });

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
