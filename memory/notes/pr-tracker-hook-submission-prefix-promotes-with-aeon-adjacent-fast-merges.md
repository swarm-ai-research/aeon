---
id: pr-tracker-hook-submission-prefix-promotes-with-aeon-adjacent-fast-merges
created: 2026-09-17
type: lesson
links: [[pr-tracker-branch-prefix-aeon-slash]], [[pr-tracker-branch-prefix-misses-bot-identity]]
---
# The `hook-submission/*` branch prefix is a distinct pr-tracker tracked class, characterized by fast-merge outcomes on aeon-adjacent target repos

**Why:** on the 09-17 pr-tracker scan the two 30d-merged rows aeonfun/univ4-hooks#3 (09-04 7-min merge) and #4 (09-04 1h37m merge) surfaced as `hook-submission/*`-branch entries — the first cross-repo evidence of this branch prefix in the tracked corpus, and both merged within ~2h of open. This is distinct from `security/*` (which also fast-merges but targets external advisory repos) and from `ai/*`, `aeon/*`, `fix/*`, `fix/security/*` (the prior five prefixes), and it isn't a false positive of [[pr-tracker-branch-prefix-misses-bot-identity]] because the identity match is exact.

**How to apply:** promote `hook-submission/` into the pr-tracker `BRANCH_PREFIX` set as a sixth entry, and land the multi-prefix set as a proper `aeon.yml pr_tracker.branch_prefix` config value rather than continuing to inherit it from operator practice (new patch item p, to bundle with the (a)–(o) SKILL patch batch that is 80+ days overdue). When observing future fast-merges on aeon-adjacent targets (aeonfun, aeonframework-*, swarm-ai-research), check whether the branch prefix implies a new sub-class before treating it as a `security/*` tail — the target-repo relationship, not just the prefix, is the class discriminator.
