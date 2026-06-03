/**
 * goal-loop.test.mjs — Tests for the goal loop engine.
 *
 * Run: node scripts/fleet-executors/goal-loop.test.mjs
 */

import { GoalLoop, parseGoalAction, buildStepPrompt, GOAL_STEP_SYSTEM_PROMPT } from "./goal-loop.mjs";

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    passed++;
    console.log(`  ✓ ${label}`);
  } else {
    failed++;
    console.error(`  ✗ ${label}`);
  }
}

// ── parseGoalAction ──────────────────────────────────────────

console.log("parseGoalAction:");
{
  // Valid action
  const action = parseGoalAction('{"type":"action","action_name":"search","action_params":{"q":"test"},"description":"searching"}');
  assert(action !== null, "parses valid action");
  assert(action.type === "action", "type is action");
  assert(action.action_name === "search", "action_name preserved");

  // Valid complete
  const complete = parseGoalAction('{"type":"complete","title":"Done","body":"# Result","description":"finished"}');
  assert(complete !== null, "parses valid complete");
  assert(complete.type === "complete", "type is complete");
  assert(complete.title === "Done", "title preserved");

  // Valid noop
  const noop = parseGoalAction('{"type":"noop","description":"nothing to do"}');
  assert(noop !== null, "parses valid noop");
  assert(noop.type === "noop", "type is noop");

  // Valid needs_capability
  const cap = parseGoalAction('{"type":"needs_capability","description":"need web access","suggested_preset":"web"}');
  assert(cap !== null, "parses needs_capability");
  assert(cap.type === "needs_capability", "type is needs_capability");

  // Wrapped in prose
  const prose = parseGoalAction('Here is my decision:\n```json\n{"type":"noop","description":"thinking"}\n```\nDone.');
  assert(prose !== null, "parses JSON wrapped in prose");

  // Invalid: no type
  assert(parseGoalAction('{"foo":"bar"}') === null, "rejects missing type");

  // Invalid: empty string
  assert(parseGoalAction("") === null, "rejects empty string");

  // Invalid: malformed JSON
  assert(parseGoalAction("{broken json") === null, "rejects malformed JSON");

  // Invalid: action with no name
  assert(parseGoalAction('{"type":"action"}') === null, "rejects action without name");

  // Invalid: complete with no body
  assert(parseGoalAction('{"type":"complete","title":"x"}') === null, "rejects complete without body");
}

// ── buildStepPrompt ──────────────────────────────────────────

console.log("\nbuildStepPrompt:");
{
  const prompt = buildStepPrompt("test goal", [], 0, 100);
  assert(prompt.includes("test goal"), "contains goal");
  assert(prompt.includes("(no previous steps)"), "shows no-previous-steps");
  assert(prompt.includes("0 / 100"), "shows budget");

  const withSteps = buildStepPrompt("goal", [
    { action_type: "search", output_summary: "found 3 results" },
    { action_type: "read", output_summary: "read file.txt" },
  ], 50, 100);
  assert(withSteps.includes("search"), "shows previous step action");
  assert(withSteps.includes("50 / 100"), "shows updated budget");
}

// ── GoalLoop.run — Happy path ────────────────────────────────

console.log("\nGoalLoop.run — complete on first action:");
{
  let inferenceCalls = 0;

  const result = await GoalLoop.run({
    goal: "say hello",
    maxSteps: 5,
    inference: async () => {
      inferenceCalls++;
      return { content: '{"type":"complete","title":"Hello","body":"Hello, world!","description":"said hello"}' };
    },
    executeAction: async () => ({ output: "done", cost: 0 }),
  });

  assert(result.outcome === "complete", "outcome is complete");
  assert(result.stepsExecuted === 0, "no steps executed (completed immediately)");
  assert(result.artifact.title === "Hello", "artifact has title");
  assert(inferenceCalls === 1, "inference called once");
}

// ── GoalLoop.run — Multi-step ────────────────────────────────

console.log("\nGoalLoop.run — multi-step execution:");
{
  let stepCount = 0;

  const result = await GoalLoop.run({
    goal: "do two things",
    maxSteps: 10,
    inference: async () => {
      stepCount++;
      if (stepCount <= 2) {
        return { content: `{"type":"action","action_name":"step${stepCount}","action_params":{},"description":"doing step ${stepCount}"}` };
      }
      return { content: '{"type":"complete","title":"Done","body":"All done","description":"finished"}' };
    },
    executeAction: async ({ actionName }) => ({ output: `executed ${actionName}`, cost: 5 }),
  });

  assert(result.outcome === "complete", "outcome is complete");
  assert(result.stepsExecuted === 2, "2 steps executed");
  assert(result.creditsSpent === 10, "10 credits spent (2 x 5)");
  assert(result.artifact.body === "All done", "artifact body correct");
}

// ── GoalLoop.run — Max steps fallback ────────────────────────

console.log("\nGoalLoop.run — max steps fallback:");
{
  const result = await GoalLoop.run({
    goal: "infinite task",
    maxSteps: 3,
    inference: async () => ({ content: '{"type":"action","action_name":"loop","action_params":{},"description":"looping"}' }),
    executeAction: async () => ({ output: "looped", cost: 0 }),
  });

  assert(result.outcome === "complete", "fallback outcome is complete");
  assert(result.stepsExecuted === 3, "3 steps executed");
  assert(result.artifact.description.includes("maxSteps"), "description mentions max steps");
}

// ── GoalLoop.run — Unparseable fallback ──────────────────────

