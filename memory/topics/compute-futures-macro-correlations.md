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
