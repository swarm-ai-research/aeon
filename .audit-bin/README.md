# .audit-bin — pre-built scanner binaries

Committed ELF binaries for the `workflow-security-audit` skill. Committing them avoids
PyPI/curl installs that may be blocked in the GitHub Actions sandbox.

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GH Actions auditor (Trail of Bits) | 1.25.2 | PyPI / GitHub releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | see below | GitHub releases |
| `actionlint.tar.gz` | Source archive for the `actionlint` binary above | — | GitHub releases |

**actionlint version:** run `.audit-bin/actionlint --version` to confirm the committed binary's
version, then record it here when you replace it.

## How the skill uses these

`skills/workflow-security-audit/SKILL.md` step 0b checks for `.audit-bin/zizmor` and
`.audit-bin/actionlint` before attempting any network install. If present and executable,
they are prepended to `$PATH` and used directly.

On GitHub Actions runners, direct binary execution via subprocess (not shell PATH expansion)
is required — bare `./.audit-bin/zizmor` calls may hit a permission-approval wall in some
sandbox configurations.

## Updating a binary

1. Download the new release from the tool's GitHub releases page.
2. Replace the binary here (and the `.tar.gz` for actionlint).
3. `chmod +x .audit-bin/zizmor .audit-bin/actionlint`
4. Update the version in this table.
5. For zizmor: also bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`.
6. Commit with a message like `chore(audit-bin): bump zizmor 1.25.2 → X.Y.Z`.
