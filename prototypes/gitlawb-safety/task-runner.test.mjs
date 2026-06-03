#!/usr/bin/env node
// Offline tests for the GitLawb task runner.

import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    passed += 1;
    console.log(`  ✓ ${label}`);
  } else {
    failed += 1;
    console.error(`  ✗ ${label}`);
  }
}

const REPO = process.cwd();
const tmp = mkdtempSync(join(tmpdir(), "gitlawb-task-runner-test-"));
const artifactsDir = join(tmp, "artifacts");
mkdirSync(artifactsDir, { recursive: true });

const instancesPath = join(tmp, "instances.json");
const tasksPath = join(tmp, "tasks.json");
const configPath = join(tmp, "runner.json");
const mockExecutorPath = join(tmp, "mock-autonomous-executor.mjs");
const mockHarnessPath = join(tmp, "mock-harness.mjs");

writeFileSync(instancesPath, JSON.stringify({
  instances: [{
    name: "aeon-researcher",
    did: "did:key:test-researcher",
    host: "gitlawb",
    status: "active",
    capabilities: ["git:fetch", "issue:create"],
    purpose: "Research and analysis",
  }],
}, null, 2));

writeFileSync(tasksPath, JSON.stringify({
  tasks: [{
    id: "task-autonomous",
    kind: "research",
    status: "pending",
    assignee_did: "did:key:test-researcher",
    payload: { title: "Exercise autonomous task loop" },
  }],
}, null, 2));

writeFileSync(mockExecutorPath, `
const last = process.env.GITLAWB_LAST_ACTION_JSON ? JSON.parse(process.env.GITLAWB_LAST_ACTION_JSON) : null;
console.log(JSON.stringify({
  type: "fleet_autonomous_step",
  status: "in_progress",
  task: { id: "task-autonomous", goal: "Exercise autonomous task loop" },
  actions: { available: ["read_file", "create_issue"] },
  state: { stepCount: last ? 1 : 0, previousActions: last ? [last.name] : [] },
  doomLoop: { detected: false }
}));
`);

writeFileSync(mockHarnessPath, `
let input = "";
process.stdin.on("data", chunk => { input += chunk; });
process.stdin.on("end", () => {
  if (input.includes('"stepCount": 0')) {
    console.log(JSON.stringify({
      type: "action",
      name: "read_file",
      params: { path: "README.md" },
      description: "read README for task context"
    }));
  } else {
    console.log(JSON.stringify({
      type: "complete",
      summary: "mock autonomous task completed after one reported action",
      description: "executor observed prior action"
    }));
  }
});
`);

writeFileSync(configPath, JSON.stringify({
  repoDir: REPO,
  agents: {
    "aeon-researcher": {
      executor: "autonomous",
      command: `node ${JSON.stringify(mockExecutorPath)}`,
      harnessCommand: `node ${JSON.stringify(mockHarnessPath)}`,
      maxSteps: 3,
    },
  },
}, null, 2));

console.log("Autonomous task-runner loop:");
{
  const proc = spawnSync("node", [
    "prototypes/gitlawb-safety/task-runner.mjs",
    "once",
    "--instances", instancesPath,
    "--config", configPath,
    "--tasks-file", tasksPath,
    "--artifacts-dir", artifactsDir,
    "--dry-run",
    "--agent", "researcher",
  ], {
    cwd: REPO,
    encoding: "utf8",
    timeout: 30000,
  });

  assert(proc.status === 0, `runner exits 0 (${proc.stderr || proc.stdout})`);
  assert(proc.stdout.includes("AUTONOMOUS_STEP aeon-researcher task-autonomous step=1"), "logs first autonomous step");
  assert(proc.stdout.includes("AUTONOMOUS_STEP aeon-researcher task-autonomous step=2"), "feeds last action into second step");
  assert(proc.stdout.includes("TASK_OK aeon-researcher task-autonomous"), "task completes");

  const artifactPath = join(artifactsDir, "task-autonomous.json");
  assert(existsSync(artifactPath), "writes task artifact");
  const artifact = JSON.parse(readFileSync(artifactPath, "utf8"));
  assert(artifact.result.executor === "autonomous", "artifact records autonomous executor");
  assert(artifact.result.steps.length === 2, "artifact records both loop steps");
  assert(artifact.result.steps[0].decision.name === "read_file", "artifact records harness action");
  assert(artifact.result.summary.includes("mock autonomous task completed"), "artifact records final summary");
}

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) throw new Error(`${failed} test(s) failed`);
