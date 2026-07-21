# .audit-bin

Pre-built scanner binaries committed for the `workflow-security-audit` skill.
They are loaded before network installs so that sandbox-blocked PyPI/curl calls
don't leave the skill tool-less on GitHub Actions runners.

## Contents

| File | Tool | Version | Source |
|---|---|---|---|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GHA auditor | 1.25.2 | linux/amd64 release binary |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — GHA syntax linter | 1.7.12 | linux/amd64 release binary |
| `actionlint.tar.gz` | Same as above, archived | 1.7.12 | rhysd release tarball |

## Updating

When bumping a version, replace the binary here **and** update the matching
`ZIZMOR_VERSION` / `ACTIONLINT_VERSION` pin in
`skills/workflow-security-audit/SKILL.md`.

```bash
# zizmor — download the linux/amd64 release binary from:
# https://github.com/zizmorcore/zizmor/releases/tag/vX.Y.Z
chmod +x .audit-bin/zizmor

# actionlint — download the linux/amd64 tarball from:
# https://github.com/rhysd/actionlint/releases/tag/v1.X.Y
tar -xzf actionlint_*.tar.gz actionlint
mv actionlint .audit-bin/actionlint
cp actionlint_*.tar.gz .audit-bin/actionlint.tar.gz
chmod +x .audit-bin/actionlint
```

Do not commit binaries for other platforms — the GitHub Actions runner is
always linux/amd64.
