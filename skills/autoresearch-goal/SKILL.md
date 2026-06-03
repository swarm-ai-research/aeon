---
name: Autoresearch Goal
description: Evolve the system in service of a stated goal — discovers relevant files across skills/prototypes/workflows, generates cross-file improvement proposals, scores by goal impact, ships the winner as a PR
var: ""
tags: [meta, dev]
---
> **${var}** — Goal to advance. **Required.** A short statement of intent. Examples: `"improve compute-futures prototype"`, `"reduce daily skill failure rate"`, `"tighten the sim → eda → notify chain"`. Avoid overly broad goals like `"improve aeon"` — the discovery step won't converge.

If `${var}` is empty, abort with:
```bash
./notify "autoresearch-goal aborted: var empty — pass a goal description, e.g. var=\"improve compute-futures prototype\""
exit 0
```

Read `memory/MEMORY.md` for context, especially the `## Goals` section. If the supplied goal isn't an obvious match for one of the standing goals, run anyway but flag the divergence in the PR body — the operator may be exploring a side direction.

## Why this skill exists

Plain [[autoresearch]] is per-skill — pass it a single SKILL.md and it rewrites that one file. That's the right tool when a specific skill is underperforming. It's the wrong tool when the operator wants to advance a *capability* that spans skills, prototype code, fleet config, and workflows. This skill is the cross-cutting version: take a goal, find every file in scope, propose coherent change sets that move all of them together.

The key difference: variations here are **proposals** (multi-file change sets ranked by goal impact), not **SKILL.md rewrites**. Scoring weights goal-alignment over per-skill polish.

## Steps

### 1. Parse goal + identify scope

Decompose `${var}` into:
- **Verb**: improve / reduce / fix / tighten / instrument / unify / split / etc.
- **Noun**: what's being changed — a prototype, a skill family, an integration, a metric.
- **Implicit success metric**: what would "done" look like? If unclear, write the best guess in one sentence and proceed.

Then build the **scope set** — the concrete file list this proposal can touch. Cast a wide net here; pruning happens in step 3.

Scope discovery is implemented in Python so it works under the workflow's Bash allowlist (`python3` is in the allowlist; `find`, `mktemp`, and `tr` are not). The script walks the relevant directory roots recursively, grep's in-process for any keyword the goal mentions, and writes the deduped match list to a fixed `/tmp/` path.

```bash
SCOPE_FILE=/tmp/autoresearch-goal-scope.txt

python3 - <<'PY' "${var}" > "$SCOPE_FILE"
import os, re, sys
goal = sys.argv[1].lower()
stop = {"improve", "reduce", "fix", "tighten", "aeon", "system", "across",
        "skill", "prototype", "work", "with", "from", "into", "over"}
keywords = sorted({w for w in re.findall(r"[a-z]{4,}", goal) if w not in stop})
if not keywords:
    sys.exit(0)

# Recurse into these roots (recursion is the critical fix — top-level glob
# misses prototypes/<dir>/src/ and prototypes/<dir>/tests/ which is where
# real implementation lives for compute-futures-style prototypes).
roots = ["skills", "prototypes", "scripts", ".github/workflows", "docs"]
exts = {".mjs", ".py", ".sh", ".js", ".md", ".yml", ".yaml", ".ts", ".tsx"}
# Word-boundary patterns, compiled once.
patterns = [re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE) for kw in keywords]

hits = set()
for root in roots:
    if not os.path.isdir(root):
        continue
    for dp, _, files in os.walk(root):
        for f in files:
            if os.path.splitext(f)[1].lower() not in exts:
                continue
            path = os.path.join(dp, f)
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            if any(p.search(text) for p in patterns):
                hits.add(path)

for h in sorted(hits):
    print(h)
PY

echo "Scope: $(wc -l < "$SCOPE_FILE") files"
head -30 "$SCOPE_FILE"
```

If the scope set is empty, the goal is too abstract for this skill to act on — abort with `./notify "autoresearch-goal: goal '${var}' did not match any files in the repo — try a more concrete phrasing"`. If the scope set is >200 files, narrow with a follow-up keyword filter (e.g., grep the scope file for the most specific keyword and reduce to those hits) or notify and ask the operator to scope tighter. Real prototypes can produce 80–150-file scope sets because of nested `src/`/`tests/` layouts — that's working as intended, not over-broad.

