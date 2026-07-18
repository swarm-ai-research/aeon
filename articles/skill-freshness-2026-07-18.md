# Skill Freshness — 2026-07-18

**Verdict:** ✅ FRESHNESS_OK — all 2 tracked dependencies are within their freshness windows

*Audited 44 enabled skills · 2 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies are within threshold.)*

## Healthy consumers

- pr-tracker — 1 dep (`memory/topics/pr-status.md`, 0.1h, thresh 168h), all fresh.
- stale-content-pr-sweeper — 1 dep (`memory/state/notegraph.json`, 0.1h, thresh 720h), all fresh.
- + 42 more all-fresh consumers (no implicit on-disk deps discovered for their SKILL.md refs — either self-references, non-existent files skipped per policy, or producers with on-demand cadence).

## Source status

- `aeon.yml`: 44 entries enabled (of ~180+ total)
- Implicit references discovered (surviving filter): 11 total; 2 existed on disk and were scored
- Explicit `chains: consume:` edges: 0 (all chain blocks are commented out in aeon.yml)
- Files not yet on disk (skipped — implicit references that never existed): 9

## Known limitation: GHA mtime blind spot

All 2 tracked dependencies report ~0.1h age because GitHub Actions `git checkout` sets every file's mtime to the checkout time, not the file's actual last-written timestamp. The ages above reflect "time since this workflow's checkout" — not "time since the file was last meaningfully updated."

Per [[skill-freshness-mtime-blind-in-gha]], the correct fix is to use `git log -1 --format=%ct -- <path>` instead of `stat --format=%Y`. However, this repo currently contains a single snapshot commit (`d4892f9`), so git log would return the same timestamp for every file regardless. The structural fix (running this skill on a repo with incremental commits rather than daily snapshots) is the long-term path.

**Practical consequence:** This skill cannot currently detect staleness from mtime in this environment. It CAN detect:
1. Explicitly-consumed chain outputs that are MISSING (no chain consume edges currently active)
2. Canonical `articles/{producer}-${today}.md` files that are MISSING for daily/weekly producers — but the two canonical-pattern references found (`articles/vuln-scan-*.md` and `articles/fleet-status-*.md`) point to producers not defined in aeon.yml, so they are treated as on-demand and not flagged.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
