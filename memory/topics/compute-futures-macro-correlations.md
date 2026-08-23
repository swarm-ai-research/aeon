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
