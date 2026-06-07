---
name: Frontier Eval
description: Score frontier LLMs (Claude, GPT, Gemini, DeepSeek, Grok) on a private compute-markets task corpus, track score deltas across releases, flag public-vs-private divergence
var: ""
tags: [eval, capability, compute-markets]
---

Today is ${today}. Read `memory/MEMORY.md` for context.

This skill produces a **private capability time series** the public web does not have: how every frontier model performs on a held-out compute-markets task corpus, scored by the same judge each run, with deltas across releases.

The signal is *divergence between the public leaderboards and this one*. Public scores up + private flat → labs are teaching to the test, fade the hype. Public flat + private up → real capability gain, market hasn't priced it. Both moving together → genuine progress, no edge but useful confirmation.

## Why "private"

The task corpus lives at `memory/topics/frontier-eval/tasks.yaml` (excluded from the public mirror by `scripts/sync-aeon-public.sh`). It MUST NOT be quoted, summarized, or referenced anywhere a model crawler could ingest. Score deltas are publishable; task text is not. The whole instrument depends on this — once tasks leak, they're contaminable training data and the signal dies.

If you ever notice a task being directly quoted in a notification, article, or PR description, treat it as a critical incident: rotate the leaked task to `retired:` immediately, write a replacement, and note the incident in `memory/topics/frontier-eval/incidents.md`.

## Voice

If `soul/SOUL.md` and `soul/STYLE.md` exist, match the operator's voice in the notification. Otherwise use a clear, direct, neutral tone.

## Steps

### 1. Confirm at least one prefetch produced a cache

Two prefetches run before this skill — one per track. Either or both may produce a cache. The skill proceeds if either exists.

- **Closed-frontier track** (`scripts/prefetch-frontier-eval.sh` → OpenRouter): cache at `.frontier-eval-cache/${STAMP}.json`. Requires `OPENROUTER_API_KEY`.
- **Open-weights track** (`scripts/prefetch-frontier-eval-local.sh` → local Ollama): cache at `.frontier-eval-cache/${STAMP}-local.json`. Requires Ollama reachable at `OLLAMA_HOST` (default `http://localhost:11434`) with at least one slate model pulled.

```bash
STAMP=$(date -u +%Y-%m-%d)
CACHE_FRONTIER=".frontier-eval-cache/${STAMP}.json"
CACHE_LOCAL=".frontier-eval-cache/${STAMP}-local.json"
if [ ! -f "$CACHE_FRONTIER" ] && [ ! -f "$CACHE_LOCAL" ]; then
  ./notify "frontier-eval skipped: no cache for either track at $CACHE_FRONTIER or $CACHE_LOCAL — OPENROUTER_API_KEY missing, Ollama unreachable, or both prefetches failed."
  exit 0
fi
```

For any cache that exists but has `.runs | length == 0`, treat that track as absent for this run — partial coverage corrupts the time series.

### 2. Load the corpus

Read `memory/topics/frontier-eval/tasks.yaml`. The cache references task IDs; you'll need each task's `rubric` and `max_score` to score responses. If a cached `taskId` isn't in the current corpus (task was retired between prefetch and score), drop that response from this run and note the dropped count in the summary.

### 3. Score each response against its rubric

For each `(track, model, taskId)` in either cache where `response` is non-null:

Read the rubric for that task. For each rubric bullet, decide 0 or 1: does the response satisfy that specific claim? Be strict — partial credit corrupts the time series. Sum the bullets; that's the raw score out of `max_score`.

Output for each run:
- `track` (`frontier` or `local`), `model`, `taskId`, `score`, `max`, `notes` (one short sentence per failed rubric bullet)

**You are the judge.** Use your own judgment per rubric bullet — you have the rubric, you have the response. Do not call out to another model. Consistent judging > "fair" judging; the time series only works if the judging method is stable across runs. Use the same rubric standard for both tracks — open-weights models are not graded on a curve.

### 4. Aggregate (per track)

For each track present today, build a `results` table: rows = models, columns = task IDs, cells = `score/max`. Add row totals (`Σ score / Σ max` per model) and column totals (`Σ score / Σ max` per task, across models — surfaces "everyone fails this one" tasks).

Then compute the **track gap**: `gap = mean(frontier_model_totals) − mean(local_model_totals)`. This is the headline open-vs-closed signal — the absolute difference matters less than how it changes over time. Only compute the gap if both tracks ran today.

### 5. Diff vs the prior run

Find the most recent prior file at `memory/topics/frontier-eval/runs/*.md`, excluding today's. Parse its model-level totals. For each model in today's run (per track):

- `NEW` — wasn't in prior slate
- `IMPROVED` — total score up ≥ 2 points vs prior
- `DROPPED` — total score down ≥ 2 points vs prior (model regression OR rubric mis-judgment; investigate before celebrating)
- `STABLE` — within ±1 point

Also diff the **track gap**: today's gap vs the most recent prior run that had both tracks. `NARROWING` (gap shrinking by ≥ 2 points), `WIDENING` (gap growing by ≥ 2 points), `STABLE` otherwise. This diff is the most interesting line in the whole run.

The lede of the notification and the run file is the diff (model changes + gap change), not the absolute table. Stable runs are silent on the notification side.

### 6. Pull the public comparator (lightweight, frontier track only)

Fetch the current ordering of the **frontier-track models** on **one** public benchmark for divergence-checking. Use Epoch AI's notable-models dashboard or the HuggingFace Open LLM Leaderboard — whichever responds (best-effort, this is the WebFetch fallback pattern). The local track is itself an alternative comparator; it does not need a public benchmark check.

