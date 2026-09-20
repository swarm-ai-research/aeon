# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding

---

### 2026-08-16

**Track A — DePIN proxy** (n=180)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | −0.1096 | 0.1435 | null |
| TAO | −0.1167 | 0.1191 | null |
| IO | −0.0712 | 0.3436 | null |

All three tokens showed weak negative partial correlations with NATGAS after controlling for crypto-beta. No signal cleared the 0.15 threshold.

**Track B — sweep P&L** (n=57 joined days)

| mode | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| basket | −0.0475 | 0.7308 | null |
| spread | −0.0156 | 0.9100 | null |
| synthetic | −0.0466 | 0.7357 | null |
| x402 | −0.0466 | 0.7357 | null |

First Track B fire (n=57 ≥ 30). All four modes near-zero; p-values 0.73–0.91.

**Consecutive-reads check:** first snapshot — no prior week. No flagged findings.

---

### 2026-09-20

**Track A — DePIN proxy** (n=180)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | −0.2098 | 0.0044 | weak signal |
| TAO | −0.1599 | 0.0316 | weak signal |
| IO | −0.0367 | 0.6257 | null |

RENDER and TAO both clear the 0.15 threshold this week — both negative (higher NATGAS returns associate with lower RENDER/TAO returns after removing crypto-beta). RENDER's partial ρ has moved from −0.110 (null, 2026-08-16) to −0.210 (weak signal), a meaningful step-up over 35 days. TAO moved from −0.117 to −0.160. Neither crosses 0.25; neither triggers the flagged consecutive-read rule.

Wider partial-corr inspection (DEPIN vs all non-control macros, ctrl={BTC,SOL}):
- RENDER is selective: NATGAS is the strongest signal (−0.210, p=0.004); ETH residual shows a secondary positive partial (0.169, p=0.023); all commodity/FX macros are null.
- TAO: NATGAS is the only signal (−0.160, p=0.032); everything else null.
- IO: no signal anywhere in the macro basket (all |ρ| < 0.09, all p > 0.24).

**Track B — sweep P&L** (n=88 joined days)

| mode | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| basket | −0.0917 | 0.3985 | null |
| spread | 0.0783 | 0.4716 | null |
| synthetic | −0.0682 | 0.5310 | null |
| x402 | −0.0682 | 0.5310 | null |

Track B null across all modes for the second consecutive snapshot (n=88, up from n=57). synthetic ≡ x402 numerically — consistent with role-level identity noted in [[compute-futures-eda]]. The sweep P&L shows no NATGAS signal at either the token-price or marketplace-clearing level.

**Consecutive-reads check:**
- RENDER: current |ρ|=0.210 < 0.25 → does not meet flagged threshold. No consecutive-read trigger.
- TAO: current |ρ|=0.160 < 0.25 → same.
- Track B: all null both snapshots.

No flagged findings this week. Headline: **Track A RENDER and TAO show weak negative partial correlations with NATGAS (ρ=−0.21/−0.16); Track B all null.**

**Watch:** RENDER is trending toward the 0.25 threshold (−0.110 → −0.210 over 35 days). If it crosses 0.25 with p<0.05 on next snapshot, and this week's reading (−0.210, p<0.10) satisfies the prior-week condition, that would trigger a flagged notification.
