## Verdict
WORKFLOW_AUDIT_NEW_INFO — 70 new lower-severity finding(s)

## Summary
- **NEW:** 70 (0 crit / 0 high / 11 med / 59 low)
- **REINTRODUCED:** 0
- **UNCHANGED:** 66
- **RESOLVED:** 52
- **Auto-fixed:** 0
- **Manual review:** 0 (no new Critical/High)

## Progress vs 2026-06-28
- **13 of 16 unpinned-uses Critical findings resolved** — SHA-pinning landed on chain-runner, fleet-runner, lint, messages, sync-aeon-public-results, and sync-upstream. Only `aeon.yml` still uses `@v5` tags (3 remaining, UNCHANGED).
- **0 REINTRODUCED** — nothing previously marked resolved has come back.
- **0 NEW Critical/High** — the 70 new findings are 11 Medium (all `artipacked`) + 59 Low (`template-injection`, `anonymous-definition`, `undocumented-permissions`, `concurrency-limits`).

## Attack chains worth reading first
_None — no new Critical or High findings this run._

## Full report
`articles/workflow-security-audit-2026-07-05.md`

## Source status
zizmor: ok (1.25.2) · actionlint: ok (1.7.12) · hand-rolled: ok

## Notes
- Scanner-behavior drift: zizmor 1.25.2 emits multiple findings for the same secret referenced across steps in one job. Prior audit produced 36 secrets-outside-env fingerprints; the same underlying 36 exposures now surface as 43 raw findings (7 duplicates that collapse to the same `(rule, file, secret)` tuple). No new secret exposures were introduced.
- The 32 additional `template-injection` Low and 3 additional `artipacked` Medium findings are the byproduct of new workflow steps added between 2026-06-28 and today — every one is a `note`/`warning`-level flag, none reach shell-injection severity per hand-rolled backstops.
