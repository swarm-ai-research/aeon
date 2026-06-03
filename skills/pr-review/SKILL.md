---
name: PR Review
description: Auto-review open PRs with severity-tagged findings, inline comments, and a one-line verdict
var: ""
tags: [dev]
---
<!-- autoresearch: variation B — sharper output: severity-tagged & capped findings, inline comments on exact lines, one-line verdict; folds in skip rules (A) and SHA dedup + large-diff fallback (C) -->

> **${var}** — Repo scope plus optional operator policy. If `${var}` is multiline, treat the first non-empty line as the repo selector (`owner/repo` or `owner/repo#N`) and treat the remaining lines as additional review policy that overrides the default verdict wording.

Read `memory/MEMORY.md` and `memory/watched-repos.md`.
Read the last 2 days of `memory/logs/` to pull the `headRefOid` of any PR reviewed recently — used for dedup.
If present, read these optional review-context files before reviewing:
- `memory/topics/pr-review-rules.md` — fleet-wide review rules and standards
- `memory/topics/pr-review-rules/<owner>__<repo>.md` — repo-specific review rules, architecture notes, and merge gates

## Variable handling

- If `${var}` is empty, review every repo in `memory/watched-repos.md`.
- If `${var}` is a single line, use it as the repo selector.
- If `${var}` is multiline:
  - First non-empty line: repo selector.
  - Remaining lines: operator policy. Apply it when deciding the final verdict and when wording the summary review.
- If the operator policy defines custom verdict labels such as `APPROVE`, `REQUEST_CHANGES`, and `BLOCK`, use those exact labels in the review body.
- If the selector is `owner/repo#N`, review only that PR number in that repo.

If `memory/watched-repos.md` is empty or missing, log `PR_REVIEW_NO_REPOS` and end.

## What this skill optimizes for

Noise is the documented failure mode of automated PR review. Every finding emitted must be severity-tagged, line-specific, and justified with a one-sentence "why it matters". If there is nothing worth saying, say so in one line and move on.

## For each repo

```bash
gh pr list -R owner/repo --state open --limit 20 \
  --json number,title,author,isDraft,labels,headRefOid,updatedAt
```

### Skip rules

Skip a PR if any of the following hold (record the skip reason for the run summary):

- `isDraft: true`
- title matches `^(WIP|\[WIP\]|Draft:)` (case-insensitive)
- has label `no-review`, `do-not-merge`, `wip`, or `blocked`
- author login contains `[bot]` (dependabot, renovate, etc.) or equals `aeonframework`
- this PR's current `headRefOid` already appears in the last 2 days of `memory/logs/` against the same PR (already reviewed at this commit)
- a bot reviewer (`coderabbitai`, `copilot-pull-request-reviewer`, `claude`) posted a review in the last 30 min — skip to avoid piling on. Check via:
  ```bash
  gh api repos/owner/repo/pulls/NUMBER/reviews --jq '.[] | {user: .user.login, submitted_at}'
  ```

### For each remaining PR

1. **Fetch context**:
   ```bash
   gh pr view NUMBER -R owner/repo \
     --json title,body,headRefOid,baseRefName,files,additions,deletions,statusCheckRollup
   ```
   If the `body` contains `Fixes #N` or `Closes #N`, fetch the linked issue for context:
   ```bash
   gh issue view N -R owner/repo --json title,body,labels
   ```

   Also inspect the PR checks before deciding the verdict:
   - Identify whether type checks, tests, lint, formatting, build, and repo-specific quality gates are present in `statusCheckRollup`.
   - Treat names like `typecheck`, `pyright`, `mypy`, `tsc`, `ruff`, `eslint`, `pytest`, `unit`, `integration`, `build`, `check`, `quality`, `smoke`, and `validate` as high-signal quality checks.
   - If a relevant check is failing, timed out, cancelled, or missing for the touched surface area, factor that into the review even if the diff looks small.
   - Build a short **evidence summary** for yourself: which high-signal checks passed, which failed, and which are missing.

2. **Expand context beyond the diff**:
   - For the 1-3 highest-risk changed files, inspect adjacent code before finalizing findings:
     - direct imports / dependencies used by the changed code
     - obvious callers or entrypoints affected by the change
     - nearby tests covering the touched behavior
     - config / schema / CLI / workflow files that control the changed path
   - Prefer repo-native evidence over speculation. If you cannot verify an important assumption from surrounding code or checks, call out the missing evidence explicitly.

3. **Fetch the diff**:
   ```bash
   gh pr diff NUMBER -R owner/repo
   ```
   - If `additions + deletions > 3000`, review only the top-5 largest-delta files from the `files` array (not the full diff).
   - If `gh pr diff` fails, fall back to per-file patches:
     ```bash
     gh api repos/owner/repo/pulls/NUMBER/files --jq '.[] | {path, patch}'
     ```
   - If the diff comes back empty (e.g. mid-rebase), skip the PR with reason `empty-diff`.

4. **Early-exit for trivial PRs**: if the diff is docs-only (`.md`/`.rst`/`docs/**`), lockfile-only, or test-only, skip deep review and post the 1-line ack form in step 6 only after confirming there is no failing type-check / lint / build / quality signal that still needs to be called out.

