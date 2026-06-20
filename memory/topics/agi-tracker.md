# AGI Tracker

A public GitHub Pages site that models frontier-agent capability via METR time-horizon measurements and scores predictions from Aschenbrenner's *Situational Awareness*. Built 2026-06-10. Weekly skill refreshes the data and re-scores the scorecard.

## Surface
- [[agi-tracker-site]] — interactive page at `docs/agi-tracker/index.html`
- [[agi-tracker-data-model]] — `data.js` is the canonical store
- [[agi-tracker-weekly-skill]] — Mon 13:00 UTC refresh in `skills/agi-tracker/`
- [[aschenbrenner-8-claim-scorecard]] — eight *Situational Awareness* claims tracked

## Methodology
- [[metr-doubling-4-38mo]] — fitted post-2023 doubling time
- [[metr-saturates-above-16h]] — benchmark suite reliability ceiling

## Snapshot (as of 2026-06-10)
| Metric | Value |
|---|---|
| Anchor time horizon (2026-03) | ~6.6 h |
| Fitted doubling (post-2023) | 4.38 mo |
| METR TH1.1 doubling | 4.3 mo |
| Opus 4.6 horizon | 14.5 h *(saturating)* |
| "Year-long programs" projection — 3.0 mo doubling | 2028-03 |
| "Year-long programs" projection — 4.3 mo doubling | 2029-02 |
| "Year-long programs" projection — 7.0 mo doubling | 2030-12 |

## Adjacent tooling caveats
- [[generate-skills-json-newline-bug]] — generator splices raw `\n` for skills with two schedules
- [[skills-json-count-drift]] — committed `skills.json` lags on-disk count
