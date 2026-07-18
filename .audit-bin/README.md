# .audit-bin — pre-cached security scanner binaries

Pre-built Linux x86-64 executables committed here so the `workflow-security-audit`
skill can run offline on GitHub Actions runners where outbound PyPI and curl installs
may be blocked by the sandbox.

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `actionlint` | 1.7.12 | [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | 1.7.12 | archive from the same release |
| `zizmor` | 1.25.2 | [zizmorcore/zizmor releases](https://github.com/zizmorcore/zizmor/releases) |

## Updating

When `workflow-security-audit/SKILL.md` bumps `ZIZMOR_VERSION` or `ACTIONLINT_VERSION`:

1. Download the new Linux x86-64 binary from the release page.
2. Replace the file here and `chmod +x` it.
3. Update the version table above.
4. Commit alongside the SKILL.md version-pin change.

The skill's step 0b checks `.audit-bin/` first; network installs are only attempted
if the binary is absent or not executable.
