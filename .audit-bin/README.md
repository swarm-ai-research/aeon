# .audit-bin/

Pre-built scanner binaries committed for use by `skills/workflow-security-audit/SKILL.md`.
Committing them avoids PyPI/curl installs that may be blocked in the GitHub Actions sandbox.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits SARIF-capable GH Actions auditor) | 1.25.2 | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) (workflow syntax linter) | 1.7.12 | linux/amd64 |
| `actionlint.tar.gz` | actionlint release tarball (source for the binary above) | 1.7.12 | linux/amd64 |

Both binaries target **x86-64 Linux** (GitHub-hosted `ubuntu-*` runners).

## Updating

1. Download the new release binary from the tool's GitHub releases page.
2. Replace the file here (`zizmor` or `actionlint` / `actionlint.tar.gz`).
3. Bump the version pin in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION=` for zizmor; update the actionlint version comment for actionlint).
4. Open a PR — the workflow-security-audit skill reads from this directory on every run.
