# Memory Checkpoints

Git-backed checkpoint/versioning for `memory/`, ported from
[fabro-checkpoint](https://github.com/fabro-sh/fabro)'s branch-per-run model
(hxmp.5). Lets you roll the agent's memory back to any prior run and fork a new
line of work from a known-good snapshot.

## Model

- Every checkpoint is a commit on a dedicated **`aeon-checkpoints`** branch whose
  tree contains **only `memory/`**. This keeps the checkpoint history isolated
  from `main` and grows it monotonically — one commit per run.
- Each checkpoint also gets a human-readable **tag**: `aeon/ckpt/<utc>-<skill>`.
  The tags are the per-run markers `list`/`prune` operate on; the branch is the
  durable store beneath them.
- Provenance lives in **commit trailers**, so it survives `git log` and rebases:

  ```
  Aeon-Run-At: 2026-06-27T02:30:39Z
  Aeon-Skill:  heartbeat
  Aeon-Run-Id: 12345678
  Aeon-Run-Url: https://github.com/<owner>/aeon/actions/runs/12345678
  Aeon-Parent: f8e307b
  ```

## CLI

```bash
scripts/memory-checkpoint.sh create [--skill NAME] [--run-id ID] [--run-url URL] [--no-tag]
scripts/memory-checkpoint.sh list [-n N]
scripts/memory-checkpoint.sh show <ref>
scripts/memory-checkpoint.sh rollback <ref> [--force]
scripts/memory-checkpoint.sh fork <ref> <new-branch> [--base BRANCH]
scripts/memory-checkpoint.sh prune --keep N
```

`<ref>` is a checkpoint tag, a commit sha, or an offset against the branch
(e.g. `@{2}`). `create` is idempotent — if `memory/` is unchanged since the last
checkpoint it no-ops.

### Examples

```bash
# Snapshot current memory state
scripts/memory-checkpoint.sh create --skill reflect

# See recent checkpoints
scripts/memory-checkpoint.sh list

# Inspect one (provenance + what memory files changed vs its parent)
scripts/memory-checkpoint.sh show aeon/ckpt/20260627T0230Z-reflect

# Roll memory/ back to a prior run (stages the change; commit to keep it)
scripts/memory-checkpoint.sh rollback aeon/ckpt/20260627T0230Z-reflect

# Fork: a new branch = main with memory/ swapped to a checkpoint
scripts/memory-checkpoint.sh fork aeon/ckpt/20260627T0230Z-reflect experiment-a

# Keep only the 200 newest checkpoint tags
scripts/memory-checkpoint.sh prune --keep 200
```

`rollback` refuses to run if `memory/` has uncommitted changes (pass `--force`
to override). It materializes the checkpoint's tree exactly, so files added
since the checkpoint are removed.

## CI integration

The `aeon.yml` workflow has an opt-in **Checkpoint memory** step that runs after
a successful skill run commits its memory changes. Enable it by setting the
repository (or org) variable:

```bash
gh variable set AEON_MEMORY_CHECKPOINTS --body true
```

When enabled, each run creates a checkpoint with full run provenance and pushes
the `aeon-checkpoints` branch plus its new tag to origin. The step is
`continue-on-error`, so a checkpoint failure never fails an otherwise-good run.

To bound growth over time, run `prune --keep N` periodically (e.g. from a
maintenance skill) and `git gc` to reclaim space.
