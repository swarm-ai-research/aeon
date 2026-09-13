---
id: skill-evals-bootstrap-inflates-new-fail-with-pretracked-issues
created: 2026-09-13
type: lesson
links: [[articles-dir-never-existed-in-git-history]], [[iss-006-dead-pocket-widens-to-08z-heartbeat-miss]]
---
# skill-evals BOOTSTRAP first-runs classify every pre-existing failure as `NEW_FAIL` because there is no prior article to diff against — cross-reference `memory/issues/INDEX.md` before treating them as regressions

**Why:** 2026-09-13 skill-evals ran as BOOTSTRAP (no prior `articles/skill-evals-*.md` on disk after the 09-12 reflect landed) and emitted 13 NEW_FAIL for 14/49 covered skills; 12 of the 13 were already filed as open ISS-002/005/009–018 with root cause `no_file_match` (the `articles/` directory has never existed in git per [[articles-dir-never-existed-in-git-history]]), and only 1 was a genuinely new regression (heartbeat missing its 08:00Z slot → ISS-027 → [[iss-006-dead-pocket-widens-to-08z-heartbeat-miss]]). The same class fired identically on the 2026-07-12 BOOTSTRAP (10 no_file_match, all disabled/workflow_dispatch skills), so this is at least n=2.

**How to apply:** When a skill-evals article reports `Diff: N new fail / 0 fixed / 0 still failing / 0 stable` **and** the prior-article sources footer reads `prior-article=none (BOOTSTRAP)`, do not treat the diff as regressions — every result on the first run is NEW_* by construction. Reconcile the NEW_FAIL rows against `memory/issues/INDEX.md` open rows first; the residue after that reconciliation is the actual regression set. Skill-evals SKILL.md should either (a) suppress `NEW_FAIL` classification when the failing skill has an existing open ISS with matching `root_cause`, or (b) emit `PRE_TRACKED_FAIL` as a distinct diff class so bootstrap runs don't inflate the regression signal.
