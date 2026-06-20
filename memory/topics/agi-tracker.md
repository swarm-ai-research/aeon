# AGI Tracker

Public GitHub Pages site modeling frontier-agent capability and scoring
Aschenbrenner's *Situational Awareness* predictions. Initial build: 2026-06-10.

## Files
- `docs/agi-tracker/index.html` — self-contained interactive page: log-scale chart of METR 50% time horizons, adjustable doubling-time projection (slider + presets 3.0 / 4.3 / 7.0 mo), milestone table (workday → work-year tasks), Situational Awareness scorecard, caveats.
- `docs/agi-tracker/data.js` — data model: 20 time-horizon points (GPT-2 → Claude Opus 4.6), milestones, scenarios, 8-claim scorecard. Single source of truth for the page.
- `skills/agi-tracker/SKILL.md` — weekly skill (Mon 13:00 UTC, enabled in `aeon.yml`): pulls new METR measurements, re-scores the scorecard, PRs updates to `data.js`.

## Key numbers (as of 2026-06-10)
- Fitted post-2023 doubling: **4.38 mo** (matches METR TH1.1's 4.3).
- Anchor: ~6.6 h at 2026-03.
- "Year-long programs" milestone projects to **2028-03** (3.0 mo doubling) / **2029-02** (4.3 mo) / **2030-12** (7.0 mo).
- METR flags >16 h estimates as unreliable (suite saturation); Opus 4.6's 14.5 h point marked `saturating`.
