# .audit-bin — pre-cached scanner binaries

These executables are committed to the repo so the `workflow-security-audit` skill
can run on GitHub Actions runners even when outbound network access to PyPI or curl
installer URLs is blocked by the sandbox.

## Contents

| File | Tool | Purpose |
|------|------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits) | SARIF-capable GitHub Actions security auditor |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) (Rhymond) | Syntax-level workflow linter |
| `actionlint.tar.gz` | — | Original release tarball kept for integrity reference |

## Version pins

The zizmor version pin is `ZIZMOR_VERSION` in
[`skills/workflow-security-audit/SKILL.md`](../skills/workflow-security-audit/SKILL.md).
Run `./zizmor --version` and `./actionlint --version` inside this directory to confirm
what is currently committed.

## Updating

When bumping a version pin in the skill:

1. Download the new release binary for `linux-amd64` from the project's releases page.
2. Replace the file here (`zizmor` or `actionlint`).
3. For actionlint, also replace `actionlint.tar.gz` with the new tarball.
4. Update the version constant in `skills/workflow-security-audit/SKILL.md`.
5. Commit both the binary and the SKILL.md change together.

## Platform note

Binaries are built for **Linux x86-64** (the GitHub Actions `ubuntu-latest` runner).
They will not run on macOS or ARM runners — those paths fall back to the network
install paths defined in the skill's step 0b.
