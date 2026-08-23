---
id: janitor-outputs-mtime-blind-on-gha-runners
created: 2026-08-23
type: lesson
links: [[skill-freshness-mtime-blind-in-gha]], [[aeon-skills-dispatch-via-messages-yml]]
---
# `janitor`'s 14d `.outputs/` mtime rule never fires on GHA — `actions/checkout` resets every tracked file's mtime to the run instant

On 2026-08-23 janitor scanned `.outputs/` (41 files) with a 14d TTL rule and deleted 0 — every mtime was ~0s (checkout time) despite many outputs being weeks old on `main`. Same structural GHA blind spot as [[skill-freshness-mtime-blind-in-gha]], different skill: any TTL check keyed on `stat` mtime for git-tracked files silently never triggers on ephemeral runners. Fix candidate: fall back to `git log -1 --format=%ct -- <file>` producer-commit timestamp, or embed a date suffix in filenames at write time so filename-parse works when mtime lies.
