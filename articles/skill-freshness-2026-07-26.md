# Skill Freshness — 2026-07-26

**Verdict:** ✅ FRESHNESS_OK — all 12 tracked dependencies within freshness thresholds

*Audited 44 enabled skills · 12 dependencies checked · 0 flagged*

## Flagged dependencies

*(None — all dependencies are fresh.)*

## Healthy consumers

- surplus-pulse — 2 deps (surplus-pulse.md, projects.md¹), both fresh.
- compute-pulse — 1 dep (compute-pulse.md), fresh.
- compute-futures-eda — 1 dep (memory/topics/compute-futures-eda/2026-07-25.md), 24h old, OK.
- compute-macro-correlate — 1 dep (compute-futures-macro-correlations.md¹), fresh.
- ai-framework-watch — 1 dep (framework-watch-state.json¹), fresh.
- cost-report — 1 dep (memory/token-usage.csv), fresh.
- skill-graph — 1 dep (skill-graph-state.json¹), fresh.
- heartbeat / batch-health / skill-health — read memory/cron-state.json, fresh.

¹ File absent on disk — implicit reference that never existed (self-bootstrapping on first run). Per spec, implicit-only MISSING is not flagged; see ignored_count below.

+ 36 more all-fresh consumers (no non-trivial cross-skill file deps detected in their SKILL.md files after filtering self-references and disabled-producer patterns).

## What this means per consumer

All consumers verified at OK across every dependency class. No action required.

**Notable non-flags (for operator awareness):**

- **compute-futures-eda** — writes `memory/topics/compute-futures-eda/${SWEEP_DATE}.md` daily at 06:00 UTC. Most recent file is `2026-07-25.md` (24h old). Threshold is 168h. ✅ OK.
- **memory/topics/framework-watch-state.json** — read by `ai-framework-watch` (Mon 08:30). File does not exist on disk. Classified implicit (self-bootstrapping: skill creates it if absent). Not flagged as MISSING per spec.
- **memory/topics/compute-futures-macro-correlations.md** — read+written by `compute-macro-correlate` (Sun 06:30). File not on disk. Implicit, self-bootstrapping. Not flagged.
- **memory/topics/projects.md** — read by `surplus-pulse` (daily 16:30). File not on disk. Implicit, self-bootstrapping. Not flagged.
- **memory/topics/skill-graph-state.json** — read by `skill-graph` (Sun 17:00). File not on disk. Implicit, self-bootstrapping. Not flagged.
- **articles/ directory** — does not exist. No enabled skill was found to have a canonical `articles/{other-producer}-${today}.md` cross-skill consumption pattern (all article references in SKILL.md files are either self-referential or reference disabled producers). Zero MISSING flags from this class.

## Source status

- `aeon.yml`: 127 skill entries, 44 enabled
- Explicit `chains: consume:` edges: 0 (all chains blocks commented out)
- Implicit references discovered: 12 (after filtering self-refs and disabled-producer patterns)
- Files not yet on disk (skipped — implicit references that never existed): 4

## ⚠ Structural limitation: mtime accuracy in snapshot environment

This run executed against a snapshot checkout (`6eebfc3 snapshot: rsavitt/aeon @ fa89d8c`, committed 2026-07-26T07:03:35Z). All files share the same git commit timestamp (~1.9h ago at run time), so `git log -1 --format=%ct` cannot distinguish file ages within the snapshot. This is the documented [[skill-freshness-mtime-blind-in-gha]] issue (MEMORY.md pointer: "Fix skill-freshness to use git log -1 --format=%ct instead of stat --format=%Y").

**Mitigation applied:** For `memory/topics/compute-futures-eda/`, filename dates were used as a secondary proxy (most recent: `2026-07-25.md`). All other files were scored by git timestamp (uniformly ~1.9h → OK). This means true staleness is undetectable by timestamp alone in this environment. A future run from the live repo (not a snapshot checkout) will recover accurate per-file ages.

---
*Companion to `skill-health` (per-skill failure detection) and `heartbeat` (per-run pulse). This skill catches the silent-staleness gap those two cannot: a consumer reading a stale file with no API errors and a 100% pass rate. Methodology: every age and threshold is computed from on-disk mtimes — this skill measures nothing it does not also report.*
