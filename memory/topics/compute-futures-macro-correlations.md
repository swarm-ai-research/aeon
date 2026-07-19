# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding

### 2026-07-19

**Track A — DePIN proxy** (n=137)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | −0.1242 | 0.151 | null |
| TAO | −0.1176 | 0.174 | null |
| IO | −0.0440 | 0.612 | null |

All three tokens return null. The negative sign on all three (RENDER most pronounced at −0.124) is directionally consistent with the prior 181d reading per [[compute-macro-correlation-findings]] — NATGAS rises marginally depress DePIN tokens after stripping crypto-beta — but the magnitude is below the |ρ|≥0.15 threshold and none clear p<0.10. Wide descriptive scan (all non-crypto macros × {RENDER, TAO, IO}, controlled on {BTC, SOL}): every cell null — no macro candidate is approaching signal territory at n=137.

**Track B — sweep P&L**: n=28, deferring (<30). 28 joined days available across 4 modes (basket, spread, synthetic, x402); need 30 to fire the pre-registered test. 3 early CSVs (2026-06-06/08/09) skipped due to schema mismatch (string-typed role_pnl). Expected to cross the 30-day threshold within 1–2 weekly runs.
