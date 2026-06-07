---
name: Compute × Macro Correlate
description: Weekly partial-correlation of compute economics against a Hyperliquid macro basket — DePIN-token proxy track runs every week (n>180d), sweep-P&L track defers until n≥30 joined days
var: ""
tags: [data, analysis, compute-futures, macro]
---

Today is ${today}. Read `memory/MEMORY.md` for context — especially [[compute-macro-correlation-findings]] (priors, control set, noise floor) and [[aeon-compute-futures-experiments]] (sweep semantics; `wallet_sum_pnl` is a Σ conservation check, NOT strategy P&L).

## Voice

If `soul/SOUL.md` + `soul/STYLE.md` are populated, match the operator's voice. Otherwise: clear, direct, neutral.

## Why this skill exists

Compute-futures sweep P&L looks superficially correlated with whatever macro you point at — but most of the basket (oil, EUR, chip-fab metals) is itself crypto-beta in disguise. We pre-registered one test on 2026-06-03:

> **Does compute economics co-vary with NATGAS returns net of crypto-beta?**

NATGAS is the only major macro nearly independent of crypto (90d ρ ≈ −0.31), and it's the energy that actually drives data-center power cost. **The DePIN-token proxy (RENDER/TAO/IO, 181d) already returned a clean null on this test** at the token-market level — see [[compute-macro-correlation-findings]]. That doesn't rule out the sweep showing something different; token prices ≠ marketplace clearing $/M-token. But it raises the bar: a real sweep signal has to clear the noise floor *and* survive the same partialling.

This skill runs two parallel tracks every week:

- **Track A — DePIN-token proxy** (RENDER, TAO, IO): always runs, n>180d, fully powered. Sanity baseline; should keep returning null until something changes upstream.
- **Track B — sweep P&L** (per-mode analyst): defers with `n=K, deferring` until ≥30 joined days. Once it fires, compare its verdict to Track A.

The two-control set is **{BTC, SOL}**, not BTC alone. SOL dominates BTC for DePIN-token crypto-beta (prototype: RENDER/TAO/IO × SOL | BTC = +0.21/+0.34/+0.36, all p<0.05), so partialling on BTC alone leaves a residual that looks like a "compute" signal but is really Solana-ecosystem beta.

## Steps

### 1. Fetch the macro basket + DePIN tokens from Hyperliquid

Public info endpoint, no auth. Sandbox-friendly: plain HTTPS POST to `https://api.hyperliquid.xyz/info`. If curl fails, retry once with WebFetch.

```bash
mkdir -p .macro-cache
```

`.macro-cache/` is gitignored — keeps the scratch price CSV out of the workflow's `git add -A` auto-commit.

Then in python (single script — keeps shape control here, not in a shell pipeline):

```python
import json, time, urllib.request
import pandas as pd

INFO = "https://api.hyperliquid.xyz/info"
end_ms = int(time.time() * 1000)
start_ms = end_ms - 180 * 24 * 60 * 60 * 1000  # 180 days

# Symbol map — labels are stable; right-hand side is the hyperliquid coin id.
# xyz:* are commodity/FX perps that aren't in the SDK's name_to_coin mapping
# but ARE returned by candleSnapshot when you pass the prefixed string directly.
MACROS = {
    "BTC": "BTC", "ETH": "ETH", "SOL": "SOL",
    "NATGAS": "xyz:NATGAS",         # primary: data-center power signal
    "CL_WTI": "xyz:CL",
    "BRENT":  "xyz:BRENTOIL",
    "COPPER": "xyz:COPPER", "PLATINUM": "xyz:PLATINUM", "PALLADIUM": "xyz:PALLADIUM",
    "GOLD":   "xyz:GOLD",  "SILVER": "xyz:SILVER",
    "EUR":    "xyz:EUR",   "JPY":    "xyz:JPY",
}
DEPIN = {"RENDER": "RENDER", "TAO": "TAO", "IO": "IO"}  # always-on track A

def candles(coin):
    body = {"type": "candleSnapshot",
            "req": {"coin": coin, "interval": "1d",
                    "startTime": start_ms, "endTime": end_ms}}
    req = urllib.request.Request(INFO, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

frames, failures = {}, {}
for label, coin in {**MACROS, **DEPIN}.items():
    try:
        c = candles(coin)
        if not c:
            failures[label] = "empty"; continue
        s = pd.Series({pd.Timestamp(x["T"], unit="ms", tz="UTC").normalize(): float(x["c"])
                       for x in c}, name=label)
        frames[label] = s
    except Exception as e:
        failures[label] = str(e)[:120]
    time.sleep(0.1)

# Primary axes are mandatory: BTC + SOL (controls) and NATGAS (test).
# If any are missing, treat as a transient upstream outage — clean skip, exit 0
# (per the sandbox note). The cron retries next week with the same n+7 window.
missing = [m for m in ("BTC", "SOL", "NATGAS") if m in failures]
if missing:
    import subprocess
    msg = f"compute-macro-correlate: skipping — primary fetch failed ({', '.join(missing)})"
    subprocess.run(["./notify", msg], check=False)
    raise SystemExit(0)

prices = pd.concat(frames.values(), axis=1).sort_index()
prices.to_csv(".macro-cache/prices.csv")
```

If `failures` is non-empty for non-primary assets, log them and continue with what we have. **BTC, SOL, and NATGAS are mandatory** — the partial-correlation test depends on all three. If any DePIN token fetch fails, drop just that token from Track A and continue.