5. **Review with severity tagging**. Every finding must carry exactly one tag:
   - `[CRITICAL]` — correctness break, security hole, data loss, API break, regression
   - `[ISSUE]` — likely bug, missing edge case, wrong behavior under a realistic input
   - `[NIT]` — naming, style, minor cleanup (dropped by default)

   Rules:
   - Cap at **5 findings total** per PR. Drop NITs first, then the lowest-impact ISSUEs.
   - Drop all NITs unless there are zero CRITICAL/ISSUE findings *and* a NIT is genuinely useful.
   - Every finding must name `path/to/file:LINE` and include a one-sentence "why it matters" — the consequence, not just "this is wrong".
   - No praise, no diff restating, no "this PR adds X" summaries.
   - Prefer **cross-file / cross-boundary findings** over local style comments: broken callers, mismatched contracts, missing validation, untested wiring, stale config, or behavior unsupported by surrounding code.
   - Be conservative about **type safety and quality gates**:
     - Missing or failing type-check coverage on changed typed code (`ts/tsx`, `py` with mypy/pyright, etc.) is at least `[ISSUE]`.
     - Missing or failing lint / repo-quality checks on changed production code is at least `[ISSUE]`.
     - If the PR changes build plumbing, dependency wiring, CLI entrypoints, or framework config, lack of a matching build/validation signal is an `[ISSUE]` unless the PR body clearly explains why no such check exists.
     - If a quality signal already proves a concrete correctness or safety break, escalate to `[CRITICAL]` when the failure implies broken main-branch behavior rather than just incomplete evidence.
   - Suppress low-value nitpicks:
     - Do not comment on formatting, import ordering, naming preference, or micro-style unless it creates a real correctness, readability, or maintenance hazard.
     - If a stronger bug/reliability finding exists in the same file, drop weaker style commentary entirely.

6. **Determine a verdict**:
   - Default mapping:
     - `approve-ready` — no CRITICAL, no ISSUE
     - `blocked: <one-phrase reason>` — at least one CRITICAL
     - `discussion-needed` — ISSUE findings but no CRITICAL
   - If operator policy defines a custom decision policy, follow it instead of the default wording.
   - For the common merge-gate policy, map:
     - `APPROVE` — risk is low and evidence is sufficient
     - `REQUEST_CHANGES` — important test coverage, type-check evidence, or reliability/quality safeguards are missing, but no critical break is present
     - `BLOCK` — any critical security or correctness risk is present
   - Never emit `APPROVE` when the touched surface lacks convincing type-check / lint / test / build evidence appropriate to the change.
   - Also assign a **merge confidence score** from `0/5` to `5/5`:
     - `5/5` — strong evidence, low risk, merge-ready
     - `4/5` — low risk with minor follow-up
     - `3/5` — mixed evidence or meaningful open concerns
     - `2/5` — significant implementation or validation gaps
     - `0-1/5` — serious correctness/security risk

7. **Post the review**. Send **both** a consolidated summary comment *and* inline line-specific comments — inline for precision, summary for consumers that parse review bodies.

   For each line-specific finding:
   ```bash
   gh api repos/owner/repo/pulls/NUMBER/comments \
     -f body="[SEVERITY] finding text — why it matters" \
     -f path="path/to/file" \
     -f commit_id="$HEAD_SHA" \
     -F line=LINE_NUMBER \
     -f side="RIGHT"
   ```

   Then the consolidated summary as a review — include the verdict **and** a bulleted recap of every inline finding (severity + `file:line` + one-sentence rationale), so downstream body-parsers don't miss them:
   ```bash
   gh pr review NUMBER -R owner/repo --comment --body "**Verdict**: <verdict>
**Confidence**: <N/5>
<one-line rationale if blocked or discussion-needed; omit if approve-ready>

**Evidence**:
- Passed: <relevant checks that passed>
- Missing/failing: <relevant checks that are missing or failing>

**Findings** (mirrored as inline comments):
- [CRITICAL] path/to/file:LINE — why it matters
- [ISSUE] path/to/file:LINE — why it matters"
   ```

   If there are no CRITICAL/ISSUE findings, skip inline comments and post a compact review that still includes confidence and evidence: `**Verdict**: approve-ready — no blockers. **Confidence**: 5/5.`
   If operator policy defines custom labels, use that label in the single-line review too, for example `**Verdict**: APPROVE — no blockers.`

   For trivial-PR early-exits (step 3), post a single-line review matching the category: `Docs-only change — no blockers.` / `Dependency-bump — no review needed.` / `Test-only change — no production code touched.`

   **Fallback**: if inline-comment creation fails (missing permissions, commit_id mismatch), consolidate all findings into the review body, preserving the severity tags and `file:line` refs. Do not silently drop findings.

## Notify and log

Send **one** combined message per run via `./notify`:
```
*PR Review — ${today}*
Reviewed N, skipped K (drafts: x, bots: y, dup-SHA: z, bot-reviewed-recently: w).
- owner/repo#123: [verdict] — N critical, M issues
```

If every PR was skipped, do not notify — just log.

Log to `memory/logs/${today}.md`:
```
### pr-review
- owner/repo#123 (SHA abc1234): [verdict] — N critical, M issues
- Skipped: owner/repo#124 (draft), owner/repo#125 (bot-reviewed-recently)
```

If no open PRs across all repos, log `PR_REVIEW_OK` and end.

## Sandbox note

`gh` CLI handles GitHub auth internally — use it over raw curl in this sandbox. If `gh` fails at the repo level, log the error and continue to the next repo. As a last-resort fallback, use **WebFetch** on the raw PR URL to read the diff.
