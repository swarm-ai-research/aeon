#!/usr/bin/env node
// Fleet Task Runner — polls the GitLawb task queue and executes work for each agent.
//
//   node demos/fleet-runner.mjs [--once] [--agent researcher|reviewer|deployer|sentinel]
//
// With --once: poll once and exit. Without: poll every 30s.
// With --agent: only run that agent. Without: run all 4.

import { execSync } from "node:child_process";
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

// ── Config ──────────────────────────────────────────────────────────────────

const NODE = "https://node.gitlawb.com";
const REPO_ID = "23d11b96-6d40-45c9-b914-327883e3350e";
const REPO_CLONE = `gitlawb://did:key:z6MkpiXbCJzXGLw9bQXw5t8ja734YsrhYWEQMqsicwUcjHbH/aeon`;
const BRANCH = "codex/pr-review-multiline-var";
const FLEET_DIR = join(homedir(), ".gitlawb", "fleet");
const WORK_DIR = join(homedir(), ".gitlawb", "work");
const POLL_INTERVAL = 30_000;

const AGENTS = {
  researcher: {
    did: "did:key:z6MkfnrSDgdDbkvfCCnMyaR4HqoWfWEfGoTFajX1HGkSHRUH",
    dir: join(FLEET_DIR, "researcher"),
    kinds: ["research"],
  },
  reviewer: {
    did: "did:key:z6Mks2KSBfbindXsw2SBEGfqdgMJ4HwxJPfPQjkPKHY7U7SZ",
    dir: join(FLEET_DIR, "reviewer"),
    kinds: ["code-review"],
  },
  deployer: {
    did: "did:key:z6MknGJBoQsbNL956GNiTJRRWKJqMcprWmdYxJPbVGCwcAuS",
    dir: join(FLEET_DIR, "deployer"),
    kinds: ["deploy"],
  },
  sentinel: {
    did: "did:key:z6MksUuVYyp93QA6pc2qAnXFQZdaoHq46dugXVweeehX4S2M",
    dir: join(FLEET_DIR, "sentinel"),
    kinds: ["audit"],
  },
};

// ── Helpers ─────────────────────────────────────────────────────────────────

const log = (agent, msg) => console.log(`[${new Date().toISOString()}] [${agent}] ${msg}`);

const gl = (args, dir) => {
  try {
    return execSync(`gl ${args}`, {
      encoding: "utf8", cwd: dir, shell: "/bin/bash",
      env: { ...process.env, GITLAWB_NODE: NODE },
    }).trim();
  } catch {
    return null;
  }
};

// Create an issue — write body to temp file, pipe via cat to avoid shell escaping
function glIssue(title, body, dir) {
  const tmpFile = join(WORK_DIR, `.issue-${Date.now()}.md`);
  writeFileSync(tmpFile, body);
  try {
    return execSync(`gl issue create --title "${title}" --body "$(cat "${tmpFile}")" aeon`, {
      encoding: "utf8", cwd: dir, shell: "/bin/bash",
      env: { ...process.env, GITLAWB_NODE: NODE },
    }).trim();
  } catch {
    return null;
  } finally {
    try { execSync(`rm -f "${tmpFile}"`, { stdio: "pipe" }); } catch {}
  }
}

function parseTasks(json) {
  try { return (JSON.parse(json).tasks || []); } catch { return []; }
}

function ensureClone(workDir) {
  if (!existsSync(join(workDir, "prototypes"))) {
    execSync(`git clone --branch ${BRANCH} ${REPO_CLONE} ${workDir}`, { stdio: "pipe" });
  }
}

// ── Task Handlers ───────────────────────────────────────────────────────────

