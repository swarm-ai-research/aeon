---
id: articles-dir-never-existed-in-git-history
created: 2026-09-02
type: lesson
links: [[swarm-safety-eval-empty-writes-log-not-article]], [[skill-freshness-mtime-blind-in-gha]], [[janitor-outputs-mtime-blind-on-gha-runners]]
---
# The `articles/` directory has never existed in git history — 68 SKILL.md files write to it, which is the root cause of 13 `no_file_match` ISS tickets (ISS-002/005/008–018)

Discovered 2026-08-30 self-review: `git ls-files | grep -c '^articles/'` returns 0, yet 68 SKILL.md files reference `articles/${skill}-*.md` as their output path. The 13 `no_file_match` ISS tickets filed by `skill-evals` between 2026-06-20 and 2026-07-12 are not per-skill regressions — they are the same structural class fired 13 times because the parent directory doesn't exist on disk, so every write silently no-ops (GHA sandbox does not auto-mkdir on `>` redirect and the `.gitkeep` was never added). Fix path: materialize `articles/.gitkeep` in one PR, then re-run `skill-evals` — expect a cascade close of ISS-002/005/008–018 once same-day file-match hits.
