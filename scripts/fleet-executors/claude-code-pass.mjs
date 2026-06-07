// claude-code-pass.mjs — Patch-and-PR executor for docs/refactor/test passes.
//
// Drives the `claude` CLI with file-edit tools (Read/Edit/Write/Grep) to make
// a small, targeted change for one of the code-quality pass kinds, then
// branches → commits → pushes → opens a PR via `gh`. Returns a structured
// result the caller (reviewer.mjs) renders into a task summary.
//
// All filesystem work happens in a throwaway git worktree so the main
// checkout is untouched. This matters because the fleet workflow runs
// `task-generator.mjs` immediately before the runner, and the generator
// writes `memory/fleet-task-generator-state.json` — the main checkout is
// effectively never clean when this executor fires. A fresh worktree
// branched off HEAD gives claude an isolated, predictable starting point.
//
// Returns ok:false on:
//   - the `claude` CLI being unavailable or its run failing;
//   - any of git worktree add / commit / push or `gh pr create` failing.
// Returns ok:true with prUrl:null when claude legitimately decides nothing
// is worth changing — task-runner records the task as completed so the
// generator's cooldown gate kicks in rather than retrying immediately.

import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const DEFAULT_MODEL = process.env.GITLAWB_CODE_PASS_MODEL || "claude-sonnet-4-6";
// A patch pass involves Read/Grep/Edit cycles plus an explanation — give it
// noticeably more headroom than the read-only review path (which uses 300s).
const TIMEOUT_MS = Number(process.env.GITLAWB_CODE_PASS_TIMEOUT_MS || 600_000);
// Skip opening a new pass-PR if there are already this many open PRs of the
// same kind. Stops the */1h ticker from piling duplicates onto an unmerged
// backlog when nothing is reviewing them. 0 disables the gate.
const BACKLOG_LIMIT = Number(process.env.GITLAWB_CODE_PASS_BACKLOG_LIMIT || 3);

const KIND_CONFIG = {
  "docs-pass": {
    label: "Documentation pass",
    promptFocus:
      "Improve documentation: add missing docstrings, fix stale comments, refresh README drift " +
      "near the listed files. Do NOT rewrite working code — only touch comments, docstrings, and " +
      "documentation files. Keep the change small and reviewable.",
  },
  "refactor-pass": {
    label: "Refactor pass",
    promptFocus:
      "Make ONE small targeted refactor near the listed files: extract a duplicated helper, remove " +
      "dead code, or simplify a tangled expression. Preserve all observable behavior. Do not change " +
      "public APIs. If nothing is worth refactoring, make no changes.",
  },
  "test-pass": {
    label: "Test pass",
    promptFocus:
      "Add tests for an uncovered branch or missing edge case near the listed files. Place tests " +
      "alongside existing tests for the same module. Do not modify production code. If existing " +
      "tests already cover the area, make no changes.",
  },
};

function run(cmd, args, opts = {}) {
  const proc = spawnSync(cmd, args, { encoding: "utf8", ...opts });
  return {
    ok: proc.status === 0,
    stdout: (proc.stdout || "").trim(),
    stderr: (proc.stderr || "").trim(),
    status: proc.status,
  };
}

function shortTaskId(taskId) {
  return String(taskId || "").replace(/[^a-zA-Z0-9]/g, "").slice(0, 10) || "x";
}

// Count open PRs whose head branch starts with `aeon/${kind}-`. Returns null
// when the query fails (gh missing, auth issue, malformed JSON) — callers
// treat null as "unknown" and proceed rather than blocking work on a flaky
// metadata check.
function openPRsForKind(kind, repoDir) {
  const r = run("gh", ["pr", "list", "--state", "open", "--json", "headRefName", "--limit", "200"], { cwd: repoDir });
  if (!r.ok) return null;
  try {
    const arr = JSON.parse(r.stdout);
    if (!Array.isArray(arr)) return null;
    const prefix = `aeon/${kind}-`;
    return arr.filter((p) => typeof p?.headRefName === "string" && p.headRefName.startsWith(prefix)).length;
  } catch {
    return null;
  }
}

