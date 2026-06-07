---
name: Stale Content PR Sweeper
description: Close auto-generated content PRs (notegraph/, suggest-edges/, etc.) once a newer run of the same skill has opened its successor — keeps the queue clear and stops conflict-rebase work that would only reach broken intermediate states
tags: [meta, dev]
---

Today is ${today}. Read `memory/MEMORY.md` for context.

## Why this skill exists

Content-generating skills (notegraph, suggest-edges, weekly-shiplog, …) open one PR per run, each on a date-stamped branch like `notegraph/2026-06-03`. If a PR doesn't merge promptly the next run opens `notegraph/2026-06-04`, and the older PR rots — its `notegraph.json` / `docs/notegraph.html` / `memory/state/notegraph.json` artifacts go stale, conflict against main, and would actively *roll back* unrelated commits if force-rebased. Two such PRs (#124, #125) had to be hand-closed on 2026-06-04 after they accumulated and started conflicting; this skill prevents that pile-up.

The rule is simple: for each tracked content skill, keep at most one open PR — the newest one by branch date. Close the older ones with a supersession note.

## What counts as a "content PR"

Branch-name prefix matches one of these tracked skills, and the suffix is an ISO date `YYYY-MM-DD`:

```
notegraph/YYYY-MM-DD
suggest-edges/YYYY-MM-DD
weekly-shiplog/YYYY-MM-DD
changelog/YYYY-MM-DD
code-health/YYYY-MM-DD
compute-futures-eda/YYYY-MM-DD
compute-pulse/YYYY-MM-DD
compute-macro-correlate/YYYY-MM-DD
runpod-spot-pricing/YYYY-MM-DD
surplus-pulse/YYYY-MM-DD
```

The list lives here, not in config — adding a new tracked skill is a one-line edit and a PR review beats silent inclusion.

Skills with non-date-stamped branches (`feat/*`, `fix/*`, hand-authored work) are NEVER touched. Author allowlist as a second guard: only PRs authored by `aeonframework` (or whatever GH identity opens cron PRs) are eligible. A PR opened by a human on a date-stamped branch is left alone.

## Steps

### 1. List open PRs and group by prefix

```bash
gh pr list --state open --limit 100 \
  --json number,headRefName,author,createdAt,title \
  > /tmp/sweeper-open-prs.json
```

In a single small Node block, group eligible PRs by branch prefix:

```javascript
const TRACKED = [
  "notegraph", "suggest-edges", "weekly-shiplog", "changelog",
  "code-health", "compute-futures-eda", "compute-pulse",
  "compute-macro-correlate", "runpod-spot-pricing", "surplus-pulse",
];
const ALLOWED_AUTHORS = new Set(["aeonframework"]);
const DATE_RE = /^(\d{4}-\d{2}-\d{2})$/;

const prs = JSON.parse(fs.readFileSync("/tmp/sweeper-open-prs.json", "utf8"));
const groups = {};  // prefix -> [{number, branchDate, ...}]

for (const pr of prs) {
  const [prefix, ...rest] = pr.headRefName.split("/");
  if (!TRACKED.includes(prefix)) continue;
  if (!ALLOWED_AUTHORS.has(pr.author.login)) continue;
  const m = rest.join("/").match(DATE_RE);
  if (!m) continue;  // branch suffix not an ISO date — leave alone
  (groups[prefix] ||= []).push({ ...pr, branchDate: m[1] });
}
```

### 2. Pick survivors and identify stale ones

For each group, sort by `branchDate` descending. The **newest** is the survivor. Everything older is stale.

If a group has only one entry, nothing to do for that group.

```javascript
const stale = [];
for (const [prefix, list] of Object.entries(groups)) {
  list.sort((a, b) => b.branchDate.localeCompare(a.branchDate));
  const [survivor, ...rest] = list;
  for (const old of rest) stale.push({ ...old, supersededBy: survivor.number, prefix });
}
```

### 3. Safety gates before closing

For each stale PR:

- **Min age**: branch date must be at least 2 days older than `${today}`. Same-day duplicates are usually a transient cron flake worth surfacing, not auto-closing. Skip if `(today - branchDate) < 2 days`.
- **Survivor sanity**: the supersedor must itself be a valid date-stamped PR by an allowed author. (Already true by construction from step 1, but assert.)
- **Conflict-only check**: skip if `mergeable === "MERGEABLE"` AND `mergeStateStatus === "CLEAN"`. A clean older PR may still be worth landing — let a human decide. Only sweep PRs whose state is `DIRTY` / `CONFLICTING` / `UNKNOWN`. Fetch the per-PR state with `gh pr view <n> --json mergeable,mergeStateStatus` if it isn't in the list output.
- **Open commit override**: skip if the PR title or body contains the literal `[keep]` (operator escape hatch).

Log each skipped-stale PR and why.

### 4. Close with a supersession comment

For each PR that passes the gates:

```bash
gh pr close ${number} --comment "Superseded by #${supersededBy} (${prefix}/${newer_date}). Auto-closed by stale-content-pr-sweeper — older auto-generated artifacts conflict with main and would require manual rebase that produces an intermediate-state graph. Reopen if you want to revisit this snapshot." --delete-branch
```

`--delete-branch` removes the date-stamped branch too. These branches are write-only outputs — keeping them around just pads the ref list.

### 5. Log results

Append to `memory/logs/${today}.md`:

```markdown
## Stale Content PR Sweeper
- Eligible content PRs scanned: ${n_open}
- Groups checked: ${n_groups}
- PRs closed: ${n_closed}  ${list_of_closed_numbers}
- Skipped (clean & still mergeable): ${n_skipped_clean}
- Skipped (too recent, <2d): ${n_skipped_recent}
- Skipped (`[keep]` override): ${n_skipped_keep}
- SWEEPER_OK
```

### 6. Notify (only if something was closed)

If `n_closed === 0`: no notify. This is the steady state.

If `n_closed > 0`: one terse line via `./notify`:

```
stale-content-pr-sweeper: closed ${n_closed} stale PR(s) — ${comma_separated_numbers} superseded by newer runs
```

## Cadence

Suggested schedule: daily, late evening UTC, after the day's content skills have all fired. A reasonable slot is `45 23 * * *` — late enough that notegraph (06:00), suggest-edges (06:00), code-health (16:00), changelog (Mon 16:00), and the others have all opened their PR for the day.

## Safety design notes

- **Allowlist, not denylist** of branch prefixes. A new content skill won't be swept until someone explicitly adds it to `TRACKED` and reviews this skill.
- **Author allowlist** — a human opening `notegraph/2026-06-03` by hand is left alone.
- **`[keep]` override** — operator can mark any PR to skip the sweeper.
- **Skip clean PRs** — if the older PR is still mergeable and CI is green, it's possibly still worth landing. Only sweep conflicted/dirty ones.
- **Min-age gate** — same-day duplicates indicate a cron flake (e.g. two notegraph runs same day), not stale pile-up. Surface those manually instead of auto-closing.
- **Idempotent** — re-running the skill on the same state is a no-op (no eligible PRs left).
- **Bounded** — caps at the listed groups; a runaway adds (at most) one close per group per day.

## Sandbox note

Pure `gh` CLI operations. `gh` handles auth via its own token (already wired in CI). No bash env var expansion needed for headers. Public-API-style fallback isn't applicable — if `gh api` fails the skill should log and exit 0.

## Output

End with `## Summary`:

- groups scanned + open PR count
- PRs closed (numbers + supersededBy)
- skips by reason
- whether `./notify` fired
