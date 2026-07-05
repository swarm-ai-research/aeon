# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding

---

### 2026-07-05

**Track A — DePIN proxy** (n=123 effective; 180d window, dropna on full column set reduces to 123 due to NATGAS/BRENT/PALLADIUM gaps)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | -0.1243 | 0.1742 | null |
| TAO | -0.1039 | 0.2568 | null |
| IO | -0.0471 | 0.6081 | null |

**Track B — sweep P&L**: n=16, deferring (<30)

Sweep proof CSVs available: 2026-06-06 through 2026-07-05 (19 files, 16 parseable join days after inner-joining with return series). Modes present: basket, spread, synthetic, x402.

Headline: Track A all null (consistent with [[compute-macro-correlation-findings]] prior). No flagged consecutive-read signals. Track B defers — needs 14 more joined days.
