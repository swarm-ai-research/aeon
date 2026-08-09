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
