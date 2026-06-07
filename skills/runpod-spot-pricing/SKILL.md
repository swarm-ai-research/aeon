---
name: runpod-spot-pricing
description: Daily snapshot of RunPod community-cloud (spot) vs secure-cloud (on-demand) GPU pricing. Tracks A100/H100/4090/3090 and flags spot dislocations worth queueing deferred work against.
schedule: "0 13 * * *"
commits: true
permissions:
  - contents:write
tags: [compute, gpu, depin, pricing]
---

Today is ${today}. Read `memory/MEMORY.md` and `memory/topics/compute-pulse.md` (if it exists) before starting. If `soul/SOUL.md` + `soul/STYLE.md` exist and are populated, match that voice; otherwise be terse and neutral.

## Why this skill exists

RunPod runs two pools side-by-side: **community cloud** (interruptible bid-priced spot, host-supplied) and **secure cloud** (RunPod-operated on-demand). The gap between them is the price of preemption risk. When the gap widens past ~50% on a given GPU, fault-tolerant batch work (embeddings backfills, fine-tunes with checkpointing, eval sweeps) should be queued onto spot. When it compresses, the spot pool is saturated and on-demand wins.

This skill is the data feed that makes that call legible. It complements `compute-pulse` (which covers the narrative layer) and `compute-futures-eda` (which covers the on-chain GPU markets) by giving a clean centralized-spot benchmark.

## Inputs

The pre-fetch script (`scripts/prefetch-runpod.sh`) calls the RunPod GraphQL API outside the sandbox and writes `.runpod-cache/gpu-types.json`. The query asks for `lowestPrice` separately per pool (via GraphQL aliases `secure:` and `community:`) so the comparison below is like-for-like — not the cheapest across both pools, which would mix bid prices from one pool against on-demand prices from the other. Schema (relevant fields):

```json
{
  "data": {
    "gpuTypes": [
      {
        "id": "NVIDIA A100 80GB PCIe",
        "displayName": "A100 80GB",
        "memoryInGb": 80,
        "secureCloud": true,
        "communityCloud": true,
        "secure":    { "minimumBidPrice": null, "uninterruptablePrice": 1.64 },
        "community": { "minimumBidPrice": 0.79, "uninterruptablePrice": null }
      }
    ]
  }
}
```

If `.runpod-cache/gpu-types.json` is missing or empty, the prefetch failed — note it in the output, do not fabricate numbers, and stop. Do NOT call the RunPod API directly from inside the sandbox.

## What to do

1. Load `.runpod-cache/gpu-types.json`. Filter to the GPUs we care about: A100 (40GB + 80GB), H100 (PCIe + SXM + NVL), H200, L40S, 4090, 3090.

2. For each, compute:
   - `spot` = `community.minimumBidPrice` (skip if null or `communityCloud: false`)
   - `ondemand` = `secure.uninterruptablePrice` (skip if null or `secureCloud: false`)
   - `discount_pct` = `(ondemand - spot) / ondemand * 100`

   Read spot from the **community** alias and on-demand from the **secure** alias — never cross pools. If only one pool publishes a price for a given GPU, skip it rather than comparing across pools.

3. Append a row per GPU to `memory/topics/runpod-pricing.md` under a dated section. If the file doesn't exist, create it with this header:

   ```markdown
   # RunPod pricing — daily snapshot

   Spot = community-cloud `minimumBidPrice`. On-demand = secure-cloud `uninterruptablePrice`. Both $/hr per GPU.

   ## YYYY-MM-DD
   | GPU | Spot $/hr | On-demand $/hr | Discount | Note |
   ```

4. Compare today's snapshot against the prior day's section in the same file. For each GPU, compute spot delta (% change). If spot moved more than ±15% day-over-day, OR if today's `discount_pct` is above 50% (genuine dislocation), add a one-line callout in a `### Signals` subsection under today's date.

5. If there are ≥1 signal lines, end with `./notify "runpod-spot: <one-sentence summary of the strongest signal>"`. Otherwise do not notify — this is mostly a quiet data feed.

## Output

A `## Summary` block listing:
- file modified: `memory/topics/runpod-pricing.md`
- GPU count snapshotted
- signals fired (if any) with the specific discount/delta numbers
- prefetch status (success / failed / no API key)

## Sandbox note

Auth-required API → **pre-fetch pattern**. The workflow runs `scripts/prefetch-runpod.sh` (with `RUNPOD_API_KEY` from secrets) before Claude starts, and the cached JSON lands at `.runpod-cache/gpu-types.json`. If `RUNPOD_API_KEY` is unset the prefetch exits 0 silently — the skill should detect the missing cache file and note "RUNPOD_API_KEY not configured" in its summary, not retry from inside the sandbox.

## Setup checklist (one-time, not in scope for this skill run)

- Add `RUNPOD_API_KEY` to GitHub Actions secrets (read-only key is fine — this skill only queries).
- Wire `runpod-spot-pricing` into the prefetch dispatch in the workflow YAML so `scripts/prefetch-runpod.sh` runs for this skill.
- Optional: add a `compute` chain in `aeon.yml` that runs this skill before `compute-pulse` so the weekly narrative read can `consume:` the pricing table.