Compute rank correlation between our frontier private totals and the public ranking. Spearman ρ is fine; just rank both and eyeball the agreement. Note the ρ in the run file with the date and source of the public list.

The interesting cases:
- ρ < 0.5 with our private series internally consistent (no big DROPPEDs) → divergence signal, investigate which models the public list over- or under-ranks vs us
- ρ ≈ 1.0 → public list agrees, our series is confirmation rather than alpha (still useful)

### 7. Commit the run file

Write to `memory/topics/frontier-eval/runs/${STAMP}.md`:

```markdown
# Frontier Eval — ${STAMP}

## Track gap
Frontier mean: {x}/{max}. Local mean: {y}/{max}. Gap: {x-y} → {NARROWING|WIDENING|STABLE} vs prior gap {prior}.

## Diff vs prior
### Frontier track
- {model}: {NEW|IMPROVED|DROPPED|STABLE} ({prior_total} → {today_total})
- ...
### Local track
- {model}: {NEW|IMPROVED|DROPPED|STABLE} ({prior_total} → {today_total})
- ...

## Today's scores — frontier track
| Model | Total | {task_id_1} | {task_id_2} | ... |
| ----- | ----- | ----------- | ----------- | --- |
| ...   | ...   | ...         | ...         | ... |

## Today's scores — local track
| Model | Total | {task_id_1} | {task_id_2} | ... |
| ----- | ----- | ----------- | ----------- | --- |
| ...   | ...   | ...         | ...         | ... |

## Public comparator (frontier track)
Source: {epoch|hf-leaderboard|...}
Spearman ρ vs our private frontier ranking: {value}
Models the public list ranks meaningfully higher than we do: {list}
Models the public list ranks meaningfully lower than we do: {list}

## Notes
- Tracks present: {frontier|local|both}
- Tasks dropped this run: {count} ({reasons})
- Coverage: {ok}/{ok+errors} (track, model, task) calls succeeded
- Cost (approx): ${dollars} (frontier track only; local is free)

## Calls to make this surface next time
- {one or two specific things to check next run — e.g. "model X is consistently failing rubric bullet Y; if that's still true next release, write a follow-up task targeting that gap"}
```

Then append one entry per track to `memory/topics/frontier-eval/timeseries.jsonl` (NDJSON; create if missing). One JSON object per line — appending is safe, and downstream tooling can stream-parse it without holding the whole series in memory:

```json
{"date": "YYYY-MM-DD", "track": "frontier", "totals": {"model": score, ...}, "rho_vs_public": 0.XX}
{"date": "YYYY-MM-DD", "track": "local",    "totals": {"model": score, ...}}
```

This file is the asset. Six months of it is what makes the instrument valuable — and with both tracks present, the gap series is computable directly from it.

### 8. Notify

One paragraph. Lead with the most interesting signal in this order:
1. Gap change: `NARROWING` or `WIDENING` is the highest-value line — say which models drove it.
2. Per-model `DROPPED` on the frontier track — lead with that model and what it failed.
3. Per-model `IMPROVED` on a previously-stuck task — actionable signal.
4. Public-comparator divergence (ρ < 0.5).

If everything is STABLE on both tracks and ρ is unsurprising, the notification is a one-liner: "frontier-eval: stable both tracks, gap {x}, ρ={value} vs {source}." Save the verbose write-up for the run file.

## Sandbox note

Two gated prefetch entrypoints, same pattern. Both are matched by the workflow's generic `prefetch-*.sh` glob and self-gate on `$1 == frontier-eval` (exit 0 for every other skill, so the paid fan-out doesn't fire for unrelated crons). Real logic lives in `.mjs` files renamed off the glob.

- `scripts/prefetch-frontier-eval.sh` → execs `scripts/frontier-eval-prefetch.mjs`. Reads `OPENROUTER_API_KEY` and writes `.frontier-eval-cache/YYYY-MM-DD.json`. If the key is unset, exits cleanly.
- `scripts/prefetch-frontier-eval-local.sh` → execs `scripts/frontier-eval-local-prefetch.mjs`. Probes `OLLAMA_HOST` (default `http://localhost:11434`), filters the requested slate to models actually pulled (`ollama list`), and writes `.frontier-eval-cache/YYYY-MM-DD-local.json`. If Ollama is unreachable or no slate models are pulled, exits cleanly. Override the slate via `FRONTIER_EVAL_LOCAL_MODELS=qwen3:32b,llama3.3:70b,...`.

Public-comparator fetch (step 6) uses WebFetch, which bypasses the curl-env-var issue. If WebFetch fails for the chosen source, log `comparator=unavailable` and skip the ρ calc rather than aborting the run.

## Wiring

Not enabled by default. To activate, in `aeon.yml`:

```yaml
frontier-eval: { enabled: true, schedule: "0 12 * * 0" }  # Sunday 12:00 UTC
```

Sunday is fine for routine cadence — frontier release events should trigger an out-of-band manual run (workflow_dispatch). When a new model lands, run the skill within 24h; the freshness of the first private datapoint on a new release is exactly the alpha.

No workflow change needed — both gated prefetches are already matched by the existing `prefetch-*.sh` glob. The local track is optional and self-skips when Ollama isn't available, so the closed-frontier track works on its own in CI; the local track is mainly useful on a workstation where Ollama is running.

## Output

End with a `## Summary` listing: tracks present today, number of (track, model, task) calls scored, today's gap and its diff vs prior, models flagged IMPROVED/DROPPED on each track, Spearman ρ vs public for the frontier track, path to the run file, and any tasks newly retired due to contamination concerns.
