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

All three tokens null. Negative sign on RENDER/TAO directionally consistent with [[compute-macro-correlation-findings]] prior. Wide 30-cell descriptive scan (3 tokens × 10 non-crypto macros, controlled on {BTC, SOL}): all null at n=137. Track B: n=28, deferring — 3 early CSVs (2026-06-06/08/09) skipped on schema mismatch.

**Track B — sweep P&L**: n=28, deferring (<30)

---

### 2026-08-02

**Track A — DePIN proxy** (n=151, 2026-03-05 → 2026-08-02)

| token | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| RENDER | −0.1185 | 0.148 | null |
| TAO | −0.1162 | 0.156 | null |
| IO | −0.0300 | 0.716 | null |

All three tokens null. Directionally consistent with 07-19 snapshot (negative sign on RENDER/TAO persists; IO near-zero). Wide descriptive scan: one non-null cell — TAO × PALLADIUM ρ=−0.153 p=0.060 (weak signal, descriptive only; PALLADIUM is not the pre-registered test asset and is not independent of crypto-beta). All other 29 cells null.

**Track B — sweep P&L** (n=43, FIRST FIRE — crossed 30-day threshold)

| mode | partial ρ NATGAS ⊥ {BTC,SOL} | p | verdict |
|---|---:|---:|---|
| basket | −0.1369 | 0.391 | null |
| spread | +0.1144 | 0.475 | null |
| synthetic | −0.1003 | 0.532 | null |
| x402 | −0.1003 | 0.532 | null |

All four sweep modes null on first fire. synthetic/x402 return identical ρ (same analyst P&L series — verify whether mode separation is functioning correctly in the sweeper). No mode approaches the 0.25/0.05 threshold.

**Consecutive-read status:** Track A 2nd snapshot, all null. Track B 1st fire, all null. No flagged finding — notification threshold not met.
