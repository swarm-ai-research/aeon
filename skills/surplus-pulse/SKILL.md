---
name: surplus-pulse
description: Daily compute-futures pulse anchored to the Surplus Intelligence inference market — runs the prototype sim against the live Surplus spot feed, reports the curve re-pricing, the live anchor, and the real Base/USDC x402 rail.
schedule: "0 16 * * *"
commits: true
permissions:
  - contents:write
tags: [ai, compute, x402, depin, markets]
---

Today is ${today}. Read `memory/MEMORY.md` before starting. If `soul/SOUL.md` + `soul/STYLE.md` exist and are populated, read them to match the operator's voice for the notification; otherwise use a clear, direct, neutral tone — short sentences, no hedging.

## Why this skill exists

[Surplus Intelligence](https://www.surplusintelligence.ai/) is an OpenAI-compatible inference marketplace that sells *surplus* capacity at *market* prices, with a real x402 settlement endpoint on Base (USDC). Our `compute-futures` prototype settles against inference compute priced in $/M-tokens, and the `--surplus` adapter (`prototypes/compute-futures/src/surplus.mjs`) anchors that spot to Surplus's real prices.

This skill is one clean daily read on that market: run the simulation against the **live** Surplus feed, and report how the futures curve re-prices around the day's supply/demand events, what the live spot anchor was, and the real x402 rail a physical settlement would run over. It is the live, scheduled counterpart to the deterministic prototype.

## Sandbox note

The sim makes **no network call from inside the sandbox**. The live feed is fetched OUTSIDE the sandbox by `scripts/prefetch-surplus.sh` (run automatically before this skill), which caches Surplus prices to `.surplus-cache/prices.json`; the sim reads that cache when run with `--live`. Configure the repo secret `SURPLUS_PRICING_URL` (and optional `SURPLUS_API_KEY`) to point at a Surplus prices / OpenAI-compatible `/models` endpoint. If it is unset or unreachable, the sim transparently falls back to its built-in catalog — the run still succeeds (deterministic), just not "live". Always report which mode actually ran.

## Steps

### 1. Load context

Read:
- `memory/topics/projects.md` — the compute-futures + Surplus integration status.
- `memory/topics/surplus-pulse.md` — prior runs (create with the seed below if missing).

```markdown
# Surplus Pulse

*Last run: never*

## Run Log
- (append per-run summaries here: date · live|catalog · anchor $/M · top curve move)
```

### 2. Run the simulation against the live Surplus feed

Run the prototype with the Surplus venue, the live feed, and the x402 rail (so the proof shows the real settlement endpoint):

```bash
node prototypes/compute-futures/sim.mjs --surplus --live --x402
```

Capture the full stdout. Key lines to read out of it:
- The mode line `[surplus] live anchor: <model> → $<price>/M` (live feed used) **or** `[surplus] live feed unavailable — using catalog (set SURPLUS_PRICING_URL)` (catalog fallback). This tells you whether the run was genuinely live.
- The header `spot source: surplus (<model>, live|catalog)`.
- The `── Curve re-pricing around each event ──` section (the headline moves).
- The `── x402 physical settlement` block, including the `real rail: Surplus x402 …` endpoint line.

If the command exits non-zero, log `SURPLUS_PULSE_SIM_FAIL: <first line of stderr>`, send no notification, and stop.

### 3. Update memory/topics/surplus-pulse.md

- Set `*Last run: ${today}*`.
- Append one line to `Run Log`:
  ```
  - ${today}: <live|catalog> · anchor $<price>/M (<model>) · top move <event> <±%> · x402 endpoint reachable proof recorded
  ```

### 4. Notify

Write the summary, then send it:

```bash
mkdir -p .pending-notify-temp
./notify -f .pending-notify-temp/surplus-pulse-${today}.md
```

**Format — one short paragraph, match operator voice if soul files are populated:**

```
surplus pulse — ${today}

spot: <live|catalog> · <model> @ $<anchor>/M (Surplus Intelligence)
curve: <biggest event re-price, e.g. "supply crunch +82% at R16">
rail: x402 on Base/USDC — <real endpoint named>

one-line read: <is the Surplus inference market loosening or tightening, per the run>
```

Keep it to one paragraph. Do not paste the full sim output into the notification.

## Output

End with a `## Summary` listing: whether the run was live or catalog, the spot anchor, the top curve move, files modified (`memory/topics/surplus-pulse.md`), and the notification status.
