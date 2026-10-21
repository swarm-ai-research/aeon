# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding

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