### 2. Pull the latest sweep proofs from `fleet-state` (Track B input)

Same pattern as [[compute-futures-eda]] — proofs land on `fleet-state`, not `main`:

```bash
git fetch origin fleet-state --depth=50 2>/dev/null || true
git checkout origin/fleet-state -- memory/gitlawb-compute-futures-proofs/ 2>/dev/null || true
```

Parse all available CSVs (when the deployer is emitting them) OR all proof markdowns (until then) into a per-day per-mode mean analyst P&L. Schema reference: `seed, mode, live, role, role_pnl, ...` — see [[compute-futures-eda]] for the canonical columns.

If no CSVs / parseable proofs are present, Track B emits `track B: no sweep series yet` and skips to step 4 with just Track A results.

### 3. Compute correlations (both tracks)

Common helper:

```python
import numpy as np
import pandas as pd
from scipy import stats

def partial_corr(y, x, controls):
    """Pearson(y, x) after regressing each on the control matrix. Returns (r, p)."""
    Z = np.column_stack([np.ones(len(controls))] + [controls[:, i] for i in range(controls.shape[1])])
    y_r = y - Z @ np.linalg.lstsq(Z, y, rcond=None)[0]
    x_r = x - Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
    r, _ = stats.pearsonr(y_r, x_r)
    n = len(y); k = controls.shape[1]; df = n - 2 - k
    if df <= 0 or abs(r) >= 1: return r, np.nan
    t = r * np.sqrt(df / (1 - r * r))
    p = 2 * (1 - stats.t.cdf(abs(t), df))
    return r, p
```

**Track A (always runs):** for each DePIN token, compute partial ρ vs NATGAS controlling on {BTC, SOL}. Also write the wider partial-correlation matrix vs every non-control macro for descriptive inspection.

```python
prices = pd.read_csv(".macro-cache/prices.csv", index_col=0, parse_dates=True)
rets = np.log(prices / prices.shift(1)).dropna(how="any")

controls = rets[["BTC", "SOL"]].values
track_a = {}
for tok in ("RENDER", "TAO", "IO"):
    if tok not in rets.columns: continue
    r, p = partial_corr(rets[tok].values, rets["NATGAS"].values, controls)
    track_a[tok] = {"n": len(rets), "partial_natgas_ctrl_btc_sol": float(r), "p": float(p)}
```

**Track B (defers until n≥30):** join the per-mode P&L Series with `rets` on UTC midnight. If `len(joined) < 30`, write a one-line defer note and skip the test:

```python
joined = rets.join(sweep_pnl_by_mode, how="inner").dropna(subset=["NATGAS", "BTC", "SOL"])
track_b_n = len(joined)
track_b = {}
if track_b_n >= 30:
    controls_b = joined[["BTC", "SOL"]].values
    for mode in sweep_pnl_by_mode.columns:
        r, p = partial_corr(joined[mode].values, joined["NATGAS"].values, controls_b)
        track_b[mode] = {"n": track_b_n, "partial_natgas_ctrl_btc_sol": float(r), "p": float(p)}
```

### 4. Append findings

Append a dated block to `memory/topics/compute-futures-macro-correlations.md`. Create it with this header on first run:

```
# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding
```

Per-run block:

```
### {YYYY-MM-DD}

**Track A — DePIN proxy** (n={n})

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | … | … | … |
| TAO | … | … | … |
| IO | … | … | … |

**Track B — sweep P&L**: {`n=K, deferring (<30)` or table by mode}
```

### 5. Decide whether to notify with a finding

After appending, check the **last 2 entries** in the topic file. Notify with a non-deferred finding only when *both* of the following hold for the SAME signal (same token or same sweep mode, same partial-ρ sign):

- |ρ| ≥ 0.25 AND p < 0.05 in this snapshot
- |ρ| ≥ 0.20 AND p < 0.10 in the previous weekly snapshot

This consecutive-reads rule is the noise-floor guard from [[compute-macro-correlation-findings]] (single-snapshot null-distribution width at n=30 is ~±0.30; at n=180 it's ~±0.15).

Otherwise notify with the headline verdict (`Track A: all null`, `Track A: RENDER weak signal ρ=-0.18`, `Track B: deferring n=14`, etc.).

### 6. Commit findings

Per CLAUDE.md, never push to main. Branch + commit + open a PR:

```bash
DATE=$(date -u +%Y-%m-%d)
git checkout -b compute-macro/${DATE}
git add memory/topics/compute-futures-macro-correlations.md
git commit -m "compute-macro-correlate: ${DATE} snapshot"
gh pr create --title "compute-macro-correlate: ${DATE}" \
  --body "Weekly partial-correlation update. See memory/topics/compute-futures-macro-correlations.md."
```

### 7. Notify

One-paragraph max. Lead with the headline verdict (see step 5). Cite specific numbers; don't editorialize. If a flagged finding is now its 2nd-consecutive read, lead with that.

## Sandbox note

All endpoints are public (no auth headers). The hyperliquid POST + the GitHub `gh` CLI both work in CI. If hyperliquid is unreachable, retry once with WebFetch against the same URL with the JSON body; if still failing, log the failure and exit 0 (don't block the chain).

## Output

End with `## Summary` per CLAUDE.md: Track A partial-ρ per token (+ verdict), Track B status (deferring or per-mode table), any flagged consecutive-read findings, files written.
