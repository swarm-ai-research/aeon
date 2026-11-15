## Summary

**Executed stale-content-pr-sweeper for 2026-11-15.**

- Open PRs scanned: 15
- TRACKED-prefix date-stamped candidates: 3 (`notegraph/2026-11-08` #115, `notegraph/2026-10-29` #114, `notegraph/2026-10-26` #107)
- Eligible after author filter: **0** — all three are authored by `app/github-actions`, which is not in `ALLOWED_AUTHORS = {"aeonframework"}`
- PRs closed: **0**
- Notify: not fired (steady-state rule — zero closes = no notify)

**Files modified:** `memory/logs/2026-11-15.md` (created).

**Follow-up:** The author-allowlist defect from [[stale-content-pr-sweeper-default-author-filter-closes-zero-prs]] re-engaged today, and for the first time in the series it is suppressing a **non-zero** close count — the `notegraph/*` group has refilled to 3 entries with 2 stale candidates (#114 at 17d, #107 at 20d), both past the ≥2d min-age gate. The blast-radius-bounded claim from 10-29 no longer holds at n=2 cadence. The pending SKILL patch in the action queue (add `"app/github-actions"` to `ALLOWED_AUTHORS`) has gained urgency and should land before the next cadence tick.