function workingTreeClean(repoDir) {
  const status = run("git", ["status", "--porcelain"], { cwd: repoDir });
  return status.ok && status.stdout === "";
}

function buildPrompt(kind, target, extraFocus) {
  const cfg = KIND_CONFIG[kind];
  const targetLine = target ? `Recently changed files (focus area): ${target}` : "No specific files supplied — pick a small target near recent commits.";
  return [
    `You are running an automated ${cfg.label} as part of the Aeon fleet.`,
    "",
    cfg.promptFocus,
    extraFocus ? `Additional focus from task payload: ${extraFocus}` : "",
    "",
    targetLine,
    "",
    "Hard rules — violating any of these wastes the run:",
    "- Make AT MOST a handful of small edits across at most ~5 files.",
    "- Do NOT run git commit, git push, or `gh` — the executor handles that.",
    "- Do NOT touch CI workflows (.github/), secrets, lockfiles, or large generated artifacts.",
    "- If after exploring you decide nothing useful can be done, make no changes and explain why.",
    "- Keep the change reviewable by a human in under 5 minutes.",
    "",
    "When finished, write ONE final line of plain text describing what you changed (or that you",
    "made no changes). The executor uses that line as the PR body summary.",
  ].filter(Boolean).join("\n");
}

// Spawn `claude` with file-edit tools allowed. Returns the trimmed stdout
// (the final summary line is read from this) or null on failure.
function invokeClaude(prompt, repoDir, model) {
  const ver = run("claude", ["--version"]);
  if (!ver.ok) {
    console.log(`[code-pass] claude CLI unavailable (status=${ver.status}); aborting`);
    return null;
  }
  // Allow Read/Grep/Glob/Edit/Write plus a narrow Bash allowlist so claude can
  // explore (git log/diff/ls-files) without being able to push or change
  // identity. The executor (not claude) does the commit + push + PR.
  const allowed = "Read,Grep,Glob,Edit,Write,Bash(git diff:*),Bash(git log:*),Bash(git status:*),Bash(git ls-files:*),Bash(rg:*),Bash(node:*)";
  const proc = spawnSync(
    "claude",
    ["-p", "-", "--model", model, "--allowedTools", allowed, "--output-format", "text"],
    { cwd: repoDir, input: prompt, encoding: "utf8", timeout: TIMEOUT_MS },
  );
  if (proc.status !== 0 || !proc.stdout) {
    const why = proc.error ? proc.error.code || proc.error.message : `status=${proc.status}`;
    const errSnip = (proc.stderr || "").trim().split("\n")[0]?.slice(0, 200) || "";
    console.log(`[code-pass] claude call failed (${why}); stderr: ${errSnip}`);
    return null;
  }
  return proc.stdout.trim();
}

function extractSummary(stdout) {
  const lines = stdout.split("\n").map((s) => s.trim()).filter(Boolean);
  // Use the last non-empty line as the explicit summary if it looks like prose.
  const last = lines[lines.length - 1] || "";
  if (last.length > 0 && last.length <= 400) return last;
  return lines.slice(-3).join(" ").slice(0, 400);
}