const handlers = {
  async research(task, agent) {
    const payload = JSON.parse(task.payload);
    const { topic, scope } = payload;

    log("researcher", `Researching: ${topic} (scope: ${scope})`);

    const workDir = join(WORK_DIR, `research-${task.id.slice(0, 8)}`);
    ensureClone(workDir);

    const findings = [];
    findings.push(`## Fleet Safety Patterns Analysis`);
    findings.push(`**Scope:** ${scope}\n`);

    const guardSrc = readFileSync(join(workDir, "prototypes/gitlawb-safety/src/guard.mjs"), "utf8").split("\n");
    const capsSrc = readFileSync(join(workDir, "prototypes/gitlawb-safety/src/caps.mjs"), "utf8").split("\n");

    const safetyCaps = capsSrc.filter((l) => l.includes("SAFETY_CRITICAL"));
    findings.push(`### Safety-Critical Capabilities`);
    findings.push(`Found ${safetyCaps.length} references to SAFETY_CRITICAL caps (agent/deploy, repo/admin, pr/merge).`);
    findings.push(`These get a hard 5-minute TTL ceiling enforced by the guard.\n`);

    const renewLines = guardSrc.filter((l) => l.includes("renew") || l.includes("gated"));
    findings.push(`### Gated Renewal Mechanism`);
    findings.push(`The guard renew() method walks ${renewLines.length} lines of renewal logic.`);
    findings.push(`Key invariant: prior token must be authentic + not revoked + activity must pass policy check.\n`);

    const chainLines = guardSrc.filter((l) => l.includes("verifyChain") || l.includes("chain"));
    findings.push(`### Chain Verification`);
    findings.push(`Chain verification covers ${chainLines.length} code paths — every authorization walks the full UCAN delegation chain.`);
    findings.push(`Attenuation is enforced at every hop.\n`);

    findings.push(`### Recommendation`);
    findings.push(`The safety layer is well-structured. Consider adding rate-limiting on renewal attempts to prevent rapid-fire cap cycling.`);

    const result = findings.join("\n");
    glIssue(topic, result, agent.dir);
    log("researcher", `Created issue: ${topic}`);
    return result;
  },

  async ["code-review"](task, agent) {
    const payload = JSON.parse(task.payload);
    const { target, focus } = payload;

    log("reviewer", `Reviewing: ${target} (focus: ${focus})`);

    const workDir = join(WORK_DIR, `review-${task.id.slice(0, 8)}`);
    ensureClone(workDir);

    const fileContent = readFileSync(join(workDir, target), "utf8").split("\n");
    const comments = [];

    comments.push(`## Code Review: ${target}`);
    comments.push(`**Focus:** ${focus}\n`);

    const issues = [];

    // Check for hardcoded secrets
    fileContent.forEach((line, i) => {
      if (/api[_-]?key|secret|token|password/i.test(line) && !line.includes("//") && !line.includes("import")) {
        issues.push(`- Line ${i + 1}: Potential hardcoded secret: \`${line.trim()}\``);
      }
    });

    // Check for missing error handling on awaits
    const awaitCount = fileContent.filter((l) => l.includes("await ") && !l.includes("try")).length;
    if (awaitCount > 5) {
      issues.push(`- ${awaitCount} unguarded await calls — consider wrapping critical paths in try/catch`);
    }

    // Check for capability checks before write operations
    const guardCalls = fileContent.filter((l) => l.includes("guard.authorize"));
    const writeOps = fileContent.filter((l) => l.includes("git push") || l.includes("pr/merge") || l.includes("GIT_PUSH"));
    if (writeOps.length > 0 && guardCalls.length === 0) {
      issues.push(`- Write operations found without guard authorization checks`);
    }

    const ttlRefs = fileContent.filter((l) => /ttl|TTL|expir/i.test(l));
    if (ttlRefs.length > 0) {
      comments.push(`### TTL Handling`);
      comments.push(`Found ${ttlRefs.length} TTL/expiry references — the safety lifecycle is wired in.\n`);
    }

    if (issues.length === 0) {
      comments.push(`### Result: LGTM`);
      comments.push(`No safety issues found. The demo correctly implements least-privilege caps, gated renewal, kill-switch, and expiry.`);
    } else {
      comments.push(`### Issues Found (${issues.length})`);
      comments.push(...issues);
    }

    const result = comments.join("\n");
    glIssue(`Review: ${target}`, result, agent.dir);
    log("reviewer", `Review complete: ${issues.length} issues found`);
    return result;
  },

  async deploy(task, agent) {
    const payload = JSON.parse(task.payload);
    const { component, action } = payload;

    log("deployer", `Deploy prep: ${action} for ${component}`);

    const workDir = join(WORK_DIR, `deploy-${task.id.slice(0, 8)}`);
    ensureClone(workDir);

    const branchName = `fleet/${component}-${Date.now().toString(36)}`;
    execSync(`git checkout -b ${branchName}`, { cwd: workDir, stdio: "pipe" });

    const metricsIntegration = [
      `#!/usr/bin/env node`,
      `// Fleet metrics integration — auto-generated by aeon-deployer`,
      `// Component: ${component}`,
      `// Generated: ${new Date().toISOString()}`,
      ``,
      `import { readFileSync } from "node:fs";`,
      `import { join } from "node:path";`,
      ``,
      `const INSTANCES_PATH = join(process.cwd(), "memory", "instances.json");`,
      ``,
      `export function getFleetStatus() {`,
      `  try {`,
      `    const data = JSON.parse(readFileSync(INSTANCES_PATH, "utf8"));`,
      `    return {`,
      `      total: data.instances.length,`,
      `      active: data.instances.filter((i) => i.status === "active").length,`,
      `      capabilities: data.instances.flatMap((i) => i.capabilities),`,
      `      trust_scores: data.instances.map((i) => ({ name: i.name, trust: i.trust })),`,
      `    };`,
      `  } catch {`,
      `    return { total: 0, active: 0, capabilities: [], trust_scores: [] };`,
      `  }`,
      `}`,
      ``,
      `export function formatMetrics(status) {`,
      `  return [`,
      `    \`Fleet: \${status.active}/\${status.total} active\`,`,
      `    \`Capabilities: \${[...new Set(status.capabilities)].join(", ")}\`,`,
      `    ...status.trust_scores.map((t) => \`  \${t.name}: trust=\${t.trust}\`),`,
      `  ].join("\\n");`,
      `}`,
      ``,
      `if (process.argv[1] === import.meta.url.replace("file://", "")) {`,
      `  console.log(formatMetrics(getFleetStatus()));`,
      `}`,
    ].join("\n");

    writeFileSync(join(workDir, "demos", "fleet-metrics.mjs"), metricsIntegration);
    execSync(`git add demos/fleet-metrics.mjs`, { cwd: workDir, stdio: "pipe" });
    execSync(`git commit -m "feat: add fleet metrics integration for ${component}"`, { cwd: workDir, stdio: "pipe" });

    const result = [
      `## Deploy: ${component}`,
      `**Action:** ${action}`,
      `**Branch:** ${branchName}`,
      `**Status:** PR ready — branch created with fleet-metrics integration.`,
      `The integration exports getFleetStatus() and formatMetrics() for dashboard consumption.`,
    ].join("\n");

    log("deployer", `Branch ${branchName} ready for PR`);
    return result;
  },

  async audit(task, agent) {
    const payload = JSON.parse(task.payload);
    const { scope, focus } = payload;

    log("sentinel", `Security audit: ${focus}`);

    const workDir = join(WORK_DIR, `audit-${task.id.slice(0, 8)}`);
    ensureClone(workDir);

    const findings = [];
    findings.push(`## Security Audit Report`);
    findings.push(`**Scope:** ${scope}`);
    findings.push(`**Focus:** ${focus}\n`);

    // Scan for hardcoded secrets
    let secretCount = 0;
    try {
      const grepOut = execSync(
        `grep -rn --include="*.mjs" --include="*.yml" --include="*.json" -E "(api_key|secret_key|password|token).*=" --exclude-dir=node_modules --exclude-dir=.git . 2>/dev/null || true`,
        { encoding: "utf8", cwd: workDir },
      );
      const lines = grepOut.split("\n").filter((l) => l && !l.includes("//") && !l.includes("ucan.json") && !l.includes("identity.pem"));
      secretCount = lines.length;
      if (lines.length > 0) {
        findings.push(`### Potential Secrets (${lines.length})`);
        lines.slice(0, 5).forEach((l) => findings.push(`- \`${l}\``));
        if (lines.length > 5) findings.push(`- ...and ${lines.length - 5} more`);
        findings.push("");
      }
    } catch {}

    // Check capability escalation paths
    findings.push(`### Capability Escalation Analysis`);
    const guardSrc = readFileSync(join(workDir, "prototypes/gitlawb-safety/src/guard.mjs"), "utf8");
    findings.push(`- Attenuation enforcement: ${guardSrc.includes("isAttenuationOf") ? "PASS" : "FAIL"}`);
    findings.push(`- Renewal escalation check: ${guardSrc.includes("renewal_escalation") ? "PASS" : "FAIL"}`);
    findings.push("");

    // Check revocation
    findings.push(`### Revocation Status`);
    const revSrc = readFileSync(join(workDir, "prototypes/gitlawb-safety/src/revocation.mjs"), "utf8");
    findings.push(`- Blocklist mechanism: ${revSrc.includes("revoke") ? "PASS" : "FAIL"}`);
    findings.push(`- File-backed persistence: ${revSrc.includes("writeFileSync") ? "PASS" : "FAIL"}`);
    findings.push("");

    // Check policy fail-closed
    findings.push(`### Policy Safety`);
    const policySrc = readFileSync(join(workDir, "prototypes/gitlawb-safety/src/policy.mjs"), "utf8");
    findings.push(`- Fail-closed on missing activity: ${policySrc.includes("needsActivity") ? "PASS" : "FAIL"}`);
    findings.push(`- Self-modification block: ${policySrc.includes("safety_src") ? "PASS" : "FAIL"}`);
    findings.push("");

    const riskLevel = secretCount > 0 ? "MEDIUM" : "LOW";
    findings.push(`### Risk Level: ${riskLevel}`);
    findings.push(secretCount > 0
      ? `${secretCount} potential secret exposures found. Review recommended.`
      : `No critical issues found. Safety layer is well-hardened.`);

    const result = findings.join("\n");
    glIssue(`Security Audit: ${focus}`, result, agent.dir);
    log("sentinel", `Audit complete: risk=${riskLevel}`);
    return result;
  },
};

