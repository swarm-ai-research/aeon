#!/usr/bin/env node
// reviewer.mjs — Real code review executor for aeon-reviewer.
//
// Reads actual diffs, analyzes code for real issues (security, errors, logic),
// and posts findings as issues on the GitLawb repo.
//
// Env vars (set by task-runner):
//   GITLAWB_TASK_JSON   — full task object
//   GITLAWB_AGENT_JSON  — agent instance object
//   GITLAWB_REPO_DIR    — repo working directory

import { spawnSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { claudeReview } from "./claude-review.mjs";
import { runCodePass } from "./claude-code-pass.mjs";

const repoDir = process.env.GITLAWB_REPO_DIR || ".";
const task = JSON.parse(process.env.GITLAWB_TASK_JSON || "{}");
const agent = JSON.parse(process.env.GITLAWB_AGENT_JSON || "{}");

const payload = typeof task.payload === "string" ? JSON.parse(task.payload) : (task.payload || {});
const target = payload.target || payload.file || "";
const focus = payload.focus || "security and correctness";

const CODE_PASS_KINDS = new Set(["docs-pass", "refactor-pass", "test-pass"]);
const taskKind = task.kind ?? task.type ?? "";

// ── Code-quality pass dispatch (docs / refactor / test) ──
// Drives `claude` with file-edit tools to make a small targeted change, then
// branches → commits → pushes → opens a PR via `gh`. Exits non-zero on
// invocation failure so the task-runner records the task as failed and
// task-generator can retry it on the next cycle; exits 0 (with no PR) when
// claude legitimately decides nothing is worth changing.
if (CODE_PASS_KINDS.has(taskKind)) {
  const result = runCodePass({
    kind: taskKind,
    target,
    focus,
    repoDir,
    taskId: task.id || "",
  });
  if (!result.ok) {
    console.error(`Code-pass ${taskKind} failed: ${result.reason || "unknown"}`);
    process.exit(1);
  }
  if (result.prUrl) {
    console.log(`Code-pass ${taskKind} opened PR: ${result.prUrl} — ${result.summary}`);
  } else {
    console.log(`Code-pass ${taskKind} made no changes — ${result.summary}`);
  }
  process.exit(0);
}

// ── Renewal review (sub-swarm red-team) ──
// Routed here by src/reviewer-gate.mjs: adversarially review another agent's
// recent activity before its safety-critical capability is renewed. The verdict
// line is printed FIRST so it survives result-summary truncation, and is read
// back by the gate via the task artifact (RENEWAL_VERDICT ... fp=<fingerprint>).
if ((task.kind ?? task.type) === "renewal-review" || payload.review_kind === "renewal") {
  const fp = payload.fingerprint ?? "unknown";
  const files = Array.isArray(payload.changedFiles) ? payload.changedFiles : [];
  const lines = Number(payload.changedLines) || 0;
  const caps = Array.isArray(payload.capabilities) ? payload.capabilities : [];
  const issues = [];

  // Oversight tampering — the agent must never touch the safety machinery,
  // CI workflows, or operating instructions, regardless of its capabilities.
  const PROTECTED = ["prototypes/gitlawb-safety/src/", ".github/workflows/", "CLAUDE.md"];
  const tamper = files.find((f) => PROTECTED.some((p) => f.startsWith(p)));
  if (tamper) issues.push(`oversight_tampering:${tamper.replace(/\s+/g, "_")}`);

  // Scope creep — activity outside the fleet's allowed working surface.
  const ALLOWED = ["skills/", "articles/", "memory/", "dashboard/", "prototypes/compute-futures/"];
  const stray = files.find((f) => !ALLOWED.some((p) => f.startsWith(p)));
  if (stray) issues.push(`scope_creep:${stray.replace(/\s+/g, "_")}`);

  // Anomalous volume for a single short renewal window.
  if (lines > 1500 || files.length > 25) issues.push(`anomalous_volume:${files.length}f/${lines}l`);

  const approved = issues.length === 0;
  const reasonSlug = approved ? "" : `:${issues[0].split(":")[0]}`;
  console.log(`RENEWAL_VERDICT ${approved ? "approved" : "denied" + reasonSlug} fp=${fp}`);
  console.log(
    `Renewal review of ${payload.target_did || "agent"} [caps: ${caps.join(",") || "none"}]: ` +
      (approved ? `LGTM — ${files.length} files / ${lines} lines within scope.` : issues.join("; ")),
  );
  process.exit(0);
}

function run(cmd, args) {
  const proc = spawnSync(cmd, args, { cwd: repoDir, encoding: "utf8" });
  return proc.stdout?.trim() || "";
}

// Get the diff to review
let diff = "";
let diffSource = "";

if (target && existsSync(join(repoDir, target))) {
  // Review a specific file — show recent changes
  diff = run("git", ["log", "-p", "--follow", "-5", "--", target]);
  diffSource = `file: ${target}`;
} else {
  // Review recent changes across the repo
  diff = run("git", ["diff", "HEAD~5..HEAD"]);
  if (!diff) {
    diff = run("git", ["log", "-p", "-5"]);
  }
  diffSource = "recent commits (HEAD~5..HEAD)";
}

if (!diff) {
  console.log("No diff to review — repository may be clean");
  process.exit(0);
}

// ── Claude Code-backed review (preferred) ──
// Apply the pr-review skill methodology via the `claude` CLI. Falls through to
// the deterministic regex analysis below when the CLI is unavailable/unauth'd.
const ai = claudeReview({ diff, focus, target: target || "recent changes", repoDir });
if (ai) {
  const today = new Date().toISOString().slice(0, 10);
  const reviewTitle = `Review: ${target || "recent changes"} — ${ai.verdict} (${today})`;
  const body = [
    `## Code Review: ${target || "recent changes"}`,
    ``,
    `**Date:** ${today}`,
    `**Agent:** ${agent.name} (${agent.did})`,
    `**Focus:** ${focus}`,
    `**Source:** ${diffSource}`,
    `**Verdict:** ${ai.verdict}${ai.confidence != null ? `  ·  **Confidence:** ${ai.confidence}/5` : ""}`,
    `**Reviewer:** claude (${process.env.GITLAWB_REVIEW_MODEL || "claude-sonnet-4-6"})`,
    ``,
  ];
  if (ai.summary) body.push(ai.summary, ``);
  if (ai.findings.length > 0) {
    body.push(`### Findings`);
    for (const f of ai.findings) {
      const loc = f.file ? `${f.file}${f.line != null ? `:${f.line}` : ""}` : "";
      body.push(`- **[${f.severity}]** ${loc ? `\`${loc}\` — ` : ""}${f.why}`);
    }
    body.push(``);
  } else {
    body.push(`### Summary`, `No blocking findings.`, ``);
  }
  body.push(`*Generated by aeon-reviewer via Claude Code (pr-review methodology)*`);

  const result = spawnSync("gl", ["issue", "create", "--title", reviewTitle, "--body", body.join("\n"), "aeon"], {
    cwd: repoDir,
    encoding: "utf8",
  });
  if (result.status !== 0) {
    console.error(`Failed to create review issue: ${result.stderr || result.stdout || "unknown error"}`);
    process.exit(1);
  }
  const crit = ai.findings.filter((f) => f.severity === "CRITICAL").length;
  const iss = ai.findings.filter((f) => f.severity === "ISSUE").length;
  console.log(
    `Review complete (claude): "${reviewTitle}" — ${ai.findings.length} findings (${crit} critical, ${iss} issue). Verdict: ${ai.verdict}. Issue: ${(result.stdout || "").trim()}`,
  );
  process.exit(0);
}

console.log("claude review unavailable — falling back to pattern analysis");

const diffLines = diff.split("\n");
const addedLines = diffLines.filter(l => l.startsWith("+") && !l.startsWith("+++"));
const removedLines = diffLines.filter(l => l.startsWith("-") && !l.startsWith("---"));

// Pattern-based analysis
const findings = [];

// Security patterns
const securityPatterns = [
  [/\beval\s*\(/, "eval() call — potential code injection", "high"],
  [/\bexec\s*\(/, "exec() call — potential command injection", "high"],
  [/PRIVATE\s*KEY|private_key|privkey/i, "private key reference — verify it's not exposed", "critical"],
  [/password|secret|token|api_key/i, "sensitive value reference — check for hardcoded secrets", "medium"],
  [/rm\s+-rf?\s+\//, "destructive filesystem operation", "critical"],
  [/curl\s.*\$[{(]/, "curl with variable expansion — sandbox may block", "low"],
  [/\bTODO\b|\bFIXME\b|\bHACK\b/, "technical debt marker", "low"],
];

// Error handling patterns
const errorPatterns = [
  [/catch\s*\(\s*\w*\s*\)\s*\{\s*\}/, "empty catch block — silently swallows errors", "medium"],
  [/\.catch\s*\(\s*\(\)\s*=>/, "promise catch with empty handler", "medium"],
  [/\bprocess\.exit\s*\(\s*0\s*\)/, "process.exit(0) in error path — may hide failures", "low"],
];

// Check added lines for issues
for (const line of addedLines) {
  for (const [pattern, desc, severity] of securityPatterns) {
    if (pattern.test(line)) {
      findings.push({ severity, description: desc, line: line.trim().slice(0, 120) });
    }
  }
  for (const [pattern, desc, severity] of errorPatterns) {
    if (pattern.test(line)) {
      findings.push({ severity, description: desc, line: line.trim().slice(0, 120) });
    }
  }
}

// Check for large blocks of removed code (potential accidental deletion)
if (removedLines.length > 50 && addedLines.length < 10) {
  findings.push({
    severity: "medium",
    description: `Large deletion (${removedLines.length} lines removed, ${addedLines.length} added) — verify intentional`,
    line: "(bulk change)",
  });
}

// Positive checks
const positives = [];
if (addedLines.some(l => l.includes("try") && l.includes("catch"))) positives.push("error handling present");
if (addedLines.some(l => l.includes("//") || l.includes("/*"))) positives.push("comments added");
if (addedLines.some(l => l.includes("test") || l.includes("describe") || l.includes("it("))) positives.push("tests included");

// Determine severity summary
const criticals = findings.filter(f => f.severity === "critical").length;
const highs = findings.filter(f => f.severity === "high").length;
const mediums = findings.filter(f => f.severity === "medium").length;

let verdict;
if (criticals > 0) verdict = "BLOCKING";
else if (highs > 0) verdict = "ISSUES";
else if (mediums > 0) verdict = "MINOR_ISSUES";
else verdict = "LGTM";

// Build review report
const today = new Date().toISOString().slice(0, 10);
const reviewTitle = `Review: ${target || "recent changes"} — ${verdict} (${today})`;

const body = [
  `## Code Review: ${target || "recent changes"}`,
  ``,
  `**Date:** ${today}`,
  `**Agent:** ${agent.name} (${agent.did})`,
  `**Focus:** ${focus}`,
  `**Source:** ${diffSource}`,
  `**Verdict:** ${verdict}`,
  ``,
  `### Stats`,
  `- Lines added: ${addedLines.length}`,
  `- Lines removed: ${removedLines.length}`,
  `- Findings: ${findings.length}`,
  ``,
];

if (findings.length > 0) {
  body.push(`### Findings`);
  for (const f of findings) {
    body.push(`- **[${f.severity.toUpperCase()}]** ${f.description}`);
    body.push(`  \`${f.line}\``);
  }
  body.push("");
}

if (positives.length > 0) {
  body.push(`### Positive`);
  for (const p of positives) {
    body.push(`- ${p}`);
  }
  body.push("");
}

if (findings.length === 0 && positives.length === 0) {
  body.push(`### Summary`);
  body.push(`No significant issues found in the reviewed diff.`);
  body.push("");
}

body.push(`*Generated by aeon-reviewer via GitLawb task runner*`);

// Create the issue
const result = spawnSync("gl", [
  "issue", "create",
  "--title", reviewTitle,
  "--body", body.join("\n"),
  "aeon",
], { cwd: repoDir, encoding: "utf8" });

if (result.status !== 0) {
  const err = result.stderr || result.stdout || "unknown error";
  console.error(`Failed to create review issue: ${err}`);
  process.exit(1);
}

const issueUrl = (result.stdout || "").trim();
console.log(`Review complete: "${reviewTitle}" — ${findings.length} findings (${criticals} critical, ${highs} high, ${mediums} medium). Verdict: ${verdict}. Issue: ${issueUrl}`);
