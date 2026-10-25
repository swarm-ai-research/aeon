# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding

---

### 2026-08-09

**Track A — DePIN proxy** (n=158 log-return days, 180d price window ending 2026-08-09)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | -0.121 | 0.132 | null |
| TAO | -0.117 | 0.148 | null |
| IO | -0.039 | 0.633 | null |

Wider descriptive matrix (partial ρ vs all non-control macros, ⊥ {BTC,SOL}):

| token | ETH | NATGAS | CL_WTI | BRENT | COPPER | PLATINUM | PALLADIUM | GOLD | SILVER | EUR | JPY |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RENDER | 0.147(0.068) | -0.121(0.132) | 0.104(0.198) | 0.058(0.475) | 0.012(0.880) | -0.001(0.990) | -0.027(0.740) | 0.028(0.729) | -0.012(0.879) | -0.116(0.150) | 0.123(0.126) |
| TAO | -0.046(0.572) | -0.116(0.148) | 0.005(0.955) | 0.004(0.965) | -0.105(0.192) | -0.113(0.162) | -0.137(0.088) | -0.062(0.445) | -0.023(0.773) | -0.110(0.173) | -0.013(0.869) |
| IO | 0.054(0.502) | -0.039(0.633) | -0.016(0.847) | -0.037(0.650) | 0.073(0.368) | -0.002(0.981) | 0.024(0.769) | 0.006(0.945) | 0.025(0.758) | 0.056(0.488) | -0.030(0.709) |

Format: ρ(p). No signal across the basket reaches the 0.15 weak-signal threshold except RENDER/ETH (ρ=0.147, p=0.068) — residual ETH beta after BTC+SOL partialling; not tested, purely descriptive.

**Track B — sweep P&L** (n=50 joined days, 2026-06-06→2026-08-08; 4 modes)

| mode | n | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---:|---|
| basket | 50 | -0.118 | 0.424 | null |
| spread | 50 | -0.026 | 0.859 | null |
| synthetic | 50 | -0.080 | 0.590 | null |
| x402 | 50 | -0.080 | 0.590 | null |

Notes: `synthetic` and `x402` analyst P&L series are identical (same mean across all 50 days), suggesting x402 currently routes through the synthetic clearing path. Track B fired for the first time this run (n=50 ≥ 30); no prior snapshot to compare for consecutive-reads flagging.

**Headline: Track A all null (3/3 tokens), Track B all null (4/4 modes). Pre-registered NATGAS test holds.**

---

### 2026-08-16

**Track A — DePIN proxy** (n=180)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | −0.1096 | 0.1435 | null |
| TAO | −0.1167 | 0.1191 | null |
| IO | −0.0712 | 0.3436 | null |

All three tokens show weak negative partial correlations with NATGAS after controlling for BTC and SOL crypto-beta. No signal clears the 0.15 threshold. Consistent with the prior 181d null reported in [[compute-macro-correlation-findings]].

**Track B — sweep P&L** (n=57 joined days, ≥30 threshold met)

| mode | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| basket | −0.0475 | 0.7308 | null |
| spread | −0.0156 | 0.9100 | null |
| synthetic | −0.0466 | 0.7357 | null |
| x402 | −0.0466 | 0.7357 | null |

Track B fires for the first time (n=57 ≥ 30). All four modes show near-zero partial correlations with NATGAS; p-values are large (0.73–0.91). synthetic ≡ x402 numerically, consistent with [[compute-futures-eda]] role-level identity. No sweep mode shows any NATGAS signal net of crypto-beta.

**Failures:** BRENT and PALLADIUM returned 166 days (vs 181 for other series) — non-mandatory, retained with shorter history. No primary series failures.

**Consecutive-reads check:** first snapshot — no prior week to compare. No flagged findings.

---

### 2026-08-23

**Track A — DePIN proxy** (n=172)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | −0.1280 | 0.0962 | null |
| TAO | −0.1303 | 0.0904 | null |
| IO | −0.0305 | 0.6932 | null |

All three DePIN tokens remain null vs NATGAS partial ρ after controlling for {BTC, SOL}. RENDER and TAO drift slightly deeper negative (from −0.11/−0.12 on 08-16 to −0.13/−0.13), but neither clears the 0.15 threshold. IO flattens toward zero (from −0.07 to −0.03). No signal. n=172 after joint dropna across all 16 symbols (181 raw candles each; BRENT and PALLADIUM at 173 days — both non-primary, present).

**Track B — sweep P&L** (n=60 joined days)

| mode | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| basket | −0.1123 | 0.4013 | null |
| spread | +0.0811 | 0.5450 | null |
| synthetic | −0.0948 | 0.4789 | null |
| x402 | −0.0948 | 0.4789 | null |

Track B n grows from 57 → 60 (3 new CSV days: 08-20, 08-21, 08-22). All four modes null; p-values 0.40–0.55. spread sign flips +/− vs 08-16 (from −0.016 to +0.081) but magnitude remains small. synthetic ≡ x402 numerically (role-level identity confirmed again). No NATGAS signal net of crypto-beta in any sweep mode.

**Consecutive-reads check:** prior week (08-16) Track A: RENDER −0.11, TAO −0.12, IO −0.07 (all null); Track B: all modes |ρ|<0.05 (all null). This week: same null class. No signal clears the 0.15 threshold in either snapshot — consecutive-reads rule never activates. No flagged findings.

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

---

### 2026-09-27

**Track A — DePIN proxy** (n=180, date range 2026-03-31 → 2026-09-27)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | -0.2047 | 0.0055 | weak signal |
| TAO | -0.1573 | 0.0346 | weak signal |
| IO | -0.0078 | 0.9181 | null |

Note: RENDER and TAO show a negative partial correlation vs NATGAS after controlling for crypto-beta — both statistically significant (p<0.05) but both below the |ρ|≥0.25 flagging threshold. IO is clean null. This is the first snapshot; prior MEMORY note described the token-level result as "clean null" at 181d (earlier window); the weak signals in RENDER/TAO are borderline and require a second consecutive read before elevation.

**Track B — sweep P&L** (n=94 joined days, range 2026-06-06 → 2026-09-27)

| mode | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| basket | -0.1082 | 0.3019 | null |
| spread | +0.1062 | 0.3110 | null |
| synthetic | -0.0996 | 0.3423 | null |
| x402 | -0.0996 | 0.3423 | null |

All sweep modes return null. No mode clears the noise floor at this sample size.

**Wider descriptive (partial ρ vs non-NATGAS macros, RENDER only):**
ETH: +0.155 (p=0.037), COPPER: +0.125 (p=0.095). All others null. Not pre-registered — descriptive only, no claims.

**Consecutive-reads flagging**: First snapshot. No prior entry to compare. No findings elevated.