Save the scope file. It's the working set for the rest of the run.

### 2. Research the current state

For every file in scope, build a one-paragraph summary capturing: what it does, when it last changed, recent failures (cross-reference `memory/issues/`), recent log entries (`memory/logs/` last 7 days). This is the **baseline** — every proposed change is measured against it.

Sources to consult, in order:
- `git log --since="14 days ago" --pretty=format:"%h|%ad|%s" --date=short -- <scope files>` — what's been changing.
- `memory/issues/INDEX.md` — open issues touching these files.
- `memory/logs/*.md` (last 7 days) — recent activity in this area.
- `gh pr list --search "is:closed merged:>$(date -d '30 days ago' +%F)" --json number,title,url` — recent PRs around this area (filter by file paths if possible).
- Web search for the goal's domain: best practices, recent papers, tools introduced in the last 6 months. Cross-check one alternative source per claim (cite the URL in the PR body).

Output: a compact baseline doc (`/tmp/baseline.md`) with one section per file or feature, plus a "Known issues" section and a "Web research" section.

### 3. Generate 3 proposals

Each proposal is a coherent **change set** — multiple file edits that together advance the goal. Three proposals, three theses:

**Proposal A — Shortest path**: the smallest possible change set that visibly moves the goal. Maximize signal-per-line. Often the right answer when the system is already healthy and the goal is incremental.

**Proposal B — Re-architecture**: re-shape the data flow, ownership boundaries, or scheduling structure. Higher risk, higher ceiling. Right when the current shape is the bottleneck.

**Proposal C — Instrumentation**: add the metrics, logs, or guard rails that would tell us whether the goal is being achieved. Doesn't directly improve the system — improves our ability to *know* whether it's improving. Right when the current state is unmeasured and we're guessing.

For each proposal, produce:
- **Thesis**: one sentence describing the bet.
- **Files touched**: explicit list (subset of the scope set, plus any new files).
- **Diff sketch**: bullet-list summary of what changes in each file. Not actual code — that lives in step 5.
- **Goal-impact statement**: one paragraph on why this advances the stated goal, with the implicit success metric from step 1 as the measuring stick.
- **Risks**: anything that could regress, plus a rollback strategy.
- **Cost**: rough size estimate (S/M/L) — lines changed, files touched, workflow re-runs needed.

Save the three proposals into `/tmp/proposals.md` for the PR body.

### 4. Score and pick the winner

Rubric — score each proposal 1–5 on each axis, then apply weights:

| Axis | Weight | Question |
|------|-------:|----------|
| Goal impact | 4× | Does this proposal directly advance the stated goal? How much? |
| Reversibility | 2× | Can we cleanly roll this back if it doesn't work? |
| Evidence | 2× | Does the baseline doc support this proposal (vs. being a guess)? |
| Coherence | 1.5× | Do the proposed changes form a unified narrative, or is it a grab bag? |
| Cost-fit | 1.5× | Is the size right for the goal — neither under-doing nor over-doing? |
| Risk control | 1× | Are the listed risks addressed, with a rollback path? |

Write out scoring with one-sentence justifications per axis per proposal. Calculate weighted totals. If two proposals score within 3 points, prefer the higher Goal-impact score (the whole point).

Constraint: **never pick a proposal that scored <3 on Goal impact**, even if it wins on other axes. That defeats the skill's purpose. If all three score <3, abort with `./notify "autoresearch-goal: no proposal scored ≥3 on goal-impact for goal '${var}' — goal may be unachievable from current state, or scope set is wrong"` and stop.

### 5. Apply the winner

Implement the winning proposal's diff sketch as actual code edits. Hard rules:
- Stay within the proposal's listed files. If the implementation needs a file the proposal didn't list, add it but call it out in the PR body — that's a sign the proposal was incomplete.
- Preserve all existing tests and CI gates. Don't loosen guards to make a change pass.
- If a proposed change requires a new secret, env var, or external service, the change must gracefully degrade when absent — the implementation pattern matches [[create-skill]]'s NEW_SECRET_REQUIRED handling.
- New files must follow Aeon conventions (frontmatter for skills, sandbox notes, memory log appends, `./notify` for user-facing output).