console.log("\nGoalLoop.run — unparseable fallback:");
{
  const result = await GoalLoop.run({
    goal: "confuse the parser",
    maxSteps: 10,
    maxConsecutiveNoops: 2,
    inference: async () => ({ content: "I don't know what to do, here's some prose" }),
    executeAction: async () => ({ output: "n/a", cost: 0 }),
  });

  assert(result.outcome === "complete", "fallback after unparseable");
  assert(result.artifact.description.includes("unparseable"), "mentions unparseable");
}

// ── GoalLoop.run — Noop limit ────────────────────────────────

console.log("\nGoalLoop.run — noop limit:");
{
  const result = await GoalLoop.run({
    goal: "do nothing",
    maxSteps: 10,
    maxConsecutiveNoops: 2,
    inference: async () => ({ content: '{"type":"noop","description":"waiting"}' }),
    executeAction: async () => ({ output: "n/a", cost: 0 }),
  });

  assert(result.outcome === "complete", "fallback after noops");
  assert(result.artifact.description.includes("no-ops"), "mentions no-ops");
}

// ── GoalLoop.run — Same description stuck ────────────────────

console.log("\nGoalLoop.run — same description stuck:");
{
  const result = await GoalLoop.run({
    goal: "repeat yourself",
    maxSteps: 10,
    maxReformulations: 2,
    inference: async () => ({ content: '{"type":"action","action_name":"x","action_params":{},"description":"same thing"}' }),
    executeAction: async () => ({ output: "did it", cost: 0 }),
  });

  assert(result.outcome === "blocked_stuck", "stuck after repeated description");
  assert(result.stuckReason.includes("same step repeated"), "stuck reason explains why");
}

// ── GoalLoop.run — Capability gap ────────────────────────────

console.log("\nGoalLoop.run — capability gap:");
{
  const result = await GoalLoop.run({
    goal: "do something impossible",
    maxSteps: 5,
    inference: async () => ({ content: '{"type":"needs_capability","description":"need database access"}' }),
    executeAction: async () => ({ output: "n/a", cost: 0 }),
  });

  assert(result.outcome === "blocked_capability", "blocked on capability gap");
  assert(result.capabilityNeeded === "need database access", "capability described");
}

// ── GoalLoop.run — Doom loop detection ───────────────────────

console.log("\nGoalLoop.run — doom loop:");
{
  let callCount = 0;

  const result = await GoalLoop.run({
    goal: "get stuck in a loop",
    maxSteps: 30,
    maxReformulations: 100, // disable description-based stuck detection
    inference: async () => {
      callCount++;
      // Return the same action with same params every time
      return { content: '{"type":"action","action_name":"stuck","action_params":{"x":1},"description":"step ' + callCount + '"}' };
    },
    executeAction: async () => ({ output: "done", cost: 0 }),
  });

  assert(result.outcome === "blocked_stuck", "stuck from doom loop");
  assert(result.stuckReason.includes("doom loop"), "stuck reason mentions doom loop");
}

// ── GoalLoop.run — onStep callback ───────────────────────────

console.log("\nGoalLoop.run — onStep callback:");
{
  const steps = [];

  await GoalLoop.run({
    goal: "callback test",
    maxSteps: 5,
    inference: async () => ({ content: '{"type":"complete","title":"Done","body":"ok","description":"done"}' }),
    executeAction: async () => ({ output: "result", cost: 0 }),
    onStep: (info) => steps.push(info),
  });

  // onStep is NOT called for complete (no action executed)
  assert(steps.length === 0, "onStep not called when completing immediately");
}

// ── GoalLoop.run — Action error ──────────────────────────────

console.log("\nGoalLoop.run — action error:");
{
  const result = await GoalLoop.run({
    goal: "handle errors",
    maxSteps: 5,
    inference: async () => ({ content: '{"type":"complete","title":"Done","body":"ok","description":"done"}' }),
    executeAction: async () => { throw new Error("action failed"); },
  });

  // Should still complete since the decision was "complete", not "action"
  assert(result.outcome === "complete", "completes despite action error");
}

// ── GoalLoop.run — Budget tracking ───────────────────────────

console.log("\nGoalLoop.run — budget tracking:");
{
  let stepNum = 0;

  const result = await GoalLoop.run({
    goal: "spend credits",
    maxSteps: 5,
    budgetCredits: 100,
    inference: async () => {
      stepNum++;
      if (stepNum <= 3) {
        return { content: `{"type":"action","action_name":"work","action_params":{},"description":"step ${stepNum}"}` };
      }
      return { content: '{"type":"complete","title":"Done","body":"ok","description":"done"}' };
    },
    executeAction: async () => ({ output: "did work", cost: 50 }),
  });

  assert(result.outcome === "complete", "completes");
  assert(result.creditsSpent === 150, "spent 150 (3 x 50)");
  // Budget is soft, so it doesn't block
}

// ── GOAL_STEP_SYSTEM_PROMPT ──────────────────────────────────

console.log("\nGOAL_STEP_SYSTEM_PROMPT:");
{
  assert(GOAL_STEP_SYSTEM_PROMPT.includes("action"), "mentions actions");
  assert(GOAL_STEP_SYSTEM_PROMPT.includes("complete"), "mentions complete");
  assert(GOAL_STEP_SYSTEM_PROMPT.includes("noop"), "mentions noop");
  assert(GOAL_STEP_SYSTEM_PROMPT.includes("JSON"), "mentions JSON output");
}

// ── Results ──────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
