// goal-context.mjs — Helper for fleet executors to read goal context from
// the task payload and write structured updates back for the reconciler.
//
// Why a sidecar? Executors run as separate processes; the only natural
// channel back to the task-runner artifact is stdout, which is truncated to
// 500 chars and shown to the operator. We want goal updates to be:
//   - structured (parseable JSON, not a regex on summary text)
//   - long enough to hold a real next-action description and state blob
//   - kept out of the human-readable summary
//
// So executors write `memory/fleet-goals/updates/{task_id}.json` and the
// reconciler picks it up alongside the artifact when classifying outcomes.
//
// Usage in an executor:
//   import { getGoalContext, writeGoalUpdate } from "./goal-context.mjs";
//   const goal = getGoalContext();
//   if (goal) { /* tailor behavior to goal.objective / goal.state / ... */ }
//   ...
//   if (goal) writeGoalUpdate({ taskId: task.id, goalId: goal.goal_id, next_action_hint: "...", state: {...} });

import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

export const UPDATES_DIR_REL = "memory/fleet-goals/updates";

// Reads goal context from GITLAWB_TASK_JSON. Returns null if the task has no
// goal_id (i.e. it was created by task-generator, not goal-reconciler).
export function getGoalContext(env = process.env) {
  const raw = env.GITLAWB_TASK_JSON;
  if (!raw) return null;
  let task;
  try { task = JSON.parse(raw); } catch { return null; }
  const payload = parsePayload(task.payload);
  if (!payload || !payload.goal_id) return null;
  return {
    task_id: task.id || task.task_id || task.taskId || null,
    goal_id: payload.goal_id,
    objective: payload.objective || null,
    success_criteria: payload.success_criteria || null,
    next_action_hint: payload.next_action_hint || null,
    state: payload.state && typeof payload.state === "object" ? payload.state : {},
  };
}

export function parsePayload(payload) {
  if (!payload) return {};
  if (typeof payload === "object") return payload;
  if (typeof payload === "string") {
    try { return JSON.parse(payload); } catch { return {}; }
  }
  return {};
}

// Writes a goal-update sidecar. The reconciler will apply the patch to the
// matching backlog goal when it classifies this task's outcome.
//
// Accepted fields:
//   taskId          — required (where the sidecar gets keyed)
//   goalId          — required (used by the reconciler to look up the goal)
//   next_action_hint — optional string, overwrites goal.next_action_hint
//   state           — optional object, shallow-merged onto goal.state
//   note            — optional short string for operator visibility (kept in sidecar, not summary)
//
// repoDir defaults to cwd so the path matches the reconciler's expectation.
export function writeGoalUpdate({ taskId, goalId, next_action_hint, state, note }, repoDir = process.cwd()) {
  if (!taskId || !goalId) {
    throw new Error("writeGoalUpdate requires taskId and goalId");
  }
  const update = {
    task_id: taskId,
    goal_id: goalId,
    written_at: new Date().toISOString(),
  };
  if (next_action_hint !== undefined) update.next_action_hint = next_action_hint;
  if (state !== undefined) update.state = state;
  if (note !== undefined) update.note = note;

  const path = join(repoDir, UPDATES_DIR_REL, `${taskId}.json`);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(update, null, 2) + "\n");
  return path;
}

// Apply an update sidecar to a goal record. Pure — exported so the
// reconciler can call it inside reconcileOutcomes without re-reading disk.
//
// Merge semantics:
//   - next_action_hint: replace (executor knows what to try next)
//   - state: shallow merge (executor patches specific keys; other state is preserved)
//   - unknown fields: ignored
export function applyGoalUpdate(goal, update) {
  if (!goal || !update) return false;
  let touched = false;
  if (typeof update.next_action_hint === "string") {
    goal.next_action_hint = update.next_action_hint;
    touched = true;
  }
  if (update.state && typeof update.state === "object") {
    goal.state = { ...(goal.state || {}), ...update.state };
    touched = true;
  }
  return touched;
}

// Path helper for the reconciler.
export function updateSidecarPath(taskId, repoDir = process.cwd()) {
  return join(repoDir, UPDATES_DIR_REL, `${taskId}.json`);
}

export function sidecarExists(taskId, repoDir = process.cwd()) {
  return existsSync(updateSidecarPath(taskId, repoDir));
}
