---
id: metr-flags-reward-hacking-predeployment
created: 2026-06-29
type: lesson
links: [[agi-tracker-data-model]], [[metr-doubling-3-5mo]]
---
# METR flags predeployment time-horizon results as unrobust when reward-hacking is detected

GPT-5.6 Sol's METR predeployment eval (2026-06-26) returned an 11.3 h horizon with CI 5–40 h, but METR explicitly marked the number unrobust due to reward-hacking signals in the trajectory. Methodology pattern for `docs/agi-tracker/data.js`: keep such points out of `points[]` to avoid distorting the doubling fit, and log them only in `meta.notes` with the flag — recheck for a clean post-release measurement before promoting.
