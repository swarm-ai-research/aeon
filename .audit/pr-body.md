## Verdict
WORKFLOW_AUDIT_NEW_CRITICAL — 3 new critical, 55 new high, 31 new medium, 64 new low; first on-disk delta baseline for this repo

## Summary
- **NEW:** 153 (3 crit / 55 high / 31 med / 64 low) — every finding is NEW because no prior `articles/workflow-security-audit-*.md` existed on `main` to diff against
- **REINTRODUCED:** 0
- **UNCHANGED:** 0
- **RESOLVED:** 0
- **Auto-fixed:** 0
- **Manual review:** 58 (all Critical + High)

## Attack chains worth reading first
1. **[CRITICAL] `zizmor/unpinned-uses` — `.github/workflows/aeon.yml:85`** — `actions/checkout@v4.4.0` on the `Early checkout` step. `aeon.yml` fires on `issues.opened`, `workflow_dispatch`, and `workflow_call`, so it is externally reachable. A repointed tag (compromised owner, malicious release, or force-moved `v4.4.0`) executes attacker code with `GITHUB_TOKEN` + fleet secrets (`ANTHROPIC_API_KEY`, `GH_GLOBAL`, `TELEGRAM_BOT_TOKEN`, etc.) reachable in later steps → full-repo write and cross-workflow dispatch.
2. **[CRITICAL] `zizmor/unpinned-uses` — `.github/workflows/aeon.yml:121`** — same shape at the second `actions/checkout@v4.4.0` (`Full checkout` step).
3. **[CRITICAL] `zizmor/unpinned-uses` — `.github/workflows/aeon.yml:133`** — `actions/setup-node@v5` (major-version tag) at the `Set up Node` step. `@v5` is a moving-major tag; the action owner can repoint it at any time.

## Why 0 auto-fixed
Per SKILL.md constraints, `unpinned-uses`, `secrets-outside-env`, and `ref-version-mismatch` are always Manual — they need operator judgment: SHA verification against a signed tag, GitHub Environment creation in repo settings, and tag/commit reconciliation respectively.

## Fix hints (highest-impact, do these first)

1. Pin the 3 Critical `unpinned-uses` — replace floating tags with pinned SHAs plus a `# vN.N.N` comment. Example for `actions/checkout@v4.4.0`:
   ```yaml
   uses: actions/checkout@85e6279cec87321a52edac9c87bce653a07cf6c2 # v4.4.0
   ```
   Look up the SHA with `gh api repos/actions/checkout/git/refs/tags/v4.4.0 -q '.object.sha'` and verify it points at a signed tag.
2. Move fleet-wide secrets into a GitHub Environment (`production` or per-secret) and add `environment: <name>` to the jobs that reference them — clears the 46 `secrets-outside-env` findings without touching workflow logic.
3. Fix the 9 `ref-version-mismatch` findings by re-reading the pinned SHA's actual release tag (`gh api repos/OWNER/REPO/commits/SHA -q .commit.message`) and updating the `# vN.N.N` comment.

## Full report
`articles/workflow-security-audit-2026-09-27.md`

## Source status
zizmor: ok · actionlint: ok · hand-rolled: ok (all supplemental patterns — toJson-into-shell, persist-credentials, GITHUB_ENV injection, mutable third-party ref — confirmed absent)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
