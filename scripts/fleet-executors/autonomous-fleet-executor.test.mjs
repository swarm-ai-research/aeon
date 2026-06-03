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

// ── Results ──────────────────────────────────────────────────

console.log(`\n${passed} passed, ${failed} failed`);
try { rmSync(TEST_DIR, { recursive: true, force: true }); } catch {}
if (failed > 0) throw new Error(`${failed} test(s) failed`);
