# AGI Tracker

A public GitHub Pages site that models frontier-agent capability via METR time-horizon measurements and scores predictions from Aschenbrenner's *Situational Awareness*. Built 2026-06-10. Weekly skill refreshes the data and re-scores the scorecard.

## Surface
- [[agi-tracker-site]] — interactive page at `docs/agi-tracker/index.html`
- [[agi-tracker-data-model]] — `data.js` is the canonical store
- [[agi-tracker-weekly-skill]] — Mon 13:00 UTC refresh in `skills/agi-tracker/`
- [[aschenbrenner-8-claim-scorecard]] — eight *Situational Awareness* claims tracked

## Methodology
- [[metr-doubling-3-5mo]] — current central fit (Jan-2024 → Feb-2026, ~3.5 mo, ≈10×/yr)
- [[metr-doubling-4-38mo]] — earlier TH1.1 fit, now the slow-tail estimate (superseded 2026-06-29)
- [[metr-saturates-above-16h]] — benchmark suite reliability ceiling (Opus 4.6 + Mythos Preview both saturating)
- [[metr-flags-reward-hacking-predeployment]] — methodology pattern for unrobust predeployment evals (GPT-5.6 Sol)

## Snapshot (as of 2026-06-29)
| Metric | Value |
|---|---|
| Mon 13:00 slot status | **fired** 2026-06-29 — first hit after 2026-06-15 + 2026-06-22 misses; 19-day data gap closed |
| Anchor (latest reliable, non-saturating) | Gemini 3.1 Pro · 6.4 h · 2026-02 |
| METR central doubling (Jan-2024→Feb-2026) | ~3.5 mo (~105 d, ≈10×/yr) |
| 2025-only trend | ~3.0 mo |
| Long-run 2019–2025 | ~7.0 mo |
| Points added this run | GPT-5.2 (high) 352m / 2025-12-11; Gemini 3.1 Pro 384m / 2026-02-19; Claude Mythos Preview 1045m / 2026-04-07 |
| Promoted | GPT-5.3 Codex estimate → measured (390 → 350m) |
| Refreshed `saturating` | Claude Opus 4.6 870 → 719m (TH1.1) — 12.0 h |
| Mythos Preview horizon | ~17.4 h *(saturating, CI 8.5–55h)* |
| GPT-5.6 Sol (predeployment, METR flagged unrobust) | ~11.3 h — notes-only, see [[metr-flags-reward-hacking-predeployment]] |
| "Year-long programs" projection — 3.0 mo doubling | ~May 2028 |
| "Year-long programs" projection — 3.5 mo doubling | ~Sep 2028 |
| "Year-long programs" projection — 4.3 mo doubling | ~Feb 2029 |
| "Year-long programs" projection — 7.0 mo doubling | ~2031 |
| Branch | `agi-tracker/2026-06-29` pushed; PR creation blocked by repo policy (same App perm gap) |

## Pending candidates (for future refresh)
- **GPT-5.4** — METR-added 2026-04-10, no official 50%-horizon yet on the mirror.
- **GPT-5.5** — released June 2026, METR measurement pending.
- **GPT-5.6 Sol / Terra / Luna** — METR predeployment 2026-06-26 but explicitly unrobust; recheck for a clean post-release measurement.
- **DeepSeek-V4-Pro / V4-Flash** — released June 2026, no METR yet.
- **Claude Mythos 5 / Fable 5** — released 2026-06-09 (Mythos 5 briefly available, then withdrawn). Distinct SKU from Mythos Preview already in `points[]`. Recheck when METR publishes.
- **Grok 4.3** — on Bedrock; METR measurement TBD.

## Adjacent tooling caveats
- [[generate-skills-json-newline-bug]] — generator splices raw `\n` for skills with two schedules
- [[skills-json-count-drift]] — committed `skills.json` lags on-disk count
