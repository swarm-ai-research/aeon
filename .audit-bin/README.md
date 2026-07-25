# .audit-bin

Pre-built scanner binaries committed for use by the `workflow-security-audit` skill. They exist because `bash <(curl …)` and `pipx install` are blocked in the GitHub Actions sandbox — see `memory/notes/sandbox-blocks-piped-curl-installers.md`.

## Contents

| File | Tool | Version | Purpose |
|------|------|---------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits) | 1.25.2 | SARIF-capable GitHub Actions security auditor |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) | 1.7.12 | Syntax-level workflow linter with shellcheck integration |
| `actionlint.tar.gz` | actionlint | 1.7.12 | Source archive used to extract the binary above |

Both binaries are Linux amd64 executables (matching GitHub-hosted `ubuntu-*` runners).

## Updating

When bumping either tool, replace the binary **and** update the version pin in `skills/workflow-security-audit/SKILL.md`:

```bash
# zizmor — download the release binary from https://github.com/zizmorcore/zizmor/releases
# actionlint — run the official install script and copy the binary here:
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
cp actionlint .audit-bin/actionlint
chmod +x .audit-bin/actionlint
```

After updating, verify both tools run cleanly:
```bash
.audit-bin/zizmor --version
.audit-bin/actionlint --version
```
