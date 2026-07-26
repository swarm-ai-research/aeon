# .audit-bin — pre-cached security-audit binaries

Pre-built executables committed so the `workflow-security-audit` skill can run
without network access on GitHub Actions runners where outbound PyPI/curl may
be sandbox-blocked.

## Contents

| File | Tool | Version | Source |
|---|---|---|---|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GH Actions auditor | 1.25.2 | Trail of Bits |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | see binary | rhysd |
| `actionlint.tar.gz` | upstream release archive (linux/amd64) from which `actionlint` was extracted | — | rhysd |

Platform: **linux/amd64** (GitHub Actions `ubuntu-latest`).

## Updating

**zizmor:** bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`, then
replace this binary with the new release from
<https://github.com/woodruffw/zizmor/releases>.

**actionlint:** download the latest release archive from
<https://github.com/rhysd/actionlint/releases>, extract the binary, and replace
`actionlint` and `actionlint.tar.gz` here.

Both binaries must be `chmod +x` before committing.
