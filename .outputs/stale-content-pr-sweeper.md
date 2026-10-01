## Summary — stale-content-pr-sweeper

Ran `skills/stale-content-pr-sweeper/SKILL.md` at 2026-10-01. The skill executed faithfully with its current (unpatched) filters: 48 open PRs → **0 eligible → 0 closes → no notify** (steady-state silent exit).

**Why zero:**
- `ALLOWED_AUTHORS = {"aeonframework"}` filters out all 21 PRs on tracked prefixes — every open PR is authored by `app/github-actions` (the GitHub App identity, not the user identity).
- `TRACKED` list omits `compute-macro` and `skill-graph`, which are the actual branch prefixes used in production.
- Combined, both filters drop all 48 open PRs. This is the n=5 confirmation of the known no-op bug per `[[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]]` + `[[stale-content-pr-sweeper-tracked-prefix-drift]]`.

**Files modified:** `memory/logs/2026-10-01.md` (new).

**Follow-ups (unchanged, already on action queue at `MEMORY.md:52`):** patch SKILL.md — add `"app/github-actions"` to `ALLOWED_AUTHORS` and add `compute-macro` + `skill-graph` to `TRACKED`. Under the patched skill, 30 PRs would close in one sweep (survivors #82 / #81 / #83 / #84; stale: 9 notegraph + 10 suggest-edges + 4 compute-macro + 7 skill-graph), all past the 2-day min-age gate. Did not apply the patch — this invocation was execute, not patch.
