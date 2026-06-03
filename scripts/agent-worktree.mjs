#!/usr/bin/env node
/**
 * agent-worktree — isolate concurrent Claude sessions into their own git
 * worktrees so they stop stepping on each other.
 *
 * The hazard this solves
 *   Multiple `claude` sessions opened in different terminals all share one
 *   working tree. When session A runs `git checkout -b foo` and starts a
 *   commit, session B running `git checkout -b bar` at the same time will
 *   silently change A's HEAD. A's commit then lands on the wrong branch,
 *   and `git push -u origin foo` from A pushes whatever HEAD points to —
 *   often not what A built. Recovery is force-push + cherry-pick.
 *
 *   This script creates a sibling git worktree per session so each Claude
 *   has its own HEAD, index, and untracked files. The shared git object
 *   store keeps fetches/pushes fast and consistent.
 *
 * Commands
 *   ./agent-worktree spawn <name> [--branch <branch>]
 *     Create a new worktree at ../aeon-<name>/ on a new branch
 *     `agent/<name>` (overridable). Prints the cd target.
 *
 *   ./agent-worktree list
 *     Show all worktrees with branch, last commit, and any claude process
 *     that's currently rooted in them.
 *
 *   ./agent-worktree remove <name>
 *     Remove the named worktree (after `git worktree prune`). Refuses if
 *     the working tree has uncommitted changes (override with --force).
 *
 *   ./agent-worktree status
 *     One-line summary: how many worktrees, how many active claudes,
 *     whether any are sharing trees.
 *
 * Layout
 *   Main checkout: <repo>/   (typically ~/aeon/)
 *   Worktrees:     <repo>-<name>/   (sibling directories, e.g. ~/aeon-find/)
 */
import { existsSync, mkdirSync, readdirSync, statSync, rmSync } from "node:fs";
import { resolve, basename, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync, spawnSync } from "node:child_process";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(SCRIPT_DIR, "..");
const REPO_BASENAME = basename(ROOT); // e.g. "aeon"
const PARENT_DIR = dirname(ROOT);     // e.g. "/Users/raelisavitt"

function sh(cmd, args, opts = {}) {
  return spawnSync(cmd, args, { cwd: ROOT, encoding: "utf8", ...opts });
}

function git(args, opts = {}) {
  const r = sh("git", args, opts);
  if (r.status !== 0 && !opts.allowFail) {
    throw new Error(`git ${args.join(" ")} failed (status=${r.status}):\n${r.stderr || r.stdout}`);
  }
  return r;
}