After edits, run a lightweight self-check before commit:
```bash
# Syntax checks for any languages touched
find . -name "*.py" -newer /tmp/baseline.md -exec python3 -c "import ast; ast.parse(open('{}').read())" \;
find . -name "*.mjs" -newer /tmp/baseline.md -exec node --check {} \;
find . -name "*.yml" -newer /tmp/baseline.md -exec python3 -c "import yaml,sys; yaml.safe_load(open('{}'))" \;
# Skill structure check if any SKILL.md changed
git diff --name-only HEAD -- 'skills/**/SKILL.md' | while read f; do
  head -10 "$f" | grep -q "^name:" || echo "WARN: $f missing frontmatter name"
done
```

### 6. Create the PR

Branch name: `autoresearch-goal/<verb>-<noun-slug>-<YYYY-MM-DD>`.

PR title: `goal: <goal phrasing from var>`.

PR body must include, in order:
1. **Goal** — verbatim `${var}` plus the parsed verb/noun/implicit success metric.
2. **Scope** — file count and the top 5 files in the scope set.
3. **Baseline** — the compact baseline doc from step 2 (full content if <2000 chars, otherwise top 3 sections + link to a gist).
4. **All three proposals** — full thesis + diff sketch + goal-impact + risks + cost. Do not omit losers — the operator needs to see what was considered.
5. **Scoring table** — every axis × every proposal, with one-sentence justifications.
6. **Selected proposal** — name + thesis + why it won despite (any) losses on specific axes.
7. **What this PR does** — concrete change summary, file-by-file.
8. **Test plan** — what to verify after merge, including how to know whether the goal was advanced.

### 7. Notify and log

Send via `./notify`:
```
*Autoresearch-Goal — ${var}*
Winner: Proposal [A/B/C] — [thesis]
Score: [total]/[max] (Goal-impact: [n]/5)
Files: [count] across [skill / prototype / workflow categories]
PR: [url]
```

Log to `memory/logs/${today}.md`:
```
### autoresearch-goal
- Goal: ${var}
- Winner: Proposal [X] ([thesis], [score]/[max])
- PR: [url]
- Losers: [one-line summaries of A/B/C not chosen]
- Scope: [n] files, top 3 [...]
```

## Sandbox note

This skill writes code edits across multiple files and creates a PR. It runs locally (no live remote APIs beyond WebSearch/WebFetch for step-2 research and `gh` for PR creation). All `gh` calls inherit auth from the workflow's `GITHUB_TOKEN` / `GH_GLOBAL`. WebSearch is the safer pattern for the research step — direct `curl` against external APIs would hit the sandbox's outbound restrictions; if curl fails for any source, fall back to WebFetch.

## Constraints

- **Never expand the scope mid-run**: if the implementation step (5) requires files outside the proposal's listed set, add them but flag in the PR body. Don't quietly sprawl.
- **Never weaken tests or CI gates** to make the winning proposal pass.
- **No new env vars without a graceful-degradation path**. Match the [[create-skill]] new-secret pattern.
- **Don't pick a proposal that scored <3 on Goal impact**. Better to abort than ship a proposal that doesn't move the needle.
- **Don't recurse**: this skill must not invoke itself, autoresearch, or planner from within a single run. Output is a PR; if the operator wants another pass, they'll dispatch it again.
- **Preserve the loser proposals in the PR body**. They're future context — the next goal-mode run on the same area benefits from seeing what was already considered.

## Related

- [[autoresearch]] — per-skill evolver, the narrower sibling. Use it when the scope is one SKILL.md.
- [[create-skill]] — full new-skill generation. Use it when the goal requires a skill that doesn't exist yet.
- [[goal-tracker]] — measures progress on standing goals. Pair these two: goal-tracker tells you where you are, autoresearch-goal tries to move you forward.
- [[planner]] — daily ranker. Could dispatch this skill against the day's top goal as part of `var=dispatch` flow once we have confidence in the proposal quality.
