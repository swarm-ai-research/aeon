/**
 * autonomous-fleet-executor.test.mjs — Tests for the Codex-native fleet executor.
 *
 * Run: node scripts/fleet-executors/autonomous-fleet-executor.test.mjs
 */

import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";
import { DoomLoopDetector } from "./doom-loop.mjs";
import { getActionsForSignal } from "./signal-action-map.mjs";

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

// Repo root resolved from this file's location (scripts/fleet-executors/),
// so the suite is portable across machines and CI checkouts.
const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const TEST_DIR = mkdtempSync(join(tmpdir(), "autonomous-fleet-executor-test-"));
const STATE_FILE = join(TEST_DIR, "fleet-state.json");

function runExecutor(taskPayload, agentConfig) {
  return spawnSync("node", ["scripts/fleet-executors/autonomous-fleet-executor.mjs"], {
    cwd: REPO,
    encoding: "utf8",
    timeout: 30000,
    env: {
      ...process.env,
      GITLAWB_TASK_JSON: JSON.stringify({ id: "test", kind: "research", payload: taskPayload }),
      GITLAWB_AGENT_JSON: JSON.stringify(agentConfig),
      GITLAWB_REPO_DIR: REPO,
      GITLAWB_AUTONOMOUS_STATE_FILE: STATE_FILE,
    },
  });
}

// ── Syntax ───────────────────────────────────────────────────

console.log("Syntax:");
{
  const p = spawnSync("node", ["-c", "scripts/fleet-executors/autonomous-fleet-executor.mjs"], { encoding: "utf8", cwd: REPO });
  assert(p.status === 0, "parses cleanly");
}

// ── Building blocks ──────────────────────────────────────────

console.log("\nBuilding blocks:");
{
  const m1 = await import("./doom-loop.mjs");
  assert(typeof m1.DoomLoopDetector === "function", "DoomLoopDetector");
  const m2 = await import("./signal-action-map.mjs");
  assert(typeof m2.getActionsForSignal === "function", "getActionsForSignal");
}

// ── Goal extraction ──────────────────────────────────────────

console.log("\nGoal extraction:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { stdout } = runExecutor(
    { title: "Analyze changes", topic: "executors", scope: "scripts/" },
    { name: "aeon-researcher", capabilities: ["git:fetch", "issue:create"], purpose: "Research agent" }
  );
  const out = JSON.parse(stdout);
  assert(out.task.goal.includes("Analyze changes"), "has title");
  assert(out.task.goal.includes("executors"), "has topic");
  assert(out.task.goal.includes("scripts/"), "has scope");
  assert(out.task.goal.includes("Research agent"), "has purpose");
}

// ── Signal type ──────────────────────────────────────────────

console.log("\nSignal type:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { stdout } = runExecutor(
    { title: "test" },
    { name: "aeon-researcher", capabilities: ["git:fetch"] }
  );
  const out = JSON.parse(stdout);
  assert(out.task.signalType === "manual_trigger", "research → manual_trigger");
}

// ── Capability constraints ───────────────────────────────────

console.log("\nCapability constraints:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { stdout } = runExecutor(
    { title: "test" },
    { name: "aeon-researcher", capabilities: ["git:fetch", "issue:create"] }
  );
  const out = JSON.parse(stdout);
  assert(out.actions.available.includes("create_issue"), "researcher can create issues");
  assert(out.actions.available.includes("read_file"), "researcher can read files");
  assert(!out.actions.available.includes("merge_pr"), "researcher cannot merge PRs");

  try { rmSync(STATE_FILE); } catch {}
  const { stdout: s2 } = runExecutor(
    { title: "test" },
    { name: "aeon-deployer", capabilities: ["git:push", "pr:merge", "agent:deploy"] }
  );
  const out2 = JSON.parse(s2);
  assert(out2.actions.available.includes("merge_pr"), "deployer can merge PRs");
}

// ── Context ──────────────────────────────────────────────────

console.log("\nContext:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { stdout } = runExecutor(
    { title: "test" },
    { name: "test-agent", capabilities: ["git:fetch"] }
  );
  const out = JSON.parse(stdout);
  assert(out.context.branch.length > 0, "branch detected");
  assert(typeof out.context.recentCommits === "string", "recentCommits present");
}

// ── Doom loop ────────────────────────────────────────────────

console.log("\nDoom loop:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { stdout } = runExecutor(
    { title: "test" },
    { name: "test-agent", capabilities: [] }
  );
  const out = JSON.parse(stdout);
  assert(out.doomLoop.detected === false, "no doom loop on first run");
}

// ── State persistence ────────────────────────────────────────

