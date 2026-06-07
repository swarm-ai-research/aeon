// claude-code-pass.test.mjs — Tests for runCodePass.
//
// Each test owns a fresh git repo + bare remote in tmpdir, with shell stubs
// for `claude` and `gh` on PATH. No real CLI or network access.
//
// Run: node scripts/fleet-executors/claude-code-pass.test.mjs

import { mkdtempSync, writeFileSync, rmSync, chmodSync, mkdirSync, readFileSync, existsSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import assert from "node:assert/strict";
import { runCodePass } from "./claude-code-pass.mjs";

function git(args, cwd) {
  const r = spawnSync("git", args, { cwd, encoding: "utf8" });
  return { status: r.status, stdout: (r.stdout || "").trim(), stderr: (r.stderr || "").trim() };
}

function freshRepo() {
  const dir = mkdtempSync(join(tmpdir(), "code-pass-test-"));
  for (const args of [
    ["init", "-q"],
    ["config", "user.email", "t@e.st"],
    ["config", "user.name", "t"],
    ["commit", "--allow-empty", "-q", "-m", "init"],
  ]) {
    const r = git(args, dir);
    assert.equal(r.status, 0, `git ${args.join(" ")} failed: ${r.stderr}`);
  }
  return dir;
}

// freshRepo() + bare remote + bin/ dir with stub claude/gh installed at the
// front of PATH. Returns { work, localDir, remoteDir, binDir, ghLog }.
function freshRepoWithRemote({ claudeScript, ghScript = `#!/usr/bin/env bash\necho "gh: $@" >> "$GH_LOG"\necho "https://github.com/stub/repo/pull/42"\n` }) {
  const work = mkdtempSync(join(tmpdir(), "code-pass-e2e-"));
  const remoteDir = join(work, "remote.git");
  const localDir = join(work, "local");
  const binDir = join(work, "bin");
  const ghLog = join(work, "gh.log");
  mkdirSync(binDir);
  writeFileSync(join(binDir, "claude"), claudeScript);
  chmodSync(join(binDir, "claude"), 0o755);
  writeFileSync(join(binDir, "gh"), ghScript);
  chmodSync(join(binDir, "gh"), 0o755);
  spawnSync("git", ["init", "--bare", "-q", remoteDir]);
  spawnSync("git", ["clone", "-q", remoteDir, localDir]);
  git(["config", "user.email", "t@e.st"], localDir);
  git(["config", "user.name", "t"], localDir);
  writeFileSync(join(localDir, "lib.mjs"), "// initial\n");
  git(["add", "lib.mjs"], localDir);
  git(["commit", "-q", "-m", "init"], localDir);
  git(["branch", "-M", "main"], localDir);
  git(["push", "-q", "-u", "origin", "main"], localDir);
  return { work, localDir, remoteDir, binDir, ghLog };
}

function withStubbedEnv(binDir, ghLog, fn) {
  const oldPath = process.env.PATH;
  const oldLog = process.env.GH_LOG;
  process.env.PATH = `${binDir}:${oldPath}`;
  process.env.GH_LOG = ghLog;
  try { return fn(); } finally {
    process.env.PATH = oldPath;
    if (oldLog === undefined) delete process.env.GH_LOG; else process.env.GH_LOG = oldLog;
  }
}

// Stub that, when invoked inside a worktree, finds the file the test wrote
// to the main checkout's lib.mjs and appends to its OWN copy. Each worktree
// has its own working tree — claude writing to ./lib.mjs touches only that
// worktree. Returns its final message on stdout.
const CLAUDE_EDIT_STUB = `#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "stub claude"; exit 0; fi
cat > /dev/null
echo "added a docstring" >> "$(pwd)/lib.mjs"
echo "Added a brief docstring to lib.mjs."
`;
const CLAUDE_NOOP_STUB = `#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "stub claude"; exit 0; fi
cat > /dev/null
echo "nothing worth changing here"
`;

// 1. Unknown kind → ok:false. No worktree created.
{
  const env = freshRepoWithRemote({ claudeScript: CLAUDE_NOOP_STUB });
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "bogus-pass", repoDir: env.localDir, taskId: "t1" })
    );
    assert.equal(result.ok, false);
    assert.match(result.reason, /unknown code-pass kind/);
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1, "only the main worktree should exist");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  unknown kind rejected");
}

