---
id: watched-repos-config-missing-silent-short-circuits-6-skills
created: 2026-08-13
type: lesson
links: [[enabled-skills-can-never-dispatch]], [[fleet-ops]]
---
# A missing `memory/watched-repos.md` silently short-circuits six enabled skills — every dispatch is a no-op that produces only a log line

Six enabled skills (`code-health`, `github-monitor`, `issue-triage`, `changelog`, `weekly-shiplog`, `repo-revive`) treat `memory/watched-repos.md` as a required config; when the file is absent each dispatch runs its SKILL.md config short-circuit (`CODE_HEALTH_EMPTY_CONFIG` / `GITHUB_MONITOR_EMPTY_CONFIG` / `ISSUE_TRIAGE_OK no-watched-repos` / …) and exits before any `gh` call, article write, or notify — the operator sees six healthy `last_status: success` cron-state entries with zero material output. As of 2026-08-13 this cluster has run eight consecutive days in that shape (streak-8 per today's `code-health` + `issue-triage` + `github-monitor` logs, same-day short-circuit cycle continues) and stays invisible to the health rubric because every skill's exit path is a documented OK-return. Fix path is exactly two options: populate `memory/watched-repos.md` with `owner/repo` entries to activate the six skills, or land `enabled: false` on each in `aeon.yml` so the fleet fires exactly what it can act on; the current state costs six dispatch slots per day for zero work and inflates the enabled-skill count feeding ms-02.
