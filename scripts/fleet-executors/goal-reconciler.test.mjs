// goal-reconciler.test.mjs — Tests for the reconciler's pick/spawn loop and
// outcome reconciliation.
//
// Run: node scripts/fleet-executors/goal-reconciler.test.mjs

import { BACKLOG_VERSION } from "./goal-store.mjs";
import { reconcile, reconcileOutcomes, buildCreateArgs, buildPayload } from "./goal-reconciler.mjs";

let passed = 0;
let failed = 0;

function assert(cond, label) {
  if (cond) { passed++; console.log(`  ✓ ${label}`); }
  else { failed++; console.error(`  ✗ ${label}`); }
}

const NOW = new Date("2026-06-02T12:00:00Z");
const TID1 = "00000000-0000-0000-0000-000000000001";
const TID2 = "00000000-0000-0000-0000-000000000002";

function makeBacklog(overrides = []) {
  const defaults = [
    { id: "g-research", title: "Research", owner_role: "researcher", kind: "research", capability: "issue:create", status: "active", cadence_hours: 0, last_attempted_at: null },
    { id: "g-review",   title: "Review",   owner_role: "reviewer",   kind: "code-review", capability: "pr:review",   status: "active", cadence_hours: 0, last_attempted_at: null },
  ];
  return { version: BACKLOG_VERSION, goals: defaults.map((d, i) => ({ ...d, ...(overrides[i] || {}) })) };
}

const okResult = (taskId) => ({ ok: true, taskId });
const failResult = () => ({ ok: false, taskId: null });

// ── buildCreateArgs ──────────────────────────────────────────
console.log("buildCreateArgs:");
{
  const args = buildCreateArgs({ kind: "research", assigneeDid: "did:key:z6Mxxx", capability: "issue:create", payload: { goal_id: "g1" } });
  assert(args[0] === "task" && args[1] === "create", "task create prefix");
  assert(args[2] === "research", "KIND is positional (3rd arg), not behind --kind");
  assert(!args.includes("--kind"), "no --kind flag (regression guard)");
  assert(args.includes("--assignee-did") && args.includes("did:key:z6Mxxx"), "carries assignee");
  assert(args.includes("--capability") && args.includes("issue:create"), "carries capability");
  const payloadIdx = args.indexOf("--payload");
  assert(payloadIdx > 0 && JSON.parse(args[payloadIdx + 1]).goal_id === "g1", "payload is JSON-encoded");
}

// ── buildPayload ─────────────────────────────────────────────
console.log("buildPayload:");
{
  const p = buildPayload({ id: "g1", title: "Do X", objective: "obj", success_criteria: "sc", next_action_hint: "hint", state: { step: 3 } });
  assert(p.goal_id === "g1", "goal_id preserved");
  assert(p.title.startsWith("[goal:g1]"), "title prefixed for downstream attribution");
  assert(p.objective === "obj", "objective preserved");
  assert(p.next_action_hint === "hint", "hint preserved");
  assert(p.state.step === 3, "state preserved");

  const fallback = buildPayload({ id: "g2", title: "Just a title" });
  assert(fallback.objective === "Just a title", "objective falls back to title");

  // executor_payload is merged in so reviewer/deployer/etc. see the fields
  // they actually read (target/focus/action/component/topic). Goal metadata
  // still wins on shared keys so attribution + writeback stay intact.
  const merged = buildPayload({
    id: "g3",
    title: "Review the queue",
    objective: "obj3",
    executor_payload: { target: "owner/repo open PRs", focus: "merge gate", title: "REPLACED" },
  });
  assert(merged.target === "owner/repo open PRs", "executor_payload.target flows through");
  assert(merged.focus === "merge gate", "executor_payload.focus flows through");
  assert(merged.title === "[goal:g3] Review the queue", "goal metadata overrides executor_payload on shared keys");
  assert(merged.objective === "obj3", "goal objective preserved over executor_payload");
}

// ── reconcile: happy path ────────────────────────────────────
console.log("reconcile happy path:");
{
  const backlog = makeBacklog();
  const spawns = [];
  const created = [];
  let n = 0;
  const result = reconcile({
    backlog, spawns,
    now: NOW,
    maxPerCycle: 5,
    pendingFn: () => 0,
    createFn: (args) => { created.push(args); return okResult(`00000000-0000-0000-0000-00000000000${++n}`); },
    log: () => {},
  });
  assert(result.spawned.length === 2, "spawned both due goals");
  assert(created.length === 2, "called gl task create twice");
  assert(backlog.goals.every((g) => g.last_attempted_at === NOW.toISOString()), "marked both attempted");
  assert(spawns.length === 2, "appended both spawns to ledger");
  assert(spawns[0].task_id && spawns[1].task_id, "task ids recorded");
  assert(spawns.every((s) => s.spawned_at === NOW.toISOString()), "spawn timestamps stamped");
}