// 2. Dirty main checkout — must NOT block the pass (the fleet runner always
// has state-file dirt when this executor fires).
{
  const env = freshRepoWithRemote({ claudeScript: CLAUDE_EDIT_STUB });
  // Simulate the task-generator having written state right before us.
  mkdirSync(join(env.localDir, "memory"), { recursive: true });
  writeFileSync(join(env.localDir, "memory/fleet-task-generator-state.json"), `{"lastRun":"2026-05-30T00:00:00Z"}\n`);
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", target: "lib.mjs", repoDir: env.localDir, taskId: "dirty" })
    );
    assert.equal(result.ok, true, `expected success even with dirty main checkout, got ${JSON.stringify(result)}`);
    assert.equal(result.prUrl, "https://github.com/stub/repo/pull/42");
    // The state-file dirt must still be present in the main checkout — we
    // mustn't have touched it.
    assert.ok(existsSync(join(env.localDir, "memory/fleet-task-generator-state.json")),
      "state file should still exist in main checkout");
    const status = git(["status", "--porcelain", "--untracked-files=all", "memory/"], env.localDir).stdout;
    assert.match(status, /fleet-task-generator-state\.json/, "state-file dirt should be untouched");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  dirty main checkout no longer blocks the pass (Codex P1 fix)");
}

// 3. Happy path — claude makes changes → branch + commit + push + PR.
{
  const env = freshRepoWithRemote({ claudeScript: CLAUDE_EDIT_STUB });
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", target: "lib.mjs", repoDir: env.localDir, taskId: "happy-001" })
    );
    assert.equal(result.ok, true, `expected ok=true, got ${JSON.stringify(result)}`);
    assert.equal(result.prUrl, "https://github.com/stub/repo/pull/42");
    assert.match(result.branch, /^aeon\/docs-pass-\d{4}-\d{2}-\d{2}-happy001$/);
    // Branch must exist on remote with the commit.
    const refs = spawnSync("git", ["ls-remote", env.remoteDir], { encoding: "utf8" }).stdout;
    assert.match(refs, new RegExp(`refs/heads/${result.branch}`));
    // Main checkout must be untouched (still on main, lib.mjs unchanged).
    assert.equal(git(["branch", "--show-current"], env.localDir).stdout, "main");
    assert.equal(readFileSync(join(env.localDir, "lib.mjs"), "utf8"), "// initial\n");
    // Worktree must be cleaned up.
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1, "the patch-pass worktree should be removed");
    assert.match(readFileSync(env.ghLog, "utf8"), /pr create --title/);
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  happy path → worktree + branch + commit + push + PR; main untouched");
}

// 4. No-changes path — claude declines to edit anything. No branch on remote,
// no local branch, worktree cleaned up.
{
  const env = freshRepoWithRemote({
    claudeScript: CLAUDE_NOOP_STUB,
    // Allow `gh pr list` (used by the backlog gate) to succeed with an empty
    // list; reject anything else so the test still catches an unintended
    // `gh pr create`.
    ghScript: `#!/usr/bin/env bash\nif [ "$1" = "pr" ] && [ "$2" = "list" ]; then echo "[]"; exit 0; fi\necho "gh should not have been called: $@" >&2\nexit 99\n`,
  });
  try {
    const r1 = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "refactor-pass", repoDir: env.localDir, taskId: "noop-a" })
    );
    const r2 = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "refactor-pass", repoDir: env.localDir, taskId: "noop-b" })
    );
    assert.equal(r1.ok, true);
    assert.equal(r1.prUrl, null);
    assert.equal(r2.ok, true);
    // After two no-op runs, only `main` should remain locally.
    const branches = git(["branch", "--list"], env.localDir).stdout
      .split("\n").map((s) => s.replace(/^\*?\s+/, "").trim()).filter(Boolean);
    assert.deepEqual(branches, ["main"], `unexpected branches after no-op runs: ${branches.join(", ")}`);
    // gh must never have been invoked.
    assert.equal(existsSync(env.ghLog), false, "gh log should not exist (gh never called)");
    // No leftover worktree dirs.
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1, "no patch-pass worktree should remain");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  no-changes path → no PR, no leaked branch, worktree cleaned up");
}