function listWorktrees() {
  // `git worktree list --porcelain` emits stanzas like:
  //   worktree /path
  //   HEAD <sha>
  //   branch refs/heads/<name>
  // separated by blank lines. Parse into objects.
  const out = git(["worktree", "list", "--porcelain"]).stdout;
  const stanzas = out.split("\n\n").filter(Boolean);
  return stanzas.map((s) => {
    const obj = {};
    for (const line of s.split("\n")) {
      const sp = line.indexOf(" ");
      const key = sp >= 0 ? line.slice(0, sp) : line;
      const val = sp >= 0 ? line.slice(sp + 1) : true;
      obj[key] = val;
    }
    return {
      path: obj.worktree,
      head: obj.HEAD,
      branch: typeof obj.branch === "string" ? obj.branch.replace(/^refs\/heads\//, "") : "(detached)",
      bare: obj.bare === true,
      locked: obj.locked === true,
    };
  }).filter((w) => !w.bare);
}

function findClaudeProcesses() {
  // ps -E exposes the working directory? Not portable. Use lsof to find
  // claude processes' cwd; fall back to ps if lsof isn't there.
  const r = sh("ps", ["-Ao", "pid,tty,ppid,stat,pcpu,command"]);
  if (r.status !== 0) return [];
  const lines = r.stdout.split("\n").slice(1);
  const claudes = [];
  for (const line of lines) {
    const m = line.match(/^\s*(\d+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(.+)$/);
    if (!m) continue;
    if (!/(^|\s|\/)claude(\s|$)/.test(m[6])) continue;
    if (/agent-worktree/.test(m[6])) continue; // skip ourselves
    const [, pid, tty, ppid, stat, pcpu, command] = m;
    // lsof to get cwd
    const lr = sh("lsof", ["-a", "-p", pid, "-d", "cwd", "-Fn"], { allowFail: true });
    let cwd = null;
    if (lr.status === 0) {
      for (const ll of lr.stdout.split("\n")) {
        if (ll.startsWith("n")) { cwd = ll.slice(1); break; }
      }
    }
    claudes.push({ pid, tty: tty === "??" ? null : tty, ppid, stat, pcpu: Number(pcpu), command, cwd });
  }
  return claudes;
}

// Return the command line of the process that launched the claude — used to
// detect wrappers like `openclaude` so the migrated session relaunches via
// the same wrapper instead of bare `claude`.
function parentCommandFor(ppid) {
  if (!ppid) return null;
  const r = sh("ps", ["-p", String(ppid), "-o", "command="], { allowFail: true });
  if (r.status !== 0) return null;
  return r.stdout.trim() || null;
}

function detectWrapper(parentCmd) {
  // Recognized cases:
  //   1. `-zsh` / `/bin/zsh`                     → no wrapper (interactive shell)
  //   2. `/bin/sh /usr/bin/command openclaude`   → wrapper = openclaude
  //   3. `openclaude` / `/usr/local/bin/openclaude` → wrapper = openclaude
  //   4. anything else with a last non-flag token → that token
  //
  // The bug a previous revision had: bailing on any parent whose first token
  // looked like a shell. That misfires on case 2 (the documented openclaude
  // shape) because /bin/sh is the interpreter for the wrapper script.
  if (!parentCmd) return null;
  const tokens = parentCmd.trim().split(/\s+/);
  const firstBase = tokens[0].replace(/^-/, "").split("/").pop();
  const isShell = /^(zsh|bash|sh|fish|dash|ksh)$/.test(firstBase);

  // Bare shell invocation (no script being run) → claude was a direct child.
  if (isShell && tokens.length === 1) return null;

  // Shell is running a script: the wrapper is the script, not the shell.
  // Walk backwards skipping flag tokens (-c, --login, etc.) and `command`
  // (the POSIX builtin used to bypass shell functions in some wrappers).
  if (isShell) {
    for (let i = tokens.length - 1; i > 0; i--) {
      const t = tokens[i];
      if (t.startsWith("-")) continue;
      const base = t.split("/").pop();
      if (!base || base === "command") continue;
      if (base === "claude") return null;
      return base;
    }
    return null;
  }

  // Parent isn't a shell — it IS the wrapper (or claude itself).
  const last = tokens[tokens.length - 1].split("/").pop();
  if (!last || last === "claude") return null;
  return last;
}

function cmdSpawn(args) {
  const name = args._[0];
  if (!name) die("usage: agent-worktree spawn <name> [--branch <branch>]");
  if (!/^[a-z0-9][a-z0-9_-]*$/i.test(name)) die("name must be alphanumeric / dash / underscore");
  const branch = args.branch || `agent/${name}`;
  const target = resolve(PARENT_DIR, `${REPO_BASENAME}-${name}`);
  if (existsSync(target)) die(`already exists: ${target}`);

  // Always branch from origin/main so the worktree starts on a clean,
  // up-to-date base regardless of what the main checkout is currently on.
  git(["fetch", "origin", "main", "--quiet"], { allowFail: true });
  git(["worktree", "add", "-b", branch, target, "origin/main"]);

  console.log(`\nCreated worktree:`);
  console.log(`  path:    ${target}`);
  console.log(`  branch:  ${branch}`);
  console.log(`  base:    origin/main`);
  console.log(`\nNext steps:`);
  console.log(`  cd ${target}`);
  console.log(`  claude   # this Claude session is now isolated from the others`);
}

function cmdList() {
  const worktrees = listWorktrees();
  const claudes = findClaudeProcesses();
  // group claudes by which worktree they belong to (longest matching path prefix)
  const wByPath = worktrees.map((w) => ({ ...w, claudes: [] }));
  for (const c of claudes) {
    if (!c.cwd) continue;
    const match = wByPath
      .filter((w) => c.cwd === w.path || c.cwd.startsWith(w.path + "/"))
      .sort((a, b) => b.path.length - a.path.length)[0];
    if (match) match.claudes.push(c);
  }

  const here = ROOT;
  console.log(`${wByPath.length} worktree(s):\n`);
  for (const w of wByPath) {
    const marker = w.path === here ? " ← here" : "";
    console.log(`  ${w.path}${marker}`);
    console.log(`    branch:  ${w.branch}`);
    console.log(`    head:    ${(w.head || "").slice(0, 12)}`);
    if (w.claudes.length > 0) {
      console.log(`    claude:  ${w.claudes.map((c) => `pid ${c.pid}`).join(", ")}`);
    }
    console.log();
  }

  // surface the hazard if any worktree has >1 claude
  const shared = wByPath.filter((w) => w.claudes.length > 1);
  if (shared.length > 0) {
    console.log(`⚠  ${shared.length} worktree(s) have more than one claude attached — sessions will step on each other:`);
    for (const w of shared) console.log(`     ${w.path}: ${w.claudes.length} claudes`);
    console.log(`   Spawn isolated worktrees with: ./agent-worktree spawn <name>`);
  }
}

function cmdRemove(args) {
  const name = args._[0];
  if (!name) die("usage: agent-worktree remove <name> [--force]");
  const target = resolve(PARENT_DIR, `${REPO_BASENAME}-${name}`);
  if (!existsSync(target)) die(`no such worktree: ${target}`);

  // Refuse if there are uncommitted changes — losing those silently is the
  // whole class of bug this script exists to prevent.
  if (!args.force) {
    const status = git(["status", "--porcelain"], { cwd: target }).stdout.trim();
    if (status) {
      console.error(`Refusing to remove: worktree has uncommitted changes.\n${status}\n\nCommit, stash, or pass --force.`);
      process.exit(1);
    }
  }

  git(["worktree", "remove", target, ...(args.force ? ["--force"] : [])]);
  git(["worktree", "prune"]);
  console.log(`Removed: ${target}`);
}

// ── iTerm2 control (macOS + iTerm2 only) ─────────────────────────────────
function osascript(script) {
  return spawnSync("osascript", ["-"], { input: script, encoding: "utf8" });
}

function itermAvailable() {
  if (process.platform !== "darwin") return false;
  const r = osascript('tell application "System Events" to (name of processes) contains "iTerm2"');
  return r.status === 0 && r.stdout.trim() === "true";
}

// List iTerm sessions: [{ tty, isProcessing }]
function itermSessions() {
  const r = osascript(`
    tell application "iTerm2"
      set out to ""
      repeat with w in windows
        repeat with t in tabs of w
          repeat with s in sessions of t
            set out to out & (tty of s) & "|" & (is processing of s) & linefeed
          end repeat
        end repeat
      end repeat
      return out
    end tell
  `);
  if (r.status !== 0) return [];
  return r.stdout.split("\n").filter(Boolean).map((line) => {
    const [tty, busy] = line.split("|");
    return { tty, isProcessing: busy === "true" };
  });
}

// Send a line of text to the iTerm session whose tty matches. `withReturn`
// controls whether the line is followed by Enter — true for commands, false
// for raw control chars (escape).
function itermSendLine(tty, text, withReturn = true) {
  const escaped = text.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  const newlineArg = withReturn ? "" : " newline NO";
  const script = `
    tell application "iTerm2"
      repeat with w in windows
        repeat with t in tabs of w
          repeat with s in sessions of t
            if tty of s is "${tty}" then
              tell s to write text "${escaped}"${newlineArg}
              return "ok"
            end if
          end repeat
        end repeat
      end repeat
      return "not_found"
    end tell
  `;
  return osascript(script).stdout.trim() === "ok";
}

// Send a raw escape character (ASCII 27) — used to dismiss permission
// prompts / modals inside claude before sending /exit.
function itermSendEscape(tty) {
  const script = `
    tell application "iTerm2"
      repeat with w in windows
        repeat with t in tabs of w
          repeat with s in sessions of t
            if tty of s is "${tty}" then
              tell s to write text (ASCII character 27) newline NO
              return "ok"
            end if
          end repeat
        end repeat
      end repeat
      return "not_found"
    end tell
  `;
  return osascript(script).stdout.trim() === "ok";
}

// Poll until the iTerm session's `is processing` flag matches `wanted` or
// the timeout expires. Returns true on success, false on timeout.
function waitForItermBusy(tty, wanted, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const sessions = itermSessions();
    const s = sessions.find((x) => x.tty === tty);
    if (!s) return false;
    if (s.isProcessing === wanted) return true;
    // synchronous wait — small busy-loop is fine for this scale
    const until = Date.now() + 200;
    while (Date.now() < until) { /* spin */ }
  }
  return false;
}

// Poll until a claude process appears with the given cwd or timeout expires.
function waitForClaudeIn(cwd, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const claudes = findClaudeProcesses();
    if (claudes.some((c) => c.cwd && (c.cwd === cwd || c.cwd.startsWith(cwd + "/")))) return true;
    const until = Date.now() + 300;
    while (Date.now() < until) { /* spin */ }
  }
  return false;
}