// ── reconcile: spawn without task id still marks attempted but logs warn ─
console.log("reconcile handles missing task id:");
{
  const backlog = makeBacklog();
  const spawns = [];
  const result = reconcile({
    backlog, spawns,
    now: NOW, maxPerCycle: 5,
    pendingFn: () => 0,
    createFn: () => ({ ok: true, taskId: null }),
    log: () => {},
  });
  assert(result.spawned.length === 2, "spawned reported");
  assert(spawns.length === 0, "no spawn-log entry without task id (can't reconcile later)");
  assert(backlog.goals.every((g) => g.last_attempted_at === NOW.toISOString()), "still attempted (cadence advances)");
}

// ── reconcile: skip when pending tasks exist ─────────────────
console.log("reconcile skips on pending:");
{
  const backlog = makeBacklog();
  const spawns = [];
  const result = reconcile({
    backlog, spawns,
    now: NOW, maxPerCycle: 5,
    pendingFn: (did) => did.includes("z6Mks2") ? 3 : 0,
    createFn: () => okResult(TID1),
    log: () => {},
  });
  assert(result.spawned.includes("g-research"), "researcher still spawned");
  assert(!result.spawned.includes("g-review"), "reviewer skipped due to pending");
  const reviewerGoal = backlog.goals.find((g) => g.id === "g-review");
  assert(reviewerGoal.last_attempted_at == null, "skipped goal NOT marked attempted");
}

// ── reconcile: respects maxPerCycle ──────────────────────────
console.log("reconcile respects maxPerCycle:");
{
  const backlog = makeBacklog();
  const result = reconcile({
    backlog, spawns: [],
    now: NOW, maxPerCycle: 1,
    pendingFn: () => 0,
    createFn: () => okResult(TID1),
    log: () => {},
  });
  assert(result.spawned.length === 1, "cap honored");
}

// ── reconcile: unknown owner_role ────────────────────────────
console.log("reconcile handles unknown owner_role:");
{
  const backlog = { version: BACKLOG_VERSION, goals: [
    { id: "g-bogus", title: "B", owner_role: "phantom", kind: "research", capability: "x", status: "active" },
  ] };
  const result = reconcile({
    backlog, spawns: [],
    now: NOW, maxPerCycle: 5,
    pendingFn: () => 0,
    createFn: () => okResult(TID1),
    log: () => {},
  });
  assert(result.spawned.length === 0, "unknown role skipped, not spawned");
}

// ── reconcile: createFn failure does not mark attempted ─────
console.log("reconcile leaves failed goal unmarked:");
{
  const backlog = makeBacklog();
  const result = reconcile({
    backlog, spawns: [],
    now: NOW, maxPerCycle: 5,
    pendingFn: () => 0,
    createFn: failResult,
    log: () => {},
  });
  assert(result.spawned.length === 0, "no spawns reported");
  assert(backlog.goals.every((g) => g.last_attempted_at == null), "no goal marked attempted");
}

// ── reconcileOutcomes: artifact → advanced ───────────────────
console.log("reconcileOutcomes advanced:");
{
  const backlog = makeBacklog();
  backlog.goals[0].consecutive_noops = 2; // prove this resets on advance
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-research", task_id: TID1 }];
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: (id) => id === TID1 ? { result: { summary: "Filed issue ISS-042" } } : null,
    readMetricsFn: () => [],
    log: () => {},
  });
  assert(out.resolved.length === 1, "one outcome resolved");
  assert(out.resolved[0].outcome === "advanced", "classified as advanced");
  assert(backlog.goals[0].consecutive_noops === 0, "noop streak reset on advance");
  assert(spawns[0].resolved_at === NOW.toISOString(), "spawn marked resolved");
  assert(spawns[0].outcome === "advanced", "outcome stamped on spawn");
}

// ── reconcileOutcomes: artifact summary signals noop ─────────
console.log("reconcileOutcomes noop:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-research", task_id: TID1 }];
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => ({ result: { summary: "No-op: nothing to do this cycle" } }),
    readMetricsFn: () => [],
    log: () => {},
  });
  assert(out.resolved[0].outcome === "noop", "noop pattern matched");
  assert(backlog.goals[0].consecutive_noops === 1, "noop streak incremented");
}

// ── reconcileOutcomes: metrics ok=false → blocked ────────────
console.log("reconcileOutcomes blocked:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-research", task_id: TID1 }];
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => null,
    readMetricsFn: () => [{ type: "task", taskId: TID1, ok: false, reason: "exec threw" }],
    log: () => {},
  });
  assert(out.resolved[0].outcome === "blocked", "metrics failure classified blocked");
}

// ── reconcileOutcomes: metric shape guard ────────────────────
//
// Codex review on PR #121 caught that the predicate originally read
// `ev.event === "task"` but MetricsRecorder writes `{ts, type, ...fields}`.
// This guard locks the correct field down so a future refactor can't
// silently revert it (failed tasks would then fall through to the lost
// timeout instead of being marked blocked promptly).
console.log("reconcileOutcomes ignores wrong-shape metric events:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-research", task_id: TID1 }];
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => null,
    // old wrong shape — predicate must NOT match this
    readMetricsFn: () => [{ event: "task", taskId: TID1, ok: false, reason: "wrong shape" }],
    log: () => {},
  });
  // 1h-old spawn, lostHours=2 → still pending, not classified as blocked
  assert(out.resolved.length === 0, "wrong-shape event not picked up");
  assert(out.pending === 1, "spawn stays pending without a real type:task event");
}

