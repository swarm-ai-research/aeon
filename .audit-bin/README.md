# .audit-bin

Pre-bundled static binaries for the `workflow-security-audit` skill.

Bundling these avoids download failures when the GitHub Actions sandbox blocks outbound network
requests to PyPI or raw.githubusercontent.com (the default install paths for these tools).

## Contents

| Binary | Tool | Purpose |
|--------|------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (zizmorcore) | SARIF-capable GitHub Actions security auditor |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) (rhysd) | Syntax-level GitHub Actions workflow linter |
| `actionlint.tar.gz` | actionlint archive | Source archive for the bundled actionlint binary |

The `workflow-security-audit` skill checks for these binaries first (via `export PATH=".audit-bin:$PATH"`)
before falling back to network installs.

## Updating

To replace a binary, download the appropriate release for `linux/amd64` from the tool's GitHub
releases page, verify the checksum, and overwrite the file. Bump `ZIZMOR_VERSION` in
`skills/workflow-security-audit/SKILL.md` to match.