// 5. gh failure — branch on remote stays so an operator can open the PR
// manually, worktree is cleaned up, task fails.
{
  const env = freshRepoWithRemote({
    claudeScript: CLAUDE_EDIT_STUB,
    ghScript: `#!/usr/bin/env bash\necho "simulated gh failure" >&2\nexit 1\n`,
  });
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", repoDir: env.localDir, taskId: "ghfail" })
    );
    assert.equal(result.ok, false);
    assert.match(result.reason, /gh pr create failed/);
    // Worktree gone, but branch is on origin.
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1);
    const refs = spawnSync("git", ["ls-remote", env.remoteDir], { encoding: "utf8" }).stdout;
    assert.match(refs, /aeon\/docs-pass-/, "branch should remain on remote after gh failure");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  gh failure → branch preserved on remote, worktree cleaned up");
}

// 6. Backlog gate — when `gh pr list` reports ≥ BACKLOG_LIMIT open PRs of
// this kind, runCodePass must return ok:true with no PR and never invoke
// claude/git/gh-create.
{
  const env = freshRepoWithRemote({
    // claude stub fails loudly — if the gate doesn't short-circuit, the test
    // will surface that by exiting with a non-zero status from claude.
    claudeScript: `#!/usr/bin/env bash\necho "claude should not have been called" >&2\nexit 77\n`,
    // Three open docs-pass PRs in the listing — matches the default limit.
    ghScript: `#!/usr/bin/env bash\necho "gh: $@" >> "$GH_LOG"\nif [ "$1" = "pr" ] && [ "$2" = "list" ]; then echo '[{"headRefName":"aeon/docs-pass-2026-06-06-aaa"},{"headRefName":"aeon/docs-pass-2026-06-06-bbb"},{"headRefName":"aeon/docs-pass-2026-06-06-ccc"},{"headRefName":"main"}]'; exit 0; fi\necho "https://github.com/stub/repo/pull/42"\n`,
  });
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", target: "lib.mjs", repoDir: env.localDir, taskId: "gated" })
    );
    assert.equal(result.ok, true, `expected ok=true skip, got ${JSON.stringify(result)}`);
    assert.equal(result.prUrl, null);
    assert.match(result.summary, /skipped/i);
    assert.match(result.summary, /backlog/i);
    // No worktree should have been created.
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1, "no worktree should be created when gated");
    // gh was called once (the list), never for create.
    const ghLog = readFileSync(env.ghLog, "utf8");
    assert.match(ghLog, /pr list/);
    assert.doesNotMatch(ghLog, /pr create/);
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  backlog gate skips PR creation when same-kind queue is at limit");
}

// 7. Backlog gate ignores unrelated open PRs — three open PRs of a *different*
// kind must not block a docs-pass run.
{
  const env = freshRepoWithRemote({
    claudeScript: CLAUDE_EDIT_STUB,
    ghScript: `#!/usr/bin/env bash\necho "gh: $@" >> "$GH_LOG"\nif [ "$1" = "pr" ] && [ "$2" = "list" ]; then echo '[{"headRefName":"aeon/refactor-pass-2026-06-06-aaa"},{"headRefName":"aeon/refactor-pass-2026-06-06-bbb"},{"headRefName":"aeon/refactor-pass-2026-06-06-ccc"}]'; exit 0; fi\necho "https://github.com/stub/repo/pull/99"\n`,
  });
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", target: "lib.mjs", repoDir: env.localDir, taskId: "cross" })
    );
    assert.equal(result.ok, true, `expected ok=true PR, got ${JSON.stringify(result)}`);
    assert.equal(result.prUrl, "https://github.com/stub/repo/pull/99");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  backlog gate only counts same-kind PRs");
}

// 8. Claude CLI unavailable (--version exits non-zero) → ok:false, worktree
//    created but cleaned up, ephemeral branch deleted.
{
  const CLAUDE_UNAVAILABLE = `#!/usr/bin/env bash\nif [ "$1" = "--version" ]; then exit 1; fi\ncat > /dev/null\necho "should not reach"\n`;
  const env = freshRepoWithRemote({ claudeScript: CLAUDE_UNAVAILABLE });
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", repoDir: env.localDir, taskId: "unavail" })
    );
    assert.equal(result.ok, false);
    assert.match(result.reason, /claude invocation failed/);
    // Worktree must be cleaned up even though claude never ran.
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1, "no worktree should remain");
    // Ephemeral branch must also be deleted.
    const branches = git(["branch", "--list", "aeon/*"], env.localDir).stdout;
    assert.equal(branches, "", "no aeon/* branch should remain when claude is unavailable");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  claude CLI unavailable → ok:false, worktree and branch cleaned up");
}

