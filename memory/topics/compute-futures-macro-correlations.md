# Compute × Macro — weekly partial-correlation log

Pre-registered test (see [[compute-macro-correlation-findings]]):
- Track A — DePIN-token proxy (RENDER/TAO/IO vs NATGAS, control {BTC, SOL}). Runs weekly, n>180d.
- Track B — sweep P&L per mode (defers until n≥30 joined days).

Verdict rules:
- |ρ| < 0.15 → null
- 0.15 ≤ |ρ| < 0.25 → weak signal (note but don't claim)
- |ρ| ≥ 0.25 AND p < 0.05 → flagged; require 2 consecutive snapshots before notifying as a real finding

---

### 2026-07-12

**Track A — DePIN proxy** (n=130, log-returns after inner-join on all 16 columns; 181 candles fetched, 130 complete rows after NATGAS/BRENT/PALLADIUM gaps)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | −0.125 | 0.161 | null |
| TAO | −0.118 | 0.186 | null |
| IO | −0.056 | 0.530 | null |

Wider partial-corr scan (ctrl={BTC,SOL}) — no non-NATGAS macro hits ≥0.15 for TAO or IO. RENDER vs ETH: r=+0.150, p=0.092 — borderline weak, not flagged (p>0.05).

**Track B — sweep P&L**: n=25, deferring (<30). Modes tracked: basket, spread, synthetic, x402. Sweep CSVs span 2026-06-06 to 2026-07-12; 5 more joined-day observations needed to unlock.