console.log("\nState persistence:");
{
  try { rmSync(STATE_FILE); } catch {}

  const env = {
    ...process.env,
    GITLAWB_TASK_JSON: JSON.stringify({ id: "state-test", kind: "research", payload: { title: "state" } }),
    GITLAWB_AGENT_JSON: JSON.stringify({ name: "test-agent", capabilities: [] }),
    GITLAWB_REPO_DIR: REPO,
    GITLAWB_AUTONOMOUS_STATE_FILE: STATE_FILE,
  };

  const r1 = spawnSync("node", ["scripts/fleet-executors/autonomous-fleet-executor.mjs"], { cwd: REPO, encoding: "utf8", timeout: 15000, env });
  assert(JSON.parse(r1.stdout).state.stepCount === 0, "first run: step 0");

  const r2 = spawnSync("node", ["scripts/fleet-executors/autonomous-fleet-executor.mjs"], { cwd: REPO, encoding: "utf8", timeout: 15000, env });
  assert(JSON.parse(r2.stdout).state.stepCount === 1, "second run: step 1");

  try { rmSync(STATE_FILE); } catch {}
}

// ── Output format ────────────────────────────────────────────

console.log("\nOutput format:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { stdout } = runExecutor(
    { title: "Fix the bug" },
    { name: "aeon-researcher", capabilities: ["git:fetch"] }
  );
  const out = JSON.parse(stdout);
  assert(out.type === "fleet_autonomous_step", "type field");
  assert(out.instructions.includes("aeon-researcher"), "instructions mention agent");
  assert(out.instructions.includes("Fix the bug"), "instructions mention goal");
  assert(out.instructions.includes("Step 1"), "instructions mention step");
  assert(typeof out.actions.prompt === "string", "has action prompt");
}

// ── Goal context: sidecar written for goal-spawned tasks ─────
//
// Regression guard for PR #122 Codex review: live aeon-researcher runs THIS
// executor (not researcher.mjs), so goal-spawned tasks must produce the
// sidecar here too — otherwise next_action_hint / state never advance.

console.log("\nGoal context sidecar:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { mkdtempSync: mk, existsSync, readFileSync, rmSync: rm } = await import("node:fs");
  const goalRepo = mk(join(tmpdir(), "autonomous-fleet-goal-repo-"));
  const taskId = "11111111-2222-3333-4444-555555555555";
  const payload = { goal_id: "g-research-test", title: "T", objective: "obj", next_action_hint: "do X", state: { prev: 1 } };
  const env = {
    ...process.env,
    GITLAWB_TASK_JSON: JSON.stringify({ id: taskId, kind: "research", payload }),
    GITLAWB_AGENT_JSON: JSON.stringify({ name: "aeon-researcher", capabilities: ["issue:create"] }),
    GITLAWB_REPO_DIR: goalRepo,
    GITLAWB_AUTONOMOUS_STATE_FILE: STATE_FILE,
  };
  const r = spawnSync("node", ["scripts/fleet-executors/autonomous-fleet-executor.mjs"], { cwd: REPO, encoding: "utf8", timeout: 15000, env });
  const out = JSON.parse(r.stdout);
  assert(out.goalContext && out.goalContext.goal_id === "g-research-test", "goalContext surfaced in output");
  assert(out.instructions.includes("Goal context"), "instructions mention goal context");
  assert(out.instructions.includes("do X"), "instructions carry forward next_action_hint");

  const sidecar = join(goalRepo, "memory/fleet-goals/updates", `${taskId}.json`);
  assert(existsSync(sidecar), "sidecar written under repoDir");
  const update = JSON.parse(readFileSync(sidecar, "utf8"));
  assert(update.goal_id === "g-research-test", "sidecar carries goal id");
  assert(update.state.prev === 1, "sidecar preserves prior state");
  assert(typeof update.state.last_step_count === "number", "sidecar records step progress");
  assert(typeof update.next_action_hint === "string" && update.next_action_hint.length > 0, "sidecar writes a next-action hint");
  try { rm(goalRepo, { recursive: true, force: true }); } catch {}
}

// ── Goal context: no sidecar when task lacks goal_id ─────────
console.log("\nNo sidecar without goal_id:");
{
  try { rmSync(STATE_FILE); } catch {}
  const { mkdtempSync: mk, existsSync, rmSync: rm } = await import("node:fs");
  const repo = mk(join(tmpdir(), "autonomous-fleet-nogoal-repo-"));
  const env = {
    ...process.env,
    GITLAWB_TASK_JSON: JSON.stringify({ id: "no-goal", kind: "research", payload: { title: "plain task" } }),
    GITLAWB_AGENT_JSON: JSON.stringify({ name: "aeon-researcher", capabilities: [] }),
    GITLAWB_REPO_DIR: repo,
    GITLAWB_AUTONOMOUS_STATE_FILE: STATE_FILE,
  };
  spawnSync("node", ["scripts/fleet-executors/autonomous-fleet-executor.mjs"], { cwd: REPO, encoding: "utf8", timeout: 15000, env });
  assert(!existsSync(join(repo, "memory/fleet-goals/updates")), "no updates dir created for non-goal tasks");
  try { rm(repo, { recursive: true, force: true }); } catch {}
}

// ── Results ──────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
try { rmSync(TEST_DIR, { recursive: true, force: true }); } catch {}
if (failed > 0) throw new Error(`${failed} test(s) failed`);
