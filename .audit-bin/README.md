# .audit-bin/

Pre-built binaries committed for the `workflow-security-audit` skill. The skill's preflight step (0b) puts this directory on `$PATH` before trying network installs, which may be blocked in the GitHub Actions sandbox.

## Contents

| File | Version | Source |
|------|---------|--------|
| `zizmor` | 1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | 1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | 1.7.12 | Original release tarball (binary extracted from here) |

All binaries are x86-64 Linux ELF. They will not work on macOS or arm64 runners.

## Updating

1. Download the new release for `linux_amd64` from the project's releases page.
2. Replace the binary (and tarball, if keeping it for reference).
3. Update the version pin comment in `skills/workflow-security-audit/SKILL.md` — both the `ZIZMOR_VERSION` variable and the `actionlint` comment block.
