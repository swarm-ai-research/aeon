#!/usr/bin/env node
// autonomous-fleet-executor.mjs — Codex-native autonomous fleet executor.
//
// This script is designed to be run REPEATEDLY by Codex (the LLM powering
// GitHub Actions). Each run:
//   1. Reads task/agent context from env vars
//   2. Gathers repo state (git log, changes, etc.)
//   3. Checks previous actions from a state file
//   4. Uses doom-loop detection to spot stuck states
//   5. Outputs a structured JSON block telling Codex what to do next
//
// Codex reads the output, executes the recommended action (or its own
// judgment call), then runs this script again — reporting what it did via
// GITLAWB_LAST_ACTION_JSON so the action history (and doom-loop detection)
// can accumulate across runs. Each run reports `status`: "in_progress" or
// "doom_loop"; the harness decides when the task is complete and marks it.
//
// No external API keys needed — Codex IS the LLM.
//
// Env vars (set by task-runner / harness):
//   GITLAWB_TASK_JSON         — full task object
//   GITLAWB_AGENT_JSON        — agent instance object
//   GITLAWB_REPO_DIR          — repo working directory
//   GITLAWB_AUTONOMOUS_STATE_FILE — per-task action history path (optional)
//   GITLAWB_LAST_ACTION_JSON  — {name, params?, description?} the harness ran
//                               last (optional; appended to action history)

import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { DoomLoopDetector } from "./doom-loop.mjs";
import { formatActionsForPrompt } from "./signal-action-map.mjs";
import { getGoalContext, writeGoalUpdate } from "./goal-context.mjs";

// ── Bootstrap ────────────────────────────────────────────────

function safeParse(json, fallback) {
  try { return JSON.parse(json); } catch { return fallback; }
}

const repoDir = process.env.GITLAWB_REPO_DIR || ".";
const task = safeParse(process.env.GITLAWB_TASK_JSON, {});
const agent = safeParse(process.env.GITLAWB_AGENT_JSON, {});

// payload may be a JSON string, an object, or malformed — never let it crash.
const payload = typeof task.payload === "string" ? safeParse(task.payload, {}) : (task.payload || {});
const stateFile = process.env.GITLAWB_AUTONOMOUS_STATE_FILE || join(repoDir, ".fleet-state.json");

// ── State management ─────────────────────────────────────────

function loadState() {
  try {
    if (existsSync(stateFile)) {
      return JSON.parse(readFileSync(stateFile, "utf8"));
    }
  } catch {}
  return { actions: [], stepCount: 0, startedAt: new Date().toISOString() };
}

function saveState(state) {
  try {
    writeFileSync(stateFile, JSON.stringify(state, null, 2), "utf8");
  } catch {}
}

// ── Goal extraction ──────────────────────────────────────────

function extractGoal() {
  const parts = [];
  if (payload.title) parts.push(payload.title);
  if (payload.topic) parts.push(`Topic: ${payload.topic}`);
  if (payload.prompt) parts.push(payload.prompt);
  if (payload.focus) parts.push(`Focus: ${payload.focus}`);
  if (payload.target) parts.push(`Target: ${payload.target}`);
  if (payload.description) parts.push(payload.description);
  if (payload.scope) parts.push(`Scope: ${payload.scope}`);

  if (parts.length === 0) {
    parts.push(`Complete a ${task.kind || "research"} task`);
  }

  if (agent.purpose) parts.push(`Your role: ${agent.purpose}`);
  return parts.join("\n");
}

// ── Signal type ──────────────────────────────────────────────

function inferSignalType() {
  const kind = (task.kind || "").toLowerCase();
  if (kind.includes("review")) return "pr_opened";
  if (kind.includes("deploy")) return "deploy_started";
  if (kind.includes("audit") || kind.includes("sentinel")) return "scheduled_tick";
  return "manual_trigger";
}

// ── Capabilities → actions ───────────────────────────────────

const CAPABILITY_ACTIONS = {
  "git:fetch": ["run_command", "read_file", "search_code"],
  "git:push": ["run_command", "write_file"],
  "issue:create": ["create_issue"],
  "issue:comment": ["post_comment"],
  "issue:close": ["close_issue"],
  "pr:open": ["create_pr"],
  "pr:review": ["review_pr"],
  "pr:merge": ["merge_pr"],
  "repo:admin": ["run_command", "read_file", "write_file", "list_dir"],
  "agent:deploy": ["run_command"],
};

function getAgentActions() {
  const caps = agent.capabilities || [];
  const actions = new Set(["ignore", "execute", "read_file", "search_code", "run_command"]);
  for (const cap of caps) {
    for (const a of (CAPABILITY_ACTIONS[cap] || [])) actions.add(a);
  }
  return [...actions];
}

// ── Context gathering ────────────────────────────────────────

function run(cmd, args, opts = {}) {
  const proc = spawnSync(cmd, args, { cwd: repoDir, encoding: "utf8", timeout: 15000, ...opts });
  return (proc.stdout || "").trim();
}

function gatherContext() {
  const recentCommits = run("git", ["log", "--oneline", "-10", "--since=3 days ago"]);
  const recentFiles = run("git", ["diff", "--name-only", "HEAD~5..HEAD"]);
  const branch = run("git", ["branch", "--show-current"]);
  const status = run("git", ["status", "--short"]);

  let scopeContents = "";
  if (payload.scope) {
    const files = payload.scope.split(",").map(s => s.trim()).filter(Boolean);
    const snippets = [];
    for (const f of files.slice(0, 5)) {
      const fullPath = join(repoDir, f);
      if (existsSync(fullPath)) {
        try {
          const content = readFileSync(fullPath, "utf8");
          snippets.push(`### ${f}\n\`\`\`\n${content.slice(0, 2000)}\n\`\`\``);
        } catch {}
      }
    }
    scopeContents = snippets.join("\n\n");
  }

  return { recentCommits, recentFiles, branch, status, scopeContents };
}