// 9. git push failure → commit landed on the local branch but never reached
//    origin. cleanup(false) keeps the branch ref so an operator can push it
//    manually; the worktree is removed.
{
  const env = freshRepoWithRemote({
    claudeScript: CLAUDE_EDIT_STUB,
    // Backlog gate calls `gh pr list` before claude — let it succeed with an
    // empty list so the test exercises the post-push gh-not-called check.
    ghScript: `#!/usr/bin/env bash\nif [ "$1" = "pr" ] && [ "$2" = "list" ]; then echo "[]"; exit 0; fi\necho "gh should not have been called after push failure: $@" >&2\nexit 99\n`,
  });
  // Point origin at a non-existent path to force push failure.
  git(["remote", "set-url", "origin", "/tmp/aeon-bad-remote-nonexistent"], env.localDir);
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "refactor-pass", repoDir: env.localDir, taskId: "pushfail" })
    );
    assert.equal(result.ok, false);
    assert.match(result.reason, /git push failed/);
    // Worktree must be removed.
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1, "no worktree should remain after push failure");
    // Branch ref must survive locally so the commit is not lost.
    const branches = git(["branch", "--list", "aeon/*"], env.localDir).stdout;
    assert.match(branches, /aeon\/refactor-pass-/, "branch should be kept locally after push failure");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  push failure → ok:false, branch kept locally, worktree removed");
}

// 10. git worktree add failure — pre-create the branch that runCodePass would
//     generate so that `git worktree add -b <branch>` fails. The code must
//     return ok:false, clean up the temp dir, and leave no stray worktree.
{
  const today = new Date().toISOString().slice(0, 10);
  const taskId = "wtaddfail";
  const branchName = `aeon/docs-pass-${today}-${taskId.replace(/[^a-zA-Z0-9]/g, "").slice(0, 10)}`;
  const env = freshRepoWithRemote({
    claudeScript: CLAUDE_NOOP_STUB,
    ghScript: `#!/usr/bin/env bash\nif [ "$1" = "pr" ] && [ "$2" = "list" ]; then echo "[]"; exit 0; fi\necho "https://github.com/stub/repo/pull/1"\n`,
  });
  git(["branch", branchName], env.localDir);
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", repoDir: env.localDir, taskId })
    );
    assert.equal(result.ok, false);
    assert.match(result.reason, /git worktree add failed/);
    const worktrees = git(["worktree", "list", "--porcelain"], env.localDir).stdout;
    assert.equal(worktrees.match(/^worktree /gm).length, 1, "no stray worktree should remain");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  worktree add failure (branch already exists) → ok:false, no leaked worktree");
}

// 11. gh pr list failure → null backlog → proceed anyway. When `gh pr list`
//     exits non-zero, openPRsForKind returns null and the gate is skipped so
//     real work still runs (null means "unknown", not "at limit").
{
  const env = freshRepoWithRemote({
    claudeScript: CLAUDE_EDIT_STUB,
    ghScript: `#!/usr/bin/env bash\necho "gh: $@" >> "$GH_LOG"\nif [ "$1" = "pr" ] && [ "$2" = "list" ]; then exit 1; fi\necho "https://github.com/stub/repo/pull/55"\n`,
  });
  try {
    const result = withStubbedEnv(env.binDir, env.ghLog, () =>
      runCodePass({ kind: "docs-pass", target: "lib.mjs", repoDir: env.localDir, taskId: "prlistfail" })
    );
    assert.equal(result.ok, true, `expected ok=true when gh pr list fails, got ${JSON.stringify(result)}`);
    assert.equal(result.prUrl, "https://github.com/stub/repo/pull/55");
  } finally {
    rmSync(env.work, { recursive: true, force: true });
  }
  console.log("OK  gh pr list failure → null backlog → pass proceeds rather than blocking");
}

console.log("\nAll claude-code-pass tests passed.");
