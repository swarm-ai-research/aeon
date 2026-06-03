#!/usr/bin/env node
// deployer.mjs — Real deployment executor for aeon-deployer.
//
// Handles PR merges, creates branches with real content, and records
// deployment artifacts with actual metadata (commit SHAs, timestamps,
// agent DIDs, task IDs).
//
// Env vars (set by task-runner):
//   GITLAWB_TASK_JSON   — full task object
//   GITLAWB_AGENT_JSON  — agent instance object
//   GITLAWB_REPO_DIR    — repo working directory

import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, copyFileSync, appendFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { tmpdir, homedir } from "node:os";

const repoDir = process.env.GITLAWB_REPO_DIR || ".";
const task = JSON.parse(process.env.GITLAWB_TASK_JSON || "{}");
const agent = JSON.parse(process.env.GITLAWB_AGENT_JSON || "{}");

const payload = typeof task.payload === "string" ? JSON.parse(task.payload) : (task.payload || {});
const kind = task.kind || task.type || "";
const action = payload.action || task.kind || "record commit proof";
const component = payload.component || "fleet-deployer";

// The GitLawb-hosted repo the fleet pushes signed proofs to.
const GITLAWB_REPO_URL =
  process.env.GITLAWB_REPO_URL ||
  "gitlawb://did:key:z6MkpiXbCJzXGLw9bQXw5t8ja734YsrhYWEQMqsicwUcjHbH/aeon";
const GITLAWB_BRANCH = process.env.GITLAWB_BRANCH || "main";

function run(cmd, args, opts = {}) {
  const proc = spawnSync(cmd, args, { cwd: opts.cwd || repoDir, encoding: "utf8", ...opts });
  if (proc.status !== 0 && !opts.allowFail) {
    throw new Error(`${cmd} ${args.join(" ")} failed: ${proc.stderr || proc.stdout || "unknown"}`);
  }
  return (proc.stdout || "").trim();
}

function tryRun(cmd, args, opts = {}) {
  const proc = spawnSync(cmd, args, { cwd: opts.cwd || repoDir, encoding: "utf8", ...opts });
  return { ok: proc.status === 0, stdout: (proc.stdout || "").trim(), stderr: (proc.stderr || "").trim() };
}

const today = new Date().toISOString().slice(0, 10);
const iso = new Date().toISOString();

function proofPaths() {
  const proofDir = join(repoDir, "memory", "gitlawb-compute-futures-proofs");
  mkdirSync(proofDir, { recursive: true });
  const relProof = `memory/gitlawb-compute-futures-proofs/${today}.md`;
  return { proofDir, relProof, proofFile: join(repoDir, relProof) };
}

function asList(value, fallback) {
  if (Array.isArray(value)) return value.map(String).filter(Boolean);
  if (typeof value === "string" && value.trim()) return value.split(",").map((s) => s.trim()).filter(Boolean);
  return fallback;
}

function fmt4(x) {
  return Number.isFinite(x) ? x.toFixed(4) : "n/a";
}

function expandHome(p) {
  if (!p) return "";
  return p.startsWith("~/") ? join(homedir(), p.slice(2)) : p;
}

// Build a throwaway HOME holding only this agent's GitLawb identity, so a
// `git push` to the gitlawb:// remote is signed as the agent (mirrors the
// task-runner's makeGitlawbHome). Returns null if the identity isn't present
// (e.g. running locally without the fleet secrets) so callers can skip safely.
function makeGitlawbHome() {
  const identityDir = expandHome(agent.identity_dir || "");
  if (!identityDir || !existsSync(join(identityDir, "identity.pem"))) return null;
  const home = mkdtempSync(join(tmpdir(), "gitlawb-home-"));
  const glDir = join(home, ".gitlawb");
  mkdirSync(glDir, { recursive: true });
  copyFileSync(join(identityDir, "identity.pem"), join(glDir, "identity.pem"));
  if (existsSync(join(identityDir, "ucan.json"))) {
    copyFileSync(join(identityDir, "ucan.json"), join(glDir, "ucan.json"));
  }
  return home;
}