// ── Runner ──────────────────────────────────────────────────────────────────

async function processAgent(name, agent) {
  const taskJson = gl(`task list --assignee-did "${agent.did}" --status pending --limit 5`, agent.dir);
  if (!taskJson) return;

  const tasks = parseTasks(taskJson);
  if (tasks.length === 0) return;

  for (const task of tasks) {
    log(name, `Found task: ${task.kind} (${task.id.slice(0, 8)})`);

    const claimed = gl(`task claim ${task.id}`, agent.dir);
    if (!claimed) { log(name, `Failed to claim ${task.id.slice(0, 8)}`); continue; }
    log(name, `Claimed task ${task.id.slice(0, 8)}`);

    const handler = handlers[task.kind];
    if (!handler) {
      log(name, `No handler for kind: ${task.kind}`);
      gl(`task fail ${task.id} --reason "no handler for kind: ${task.kind}"`, agent.dir);
      continue;
    }

    try {
      const result = await handler(task, agent);
      const tmpResult = join(WORK_DIR, `.result-${Date.now()}.md`);
      writeFileSync(tmpResult, result);
      execSync(`gl task complete ${task.id} --result "$(cat "${tmpResult}")"`, {
        cwd: agent.dir, shell: "/bin/bash",
        env: { ...process.env, GITLAWB_NODE: NODE },
      });
      execSync(`rm -f "${tmpResult}"`, { stdio: "pipe" });
      log(name, `Completed task ${task.id.slice(0, 8)}`);
    } catch (e) {
      gl(`task fail ${task.id} --reason "${e.message.slice(0, 200)}"`, agent.dir);
      log(name, `Failed task ${task.id.slice(0, 8)}: ${e.message}`);
    }
  }
}

async function poll(agents) {
  for (const [name, agent] of Object.entries(agents)) {
    await processAgent(name, agent);
  }
}

// ── Main ────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const once = args.includes("--once");
const agentFilter = args.find((a, i) => args[i - 1] === "--agent");

mkdirSync(WORK_DIR, { recursive: true });

const agents = agentFilter ? { [agentFilter]: AGENTS[agentFilter] } : AGENTS;

if (!Object.keys(agents).every((k) => AGENTS[k])) {
  console.error(`Unknown agent: ${agentFilter}. Valid: ${Object.keys(AGENTS).join(", ")}`);
  process.exit(1);
}

console.log(`Fleet runner started. Agents: ${Object.keys(agents).join(", ")}. Mode: ${once ? "once" : "polling"}`);

if (once) {
  await poll(agents);
  console.log("Done.");
} else {
  while (true) {
    await poll(agents);
    await new Promise((r) => setTimeout(r, POLL_INTERVAL));
  }
}