// Main entry — invoked from reviewer.mjs's kind dispatch.
// Returns { ok, prUrl, kind, summary, reason } — `ok=false` carries a `reason`
// the caller surfaces to the task runner.
//
// Flow:
//   1. Create an ephemeral worktree branched off HEAD. Claude runs inside it,
//      so the main checkout (which the task-generator just dirtied with state
//      files) is untouched.
//   2. Invoke claude. If it produces no diff, remove the worktree + branch,
//      return ok with no PR.
//   3. Otherwise commit, push, gh pr create — all from inside the worktree.
//      Always remove the worktree at the end. The branch ref survives so the
//      PR can reference it; on push failure we keep the branch locally too.
export function runCodePass({ kind, target = "", focus = "", repoDir = process.cwd(), taskId = "", model = DEFAULT_MODEL } = {}) {
  const cfg = KIND_CONFIG[kind];
  if (!cfg) return { ok: false, kind, reason: `unknown code-pass kind: ${kind}` };

  if (BACKLOG_LIMIT > 0) {
    const backlog = openPRsForKind(kind, repoDir);
    if (backlog !== null && backlog >= BACKLOG_LIMIT) {
      return {
        ok: true,
        kind,
        prUrl: null,
        summary: `${cfg.label}: skipped — ${backlog} open ${kind} PR(s) already in backlog (limit ${BACKLOG_LIMIT}).`,
      };
    }
  }

  const today = new Date().toISOString().slice(0, 10);
  const branch = `aeon/${kind}-${today}-${shortTaskId(taskId)}`;
  const worktreeDir = mkdtempSync(join(tmpdir(), "aeon-code-pass-"));
  const add = run("git", ["worktree", "add", "-b", branch, worktreeDir, "HEAD"], { cwd: repoDir });
  if (!add.ok) {
    rmSync(worktreeDir, { recursive: true, force: true });
    return { ok: false, kind, reason: `git worktree add failed: ${add.stderr.slice(0, 200)}` };
  }

  // Best-effort cleanup. `git worktree remove --force` handles the working
  // directory; the branch ref is dropped separately (skipped when the branch
  // has been pushed and we want it to remain reachable).
  const cleanup = (deleteBranch) => {
    run("git", ["worktree", "remove", "--force", worktreeDir], { cwd: repoDir });
    rmSync(worktreeDir, { recursive: true, force: true });
    if (deleteBranch) run("git", ["branch", "-D", branch], { cwd: repoDir });
  };

  try {
    const claudeOut = invokeClaude(buildPrompt(kind, target, focus), worktreeDir, model);
    if (claudeOut === null) {
      cleanup(true);
      return { ok: false, kind, reason: "claude invocation failed" };
    }

    if (workingTreeClean(worktreeDir)) {
      cleanup(true);
      return {
        ok: true,
        kind,
        prUrl: null,
        summary: `${cfg.label}: no changes warranted. ${extractSummary(claudeOut)}`.slice(0, 480),
      };
    }

    const summary = extractSummary(claudeOut);
    const addR = run("git", ["add", "-A"], { cwd: worktreeDir });
    if (!addR.ok) { cleanup(true); return { ok: false, kind, reason: `git add failed: ${addR.stderr.slice(0, 200)}` }; }
    const commit = run("git", ["commit", "-m", `${kind}: ${summary.slice(0, 80)}`], { cwd: worktreeDir });
    if (!commit.ok) { cleanup(true); return { ok: false, kind, reason: `git commit failed: ${commit.stderr.slice(0, 200)}` }; }

    const push = run("git", ["push", "-u", "origin", branch], { cwd: worktreeDir });
    if (!push.ok) {
      // Commit landed locally on the branch but never reached origin. Keep the
      // branch ref so an operator can push it manually; just drop the worktree.
      cleanup(false);
      return { ok: false, kind, reason: `git push failed: ${push.stderr.slice(0, 200)}` };
    }

    const title = `${cfg.label}: ${summary.slice(0, 70)}`;
    const body = [
      `## ${cfg.label}`,
      "",
      `**Kind:** \`${kind}\``,
      target ? `**Target files:** ${target}` : "",
      focus ? `**Focus:** ${focus}` : "",
      "",
      "### Summary",
      summary || "(no summary returned)",
      "",
      "---",
      `🤖 Generated by aeon-reviewer via \`claude-code-pass.mjs\` (task ${taskId || "?"})`,
    ].filter(Boolean).join("\n");
    const pr = run("gh", ["pr", "create", "--title", title, "--body", body, "--head", branch], { cwd: worktreeDir });
    cleanup(false);
    if (!pr.ok) return { ok: false, kind, reason: `gh pr create failed: ${pr.stderr.slice(0, 200)}` };
    const prUrl = (pr.stdout.match(/https?:\/\/\S+/) || [])[0] || pr.stdout.trim();
    return { ok: true, kind, prUrl, summary, branch };
  } catch (err) {
    cleanup(true);
    throw err;
  }
}
