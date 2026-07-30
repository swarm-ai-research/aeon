# .audit-bin — pre-built scanner binaries

Pre-built Linux x86-64 binaries committed here so the `workflow-security-audit`
skill can run offline on GitHub Actions runners without needing PyPI or outbound
curl during the job.

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | Trail of Bits GH Actions auditor | 1.25.2 | [zizmorcore/zizmor releases](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | Rhymond workflow linter | 1.7.12 | [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | actionlint source tarball | 1.7.12 | same |

## Updating

When bumping the version pin in `skills/workflow-security-audit/SKILL.md`,
replace the corresponding binary here:

```bash
# zizmor — download the linux-amd64 binary from the releases page
curl -Lo .audit-bin/zizmor \
  https://github.com/zizmorcore/zizmor/releases/download/v<NEW>/zizmor-x86_64-unknown-linux-gnu
chmod +x .audit-bin/zizmor

# actionlint — use the official installer script
cd .audit-bin
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash) <NEW>
cd ..
```

Then update the version table above and commit both the binary and this README.

## Why commit binaries?

GitHub Actions sandboxes often block outbound PyPI/curl. The SKILL.md tries the
cached binary first and falls back to network install only when the binary is
absent. See the "Sandbox note" section in `skills/workflow-security-audit/SKILL.md`.
