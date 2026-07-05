# Workflow Security Audit — 2026-07-05

**Verdict:** WORKFLOW_AUDIT_NEW_INFO — 70 new lower-severity finding(s)
**Repo:** [aeonframework/aeon](https://github.com/aeonframework/aeon)
**Files audited:** 7 (7 workflows, 0 composite actions)
**Findings this run:** 136 (3 critical, 43 high, 31 medium, 59 low)
**Delta vs 2026-06-28:** 70 new, 0 reintroduced, 66 unchanged, 52 resolved
**Auto-fixed:** 0

## Regressions (previously-fixed findings now present again)

_None._

## New findings

_No new Critical or High findings._

### Medium and Low — compact summary

| Severity | Rule | File | Line | Pattern |
|---|---|---|---|---|
| Medium | `artipacked` | `.github/workflows/aeon.yml` | 83 | `- name: Early checkout` |
| Medium | `artipacked` | `.github/workflows/aeon.yml` | 119 | `- name: Checkout repo` |
| Medium | `artipacked` | `.github/workflows/chain-runner.yml` | 28 | `- name: Checkout repo` |
| Medium | `artipacked` | `.github/workflows/fleet-runner.yml` | 56 | `- name: Checkout` |
| Medium | `artipacked` | `.github/workflows/lint.yml` | 32 | `- name: Checkout` |
| Medium | `artipacked` | `.github/workflows/lint.yml` | 70 | `- name: Checkout` |
| Medium | `artipacked` | `.github/workflows/lint.yml` | 91 | `- name: Checkout` |
| Medium | `artipacked` | `.github/workflows/messages.yml` | 56 | `- name: Checkout repo` |
| Medium | `artipacked` | `.github/workflows/messages.yml` | 691 | `- name: Checkout repo` |
| Medium | `artipacked` | `.github/workflows/sync-aeon-public-results.yml` | 28 | `- name: Checkout aeon` |
| Medium | `artipacked` | `.github/workflows/sync-upstream.yml` | 22 | `- name: Checkout fork` |
| Low | `anonymous-definition` | `.github/workflows/aeon.yml` | 72 | `run:` |
| Low | `undocumented-permissions` | `.github/workflows/aeon.yml` | 77 | `contents: write` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 98 | `if [ "${{ github.event_name }}" = "workflow_dispatch" ] \|\| [` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 105 | `elif [ "${{ github.event_name }}" = "issues" ]; then` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 112 | `if [ -n "${{ steps.skill.outputs.name }}" ]; then` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 114 | `echo "label=${{ steps.skill.outputs.name }}" >> "$GITHUB_OUT` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 150 | `SKILL_FILE="skills/${{ steps.skill.outputs.name }}/SKILL.md"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 194 | `SKILL="${{ steps.skill.outputs.name }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 288 | `SKILL_NAME="${{ steps.skill.outputs.name }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 480 | `SKILL_NAME="${{ steps.skill.outputs.name }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 602 | `SKILL="${{ steps.skill.outputs.name }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 603 | `INPUT="${{ steps.run.outputs.SKILL_INPUT_TOKENS }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 604 | `OUTPUT="${{ steps.run.outputs.SKILL_OUTPUT_TOKENS }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 605 | `CACHE_READ="${{ steps.run.outputs.SKILL_CACHE_READ_TOKENS }}` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 606 | `CACHE_CREATION="${{ steps.run.outputs.SKILL_CACHE_CREATION_T` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 607 | `TOTAL="${{ steps.run.outputs.SKILL_TOTAL_TOKENS }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 625 | `echo "$(date -u +%Y-%m-%d),${{ steps.skill.outputs.name }},$` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 630 | `SKILL="${{ steps.skill.outputs.name }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 651 | `SKILL="${{ steps.skill.outputs.name }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 657 | `if [ "${{ steps.run.outputs.GATEWAY }}" = "bankr" ] && [ -n ` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 752 | `if [ "${{ steps.run.outputs.GATEWAY }}" = "bankr" ] && [ -n ` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 863 | `LABEL="${{ steps.work.outputs.label }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 927 | `SKILL="${{ steps.skill.outputs.name }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 928 | `RUN_OUTCOME="${{ steps.run.outcome }}"` |
| Low | `template-injection` | `.github/workflows/aeon.yml` | 931 | `QUALITY_SCORE="${{ steps.analyze.outputs.QUALITY_SCORE }}"` |
| Low | `anonymous-definition` | `.github/workflows/chain-runner.yml` | 20 | `run:` |
| Low | `undocumented-permissions` | `.github/workflows/chain-runner.yml` | 24 | `contents: write` |
| Low | `concurrency-limits` | `.github/workflows/fleet-runner.yml` | 4 | `on:` |
| Low | `anonymous-definition` | `.github/workflows/fleet-runner.yml` | 44 | `run:` |
| Low | `undocumented-permissions` | `.github/workflows/fleet-runner.yml` | 48 | `contents: write` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 150 | `echo '${{ secrets.GITLAWB_OPERATOR_PEM }}' > ~/.gitlawb/iden` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 151 | `echo '${{ secrets.GITLAWB_OPERATOR_UCAN }}' > ~/.gitlawb/uca` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 153 | `echo '${{ secrets.GITLAWB_RESEARCHER_PEM }}' > ~/.gitlawb/fl` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 154 | `echo '${{ secrets.GITLAWB_REVIEWER_PEM }}' > ~/.gitlawb/flee` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 155 | `echo '${{ secrets.GITLAWB_DEPLOYER_PEM }}' > ~/.gitlawb/flee` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 156 | `echo '${{ secrets.GITLAWB_SENTINEL_PEM }}' > ~/.gitlawb/flee` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 315 | `git remote set-url origin "https://x-access-token:${{ secret` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 335 | `git commit -m "chore(fleet-runner): processed ${{ steps.runn` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 347 | `PROCESSED="${{ steps.runner.outputs.processed }}"` |
| Low | `template-injection` | `.github/workflows/fleet-runner.yml` | 348 | `GENERATED="${{ steps.generator.outputs.created }}"` |
| Low | `anonymous-definition` | `.github/workflows/messages.yml` | 47 | `tick:` |
| Low | `anonymous-definition` | `.github/workflows/messages.yml` | 651 | `run:` |
| Low | `undocumented-permissions` | `.github/workflows/messages.yml` | 658 | `issues: read` |
| Low | `template-injection` | `.github/workflows/messages.yml` | 670 | `if [ "${{ github.event_name }}" = "repository_dispatch" ]; t` |
| Low | `anonymous-definition` | `.github/workflows/sync-aeon-public-results.yml` | 23 | `sync:` |
| Low | `anonymous-definition` | `.github/workflows/sync-upstream.yml` | 16 | `sync:` |
| Low | `undocumented-permissions` | `.github/workflows/sync-upstream.yml` | 19 | `contents: write` |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 71 | `run: git push origin "${{ steps.merge.outputs.branch }}"` |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 78 | `BRANCH="${{ steps.merge.outputs.branch }}"` |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 79 | `CONFLICT="${{ steps.merge.outputs.conflict }}"` |
| Low | `template-injection` | `.github/workflows/sync-upstream.yml` | 80 | `AHEAD="${{ steps.diff.outputs.ahead }}"` |

## Carried over (unchanged)

| Severity | Rule | File | Count | First seen |
|---|---|---|---|---|
| Critical | `unpinned-uses` | `.github/workflows/aeon.yml` | 3 | 2026-06-28 |
| High | `secrets-outside-env` | `.github/workflows/chain-runner.yml` | 4 | 2026-06-28 |
| High | `secrets-outside-env` | `.github/workflows/fleet-runner.yml` | 10 | 2026-06-28 |
| High | `secrets-outside-env` | `.github/workflows/messages.yml` | 27 | 2026-06-28 |
| High | `secrets-outside-env` | `.github/workflows/sync-upstream.yml` | 2 | 2026-06-28 |
| Medium | `actionlint-shellcheck` | `.github/workflows/aeon.yml` | 2 | 2026-06-28 |
| Medium | `actionlint-shellcheck` | `.github/workflows/chain-runner.yml` | 8 | 2026-06-28 |
| Medium | `actionlint-shellcheck` | `.github/workflows/fleet-runner.yml` | 6 | 2026-06-28 |
| Medium | `actionlint-shellcheck` | `.github/workflows/messages.yml` | 4 | 2026-06-28 |

## Resolved since 2026-06-28

- `unpinned-uses` in `.github/workflows/chain-runner.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/fleet-runner.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/fleet-runner.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/lint.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/lint.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/lint.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/lint.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/lint.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/messages.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/messages.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/messages.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/sync-aeon-public-results.yml` — no longer present (Critical)
- `unpinned-uses` in `.github/workflows/sync-upstream.yml` — no longer present (Critical)
- `artipacked` in `.github/workflows/aeon.yml` — no longer present (Medium)
- `artipacked` in `.github/workflows/aeon.yml` — no longer present (Medium)
- `artipacked` in `.github/workflows/chain-runner.yml` — no longer present (Medium)
- `artipacked` in `.github/workflows/fleet-runner.yml` — no longer present (Medium)
- `artipacked` in `.github/workflows/lint.yml` — no longer present (Medium)
- `artipacked` in `.github/workflows/messages.yml` — no longer present (Medium)
- `artipacked` in `.github/workflows/sync-aeon-public-results.yml` — no longer present (Medium)
- `artipacked` in `.github/workflows/sync-upstream.yml` — no longer present (Medium)
- `anonymous-definition` in `.github/workflows/aeon.yml` — no longer present (Low)
- `undocumented-permissions` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/aeon.yml` — no longer present (Low)
- `anonymous-definition` in `.github/workflows/chain-runner.yml` — no longer present (Low)
- `undocumented-permissions` in `.github/workflows/chain-runner.yml` — no longer present (Low)
- `concurrency-limits` in `.github/workflows/fleet-runner.yml` — no longer present (Low)
- `anonymous-definition` in `.github/workflows/fleet-runner.yml` — no longer present (Low)
- `undocumented-permissions` in `.github/workflows/fleet-runner.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/fleet-runner.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/fleet-runner.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/fleet-runner.yml` — no longer present (Low)
- `anonymous-definition` in `.github/workflows/messages.yml` — no longer present (Low)
- `anonymous-definition` in `.github/workflows/messages.yml` — no longer present (Low)
- `undocumented-permissions` in `.github/workflows/messages.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/messages.yml` — no longer present (Low)
- `anonymous-definition` in `.github/workflows/sync-aeon-public-results.yml` — no longer present (Low)
- `anonymous-definition` in `.github/workflows/sync-upstream.yml` — no longer present (Low)
- `undocumented-permissions` in `.github/workflows/sync-upstream.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/sync-upstream.yml` — no longer present (Low)
- `template-injection` in `.github/workflows/sync-upstream.yml` — no longer present (Low)

## Source status

- zizmor: ok (1.25.2, persona=auditor)
- actionlint: ok (1.7.12)
- hand-rolled: ok (toJson-into-shell, GITHUB_ENV/OUTPUT-write, third-party-pin — no findings)

## Notes

- Scanner-behavior drift: zizmor 1.25.2 emits multiple findings for the same secret referenced across steps in one job. Prior audit (2026-06-28) produced 36 secrets-outside-env fingerprints; the same underlying 36 secret exposures now surface as 43 raw findings (7 are duplicates that collapse to the same `(rule, file, secret)` tuple). No new secret exposures were introduced.
- SHA-pinning progress: 13 of 16 `unpinned-uses` Critical findings from 2026-06-28 are now resolved — `chain-runner.yml`, `fleet-runner.yml`, `lint.yml` (5 checkouts + setup-nodes), `messages.yml` (3), `sync-aeon-public-results.yml`, and `sync-upstream.yml` are all SHA-pinned. Only `aeon.yml` still uses `@v5` tags (3 remaining, all UNCHANGED).
- 32 new `template-injection` Low findings and 3 new `artipacked` Medium findings appeared: these are the byproduct of workflow files being edited between 2026-06-28 and today (new steps added → more interpolations for zizmor's parser to flag). Every one is a `note`/`warning`-level flag, none reach shell-injection severity per hand-rolled backstops.
- No REINTRODUCED findings — nothing previously marked auto-fixed or resolved has come back. Delta is monotonic-improving for Critical/High.

<!--
workflow-security-audit-fingerprints
92837b7d661077dc severity=Medium status=info rule=artipacked file=.github/workflows/aeon.yml step=jobs/run/steps/[0]
bac3cbba3f4c9903 severity=Medium status=info rule=artipacked file=.github/workflows/aeon.yml step=jobs/run/steps/[3]
03ae5350e79045b0 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[1]/run
03ae5350e79045b0 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[1]/run
03ae5350e79045b0 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[1]/run
c908ef8846ad966a severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[2]/run
c908ef8846ad966a severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[2]/run
075883d2d6094913 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[7]/run
08d356d735122e10 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[8]/run
00e0f9e975f55226 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[10]/run
00e0f9e975f55226 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[10]/run
72660b0388bad863 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[12]/run
72660b0388bad863 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[12]/run
72660b0388bad863 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[12]/run
72660b0388bad863 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[12]/run
72660b0388bad863 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[12]/run
72660b0388bad863 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[12]/run
ec9f060ecb19c007 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[13]/run
ec9f060ecb19c007 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[13]/run
ec9f060ecb19c007 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[13]/run
ec9f060ecb19c007 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[13]/run
ec9f060ecb19c007 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[13]/run
ec9f060ecb19c007 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[13]/run
c3477ae6096b90d7 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[14]/run
84794eed69305815 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[15]/run
84794eed69305815 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[15]/run
d330168b57002e5c severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[16]/run
f23d69aa5c2cbe39 severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[19]/run
54710b0c569cffcb severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[20]/run
54710b0c569cffcb severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[20]/run
54710b0c569cffcb severity=Low status=info rule=template-injection file=.github/workflows/aeon.yml step=jobs/run/steps/[20]/run
5227575f3a66f6fe severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=jobs/run/steps/[0]/uses_actions/checkout@v5
5801f4536c03d5e2 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=jobs/run/steps/[3]/uses_actions/checkout@v5
10de564750b432c7 severity=Critical status=manual rule=unpinned-uses file=.github/workflows/aeon.yml step=jobs/run/steps/[5]/uses_actions/setup-node@v5
6944f3030efca186 severity=Low status=info rule=undocumented-permissions file=.github/workflows/aeon.yml step=jobs/run/permissions/contents
04f2bf3bb85947ad severity=Low status=info rule=anonymous-definition file=.github/workflows/aeon.yml step=jobs/run
60f666cfe35aeb4d severity=Medium status=info rule=artipacked file=.github/workflows/chain-runner.yml step=jobs/run/steps/[0]
ded7ca2cb3cf61ee severity=Low status=info rule=undocumented-permissions file=.github/workflows/chain-runner.yml step=jobs/run/permissions/contents
22de4d9f42ead816 severity=Low status=info rule=anonymous-definition file=.github/workflows/chain-runner.yml step=jobs/run
565be780cadb7cac severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=jobs/run_secrets.GH_GLOBAL
565be780cadb7cac severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=jobs/run_secrets.GH_GLOBAL
565be780cadb7cac severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=jobs/run_secrets.GH_GLOBAL
4a8d83cc35f57d7a severity=High status=manual rule=secrets-outside-env file=.github/workflows/chain-runner.yml step=jobs/run_secrets.AEON_PRIVATE_PAT
e01e869400ab195c severity=Medium status=info rule=artipacked file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[0]
afc0c7c4f96bf9ff severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[6]/run
afc0c7c4f96bf9ff severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[6]/run
afc0c7c4f96bf9ff severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[6]/run
afc0c7c4f96bf9ff severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[6]/run
afc0c7c4f96bf9ff severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[6]/run
afc0c7c4f96bf9ff severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[6]/run
0587d285a115c0e8 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[15]/run
0587d285a115c0e8 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[15]/run
0587d285a115c0e8 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[15]/run
0587d285a115c0e8 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[15]/run
ce5bb2688f9b8fe8 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[16]/run
ce5bb2688f9b8fe8 severity=Low status=info rule=template-injection file=.github/workflows/fleet-runner.yml step=jobs/run/steps/[16]/run
84d69b49074515ea severity=Low status=info rule=undocumented-permissions file=.github/workflows/fleet-runner.yml step=jobs/run/permissions/contents
a7934a272685f108 severity=Low status=info rule=anonymous-definition file=.github/workflows/fleet-runner.yml step=jobs/run
c92cf3067e7f74a9 severity=Low status=info rule=concurrency-limits file=.github/workflows/fleet-runner.yml step=on
f4ecaf1fff5e652d severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_OPERATOR_PEM
198e26d272a74f08 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_OPERATOR_UCAN
cc301788ff1c518f severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_RESEARCHER_PEM
d3c9921048223714 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_REVIEWER_PEM
63c3b4b074ddb806 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_DEPLOYER_PEM
325273f70816fdb0 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.GITLAWB_SENTINEL_PEM
93b0956b8e64ba6f severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.SURPLUS_PRICING_URL
878197aa283f063f severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.SURPLUS_API_KEY
2328eeac3fa8c016 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.CLAUDE_CODE_OAUTH_TOKEN
886d73f696de6645 severity=High status=manual rule=secrets-outside-env file=.github/workflows/fleet-runner.yml step=jobs/run_secrets.AEON_PRIVATE_PAT
7db2bf6ce010a0bf severity=Medium status=info rule=artipacked file=.github/workflows/lint.yml step=jobs/shellcheck/steps/[0]
0e0320f78cd39d98 severity=Medium status=info rule=artipacked file=.github/workflows/lint.yml step=jobs/typecheck/steps/[0]
4350d8144550457a severity=Medium status=info rule=artipacked file=.github/workflows/lint.yml step=jobs/compute-futures-tests/steps/[0]
70aa5e0ed807f089 severity=Medium status=info rule=artipacked file=.github/workflows/messages.yml step=jobs/tick/steps/[0]
b82d60bda17b6a2b severity=Medium status=info rule=artipacked file=.github/workflows/messages.yml step=jobs/run/steps/[1]
df175e1986600035 severity=Low status=info rule=template-injection file=.github/workflows/messages.yml step=jobs/run/steps/[0]/run
fbeee022d417ac41 severity=Low status=info rule=undocumented-permissions file=.github/workflows/messages.yml step=jobs/run/permissions/issues
d0cf1990d02e968d severity=Low status=info rule=anonymous-definition file=.github/workflows/messages.yml step=jobs/tick
6b87be74ea117ac1 severity=Low status=info rule=anonymous-definition file=.github/workflows/messages.yml step=jobs/run
d8eea5ca734a21b5 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.GH_GLOBAL
d8eea5ca734a21b5 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.GH_GLOBAL
d8eea5ca734a21b5 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.GH_GLOBAL
5bbb9e31d166961d severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.TELEGRAM_BOT_TOKEN
0ebbc61a6a4ae91b severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.TELEGRAM_CHAT_ID
7c31302812d2403c severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.DISCORD_BOT_TOKEN
47532fc72a0389d3 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.DISCORD_CHANNEL_ID
e68919b7d374f1ab severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.SLACK_BOT_TOKEN
fdbbddb792fce331 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.SLACK_CHANNEL_ID
87a6bc755ab87ba1 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/tick_secrets.AEON_PRIVATE_PAT
b3de6366005f9c55 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.GH_GLOBAL
e1eea0bec6928363 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.ANTHROPIC_API_KEY
9df252d1f9648d71 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.CLAUDE_CODE_OAUTH_TOKEN
b3de6366005f9c55 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.GH_GLOBAL
b3de6366005f9c55 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.GH_GLOBAL
f151f17b89a37f5a severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.TELEGRAM_BOT_TOKEN
f8d3e0970f3027b3 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.TELEGRAM_CHAT_ID
3490e5ef0d849401 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.DISCORD_BOT_TOKEN
5ead345d4b0feca0 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.DISCORD_CHANNEL_ID
798db651b7feec39 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.DISCORD_WEBHOOK_URL
7e6a5b4c0c6d1aba severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.SLACK_BOT_TOKEN
4fffd6cb630a43a5 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.SLACK_CHANNEL_ID
7d47442fc10beb1d severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.SLACK_WEBHOOK_URL
b5bd0e797f9eb678 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.XAI_API_KEY
4c24dabb8d25bbee severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.COINGECKO_API_KEY
9ea3117d00ec0f64 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.ALCHEMY_API_KEY
39985d456376efc9 severity=High status=manual rule=secrets-outside-env file=.github/workflows/messages.yml step=jobs/run_secrets.AEON_PRIVATE_PAT
27f5f493cd9ea1e3 severity=Medium status=info rule=artipacked file=.github/workflows/sync-aeon-public-results.yml step=jobs/sync/steps/[0]
4c03f136bae8d4ab severity=Low status=info rule=anonymous-definition file=.github/workflows/sync-aeon-public-results.yml step=jobs/sync
db2edb59078747fa severity=Medium status=info rule=artipacked file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[0]
f373e7ffa3a3330d severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[6]/run
633035534730d8d8 severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[7]/run
633035534730d8d8 severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[7]/run
633035534730d8d8 severity=Low status=info rule=template-injection file=.github/workflows/sync-upstream.yml step=jobs/sync/steps/[7]/run
12f8f852130873f9 severity=Low status=info rule=undocumented-permissions file=.github/workflows/sync-upstream.yml step=jobs/sync/permissions/contents
8c6c3a10e8de1aac severity=Low status=info rule=anonymous-definition file=.github/workflows/sync-upstream.yml step=jobs/sync
81602c73ef2d4c69 severity=High status=manual rule=secrets-outside-env file=.github/workflows/sync-upstream.yml step=jobs/sync_secrets.GH_GLOBAL
81602c73ef2d4c69 severity=High status=manual rule=secrets-outside-env file=.github/workflows/sync-upstream.yml step=jobs/sync_secrets.GH_GLOBAL
5d00009436535be8 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/aeon.yml step=
b643ab88e3ee067d severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/aeon.yml step=Log token usage
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
fcc41e7740c27af5 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/chain-runner.yml step=Run chain
82c1b50412d7ffab severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
82c1b50412d7ffab severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
82c1b50412d7ffab severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
82c1b50412d7ffab severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
b8a2d94f94fd18f9 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
b8a2d94f94fd18f9 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/fleet-runner.yml step=
712a01bd54981f4c severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=Determine and dispatch scheduled skills
964c1e5eb0004214 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=Extract message
bb079613dc18b970 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=
6a47b35ec43316e4 severity=Medium status=info rule=actionlint-shellcheck file=.github/workflows/messages.yml step=Log token usage
-->
