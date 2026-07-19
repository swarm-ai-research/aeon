import numpy as np
import pandas as pd
from scipy import stats
import os, sys, glob, csv
from io import StringIO

# ── helpers ──────────────────────────────────────────────────────────────────

def partial_corr(y, x, controls):
    """Pearson(y, x) after regressing each on the control matrix. Returns (r, p)."""
    Z = np.column_stack([np.ones(len(controls))] + [controls[:, i] for i in range(controls.shape[1])])
    y_r = y - Z @ np.linalg.lstsq(Z, y, rcond=None)[0]
    x_r = x - Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
    r, _ = stats.pearsonr(y_r, x_r)
    n = len(y)
    k = controls.shape[1]
    df = n - 2 - k
    if df <= 0 or abs(r) >= 1:
        return r, np.nan
    t = r * np.sqrt(df / (1 - r * r))
    p = 2 * (1 - stats.t.cdf(abs(t), df))
    return r, p

def verdict(r, p):
    ar = abs(r)
    if ar < 0.15:
        return "null"
    if ar < 0.25:
        return f"weak (|ρ|={ar:.3f})"
    if not np.isnan(p) and p < 0.05:
        return f"FLAGGED (|ρ|={ar:.3f}, p={p:.3f})"
    return f"weak/ns (|ρ|={ar:.3f}, p={p:.3f})"

# ── load prices ───────────────────────────────────────────────────────────────

prices = pd.read_csv(".macro-cache/prices.csv", index_col=0, parse_dates=True)
rets = np.log(prices / prices.shift(1)).dropna(how="any")
n_days = len(rets)
print(f"Returns: {n_days} obs, {rets.shape[1]} cols, {rets.index[0].date()} => {rets.index[-1].date()}")

controls = rets[["BTC", "SOL"]].values

# ── Track A: DePIN tokens ────────────────────────────────────────────────────

track_a = {}
for tok in ("RENDER", "TAO", "IO"):
    if tok not in rets.columns:
        print(f"  Track A: {tok} missing from returns — skipping")
        continue
    r, p = partial_corr(rets[tok].values, rets["NATGAS"].values, controls)
    track_a[tok] = {"n": n_days, "partial_natgas_ctrl_btc_sol": float(r), "p": float(p)}
    print(f"  Track A {tok}: partial_rho={r:.4f}  p={p:.4f}  verdict={verdict(r,p)}")

# ── Also compute wide matrix for descriptive use ──────────────────────────────

non_controls = [c for c in rets.columns if c not in ("BTC", "SOL")]
wide_rows = []
for row_tok in ("RENDER", "TAO", "IO"):
    if row_tok not in rets.columns:
        continue
    for macro in non_controls:
        if macro in ("RENDER", "TAO", "IO"):
            continue
        r, p = partial_corr(rets[row_tok].values, rets[macro].values, controls)
        wide_rows.append((row_tok, macro, r, p, verdict(r, p)))

print("\nWide matrix (token x non-crypto macro, controlled on BTC+SOL):")
for row in wide_rows:
    tok, macro, r, p, v = row
    print(f"  {tok} x {macro}: rho={r:.4f}  p={p:.4f}  {v}")

# ── Track B: sweep P&L CSVs ──────────────────────────────────────────────────

proof_dir = "memory/gitlawb-compute-futures-proofs"
csv_files = sorted(glob.glob(os.path.join(proof_dir, "*.csv")))
print(f"\nTrack B: found {len(csv_files)} CSV proof files")

# Build per-day per-mode mean analyst P&L
day_mode_pnl = {}
for fpath in csv_files:
    date_str = os.path.basename(fpath).replace(".csv", "")
    try:
        df = pd.read_csv(fpath)
        if "mode" not in df.columns or "role" not in df.columns or "role_pnl" not in df.columns:
            print(f"  {date_str}: schema mismatch — skip")
            continue
        analysts = df[df["role"] == "analyst"]
        if analysts.empty:
            print(f"  {date_str}: no analyst rows")
            continue
        for mode, grp in analysts.groupby("mode"):
            mean_pnl = grp["role_pnl"].mean()
            key = (date_str, mode)
            day_mode_pnl[key] = mean_pnl
    except Exception as e:
        print(f"  {date_str}: error {e}")

if not day_mode_pnl:
    track_b_status = "track B: no sweep series yet"
    track_b = {}
    track_b_n = 0
else:
    # Pivot to DataFrame indexed by date
    records = {}
    for (date_str, mode), pnl in day_mode_pnl.items():
        dt = pd.Timestamp(date_str, tz="UTC")
        if dt not in records:
            records[dt] = {}
        records[dt][mode] = pnl

    sweep_df = pd.DataFrame.from_dict(records, orient="index").sort_index()
    sweep_df.index.name = "date"
    print(f"\nSweep series: {len(sweep_df)} days, modes: {sorted(sweep_df.columns)}")

    # Join with rets on UTC midnight
    joined = rets.join(sweep_df, how="inner").dropna(subset=["NATGAS", "BTC", "SOL"])
    track_b_n = len(joined)
    print(f"Joined (inner): {track_b_n} days")

    track_b = {}
    if track_b_n < 30:
        track_b_status = f"track B: n={track_b_n}, deferring (<30)"
        print(f"  Track B: deferring — {track_b_n} joined days, need 30")
    else:
        modes = [c for c in sweep_df.columns if c in joined.columns]
        controls_b = joined[["BTC", "SOL"]].values
        for mode in modes:
            r, p = partial_corr(joined[mode].values, joined["NATGAS"].values, controls_b)
            track_b[mode] = {"n": track_b_n, "partial_natgas_ctrl_btc_sol": float(r), "p": float(p)}
            print(f"  Track B {mode}: partial_rho={r:.4f}  p={p:.4f}  verdict={verdict(r,p)}")
        track_b_status = f"track B: n={track_b_n}, modes={modes}"

print(f"\n=== SUMMARY ===")
print(f"Track A: {track_a}")
print(f"Track B status: {track_b_status}")
if track_b:
    print(f"Track B: {track_b}")

# ── Save results for next step ─────────────────────────────────────────────────
import json
results = {
    "date": "2026-07-19",
    "n_macro": n_days,
    "track_a": track_a,
    "track_b_n": track_b_n if 'track_b_n' in dir() else 0,
    "track_b": track_b,
    "track_b_status": track_b_status if 'track_b_status' in dir() else "unknown",
    "wide_matrix": [
        {"token": tok, "macro": macro, "rho": float(r), "p": float(p), "verdict": v}
        for tok, macro, r, p, v in wide_rows
    ],
}
with open(".macro-cache/results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nResults written to .macro-cache/results.json")
