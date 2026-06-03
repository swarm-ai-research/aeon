#!/usr/bin/env node
// task-generator.mjs — Automatic task creation for the Aeon fleet.
//
// Analyzes repo state (recent commits, open PRs, fleet health, time since
// last run) and creates tasks for agents via `gl task create`.
//
// Must run BEFORE the task runner. Uses operator identity for task creation
// (agent self-creation reassigns to operator).
//
// Env vars:
//   GITLAWB_NODE     — GitLawb node URL (default: https://node.gitlawb.com)
//   GITLAWB_REPO_DIR — repo working directory (default: .)

import { spawnSync } from "node:child_process";
import { readFileSync, existsSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const repoDir = process.env.GITLAWB_REPO_DIR || ".";
const node = process.env.GITLAWB_NODE || "https://node.gitlawb.com";
const stateFile = join(repoDir, "memory/fleet-task-generator-state.json");

function run(cmd, args, opts = {}) {
  const proc = spawnSync(cmd, args, { cwd: opts.cwd || repoDir, encoding: "utf8" });
  return { ok: proc.status === 0, stdout: (proc.stdout || "").trim(), stderr: (proc.stderr || "").trim() };
}

// Load generator state
let state = { lastRun: null, tasksCreated: {} };
if (existsSync(stateFile)) {
  try { state = JSON.parse(readFileSync(stateFile, "utf8")); } catch {}
}

const now = new Date();
const iso = now.toISOString();

function dailySweepSeeds(date) {
  const ymd = date.toISOString().slice(0, 10).replaceAll("-", "");
  // 12 date-derived seeds per day — enough samples for a usable mean ± CI and
  // win-rate per mode, while staying deterministic for a given date.
  return Array.from({ length: 12 }, (_, i) => Number(`${ymd}${i + 1}`));
}

// Agent definitions
const agents = {
  researcher: {
    did: "did:key:z6MkfnrSDgdDbkvfCCnMyaR4HqoWfWEfGoTFajX1HGkSHRUH",
    kind: "research",
    capability: "issue:create",
  },
  reviewer: {
    did: "did:key:z6Mks2KSBfbindXsw2SBEGfqdgMJ4HwxJPfPQjkPKHY7U7SZ",
    kind: "code-review",
    capability: "pr:review",
  },
  deployer: {
    did: "did:key:z6MknGJBoQsbNL956GNiTJRRWKJqMcprWmdYxJPbVGCwcAuS",
    kind: "deploy",
    capability: "pr:merge",
  },
  sentinel: {
    did: "did:key:z6MksUuVYyp93QA6pc2qAnXFQZdaoHq46dugXVweeehX4S2M",
    kind: "audit",
    capability: "repo:admin",
  },
};

// Check existing pending tasks to avoid flooding
function getPendingTasks(agentDid, limit = 5) {
  const result = run("gl", ["task", "list", "--status", "pending", "--assignee-did", agentDid, "--limit", String(limit), "--node", node]);
  if (!result.ok) return [];
  try {
    const data = JSON.parse(result.stdout);
    return data.tasks || [];
  } catch {
    return [];
  }
}

// Create a task. `opts.kind` / `opts.capability` override the agent defaults
// (used for cross-cutting tasks like the compute-futures sim).
function createTask(agent, payload, opts = {}) {
  // `gl task create [OPTIONS] <KIND>` — KIND is a positional argument, not a
  // --kind flag. Passing --kind makes every creation fail with
  // "unexpected argument '--kind'", which is why the fleet logged
  // "processed 0 tasks" indefinitely.
  const args = [
    "task", "create",
    opts.kind || agent.kind,
    "--assignee-did", agent.did,
    "--capability", opts.capability || agent.capability,
    "--payload", JSON.stringify(payload),
    "--node", node,
  ];
  const result = run("gl", args);
  if (!result.ok) {
    console.error(`  Failed to create task for ${agent.did}: ${result.stderr || result.stdout}`);
    return false;
  }
  console.log(`  Task created: ${result.stdout}`);
  return true;
}

// Gather repo state
const openPRs = run("gl", ["pr", "list", "aeon", "--node", node]);
const prCount = (openPRs.stdout || "").split("\n").filter(Boolean).length;

// actions/checkout defaults to a depth=1 shallow clone, so HEAD~10 has no
// ancestor in CI and `git diff HEAD~10..HEAD` fails — silently returning [] and
// disabling reviewer/researcher task generation. Clamp the range to the history
// actually available, and fall back to the last commit's files when depth is 1.
const commitsAvailable = parseInt((run("git", ["rev-list", "--count", "HEAD"]).stdout || "1").trim(), 10) || 1;
const diffDepth = Math.min(10, commitsAvailable - 1);
const recentFiles = diffDepth > 0
  ? run("git", ["diff", "--name-only", `HEAD~${diffDepth}..HEAD`])
  : run("git", ["show", "--name-only", "--pretty=format:", "HEAD"]);
const changedFiles = (recentFiles.stdout || "").split("\n").filter(Boolean);

// Current commit. The researcher/reviewer gate on this so they only regenerate
// work when HEAD has actually advanced — `changedFiles` is *always* populated
// (last 10 commits, or HEAD under the depth-1 checkout), so without a revision
// check the cooldown alone would recreate the same "analyze/review recent
// changes" task every cycle during idle periods and flood the live fleet.
const headSha = (run("git", ["rev-parse", "HEAD"]).stdout || "").trim();

const tasksCreated = [];

// Per-agent cooldowns (hours). The generator runs every ~5 min, so these
// throttle how often each agent gets fresh work. Each agent tracks its OWN
// last-created timestamp — gating on the shared `lastRun` (bumped every run)
// kept `hoursSinceLastRun` near-zero forever, which permanently starved the
// researcher and reviewer (they never fired in production). Tune these to make
// the fleet busier (lower = more tasks/PRs) or quieter (higher).
const RESEARCH_COOLDOWN_H = 1;
const REVIEW_COOLDOWN_H = 0.5;
const AUDIT_COOLDOWN_H = 6;
const DEPLOY_PROOF_COOLDOWN_H = 12;
// Fallback: when the reviewer's HEAD-advanced gate is closed (main is quiet)
// but open PRs exist on gitlawb, give the reviewer a task to look at one of
// them. This keeps the reviewer producing during idle stretches on main.
const OPEN_PR_REVIEW_COOLDOWN_H = 2;
// Max review tasks created per cycle (one per changed file, code files first).
// The reviewer holds pr:open, so each task can land as a PR — this is the
// strongest per-cycle PR multiplier without provisioning new agent identities.
const MAX_REVIEW_FANOUT = 5;
// Code-quality pass kinds emitted alongside the main review task when changed
// files look like code. Each becomes a separate task → separate PR surface,
// dispatched by reviewer.mjs to claude-code-pass.mjs (which actually drives
// claude with file-edit tools and opens a PR via `gh`).
const CODE_PASS_KINDS = ["docs-pass", "refactor-pass", "test-pass"];
const CODE_PASS_COOLDOWN_H = 3;
// Fork cadence — daily. Targets live in memory/fork-targets.json so the
// operator can curate them. Forker tasks go to the deployer DID (needs
// `git:push` → `run_command` to invoke `gl repo fork` / `gl mirror`).
const FORK_COOLDOWN_H = 24;
const FORK_TARGETS_FILE = join(repoDir, "memory/fork-targets.json");

// ── Researcher: Analyze recent changes ──
// Gated on its own timer + changed files (not commitCount: the CI checkout is a
// depth-1 shallow clone, so commitCount maxed out at 1 and the old
// `commitCount > 3` test could never pass) + a HEAD-advanced check so idle
// periods don't recreate the same analysis task every cooldown window.
const hoursSinceResearch = state.lastResearcherTask
  ? (now - new Date(state.lastResearcherTask)) / (1000 * 60 * 60)
  : 999;
const researchHeadAdvanced = headSha !== "" && headSha !== state.lastResearchedHead;

if (hoursSinceResearch > RESEARCH_COOLDOWN_H && changedFiles.length > 0 && researchHeadAdvanced) {
  const pending = getPendingTasks(agents.researcher.did);
  if (pending.length === 0) {
    console.log("[researcher] Creating task: analyze recent changes");
    const created = createTask(agents.researcher, {
      title: `Analyze recent repo changes (${changedFiles.length} files)`,
      topic: "recent repository changes",
      scope: changedFiles.slice(0, 5).join(", ") || "full repo",
    });
    if (created) {
      tasksCreated.push("researcher");
      state.lastResearcherTask = iso;
      state.lastResearchedHead = headSha;
    }
  } else {
    console.log(`[researcher] Skipping — ${pending.length} pending task(s)`);
  }
} else if (hoursSinceResearch > RESEARCH_COOLDOWN_H && changedFiles.length > 0) {
  console.log(`[researcher] Skipping — HEAD ${headSha.slice(0, 7)} already analyzed`);
}

// ── Reviewer: Review new or changed files ──
// The reviewer holds pr:open — this is the agent that turns review findings
// into PRs, so it's the primary lever on PR volume. Own timer; fires when HEAD
// has advanced since its last review so idle periods don't re-review the same
// commit every cooldown window.
const hoursSinceReview = state.lastReviewerTask
  ? (now - new Date(state.lastReviewerTask)) / (1000 * 60 * 60)
  : 999;
const reviewHeadAdvanced = headSha !== "" && headSha !== state.lastReviewedHead;

if (hoursSinceReview > REVIEW_COOLDOWN_H && changedFiles.length > 0 && reviewHeadAdvanced) {
  const pending = getPendingTasks(agents.reviewer.did);
  if (pending.length === 0) {
    // Fan-out: enqueue one review per changed file (code files first), capped
    // by MAX_REVIEW_FANOUT so a noisy commit can't flood the fleet. Each task
    // is independent → independent PR surface.
    const isCode = (f) => /\.(mjs|js|ts|tsx|py|go|rs|yml|yaml|sh)$/.test(f);
    const ranked = [...changedFiles].sort((a, b) => Number(isCode(b)) - Number(isCode(a)));
    const targets = ranked.slice(0, MAX_REVIEW_FANOUT);
    console.log(`[reviewer] Fan-out: creating ${targets.length} review task(s) (${changedFiles.length} files changed)`);
    let createdCount = 0;
    for (const target of targets) {
      const ok = createTask(agents.reviewer, {
        title: `Review recent changes to ${target}`,
        target,
        focus: "correctness and security",
      });
      if (ok) createdCount++;
    }
    if (createdCount > 0) {
      tasksCreated.push(...Array(createdCount).fill("reviewer"));
      state.lastReviewerTask = iso;
      state.lastReviewedHead = headSha;
    }
  } else {
    console.log(`[reviewer] Skipping — ${pending.length} pending task(s)`);
  }
} else if (hoursSinceReview > REVIEW_COOLDOWN_H && changedFiles.length > 0) {
  console.log(`[reviewer] Skipping — HEAD ${headSha.slice(0, 7)} already reviewed`);
}

// ── Code-quality passes: docs / refactor / tests ──
// One task per kind in CODE_PASS_KINDS, routed to the reviewer DID so each
// pass can land as its own PR. Own timer + HEAD-advanced gate so quiet
// periods don't re-emit the same passes every cycle.
const hoursSinceCodePass = state.lastCodePass
  ? (now - new Date(state.lastCodePass)) / (1000 * 60 * 60)
  : 999;
const codePassHeadAdvanced = headSha !== "" && headSha !== state.lastCodePassHead;
const hasCodeChanges = changedFiles.some((f) => /\.(mjs|js|ts|tsx|py|go|rs|sh)$/.test(f));

if (hoursSinceCodePass > CODE_PASS_COOLDOWN_H && hasCodeChanges && codePassHeadAdvanced) {
  // Fetch >10 so the cap below is a real measurement, not capped by --limit.
  const pending = getPendingTasks(agents.reviewer.did, 11);
  if (pending.length < 10) {
    console.log(`[reviewer] Code-quality passes: ${CODE_PASS_KINDS.join(", ")}`);
    let createdCount = 0;
    for (const kind of CODE_PASS_KINDS) {
      const focusByKind = {
        "docs-pass": "missing docstrings, stale comments, README drift — open a PR with improvements",
        "refactor-pass": "duplication, dead code, simplification opportunities — open a small targeted PR",
        "test-pass": "uncovered branches, missing edge-case tests — open a PR with new tests",
      };
      const ok = createTask(
        agents.reviewer,
        {
          title: `${kind} on recent code changes`,
          target: changedFiles.slice(0, 3).join(", "),
          focus: focusByKind[kind],
        },
        { kind, capability: "pr:open" },
      );
      if (ok) createdCount++;
    }
    if (createdCount > 0) {
      tasksCreated.push(...Array(createdCount).fill("code-pass"));
      state.lastCodePass = iso;
      state.lastCodePassHead = headSha;
    }
  } else {
    console.log(`[reviewer] Skipping code-passes — ${pending.length} pending task(s)`);
  }
}

// ── Reviewer fallback: review an open PR when main is quiet ──
// The main reviewer block only fires when HEAD advances. During quiet stretches
// on main, the reviewer would sit idle even with cooldowns near zero — so if
// open PRs exist on gitlawb, hand the reviewer one of them to look at. Own
// timer (OPEN_PR_REVIEW_COOLDOWN_H) so this doesn't fire every 5-min cycle.
const reviewerFiredThisRun = tasksCreated.includes("reviewer");
const hoursSinceOpenPRReview = state.lastOpenPRReview
  ? (now - new Date(state.lastOpenPRReview)) / (1000 * 60 * 60)
  : 999;

if (!reviewerFiredThisRun && prCount > 0 && hoursSinceOpenPRReview > OPEN_PR_REVIEW_COOLDOWN_H) {
  const pending = getPendingTasks(agents.reviewer.did);
  if (pending.length === 0) {
    console.log(`[reviewer] Creating fallback task: review one of ${prCount} open PR(s)`);
    const created = createTask(agents.reviewer, {
      title: `Review an open PR (${prCount} open on aeon)`,
      target: "open-prs",
      focus: "correctness, security, and whether the PR is ready to merge",
      open_pr_count: prCount,
    });
    if (created) {
      tasksCreated.push("reviewer-open-pr");
      state.lastOpenPRReview = iso;
    }
  } else {
    console.log(`[reviewer] Skipping open-PR fallback — ${pending.length} pending task(s)`);
  }
}

// ── Deployer: Record deployment proof or handle PRs ──
const hoursSinceLastProof = state.lastDeployProof
  ? (now - new Date(state.lastDeployProof)) / (1000 * 60 * 60)
  : 999;

if (hoursSinceLastProof > DEPLOY_PROOF_COOLDOWN_H || prCount > 0) {
  const pending = getPendingTasks(agents.deployer.did);
  if (pending.length === 0) {
    const action = prCount > 0 ? "scan and report on open PRs" : "record deployment proof";
    console.log(`[deployer] Creating task: ${action}`);
    const created = createTask(agents.deployer, {
      title: `Deploy: ${action}`,
      component: "fleet-deploy",
      action,
      branch: "main",
    });
    if (created) {
      tasksCreated.push("deployer");
      if (hoursSinceLastProof > DEPLOY_PROOF_COOLDOWN_H) state.lastDeployProof = iso;
    }
  } else {
    console.log(`[deployer] Skipping — ${pending.length} pending task(s)`);
  }
}

// ── Compute-futures market sim (daily) ──
// The deployer runs the compute-futures simulation and records the curve
// proof. Assigned to the deployer because it holds git:push and the executor
// pushes a signed proof to the GitLawb-hosted repo.
const hoursSinceComputeFutures = state.lastComputeFutures
  ? (now - new Date(state.lastComputeFutures)) / (1000 * 60 * 60)
  : 999;

if (hoursSinceComputeFutures > 24) {
  // Gate only on whether a compute-futures task is already pending — not on
  // any deployer task — so the deployer's PR-scan work doesn't starve it.
  const pending = getPendingTasks(agents.deployer.did);
  const hasComputeFutures = pending.some((t) => (t.kind || t.type) === "compute-futures-sim");
  if (!hasComputeFutures) {
    console.log("[deployer] Creating task: compute-futures market sim");
    const created = createTask(
      agents.deployer,
      {
        title: "Run compute-futures market simulation and record curve proof",
        component: "compute-futures",
        action: "run compute-futures sim and record curve proof",
        commit_proof: true,
        x402: false,
      },
      { kind: "compute-futures-sim", capability: "git:push" },
    );
    if (created) {
      tasksCreated.push("compute-futures");
      state.lastComputeFutures = iso;
    }
  } else {
    console.log(`[deployer] Skipping compute-futures — already pending`);
  }
}

// ── Compute-futures market sim, x402 physical settlement (daily) ──
// Same sim, settled over the x402 rail — its own task/state so it runs daily
// alongside the cash variant without the dedup blocking either.
const hoursSinceComputeFuturesX402 = state.lastComputeFuturesX402
  ? (now - new Date(state.lastComputeFuturesX402)) / (1000 * 60 * 60)
  : 999;

if (hoursSinceComputeFuturesX402 > 24) {
  const pending = getPendingTasks(agents.deployer.did);
  const hasX402 = pending.some((t) => (t.kind || t.type) === "compute-futures-sim-x402");
  if (!hasX402) {
    console.log("[deployer] Creating task: compute-futures market sim (x402)");
    const created = createTask(
      agents.deployer,
      {
        title: "Run compute-futures market simulation (x402 settlement) and record curve proof",
        component: "compute-futures",
        action: "run compute-futures sim (x402) and record curve proof",
        commit_proof: true,
        x402: true,
      },
      { kind: "compute-futures-sim-x402", capability: "git:push" },
    );
    if (created) {
      tasksCreated.push("compute-futures-x402");
      state.lastComputeFuturesX402 = iso;
    }
  } else {
    console.log(`[deployer] Skipping compute-futures x402 — already pending`);
  }
}

// ── Compute-futures scenario sweep (daily analytics) ──
// The single cash/x402 runs prove the rail still executes. The sweep produces
// the useful signal: multiple modes and date-derived seeds so each day captures
// a small distribution rather than replaying the same deterministic path.
const hoursSinceComputeFuturesSweep = state.lastComputeFuturesSweep
  ? (now - new Date(state.lastComputeFuturesSweep)) / (1000 * 60 * 60)
  : 999;

if (hoursSinceComputeFuturesSweep > 24) {
  const pending = getPendingTasks(agents.deployer.did);
  const hasSweep = pending.some((t) => (t.kind || t.type) === "compute-futures-sweep");
  if (!hasSweep) {
    const seeds = dailySweepSeeds(now);
    console.log(`[deployer] Creating task: compute-futures scenario sweep (${seeds.join(",")})`);
    const created = createTask(
      agents.deployer,
      {
        title: "Run compute-futures scenario sweep and record analytics proof",
        component: "compute-futures",
        action: "run compute-futures scenario sweep and record analytics proof",
        commit_proof: true,
        modes: ["synthetic", "basket", "spread", "x402"],
        seeds,
        rounds: 60,
        live: true, // pull real OpenRouter prices for the darkbloom-backed modes
        pair: true, // paired synthetic-vs-basket diff to isolate the basket effect
      },
      { kind: "compute-futures-sweep", capability: "git:push" },
    );
    if (created) {
      tasksCreated.push("compute-futures-sweep");
      state.lastComputeFuturesSweep = iso;
    }
  } else {
    console.log("[deployer] Skipping compute-futures sweep — already pending");
  }
}

// ── Compute-futures market sim, Surplus Intelligence live feed (daily) ──
// Same sim anchored to the Surplus inference market with --surplus --live, so
// the fleet records a proof against a real venue's prices. Its own task/state
// so it runs daily alongside the cash + x402 variants without dedup blocking
// any of them. Live prices come from the prefetch cache (.surplus-cache/) when
// SURPLUS_PRICING_URL is set; otherwise the sim falls back to its catalog.
const hoursSinceComputeFuturesSurplus = state.lastComputeFuturesSurplus
  ? (now - new Date(state.lastComputeFuturesSurplus)) / (1000 * 60 * 60)
  : 999;

if (hoursSinceComputeFuturesSurplus > 24) {
  const pending = getPendingTasks(agents.deployer.did);
  const hasSurplus = pending.some((t) => (t.kind || t.type) === "compute-futures-sim-surplus");
  if (!hasSurplus) {
    console.log("[deployer] Creating task: compute-futures market sim (surplus, live)");
    const created = createTask(
      agents.deployer,
      {
        title: "Run compute-futures market simulation (Surplus live feed) and record curve proof",
        component: "compute-futures",
        action: "run compute-futures sim (surplus, live) and record curve proof",
        commit_proof: true,
        x402: false,
        surplus: true,
        live: true,
      },
      { kind: "compute-futures-sim-surplus", capability: "git:push" },
    );
    if (created) {
      tasksCreated.push("compute-futures-surplus");
      state.lastComputeFuturesSurplus = iso;
    }
  } else {
    console.log(`[deployer] Skipping compute-futures surplus — already pending`);
  }
}

// ── Forker: mirror + fork ecosystem repos (daily) ──
// Each target in memory/fork-targets.json with active=true becomes one task
// for the deployer (its `git:push` → `run_command` lets it invoke `gl mirror`
// for GitHub sources and `gl repo fork` for gitlawb-resident upstreams).
// Daily cadence — forking is a once-then-stable operation, not a per-cycle one.
const hoursSinceFork = state.lastFork
  ? (now - new Date(state.lastFork)) / (1000 * 60 * 60)
  : 999;

if (hoursSinceFork > FORK_COOLDOWN_H && existsSync(FORK_TARGETS_FILE)) {
  let forkTargets = [];
  try {
    const parsed = JSON.parse(readFileSync(FORK_TARGETS_FILE, "utf8"));
    forkTargets = (parsed.targets || []).filter((t) => t && t.active !== false);
  } catch (e) {
    console.log(`[forker] Skipping — could not parse ${FORK_TARGETS_FILE}: ${e.message}`);
  }
  if (forkTargets.length > 0) {
    const pending = getPendingTasks(agents.deployer.did);
    const hasFork = pending.some((t) => (t.kind || t.type) === "fork");
    if (!hasFork) {
      console.log(`[forker] Creating fork task for ${forkTargets.length} target(s)`);
      const created = createTask(
        agents.deployer,
        {
          title: `Mirror + fork ${forkTargets.length} ecosystem repo(s)`,
          component: "forker",
          action: "for each target: gl mirror (if github URL) then gl repo fork, skip if already forked",
          targets: forkTargets,
        },
        { kind: "fork", capability: "git:push" },
      );
      if (created) {
        tasksCreated.push("forker");
        state.lastFork = iso;
      }
    } else {
      console.log("[forker] Skipping — fork task already pending");
    }
  } else if (hoursSinceFork > FORK_COOLDOWN_H) {
    console.log(`[forker] Skipping — no active targets in ${FORK_TARGETS_FILE}`);
  }
}

// ── Sentinel: Security audit ──
const hoursSinceLastAudit = state.lastAudit
  ? (now - new Date(state.lastAudit)) / (1000 * 60 * 60)
  : 999;

if (hoursSinceLastAudit > AUDIT_COOLDOWN_H) {
  const pending = getPendingTasks(agents.sentinel.did);
  if (pending.length === 0) {
    // Rotate focus areas
    const focusAreas = [
      "destructive commands, key handling, capability boundaries",
      "workflow security, secret handling, env var exposure",
      "fleet health, cap expiry, trust score anomalies",
      "recent deletions, self-modification patterns, repo integrity",
    ];
    const focusIndex = Math.floor(Date.now() / (12 * 60 * 60 * 1000)) % focusAreas.length;
    const focus = focusAreas[focusIndex];

    console.log(`[sentinel] Creating task: security audit — ${focus}`);
    const created = createTask(agents.sentinel, {
      title: `Security audit: ${focus.split(",")[0]}`,
      target: "repo",
      focus,
    });
    if (created) {
      tasksCreated.push("sentinel");
      state.lastAudit = iso;
    }
  } else {
    console.log(`[sentinel] Skipping — ${pending.length} pending task(s)`);
  }
}

// Save state
state.lastRun = iso;
state.tasksCreated = state.tasksCreated || {};
state.tasksCreated[iso] = tasksCreated;
mkdirSync(join(repoDir, "memory"), { recursive: true });
writeFileSync(stateFile, JSON.stringify(state, null, 2));

console.log(`\nTask generator: ${tasksCreated.length} task(s) created [${tasksCreated.join(", ")}]`);
if (tasksCreated.length === 0) {
  console.log("Reasons: no recent activity, pending tasks exist, or too soon since last run");
}
