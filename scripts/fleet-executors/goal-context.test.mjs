// goal-context.test.mjs — Tests for the shared executor-side helper.
//
// Run: node scripts/fleet-executors/goal-context.test.mjs

import { mkdtempSync, rmSync, readFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  getGoalContext, writeGoalUpdate, applyGoalUpdate,
  parsePayload, updateSidecarPath, sidecarExists,
} from "./goal-context.mjs";

let passed = 0;
let failed = 0;

function assert(cond, label) {
  if (cond) { passed++; console.log(`  ✓ ${label}`); }
  else { failed++; console.error(`  ✗ ${label}`); }
}

const tmp = mkdtempSync(join(tmpdir(), "goal-ctx-test-"));

// ── parsePayload ─────────────────────────────────────────────
console.log("parsePayload:");
{
  assert(parsePayload(undefined).goal_id === undefined, "undefined → {}");
  assert(parsePayload(null).goal_id === undefined, "null → {}");
  assert(parsePayload({ goal_id: "g" }).goal_id === "g", "object passthrough");
  assert(parsePayload('{"goal_id":"g"}').goal_id === "g", "json string parsed");
  assert(Object.keys(parsePayload("not json")).length === 0, "malformed string → {}");
}

// ── getGoalContext ───────────────────────────────────────────
console.log("getGoalContext:");
{
  assert(getGoalContext({}) === null, "no env → null");

  const noGoal = {
    GITLAWB_TASK_JSON: JSON.stringify({ id: "t1", payload: JSON.stringify({ title: "regular task" }) }),
  };
  assert(getGoalContext(noGoal) === null, "task without goal_id → null (regular tasks unaffected)");

  const withGoal = {
    GITLAWB_TASK_JSON: JSON.stringify({
      id: "t1",
      payload: JSON.stringify({
        goal_id: "g-research",
        title: "[goal:g-research] Research",
        objective: "Find the thing",
        success_criteria: "thing found",
        next_action_hint: "look here",
        state: { step: 2 },
      }),
    }),
  };
  const ctx = getGoalContext(withGoal);
  assert(ctx !== null, "task with goal_id → object");
  assert(ctx.goal_id === "g-research", "goal_id preserved");
  assert(ctx.objective === "Find the thing", "objective preserved");
  assert(ctx.next_action_hint === "look here", "hint preserved");
  assert(ctx.state.step === 2, "state preserved");
  assert(ctx.task_id === "t1", "task_id extracted");

  // payload as already-object (task-runner sometimes parses it)
  const objPayload = { GITLAWB_TASK_JSON: JSON.stringify({ id: "t2", payload: { goal_id: "g2" } }) };
  assert(getGoalContext(objPayload).goal_id === "g2", "handles object payload");

  // malformed payload
  const bad = { GITLAWB_TASK_JSON: "not json" };
  assert(getGoalContext(bad) === null, "malformed task json → null");
}

// ── writeGoalUpdate ──────────────────────────────────────────
console.log("writeGoalUpdate:");
{
  const taskId = "11111111-1111-1111-1111-111111111111";
  const path = writeGoalUpdate({
    taskId,
    goalId: "g-research",
    next_action_hint: "try this next",
    state: { step: 3, last_topic: "fleet runner" },
    note: "advanced the loop",
  }, tmp);
  assert(existsSync(path), "sidecar written");
  const parsed = JSON.parse(readFileSync(path, "utf8"));
  assert(parsed.task_id === taskId, "task_id stamped");
  assert(parsed.goal_id === "g-research", "goal_id stamped");
  assert(parsed.next_action_hint === "try this next", "hint persisted");
  assert(parsed.state.step === 3, "state persisted");
  assert(parsed.note === "advanced the loop", "note persisted");
  assert(typeof parsed.written_at === "string", "written_at stamped");

  // optional fields really are optional
  const path2 = writeGoalUpdate({ taskId: "22222222-2222-2222-2222-222222222222", goalId: "g" }, tmp);
  const minimal = JSON.parse(readFileSync(path2, "utf8"));
  assert(!("next_action_hint" in minimal), "omits unset hint");
  assert(!("state" in minimal), "omits unset state");

  // input validation
  let threw = false;
  try { writeGoalUpdate({ goalId: "g" }, tmp); } catch { threw = true; }
  assert(threw, "missing taskId throws");
}

// ── applyGoalUpdate ──────────────────────────────────────────
console.log("applyGoalUpdate:");
{
  const goal = { id: "g1", next_action_hint: "old hint", state: { step: 1, ttl: 7 } };
  const touched = applyGoalUpdate(goal, {
    next_action_hint: "fresh hint",
    state: { step: 2 },
  });
  assert(touched === true, "returns true when something changed");
  assert(goal.next_action_hint === "fresh hint", "hint replaced");
  assert(goal.state.step === 2, "patched state key updated");
  assert(goal.state.ttl === 7, "untouched state key preserved (shallow merge)");

  const noop = applyGoalUpdate(goal, {});
  assert(noop === false, "empty update returns false");

  // unknown fields are ignored, not blindly copied
  applyGoalUpdate(goal, { malicious_field: "nope" });
  assert(!("malicious_field" in goal), "unknown fields not copied onto goal");
}

// ── sidecarExists / updateSidecarPath ────────────────────────
console.log("sidecar path helpers:");
{
  const taskId = "33333333-3333-3333-3333-333333333333";
  assert(sidecarExists(taskId, tmp) === false, "absent before write");
  writeGoalUpdate({ taskId, goalId: "g" }, tmp);
  assert(sidecarExists(taskId, tmp) === true, "present after write");
  assert(updateSidecarPath(taskId, tmp).endsWith(`${taskId}.json`), "path uses task id");
}

rmSync(tmp, { recursive: true, force: true });

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
