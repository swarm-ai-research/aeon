# Agent Worktrees

When you run multiple `claude` sessions in different terminals against the same checkout, they share one working tree. One session's `git checkout -b foo` will silently change another session's `HEAD`, so a commit started by session A can land on session B's branch and a subsequent `git push -u origin foo` pushes the wrong content. Recovery is force-push + cherry-pick.

This is a real hazard — it cost three force-pushes in a single session that landed PRs #71, #72, #73, and #77 (May 2026). The fix is one git worktree per Claude session.

## Quick reference

```bash
./agent-worktree spawn  <name>           # create ../aeon-<name>/ on branch agent/<name>
./agent-worktree list                    # show all worktrees + their claude PIDs
./agent-worktree status                  # exit 1 if any worktree has >1 claude
./agent-worktree migrate <tty> [<name>]  # move a running claude into its worktree (macOS + iTerm2)
./agent-worktree remove <name>           # tear down (refuses if dirty)
```

## Recommended pattern for multi-session work

```bash
# Terminal A
./agent-worktree spawn feature-x
cd ../aeon-feature-x
claude

# Terminal B (in parallel, doing unrelated work)
./agent-worktree spawn bugfix
cd ../aeon-bugfix
claude
```

Each session gets its own `HEAD`, index, and untracked files. The git object store is shared so `git fetch` updates both, and pushes from either go to the same remote.

## Migrating an existing session

`migrate <tty>` drives iTerm2 via AppleScript to end a running claude on a given tty and relaunch it inside its worktree. macOS + iTerm2 only.

```bash
./agent-worktree migrate s002          # → ../aeon-s002/
./agent-worktree migrate s002 hotfix   # → ../aeon-hotfix/
./agent-worktree migrate s003 --force  # interrupt even if it looks busy
```

What it does, in order:

1. Looks up the claude process on the given tty. Errors out if there isn't one.
2. Refuses if the process appears to be actively working (`stat=R*` or CPU > 5%). Pass `--force` to override.
3. Detects whether claude was launched via a wrapper (e.g. `openclaude`) — relaunches via the same wrapper afterward.
4. Sends ESC to dismiss any open permission prompt / modal.
5. Sends `/exit` and waits up to 8 s for the claude PID to disappear from `ps`.
6. Waits for iTerm to report the session is no longer busy (the shell is at a prompt).
7. Sends `cd <worktree>` then the relaunch command.
8. Waits up to 15 s for a new claude to appear with the new cwd.

It's **destructive**: the running conversation ends. `claude --continue` on the other side won't recover it because conversation history is per-working-directory and the new directory has none. Use `spawn` + manual move for sessions you want to preserve context for.

## When to use

- **Always** for parallel interactive Claude sessions in this repo
- Optional for short-lived single-purpose work (one session in the main tree is fine)
- Not needed for CI runs — GitHub Actions gets its own ephemeral checkout per job

## When the autonomous fleet runs locally

The fleet executors (`scripts/fleet-executors/*.mjs`) read `GITLAWB_REPO_DIR` to choose their working directory. If you ever invoke them locally (rather than via GitHub Actions), point that env var at a worktree:

```bash
./agent-worktree spawn fleet-local
GITLAWB_REPO_DIR=$PWD/../aeon-fleet-local node scripts/fleet-executors/researcher.mjs
```

Otherwise the executor runs in your main checkout and competes with whatever your interactive Claude session is doing.

## Cleanup

Worktrees on long-dead branches accumulate. `./agent-worktree list` shows what exists; `./agent-worktree remove <name>` tears down a specific one. Git's `git worktree prune` is run automatically after each `remove`.

The script refuses to remove a worktree with uncommitted changes — losing those silently is exactly the class of bug this tool exists to prevent. Pass `--force` if you really mean it.

## Implementation notes

- New worktrees branch from `origin/main` so they start on a clean, up-to-date base regardless of what the main checkout's `HEAD` currently is.
- The shared git object store keeps fetches and disk usage cheap; you're not duplicating history.
- The script identifies claude processes via `ps` + `lsof -d cwd` to map PID → working directory. Caveat: `lsof` may need permissions on some setups; if a claude shows no `cwd`, it's not your tool's fault.
- The script never modifies your shell — `spawn` prints a `cd` target, but you run the `cd` yourself.