// ── Main ─────────────────────────────────────────────────────

function main() {
  const state = loadState();
  const goal = extractGoal();
  const signalType = inferSignalType();
  const actions = getAgentActions();
  const context = gatherContext();

  // Codex review on PR #122 flagged that goal-context wiring landed only in
  // researcher.mjs, but the live aeon-researcher runs THIS script. So
  // goal-spawned researcher tasks never produced a sidecar and the goal's
  // next_action_hint / state never advanced between cycles. Pick up the goal
  // context here too so the LLM prompt is goal-aware AND a sidecar is written.
  const goalCtx = getGoalContext();

  // Record the action the harness executed since the last run, if it reported
  // one (GITLAWB_LAST_ACTION_JSON = {name, params?, description?}). Without this
  // the history never grows and doom-loop / previousActions stay empty.
  const lastAction = safeParse(process.env.GITLAWB_LAST_ACTION_JSON, null);
  if (lastAction && lastAction.name) {
    state.actions.push({
      name: lastAction.name,
      params: lastAction.params || {},
      description: lastAction.description || "",
      at: new Date().toISOString(),
    });
  }

  // Doom loop check
  const detector = new DoomLoopDetector({ lookback: 20, threshold: 3 });
  for (const action of state.actions) {
    detector.record(action.name, action.params || {});
  }
  const doomResult = detector.check();

  const output = {
    type: "fleet_autonomous_step",
    // The harness marks the task complete; this script reports its own view:
    // "doom_loop" when a stuck pattern is detected, else "in_progress".
    status: doomResult ? "doom_loop" : "in_progress",
    task: {
      id: task.id,
      kind: task.kind,
      goal,
      signalType,
    },
    agent: {
      name: agent.name,
      did: agent.did,
      capabilities: agent.capabilities,
    },
    context: {
      branch: context.branch,
      recentCommits: context.recentCommits || "(none)",
      recentFiles: context.recentFiles || "(none)",
      workingTreeStatus: context.status || "(clean)",
      scopeContents: context.scopeContents || null,
    },
    actions: {
      available: actions,
      // Format the capability-filtered actions (not the raw signal map) so the
      // prompt never advertises actions this agent isn't allowed to perform.
      prompt: formatActionsForPrompt(actions),
    },
    state: {
      stepCount: state.stepCount,
      previousActions: state.actions.slice(-5).map(a => `${a.name}: ${(a.description || "").slice(0, 80)}`),
      startedAt: state.startedAt,
    },
    doomLoop: doomResult ? {
      detected: true,
      message: doomResult.message,
      corrective: doomResult.corrective,
    } : { detected: false },
    goalContext: goalCtx ? {
      goal_id: goalCtx.goal_id,
      objective: goalCtx.objective,
      success_criteria: goalCtx.success_criteria,
      next_action_hint: goalCtx.next_action_hint,
      state: goalCtx.state,
    } : null,
    instructions: [
      `You are ${agent.name || "a fleet agent"}. Your goal: ${goal}`,
      "",
      goalCtx
        ? `**Goal context:** \`${goalCtx.goal_id}\`. Carry-forward hint from last cycle: ${goalCtx.next_action_hint || "(none)"}. Prior state: ${JSON.stringify(goalCtx.state)}.`
        : "",
      `Available actions: ${actions.join(", ")}`,
      "",
      doomResult
        ? `⚠ DOOM LOOP DETECTED: ${doomResult.message}. ${doomResult.corrective}`
        : `Step ${state.stepCount + 1}. Choose the next action to accomplish the goal.`,
      "",
      "Execute the action directly (run commands, read files, create issues, etc.),",
      "then run this script again. When the goal is accomplished, create the final",
      "artifact (issue, PR, or summary) and mark the task complete.",
      "",
      "If you cannot accomplish the goal, explain why and mark the task as failed.",
    ].filter(Boolean).join("\n"),
  };

  console.log(JSON.stringify(output, null, 2));

  state.stepCount++;
  saveState(state);

  // Write a goal-update sidecar so the reconciler can advance the goal's
  // next_action_hint / state between cycles. Each step rewrites it with the
  // latest step count and most recent action history — even if Codex never
  // explicitly writes one, the goal moves forward instead of resetting.
  // Sidecar failures must not poison the step (executor stdout is the task
  // artifact channel — silently swallow on write error).
  if (goalCtx && goalCtx.task_id) {
    try {
      const recent = state.actions.slice(-5).map((a) => a.name).filter(Boolean);
      const nextHint = doomResult
        ? `Doom loop after step ${state.stepCount}: ${doomResult.message}. ${doomResult.corrective}`
        : `Resume from step ${state.stepCount} on branch ${context.branch || "(unknown)"}. Recent actions: ${recent.join(" → ") || "(none)"}.`;
      writeGoalUpdate({
        taskId: goalCtx.task_id,
        goalId: goalCtx.goal_id,
        next_action_hint: nextHint,
        state: {
          ...goalCtx.state,
          last_step_count: state.stepCount,
          last_branch: context.branch || null,
          last_recent_actions: recent,
          last_run_at: new Date().toISOString(),
        },
        note: doomResult
          ? `Autonomous executor flagged doom loop for ${goalCtx.goal_id} at step ${state.stepCount}.`
          : `Autonomous executor advanced ${goalCtx.goal_id} to step ${state.stepCount}.`,
      }, repoDir);
    } catch (err) {
      console.error(`[goal-context] writeGoalUpdate failed: ${err.message}`);
    }
  }
}

main();
