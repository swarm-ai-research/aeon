"""Inline stdlib-only EDA for compute-futures sweep CSV.

Pandas is not installed in the sandbox; the vendored programmatic-eda scripts
require pandas. This mirrors the key stats they compute: null profile, per-mode
distribution summaries, IQR outlier counts, Pearson correlations, and the
project-specific multiplier/x402/spread-retail checks referenced in the skill.
"""
import csv
import math
import statistics
import sys
import json
from collections import defaultdict

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "memory/gitlawb-compute-futures-proofs/2026-11-08.csv"
PRIOR_CSV = sys.argv[2] if len(sys.argv) > 2 else "memory/gitlawb-compute-futures-proofs/2026-10-29.csv"

NUMERIC_COLS = [
    "seed", "role_pnl", "wallet_sum_pnl", "realizedAbs",
    "minSpot", "maxSpot", "minCurve", "maxCurve",
    "rounds", "settlementLegs", "x402Total", "deniedWorkers",
]


def load(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def to_float(x):
    try:
        return float(x)
    except Exception:
        return None


def nums(rows, col):
    out = []
    for r in rows:
        v = to_float(r.get(col, ""))
        if v is not None:
            out.append(v)
    return out


def summary(vals):
    if not vals:
        return None
    s = sorted(vals)
    n = len(s)
    mean = sum(s) / n
    var = sum((v - mean) ** 2 for v in s) / n
    std = math.sqrt(var)

    def pct(p):
        if n == 1:
            return s[0]
        k = (n - 1) * p
        lo = int(math.floor(k))
        hi = int(math.ceil(k))
        if lo == hi:
            return s[lo]
        return s[lo] + (s[hi] - s[lo]) * (k - lo)
    return {
        "n": n, "mean": mean, "std": std, "min": s[0], "max": s[-1],
        "q25": pct(0.25), "q50": pct(0.5), "q75": pct(0.75),
        "range": s[-1] - s[0],
        "unique": len(set(s)),
    }


def iqr_outlier_pct(vals):
    s = summary(vals)
    if not s or s["std"] == 0:
        return 0.0
    iqr = s["q75"] - s["q25"]
    lo = s["q25"] - 1.5 * iqr
    hi = s["q75"] + 1.5 * iqr
    outs = [v for v in vals if v < lo or v > hi]
    return 100.0 * len(outs) / len(vals)


def pearson(a, b):
    n = len(a)
    if n < 2:
        return None
    ma = sum(a) / n
    mb = sum(b) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(sum((v - ma) ** 2 for v in a))
    db = math.sqrt(sum((v - mb) ** 2 for v in b))
    if da == 0 or db == 0:
        return None
    return num / (da * db)


rows = load(CSV_PATH)
prior = load(PRIOR_CSV) if PRIOR_CSV else []

print(f"=== {CSV_PATH} ===")
print(f"rows={len(rows)} cols={len(rows[0])} modes={sorted(set(r['mode'] for r in rows))}")

# Null profile
print("\n== nulls ==")
null_counts = defaultdict(int)
for r in rows:
    for k, v in r.items():
        if v is None or v == "":
            null_counts[k] += 1
for c, n in null_counts.items():
    print(f"  {c}: {n}")
if not null_counts:
    print("  (none)")

modes = sorted(set(r["mode"] for r in rows))

# Per-mode distribution summaries
print("\n== per-mode summaries ==")
dist = {}
for m in modes:
    sub = [r for r in rows if r["mode"] == m]
    dist[m] = {}
    for c in NUMERIC_COLS:
        vals = nums(sub, c)
        dist[m][c] = summary(vals)

for c in ["role_pnl", "wallet_sum_pnl", "realizedAbs", "minSpot", "maxSpot", "minCurve", "maxCurve", "x402Total"]:
    print(f"\n  {c}")
    for m in modes:
        s = dist[m][c]
        if s is None:
            continue
        print(f"    {m:10s} mean={s['mean']:+.4e} std={s['std']:.4e} range=[{s['min']:+.4e}, {s['max']:+.4e}] uniq={s['unique']}")

# Per-mode outliers
print("\n== per-mode IQR outlier_pct ==")
outlier_hits = []
for m in modes:
    sub = [r for r in rows if r["mode"] == m]
    for c in NUMERIC_COLS:
        vals = nums(sub, c)
        pct = iqr_outlier_pct(vals)
        if pct > 0:
            outlier_hits.append((m, c, pct, max(abs(v) for v in vals)))
            print(f"  {m:10s} {c:18s} {pct:6.2f}%  max_abs={max(abs(v) for v in vals):.4e}")

# Per-mode correlations
print("\n== per-mode correlations |r|>=0.5 ==")
corr_hits = []
numeric_for_corr = ["seed", "role_pnl", "wallet_sum_pnl", "realizedAbs", "minSpot", "maxSpot", "minCurve", "maxCurve", "settlementLegs", "x402Total"]
for m in modes:
    sub = [r for r in rows if r["mode"] == m]
    cols = {c: nums(sub, c) for c in numeric_for_corr}
    for i, c1 in enumerate(numeric_for_corr):
        for c2 in numeric_for_corr[i + 1:]:
            a = cols[c1]
            b = cols[c2]
            if len(a) != len(b) or len(a) < 3:
                continue
            r = pearson(a, b)
            if r is None:
                continue
            if abs(r) >= 0.5:
                corr_hits.append((m, c1, c2, r))
                print(f"  {m:10s} {c1:14s} x {c2:14s} r={r:+.3f}")

# basket:synth multiplier
print("\n== basket:synth minSpot / maxSpot multiplier ==")
basket = [r for r in rows if r["mode"] == "basket"]
synth = [r for r in rows if r["mode"] == "synthetic"]
# map by seed index
basket_by_seed = defaultdict(list)
for r in basket:
    basket_by_seed[r["seed"]].append(r)
synth_by_seed = defaultdict(list)
for r in synth:
    synth_by_seed[r["seed"]].append(r)
for col in ("minSpot", "maxSpot"):
    ratios = []
    for seed in basket_by_seed:
        if seed in synth_by_seed:
            # basket seed is tagged with mode prefix 1 (as in "202611081"); need to match by the numeric index
            pass
    # Instead: pair basket row with synth row by shared seed-index. The seed column differs per mode.
# simpler: pair by role+order
basket_min_by_role = defaultdict(list)
synth_min_by_role = defaultdict(list)
basket_max_by_role = defaultdict(list)
synth_max_by_role = defaultdict(list)
for r in basket:
    basket_min_by_role[r["role"]].append(float(r["minSpot"]))
    basket_max_by_role[r["role"]].append(float(r["maxSpot"]))
for r in synth:
    synth_min_by_role[r["role"]].append(float(r["minSpot"]))
    synth_max_by_role[r["role"]].append(float(r["maxSpot"]))

for role in ("analyst", "operator", "retail"):
    bmins = basket_min_by_role[role]
    smins = synth_min_by_role[role]
    bmaxs = basket_max_by_role[role]
    smaxs = synth_max_by_role[role]
    if len(bmins) == len(smins):
        ratios_min = [bmins[i] / smins[i] for i in range(len(bmins)) if smins[i] != 0]
        ratios_max = [bmaxs[i] / smaxs[i] for i in range(len(bmaxs)) if smaxs[i] != 0]
        if ratios_min:
            smn = summary(ratios_min)
            print(f"  role={role:8s} minSpot ratio: mean={smn['mean']:.6f} std={smn['std']:.2e} min={smn['min']:.6f} max={smn['max']:.6f} uniq={smn['unique']}")
        if ratios_max:
            smx = summary(ratios_max)
            print(f"  role={role:8s} maxSpot ratio: mean={smx['mean']:.6f} std={smx['std']:.2e} min={smx['min']:.6f} max={smx['max']:.6f} uniq={smx['unique']}")

# Overall multiplier: pair basket row i with synth row i (preserving order in CSV)
print("\n== basket:synth overall multiplier (row-order pairing) ==")
if len(basket) == len(synth):
    rmin = [float(basket[i]["minSpot"]) / float(synth[i]["minSpot"]) for i in range(len(basket)) if float(synth[i]["minSpot"]) != 0]
    rmax = [float(basket[i]["maxSpot"]) / float(synth[i]["maxSpot"]) for i in range(len(basket)) if float(synth[i]["maxSpot"]) != 0]
    print(f"  minSpot ratio: mean={sum(rmin)/len(rmin):.8f} std={statistics.pstdev(rmin):.4e} uniq={len(set(rmin))}")
    print(f"  maxSpot ratio: mean={sum(rmax)/len(rmax):.8f} std={statistics.pstdev(rmax):.4e} uniq={len(set(rmax))}")
    print(f"  first ratios: min={rmin[0]:.8f} max={rmax[0]:.8f}")

# Spread retail top-loss
print("\n== spread top-6 role_pnl (losses) ==")
spread = [r for r in rows if r["mode"] == "spread"]
spread_sorted = sorted(spread, key=lambda r: float(r["role_pnl"]))
for r in spread_sorted[:6]:
    print(f"  seed={r['seed']:>12s}  role={r['role']:8s}  pnl={float(r['role_pnl']):+12.2f}  realizedAbs={float(r['realizedAbs']):.2f}")

print("\n== spread role means ==")
for role in ("analyst", "operator", "retail"):
    v = [float(r["role_pnl"]) for r in spread if r["role"] == role]
    print(f"  {role:8s} mean={sum(v)/len(v):+.2f}  std={statistics.pstdev(v):.2f}  min={min(v):+.2f}  max={max(v):+.2f}")

# synthetic vs x402 role_pnl byte-identity
print("\n== synthetic vs x402 role_pnl identity ==")
synth_sorted = sorted([r for r in rows if r["mode"] == "synthetic"], key=lambda r: (r["seed"], r["role"]))
x402_sorted = sorted([r for r in rows if r["mode"] == "x402"], key=lambda r: (r["seed"], r["role"]))
diffs = 0
for i in range(min(len(synth_sorted), len(x402_sorted))):
    if float(synth_sorted[i]["role_pnl"]) != float(x402_sorted[i]["role_pnl"]):
        diffs += 1
print(f"  n_pairs={len(synth_sorted)} diffs={diffs}")

# x402Total within x402
print("\n== x402Total (x402 mode only) ==")
x402 = [r for r in rows if r["mode"] == "x402"]
vals = [float(r["x402Total"]) for r in x402]
nonzero = [v for v in vals if v != 0]
s = summary(nonzero) if nonzero else None
print(f"  n={len(vals)} non-zero={len(nonzero)}")
if s:
    print(f"  non-zero mean={s['mean']:.4f} std={s['std']:.4f} range=[{s['min']:.4f}, {s['max']:.4f}] uniq={s['unique']}")

# Conservation (wallet_sum_pnl mean/std per mode)
print("\n== conservation (wallet_sum_pnl) ==")
for m in modes:
    vals = [float(r["wallet_sum_pnl"]) for r in rows if r["mode"] == m]
    print(f"  {m:10s} mean={sum(vals)/len(vals):+.4e} std={statistics.pstdev(vals):.4e} min={min(vals):+.4e} max={max(vals):+.4e}")

# Padded-seed analysis (seeds with role_pnl artifacts)
print("\n== seed by-mode uniq ==")
for m in modes:
    seeds = sorted(set(r["seed"] for r in rows if r["mode"] == m))
    print(f"  {m:10s} n_seeds={len(seeds)} sample={seeds[:3]}...{seeds[-3:]}")

# Constants
print("\n== constants (std=0) per mode ==")
for m in modes:
    sub = [r for r in rows if r["mode"] == m]
    for c in NUMERIC_COLS:
        vals = nums(sub, c)
        if vals and statistics.pstdev(vals) == 0:
            print(f"  {m:10s} {c:18s} = {vals[0]}")

# Prior-day comparison
if prior:
    print(f"\n=== vs prior {PRIOR_CSV} ===")
    print(f"  rows: {len(prior)} -> {len(rows)}  cols: {len(prior[0])} -> {len(rows[0])}")
    prior_modes = sorted(set(r["mode"] for r in prior))
    print(f"  modes: {prior_modes} -> {modes}")
    print("\n  basket:synth maxSpot ratio prior-day:")
    pb = [r for r in prior if r["mode"] == "basket"]
    ps = [r for r in prior if r["mode"] == "synthetic"]
    if len(pb) == len(ps):
        prm = [float(pb[i]["maxSpot"]) / float(ps[i]["maxSpot"]) for i in range(len(pb)) if float(ps[i]["maxSpot"]) != 0]
        print(f"    prior maxSpot ratio mean={sum(prm)/len(prm):.8f}")
