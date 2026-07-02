---
id: skill-freshness-mtime-blind-in-gha
created: 2026-07-02
type: lesson
links: [[gha-messages-yml-cron-underdelivery]], [[aeon-skills-dispatch-via-messages-yml]]
---
# skill-freshness's mtime-based check is blind in GitHub Actions because `git checkout` resets every file's mtime to the run instant

Every skill-freshness run in this repo since 2026-06-26 has emitted FRESHNESS_OK or FRESHNESS_NO_CHANGE — the 2026-07-02 article states it plainly: "all on-disk mtimes reflect the git checkout timestamp rather than the time each file was last genuinely written by its producer skill." Because `actions/checkout` writes every file at the run instant, every dependency's age is ≪ its threshold, so no stale-input flag can ever fire — the skill measures the checkout, not staleness. Fix path: switch to the `git log -1 --format=%ct` producer-commit timestamp per file (or a dedicated `memory/state/*.json` `written_at` field) instead of `stat --format=%Y`.