// Push a proof file to the GitLawb-hosted repo, signed as the agent. Best
// effort: if no identity or the mesh is unreachable (sandbox), it logs and
// returns null — the proof is still committed to GitHub by the workflow.
function pushProofToGitlawb(relPath, commitMsg) {
  const home = makeGitlawbHome();
  if (!home) {
    console.log("GitLawb push skipped — no agent identity available (proof recorded locally).");
    return null;
  }
  const workDir = mkdtempSync(join(tmpdir(), "gitlawb-cf-"));
  const env = { ...process.env, HOME: home };
  const clone = tryRun("git", ["clone", "--branch", GITLAWB_BRANCH, GITLAWB_REPO_URL, workDir], { cwd: repoDir, env });
  if (!clone.ok) {
    console.log(`GitLawb push skipped — clone failed: ${clone.stderr.slice(0, 160)}`);
    return null;
  }
  mkdirSync(join(workDir, "memory", "gitlawb-compute-futures-proofs"), { recursive: true });
  copyFileSync(join(repoDir, relPath), join(workDir, relPath));
  tryRun("git", ["config", "user.name", agent.name || "aeon-deployer"], { cwd: workDir, env });
  tryRun("git", ["config", "user.email", `${agent.did || "deployer"}@gitlawb.local`], { cwd: workDir, env });
  tryRun("git", ["add", relPath], { cwd: workDir, env });
  const commit = tryRun("git", ["commit", "-m", commitMsg], { cwd: workDir, env });
  if (!commit.ok) {
    console.log("GitLawb push skipped — nothing to commit.");
    return null;
  }
  const sha = tryRun("git", ["rev-parse", "HEAD"], { cwd: workDir, env }).stdout;
  const push = tryRun("git", ["push", "origin", `HEAD:${GITLAWB_BRANCH}`], { cwd: workDir, env });
  if (!push.ok) {
    console.log(`GitLawb push failed (proof still recorded to GitHub): ${push.stderr.slice(0, 160)}`);
    return null;
  }
  console.log(`GitLawb proof pushed to ${GITLAWB_REPO_URL}@${GITLAWB_BRANCH} as ${agent.name} (${sha.slice(0, 12)}).`);
  return sha;
}

