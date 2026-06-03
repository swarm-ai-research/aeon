#!/usr/bin/env node
// sentinel.mjs — Real security audit executor for aeon-sentinel.
//
// Runs actual security scans (rg pattern matching, fleet health checks,
// workflow secret exposure, recent deletions) and creates audit issues
// when findings warrant it.
//
// Env vars (set by task-runner):
//   GITLAWB_TASK_JSON   — full task object
//   GITLAWB_AGENT_JSON  — agent instance object
//   GITLAWB_REPO_DIR    — repo working directory

import { spawnSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const repoDir = process.env.GITLAWB_REPO_DIR || ".";
const task = JSON.parse(process.env.GITLAWB_TASK_JSON || "{}");
const agent = JSON.parse(process.env.GITLAWB_AGENT_JSON || "{}");

const payload = typeof task.payload === "string" ? JSON.parse(task.payload) : (task.payload || {});
const focus = payload.focus || "full repo security";

function run(cmd, args) {
  const proc = spawnSync(cmd, args, { cwd: repoDir, encoding: "utf8" });
  return { ok: proc.status === 0, stdout: (proc.stdout || "").trim(), stderr: (proc.stderr || "").trim() };
}

const findings = [];

// ── 1. Dangerous Pattern Scan ──
const dangerousPatterns = [
  { pattern: "eval(", label: "eval() calls", severity: "high" },
  { pattern: "exec(", label: "exec() calls", severity: "high" },
  { pattern: "execSync(", label: "execSync() calls", severity: "medium" },
  { pattern: "spawnSync(", label: "spawnSync() calls", severity: "low" },
  { pattern: "rm -rf", label: "rm -rf", severity: "high" },
  { pattern: "PRIVATE KEY", label: "private key references", severity: "critical" },
  { pattern: "api_key", label: "api_key references", severity: "medium" },
  { pattern: "password", label: "password references", severity: "medium" },
];

for (const { pattern, label, severity } of dangerousPatterns) {
  // --fixed-strings: patterns like "eval(" contain regex metacharacters; without
  // -F the unbalanced "(" is an invalid regex, rg exits non-zero, and the loop
  // silently skips the check — defeating the audit. These are literal substrings.
  const result = run("rg", ["-n", "--count", "--fixed-strings", pattern, repoDir, "--glob", "!node_modules", "--glob", "!.git"]);
  if (result.ok && result.stdout) {
    const counts = result.stdout.split("\n").filter(Boolean);
    const total = counts.reduce((sum, line) => {
      const n = parseInt(line.split(":").pop(), 10);
      return sum + (isNaN(n) ? 1 : n);
    }, 0);
    if (total > 0) {
      findings.push({ severity, category: "pattern", description: `${label}: ${total} occurrence(s) across ${counts.length} file(s)`, detail: counts.slice(0, 5).join("\n") });
    }
  }
}

// ── 2. Fleet Health Check ──
const instancesPath = join(repoDir, "memory/instances.json");
if (existsSync(instancesPath)) {
  try {
    const instances = JSON.parse(readFileSync(instancesPath, "utf8"));
    const agents = instances.instances || [];

    for (const inst of agents) {
      // Check cap expiry
      if (inst.cap_expires_at) {
        const expiresAt = new Date(inst.cap_expires_at);
        const hoursLeft = (expiresAt - Date.now()) / (1000 * 60 * 60);
        if (hoursLeft < 0) {
          findings.push({ severity: "critical", category: "fleet", description: `${inst.name}: capability EXPIRED (${inst.cap_expires_at})` });
        } else if (hoursLeft < 24) {
          findings.push({ severity: "high", category: "fleet", description: `${inst.name}: capability expires in ${hoursLeft.toFixed(1)}h` });
        }
      }

      // Check trust
      if (inst.trust !== undefined && inst.trust < 0.03) {
        findings.push({ severity: "high", category: "fleet", description: `${inst.name}: trust critically low (${inst.trust})` });
      }

      // Check health status
      if (inst.health === "degraded" || inst.health === "stale" || inst.health === "unreachable") {
        findings.push({ severity: "medium", category: "fleet", description: `${inst.name}: health=${inst.health}` });
      }
    }
  } catch {
    findings.push({ severity: "low", category: "fleet", description: "Could not parse memory/instances.json" });
  }
}

// ── 3. Workflow Secret Exposure Check ──
const workflowsDir = join(repoDir, ".github/workflows");
if (existsSync(workflowsDir)) {
  const rgResult = run("rg", ["-n", "secrets\\.[A-Z_]+", workflowsDir]);
  if (rgResult.ok && rgResult.stdout) {
    const secretRefs = rgResult.stdout.split("\n").filter(Boolean);
    // Check if any secret is used directly in a run: step (not just in env:)
    const directUse = secretRefs.filter(line => {
      // Lines with secrets in run: blocks (not just env:) are risky
      return line.includes("run:") && !line.includes("${{ env.");
    });
    if (directUse.length > 0) {
      findings.push({ severity: "medium", category: "workflow", description: `${directUse.length} workflow step(s) reference secrets directly in run: commands` });
    }
  }
}

// ── 4. Recent Deletions Check ──
const deletions = run("git", ["log", "--diff-filter=D", "--name-only", "--oneline", "-10"]);
if (deletions.ok && deletions.stdout) {
  const deletedFiles = deletions.stdout.split("\n").filter(l => l && !l.startsWith(" "));
  if (deletedFiles.length > 0) {
    findings.push({ severity: "low", category: "deletion", description: `${deletedFiles.length} file(s) deleted in recent commits`, detail: deletedFiles.slice(0, 5).join("\n") });
  }
}

// ── 5. Self-modification check ──
const safetyDir = join(repoDir, "prototypes/gitlawb-safety/src");
if (existsSync(safetyDir)) {
  const selfMod = run("rg", ["-n", "rm\\s+-rf|eval\\(", safetyDir]);
  if (selfMod.ok && selfMod.stdout) {
    findings.push({ severity: "critical", category: "self-modification", description: "Dangerous patterns found in safety-critical code", detail: selfMod.stdout.split("\n").slice(0, 5).join("\n") });
  }
}

// ── Build Report ──
const criticals = findings.filter(f => f.severity === "critical").length;
const highs = findings.filter(f => f.severity === "high").length;
const mediums = findings.filter(f => f.severity === "medium").length;
const lows = findings.filter(f => f.severity === "low").length;

const riskLevel = criticals > 0 ? "CRITICAL" : highs > 0 ? "HIGH" : mediums > 0 ? "MEDIUM" : "LOW";
const today = new Date().toISOString().slice(0, 10);

// Always create an audit report
const auditTitle = `Security Audit: ${riskLevel} (${today})`;

const body = [
  `## Security Audit Report`,
  ``,
  `**Date:** ${today}`,
  `**Agent:** ${agent.name} (${agent.did})`,
  `**Focus:** ${focus}`,
  `**Task:** ${task.id}`,
  `**Risk Level:** ${riskLevel}`,
  ``,
  `### Summary`,
  `- Critical: ${criticals}`,
  `- High: ${highs}`,
  `- Medium: ${mediums}`,
  `- Low: ${lows}`,
  ``,
];

if (findings.length > 0) {
  body.push(`### Findings`);
  for (const f of findings) {
    body.push(`- **[${f.severity.toUpperCase()}]** [${f.category}] ${f.description}`);
    if (f.detail) {
      body.push(`  \`\`\``);
      body.push(`  ${f.detail.split("\n").join("\n  ")}`);
      body.push(`  \`\`\``);
    }
  }
  body.push("");
} else {
  body.push(`### Findings`);
  body.push(`No issues found. Repository security posture is clean.`);
  body.push("");
}

body.push(`*Generated by aeon-sentinel via GitLawb task runner*`);

// Create issue (always — audits should leave a paper trail)
const result = spawnSync("gl", [
  "issue", "create",
  "--title", auditTitle,
  "--body", body.join("\n"),
  "aeon",
], { cwd: repoDir, encoding: "utf8" });

if (result.status !== 0) {
  const err = result.stderr || result.stdout || "unknown error";
  console.error(`Failed to create audit issue: ${err}`);
  process.exit(1);
}

const issueUrl = (result.stdout || "").trim();
console.log(`Audit complete: ${riskLevel} — ${findings.length} findings (${criticals} critical, ${highs} high). Issue: ${issueUrl}`);
