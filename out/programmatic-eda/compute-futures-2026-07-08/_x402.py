import pandas as pd
df = pd.read_csv("memory/gitlawb-compute-futures-proofs/2026-07-08.csv")
x = df[df["mode"] == "x402"]
xt = x["x402Total"]
print(f"x402 rows: {len(x)}")
print(f"x402Total non-zero rows: {(xt > 0).sum()}")
print(f"x402Total range: ${xt[xt > 0].min():.2f} - ${xt[xt > 0].max():.2f}")
print(f"x402Total mean (non-zero): ${xt[xt > 0].mean():.2f}, total sum: ${xt.sum():.2f}")
print()
print("wallet_sum_pnl per mode range:")
for m in ["basket","spread","synthetic","x402"]:
    sub = df[df["mode"] == m]["wallet_sum_pnl"]
    print(f"  {m}: mean={sub.mean():.3e}, std={sub.std():.3e}, min={sub.min():.3e}, max={sub.max():.3e}")
print()
print("seed encoding: unique seeds =", df["seed"].nunique())
print("seed str lens:", df["seed"].astype(str).str.len().value_counts().to_dict())
print()
print("Live/settlement/spotSource per mode:")
print(df.groupby("mode")[["live","settlement","spotSource"]].agg(lambda s: s.unique().tolist()).to_string())
print()
print("row counts by mode:", df["mode"].value_counts().to_dict())
print("row counts by role:", df["role"].value_counts().to_dict())