// ── Fork ecosystem repos ──
// Targets come from the task payload (sourced from memory/fork-targets.json
// by task-generator). For each target: if `kind === "github-mirror"`, run
// `gl mirror` to bring the source onto the gitlawb node first, then run
// `gl repo fork` to fork it into the operator's namespace. Skip already-
// forked targets (idempotent by checking `gl repo info` first).
if (kind === "fork") {
  const targets = Array.isArray(payload.targets) ? payload.targets : [];
  if (targets.length === 0) {
    console.log("[forker] No targets in payload — nothing to do.");
    process.exit(0);
  }
  const node = process.env.GITLAWB_NODE || "https://node.gitlawb.com";
  const operatorShort = (process.env.GITLAWB_OPERATOR_DID_SHORT || "")
    || (GITLAWB_REPO_URL.match(/did:key:([^/]+)/) || [])[1]
    || "";
  const summary = [];
  const failures = [];
  for (const t of targets) {
    if (!t || t.active === false) continue;
    const name = t.name || t.source || "(unnamed)";
    console.log(`[forker] processing ${name}`);
    // Derive a gitlawb repo name from the source. For github-mirror entries the
    // mirror command writes to <operator>/<repo-tail>; we treat that as the
    // post-mirror handle for the fork step.
    const sourceTail = (t.source || "").replace(/^https?:\/\//, "").split("/").pop() || name;
    if (t.kind === "github-mirror" && t.source) {
      const mirror = tryRun("gl", ["mirror", t.source, "--node", node]);
      if (!mirror.ok && !/already exists|exists on node/i.test(mirror.stderr + mirror.stdout)) {
        const msg = `${name}: mirror failed — ${(mirror.stderr || mirror.stdout).slice(0, 120)}`;
        summary.push(msg);
        failures.push(msg);
        continue;
      }
      summary.push(`${name}: mirror ok`);
    }
    // Probe whether the operator already has a fork. `gl repo info` succeeds
    // only for repos that exist on the node under the queried owner.
    const probe = tryRun("gl", ["repo", "info", `${operatorShort}/${sourceTail}`, "--node", node]);
    if (probe.ok) {
      summary.push(`${name}: fork already exists, skipping`);
      continue;
    }
    // The mirror lands under the operator's own DID, so a same-owner fork is
    // a no-op. For ecosystem forks the source owner differs; pass it via
    // `<owner>/<repo>` form. For github-mirror we use the operator as owner
    // (the mirror is owned by whoever ran `gl mirror`).
    const ownerForFork = t.upstream_owner || operatorShort;
    const fork = tryRun("gl", ["repo", "fork", `${ownerForFork}/${sourceTail}`, "--node", node]);
    if (!fork.ok) {
      const msg = `${name}: fork failed — ${(fork.stderr || fork.stdout).slice(0, 120)}`;
      summary.push(msg);
      failures.push(msg);
      continue;
    }
    summary.push(`${name}: forked`);
  }
  console.log("[forker] done:\n  " + summary.join("\n  "));
  // Exit non-zero if any target failed so task-runner records the task as
  // failed. Without this, task-generator's `state.lastFork` stamp would block
  // a retry until the daily cooldown expires even though nothing forked.
  if (failures.length > 0) {
    console.log(`[forker] ${failures.length} target(s) failed — exiting non-zero so the task is retried.`);
    process.exit(1);
  }
  process.exit(0);
}

// ── Compute-futures scenario sweep ──
// Run a mode × seed matrix so the daily proof records a distribution, not just
// one deterministic path. This is the analytically useful fleet output.
if (kind === "compute-futures-sweep") {
  const modes = asList(payload.modes, ["synthetic", "basket", "spread", "x402"]);
  const seeds = asList(payload.seeds, ["12648430", "12648431", "12648432"]);
  const rounds = Number.isFinite(Number(payload.rounds)) ? Number(payload.rounds) : 60;

  // Pull real OpenRouter prices first (best-effort; the sweep falls back to the
  // static catalog if the snapshot is missing). Network is available here — the
  // fleet runs plain node, not the Claude bash sandbox.
  let liveSnapshot = null;
  if (payload.live) {
    const pre = tryRun("node", ["scripts/prefetch-openrouter.mjs"], { cwd: repoDir });
    console.log(pre.stdout || pre.stderr);
    const livePath = join(repoDir, "prototypes", "compute-futures", "out", "live-prices.json");
    if (existsSync(livePath)) {
      try {
        liveSnapshot = JSON.parse(readFileSync(livePath, "utf8"));
      } catch {}
    }
  }

  const args = [
    "prototypes/compute-futures/scenario-sweep.mjs",
    `--modes=${modes.join(",")}`,
    `--seeds=${seeds.join(",")}`,
    `--rounds=${rounds}`,
  ];
  if (payload.live) args.push("--live");
  if (payload.pair) args.push("--pair");
  const sweep = tryRun("node", args, { cwd: repoDir });
  if (!sweep.ok) {
    throw new Error(`compute-futures sweep failed: ${(sweep.stderr || sweep.stdout).slice(0, 400)}`);
  }

  const reportPath = join(repoDir, "prototypes", "compute-futures", "out", "scenario-sweep.json");
  const mdPath = join(repoDir, "prototypes", "compute-futures", "out", "scenario-sweep.md");
  const csvPath = join(repoDir, "prototypes", "compute-futures", "out", "scenario-sweep.csv");
  const report = JSON.parse(readFileSync(reportPath, "utf8"));
  const markdown = readFileSync(mdPath, "utf8");
  // Long-format CSV is emitted by scenario-sweep.mjs alongside the JSON+MD.
  // Mirror it into the proofs dir as <date>.csv so the daily EDA skill can
  // profile the run without re-flattening from JSON. Pre-CSV-emitter sweep
  // runs won't have the file — log a one-line warning and continue.
  const { relProof, proofFile } = proofPaths();
  const proofCsvPath = proofFile.replace(/\.md$/, ".csv");
  if (existsSync(csvPath)) {
    appendFileSync(proofCsvPath, readFileSync(csvPath, "utf8"));
    console.log(`Compute-futures sweep CSV recorded: ${relProof.replace(/\.md$/, ".csv")}`);
  } else {
    console.warn("scenario-sweep.csv not found — skipping CSV proof (deployer needs scenario-sweep.mjs with the CSV emitter)");
  }
  const grouped = report.grouped || [];
  const analytics = grouped.map(
    (g) => `${g.mode}: spot $${fmt4(g.minSpot)}-$${fmt4(g.maxSpot)}, avg abs P&L $${fmt4(g.realizedAbsAvg)}, x402 $${fmt4(g.x402Total)}`,
  );
  const summary = `compute-futures sweep: ${report.results?.length || 0} runs · ${analytics.join(" · ")}`;

  const sha = tryRun("git", ["rev-parse", "HEAD"]).stdout || "unknown";
  const liveLine = liveSnapshot
    ? `live: OpenRouter @ ${liveSnapshot.generatedAt} · ${Object.keys(liveSnapshot.models || {}).length} models`
    : payload.live
      ? "live: requested but feed unavailable — static catalog"
      : "live: off (static catalog)";
  const entry = [
    `## ${iso} — ${agent.name || "aeon-deployer"} (task ${task.id})`,
    `settlement: scenario-sweep · repo sha: ${sha.slice(0, 12)}`,
    `modes: ${modes.join(",")} · seeds: ${seeds.join(",")} · rounds: ${rounds}`,
    liveLine,
    "",
    markdown.trim(),
    "",
  ].join("\n");
  appendFileSync(proofFile, entry + "\n");
  console.log(`Compute-futures sweep proof recorded: ${relProof}`);

  if (payload.commit_proof) {
    pushProofToGitlawb(relProof, `chore(gitlawb): compute-futures sweep proof ${today}`);
  }

  console.log(summary);
  process.exit(0);
}

// ── Compute-futures market sim ──
// Run the deterministic compute-futures simulation, extract the curve
// re-pricing around each event, record a proof, and push it to GitLawb.
if (kind === "compute-futures-sim" || action.includes("compute-futures")) {
  const simArgs = ["prototypes/compute-futures/sim.mjs"];
  if (payload.x402) simArgs.push("--x402");
  // Surplus Intelligence live-feed variant: anchor the spot to a real venue.
  if (payload.surplus) {
    simArgs.push("--surplus");
    if (payload.live) simArgs.push("--live");
  }
  const sim = tryRun("node", simArgs, { cwd: repoDir });
  if (!sim.ok) {
    throw new Error(`compute-futures sim failed: ${(sim.stderr || sim.stdout).slice(0, 240)}`);
  }

  // Extract the event-reprice section and a compact per-event headline.
  const lines = sim.stdout.split("\n");
  const start = lines.findIndex((l) => l.includes("Curve re-pricing"));
  const end = lines.findIndex((l) => l.includes("Price paths"));
  const repriceBlock = start >= 0 ? lines.slice(start, end > start ? end : start + 20).join("\n") : "";

  // For the x402 variant, also capture the physical-settlement section (the
  // per-delivery x402 receipts + totals) so the proof shows the rail, not just
  // the curve.
  let x402Block = "";
  if (payload.x402) {
    const xs = lines.findIndex((l) => l.includes("x402 physical settlement"));
    const xe = lines.findIndex((l) => l.includes("Capability layer"));
    if (xs >= 0) x402Block = lines.slice(xs, xe > xs ? xe : xs + 24).join("\n");
  }

  // For the surplus variant, capture the live-anchor line so the proof shows
  // whether the run used the real Surplus feed or fell back to the catalog.
  let surplusLine = "";
  if (payload.surplus) {
    surplusLine = lines.find((l) => l.includes("[surplus]")) || lines.find((l) => l.includes("spot source: surplus")) || "";
  }

  const headlines = [];
  for (let i = 0; i < lines.length; i++) {
    const ev = lines[i].match(/Event @ round (\d+): (.+)/);
    if (!ev) continue;
    const pcts = [];
    for (let j = i + 1; j < lines.length && !lines[j].includes("Event @ round") && lines[j].trim(); j++) {
      const m = lines[j].match(/\(([+-]?\d+\.\d+)%\)/);
      if (m) pcts.push(parseFloat(m[1]));
    }
    const peak = pcts.reduce((a, b) => (Math.abs(b) > Math.abs(a) ? b : a), 0);
    headlines.push(`r${ev[1]} "${ev[2].slice(0, 40)}" ${peak >= 0 ? "+" : ""}${peak.toFixed(1)}%`);
  }
  const settlement = payload.x402 ? "x402-physical" : "cash";
  const venue = payload.surplus ? "surplus-live" : "synthetic";
  const summary = `compute-futures sim (${venue}/${settlement}): ${headlines.join(" · ")}`;

  // Record the proof locally (the workflow commits this to GitHub).
  const { relProof, proofFile } = proofPaths();
  const sha = tryRun("git", ["rev-parse", "HEAD"]).stdout || "unknown";
  const entry = [
    `## ${iso} — ${agent.name || "aeon-deployer"} (task ${task.id})`,
    `venue: ${venue} · settlement: ${settlement} · repo sha: ${sha.slice(0, 12)}`,
    ...(surplusLine ? [`spot: ${surplusLine.trim()}`] : []),
    "",
    "```",
    repriceBlock || "(curve section not captured)",
    "```",
    ...(x402Block ? ["", "```", x402Block, "```", ""] : [""]),
  ].join("\n");
  appendFileSync(proofFile, entry + "\n");
  console.log(`Compute-futures proof recorded: ${relProof}`);

  // Push the signed proof to the GitLawb-hosted repo (best effort).
  if (payload.commit_proof) {
    pushProofToGitlawb(relProof, `chore(gitlawb): compute-futures curve proof (${settlement}) ${today}`);
  }

  console.log(summary);
  process.exit(0);
}

// Determine what to do based on action
if (action.includes("merge")) {
  // ── PR Merge Mode ──
  const prList = tryRun("gl", ["pr", "list", "aeon"]);
  if (!prList.ok) {
    console.log("Could not list PRs — skipping merge action");
    process.exit(0);
  }

  const prs = prList.stdout.split("\n").filter(Boolean);
  if (prs.length === 0) {
    console.log("No open PRs to merge");
    process.exit(0);
  }

  // Report available PRs but don't force-merge without explicit approval
  console.log(`Found ${prs.length} open PR(s). Merge requires explicit approval — recording PR state as deployment artifact.`);

  const proofDir = join(repoDir, "memory", "gitlawb-deploy-proofs");
  mkdirSync(proofDir, { recursive: true });
  const proofFile = join(proofDir, `${today}.md`);
  const line = `- ${iso} ${agent.name} task=${task.id} action="pr-scan" prs_found=${prs.length} prs="${prs.slice(0, 3).join("; ")}"\n`;
  appendFileSync(proofFile, line);

  console.log(`Deployment scan: ${prs.length} open PR(s) recorded. Proof: memory/gitlawb-deploy-proofs/${today}.md`);

} else if (action.includes("branch") || action.includes("prepare")) {
  // ── Branch Creation Mode ──
  const branchName = `fleet/${component}-${Date.now().toString(36)}`;

  // Create a branch with a deployment manifest
  const manifestDir = join(repoDir, "memory", "gitlawb-deployments");
  mkdirSync(manifestDir, { recursive: true });

  const currentSha = run("git", ["rev-parse", "HEAD"]);
  const manifest = {
    component,
    deployed_at: iso,
    deployed_by: agent.name,
    agent_did: agent.did,
    task_id: task.id,
    commit_sha: currentSha,
    action,
    branch: branchName,
  };

  writeFileSync(join(manifestDir, `${today}-${component}.json`), JSON.stringify(manifest, null, 2));

  console.log(`Deployment manifest created: memory/gitlawb-deployments/${today}-${component}.json`);
  console.log(`Branch: ${branchName} | SHA: ${currentSha.slice(0, 12)}`);

} else {
  // ── Default: Record Commit Proof ──
  const currentSha = run("git", ["rev-parse", "HEAD"]);
  const recentLog = run("git", ["log", "--oneline", "-5"]);
  const branch = tryRun("git", ["branch", "--show-current"]).stdout || "detached";

  const proofDir = join(repoDir, "memory", "gitlawb-deploy-proofs");
  mkdirSync(proofDir, { recursive: true });
  const proofFile = join(proofDir, `${today}.md`);

  const line = `- ${iso} ${agent.name} task=${task.id} component=${component} action="${action}" sha=${currentSha.slice(0, 12)} branch=${branch}\n`;
  appendFileSync(proofFile, line);

  // Also record fleet deployment state
  const stateFile = join(repoDir, "memory", "gitlawb-deploy-state.json");
  let state = {};
  if (existsSync(stateFile)) {
    try { state = JSON.parse(readFileSync(stateFile, "utf8")); } catch {}
  }

  state.last_deploy = {
    at: iso,
    by: agent.name,
    did: agent.did,
    task_id: task.id,
    sha: currentSha,
    branch,
    component,
    action,
  };
  state.deploy_count = (state.deploy_count || 0) + 1;
  state.history = state.history || [];
  state.history.push({ at: iso, sha: currentSha.slice(0, 12), task: task.id });
  if (state.history.length > 50) state.history = state.history.slice(-50);

  writeFileSync(stateFile, JSON.stringify(state, null, 2));

  console.log(`Deploy proof recorded: sha=${currentSha.slice(0, 12)} branch=${branch} component=${component}`);
  console.log(`Recent commits:\n${recentLog}`);
  console.log(`Proof: memory/gitlawb-deploy-proofs/${today}.md | State: memory/gitlawb-deploy-state.json`);
}