function cmdMigrate(args) {
  // Usage: agent-worktree migrate <tty> [<name>]
  // Default <name> is <tty> (so `migrate s002` → worktree `aeon-s002`).
  const ttyArg = args._[0];
  if (!ttyArg) die("usage: agent-worktree migrate <tty> [<name>] [--force]");
  // Accept any of: `s007`, `ttys007`, `/dev/ttys007`. Normalize to /dev/ttys007.
  const bare = ttyArg.replace(/^\/dev\//, "").replace(/^tty/, "");
  const tty = `/dev/tty${bare}`;
  const name = args._[1] || bare;
  if (!/^[a-z0-9][a-z0-9_-]*$/i.test(name)) die(`bad worktree name derived from tty: ${name}`);

  if (!itermAvailable()) die("migrate requires macOS + iTerm2 running");

  // Find the claude in that tty.
  const claudes = findClaudeProcesses();
  const target = claudes.find((c) => c.tty === tty.replace(/^\/dev\//, ""));
  if (!target) die(`no claude process found on ${tty}`);

  // Refuse to interrupt actively-busy sessions. ps STAT=R or pcpu > 5%
  // is a strong "doing work" signal. iTerm's `is processing` can be
  // misleading (true at permission prompts) so we treat it as advisory.
  const isActive = target.stat.startsWith("R") || target.pcpu > 5;
  if (isActive && !args.force) {
    die(`session on ${tty} looks actively working (stat=${target.stat} cpu=${target.pcpu}%). Pass --force to interrupt it anyway.`);
  }

  // Ensure the destination worktree exists; spawn if missing.
  const dest = resolve(PARENT_DIR, `${REPO_BASENAME}-${name}`);
  if (!existsSync(dest)) {
    console.log(`destination worktree missing, spawning: ${dest}`);
    git(["fetch", "origin", "main", "--quiet"], { allowFail: true });
    git(["worktree", "add", "-b", `agent/${name}`, dest, "origin/main"]);
  }

  // Detect whether the claude was launched via a wrapper script (e.g.
  // openclaude). When the migrated session restarts, use the same wrapper
  // so the launch path is consistent — and so the user doesn't suddenly
  // get raw claude when their muscle memory expects the wrapper UI.
  const parentCmd = parentCommandFor(target.ppid);
  const wrapper = detectWrapper(parentCmd);
  const launchCmd = wrapper || "claude";
  if (wrapper) console.log(`detected wrapper: ${wrapper}`);

  // Step 1: send Escape to dismiss any open modal/permission prompt.
  console.log(`→ ${tty}: escape (dismiss any modal)`);
  itermSendEscape(tty);
  const slowSleep = (ms) => { const u = Date.now() + ms; while (Date.now() < u) {} };
  slowSleep(400);

  // Step 2: tell claude to exit. We don't wait for /exit to take effect via
  // is-processing (claude can leave it set during shutdown); instead, poll
  // until the claude PID is gone from the process table.
  console.log(`→ ${tty}: /exit`);
  itermSendLine(tty, "/exit");

  const deadline = Date.now() + 8000;
  let claudeGone = false;
  while (Date.now() < deadline) {
    const stillThere = findClaudeProcesses().some((c) => c.pid === target.pid);
    if (!stillThere) { claudeGone = true; break; }
    slowSleep(300);
  }
  if (!claudeGone) {
    console.error(`claude (pid ${target.pid}) did not exit within 8s — aborting; check the session and try again`);
    process.exit(1);
  }

  // Step 3: the shell beneath claude (or beneath any wrapper) should now be
  // back at a prompt. iTerm should report `is processing` = false. If a
  // wrapper exited along with claude, the shell needs a beat to settle.
  console.log(`→ ${tty}: waiting for shell prompt…`);
  const shellReady = waitForItermBusy(tty, false, 5000);
  if (!shellReady) {
    console.error(`shell on ${tty} still busy after 5s — sending commands anyway, you may need to clean up`);
  }
  slowSleep(300);

  // Step 4: cd + relaunch.
  console.log(`→ ${tty}: cd ${dest}`);
  itermSendLine(tty, `cd ${dest}`);
  slowSleep(400);
  console.log(`→ ${tty}: ${launchCmd}`);
  itermSendLine(tty, launchCmd);

  // Step 5: verify a new claude attached to the worktree.
  console.log(`→ ${tty}: waiting for new claude to attach to ${dest}…`);
  const attached = waitForClaudeIn(dest, 15000);
  if (!attached) {
    console.error(`no claude detected in ${dest} within 15s. The migration may have stalled; check the terminal.`);
    process.exit(1);
  }

  // Success — find the new pid for the report.
  const newClaude = findClaudeProcesses().find((c) => c.cwd && (c.cwd === dest || c.cwd.startsWith(dest + "/")));
  console.log(`\n✓ migrated ${tty}: pid ${target.pid} → pid ${newClaude.pid}`);
  console.log(`  worktree: ${dest}`);
  console.log(`  branch:   agent/${name}`);
}

function cmdStatus() {
  const worktrees = listWorktrees();
  const claudes = findClaudeProcesses();
  const sharedTrees = new Set();
  const byTree = new Map();
  for (const c of claudes) {
    if (!c.cwd) continue;
    const match = worktrees
      .filter((w) => c.cwd === w.path || c.cwd.startsWith(w.path + "/"))
      .sort((a, b) => b.path.length - a.path.length)[0];
    if (!match) continue;
    if (!byTree.has(match.path)) byTree.set(match.path, []);
    byTree.get(match.path).push(c);
  }
  for (const [path, cs] of byTree) if (cs.length > 1) sharedTrees.add(path);

  console.log(`${worktrees.length} worktree(s), ${claudes.length} claude process(es)`);
  if (sharedTrees.size > 0) {
    console.log(`⚠  ${sharedTrees.size} worktree(s) shared by >1 claude — concurrency hazard active`);
    process.exit(1);
  } else if (claudes.length > 0) {
    console.log(`✓ each claude is in its own worktree`);
  }
}

function die(msg) { console.error(msg); process.exit(2); }

function parseArgv(argv) {
  const opts = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--branch") opts.branch = argv[++i];
    else if (a === "--force") opts.force = true;
    else if (a === "-h" || a === "--help") opts.help = true;
    else opts._.push(a);
  }
  return opts;
}

function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const args = parseArgv(rest);
  if (!cmd || args.help) {
    console.log(
      `Usage: agent-worktree <command> [args]\n` +
      `\n` +
      `Commands:\n` +
      `  spawn <name>             Create a sibling worktree at ../${REPO_BASENAME}-<name>/\n` +
      `  list                     Show all worktrees with claude processes attached\n` +
      `  status                   One-line summary, exits 1 if any worktree has >1 claude\n` +
      `  migrate <tty> [<name>]   Move a running claude on <tty> into a worktree (macOS + iTerm2)\n` +
      `  remove <name>            Remove a worktree (refuses if dirty; --force overrides)\n`,
    );
    return;
  }
  switch (cmd) {
    case "spawn":   return cmdSpawn(args);
    case "list":    return cmdList(args);
    case "status":  return cmdStatus(args);
    case "migrate": return cmdMigrate(args);
    case "remove":  return cmdRemove(args);
    default: die(`unknown command: ${cmd}`);
  }
}

main();