// ── reconcileOutcomes: stale unresolved → lost ───────────────
console.log("reconcileOutcomes lost:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T09:00:00Z", goal_id: "g-research", task_id: TID1 }]; // 3h old
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => null,
    readMetricsFn: () => [],
    log: () => {},
  });
  assert(out.resolved[0].outcome === "lost", "stale spawn classified lost");
}

// ── reconcileOutcomes: still pending leaves entry open ───────
console.log("reconcileOutcomes pending:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T11:45:00Z", goal_id: "g-research", task_id: TID1 }]; // 15min old
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => null,
    readMetricsFn: () => [],
    log: () => {},
  });
  assert(out.resolved.length === 0, "nothing resolved");
  assert(out.pending === 1, "one pending");
  assert(!spawns[0].resolved_at, "spawn still open");
}

// ── reconcileOutcomes: 3 noops in a row auto-pauses ──────────
console.log("reconcileOutcomes auto-pause:");
{
  const backlog = makeBacklog();
  backlog.goals[0].consecutive_noops = 2; // one more triggers auto-pause
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-research", task_id: TID1 }];
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => null,
    readMetricsFn: () => [{ type: "task", taskId: TID1, ok: false, reason: "x" }],
    log: () => {},
  });
  assert(out.resolved[0].autoPaused === true, "auto-pause signaled");
  assert(backlog.goals[0].status === "paused", "goal status flipped to paused");
  assert(backlog.goals[0].paused_reason && backlog.goals[0].paused_reason.includes("3"), "pause reason carries streak count");
}

// ── reconcileOutcomes: applies executor's goal-update sidecar ────────────
console.log("reconcileOutcomes applies sidecar update:");
{
  const backlog = makeBacklog();
  backlog.goals[0].state = { step: 1 };
  backlog.goals[0].next_action_hint = "old hint";
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-research", task_id: TID1 }];
  let consumedTaskId = null;
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => ({ result: { summary: "Filed ISS-099" } }),
    readMetricsFn: () => [],
    readUpdateFn: (id) => id === TID1 ? {
      task_id: TID1, goal_id: "g-research",
      next_action_hint: "scan the new files",
      state: { step: 2, last_issue: "ISS-099" },
    } : null,
    consumeUpdateFn: (id) => { consumedTaskId = id; },
    log: () => {},
  });
  assert(out.resolved[0].patched === true, "patched flag set");
  assert(out.patched === 1, "patched counter incremented");
  assert(backlog.goals[0].next_action_hint === "scan the new files", "hint replaced from sidecar");
  assert(backlog.goals[0].state.step === 2, "state.step patched");
  assert(backlog.goals[0].state.last_issue === "ISS-099", "new state key merged in");
  assert(consumedTaskId === TID1, "sidecar consumed after applying");
}

// ── reconcileOutcomes: sidecar is consumed even for orphan goals ─────────
console.log("reconcileOutcomes consumes orphan sidecar:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-gone", task_id: TID1 }];
  let consumed = false;
  reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => ({ result: { summary: "did stuff" } }),
    readMetricsFn: () => [],
    readUpdateFn: () => ({ task_id: TID1, goal_id: "g-gone", next_action_hint: "x" }),
    consumeUpdateFn: () => { consumed = true; },
    log: () => {},
  });
  assert(consumed === true, "orphan sidecar still consumed (avoid pile-up)");
}

// ── reconcileOutcomes: works without sidecar I/O (back-compat) ───────────
console.log("reconcileOutcomes back-compat with no sidecar reader:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-research", task_id: TID1 }];
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => ({ result: { summary: "did stuff" } }),
    readMetricsFn: () => [],
    log: () => {},
  });
  assert(out.resolved[0].outcome === "advanced", "still resolves without sidecar fns");
  assert(out.patched === 0, "no patches counted");
}

// ── reconcileOutcomes: orphan spawn (goal deleted) ───────────
console.log("reconcileOutcomes orphan:");
{
  const backlog = makeBacklog();
  const spawns = [{ spawned_at: "2026-06-02T11:00:00Z", goal_id: "g-gone", task_id: TID1 }];
  const out = reconcileOutcomes({
    backlog, spawns, now: NOW, noopLimit: 3, lostHours: 2,
    readArtifactFn: () => ({ result: { summary: "did stuff" } }),
    readMetricsFn: () => [],
    log: () => {},
  });
  assert(out.resolved.length === 1, "orphan still resolved");
  assert(spawns[0].resolved_at, "orphan spawn marked resolved");
  assert(backlog.goals.every((g) => g.id !== "g-gone"), "no ghost goal created");
}

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
