# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding

---

### 2026-06-20

Price data: Hyperliquid candleSnapshot, 1d, trailing 180d window. Returns shape: n=108 (2026-03-05 to 2026-06-20; n reduced from 181 raw days because NATGAS is a commodity with trading calendar gaps — dropna(how="any") removes crypto days with no NATGAS candle). Controls: {BTC, SOL}.

**Track A — DePIN proxy** (n=108)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | -0.1446 | 0.1391 | null |
| TAO | -0.1210 | 0.2166 | null |
| IO | -0.0693 | 0.4802 | null |

Descriptive note: RENDER shows the largest |ρ| at -0.145, approaching but not crossing the 0.15 null threshold. All p-values are well above 0.05. The consistent negative sign across tokens is directionally interesting (compute tokens slightly underperform on high-NATGAS-return days after removing crypto-beta) but not statistically meaningful at this n.

Wider descriptive partial-ρ (all macros, ctrl={BTC,SOL}):
- RENDER: EUR -0.151 (p=0.123), JPY +0.157 (p=0.108), NATGAS -0.145 (p=0.139) — highest non-crypto correlations are FX, not energy
- TAO: COPPER -0.157 (p=0.107), PALLADIUM -0.142 (p=0.145), EUR -0.140 (p=0.154) — metals negative, no energy
- IO: no macro factor above |ρ|=0.10

**Track B — sweep P&L**: n=1, deferring (<30). Single-day proof from 2026-06-20: modes [synthetic, basket, spread, x402], mean analyst P&L — synthetic $6.06, basket $18.08, spread $4064.80, x402 $6.06. Conservation check: wallet_sum_pnl ≈ 0 on all runs (zero-sum confirmed).
