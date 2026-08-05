# .audit-bin

Pre-built scanner binaries committed to the repo so the `workflow-security-audit` skill can run without network installs on GitHub Actions runners (where outbound PyPI/curl may be sandbox-blocked).

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | [zizmorcore/zizmor releases](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | 1.7.12 | [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases) |

`actionlint.tar.gz` is the original download archive kept alongside the extracted binary for provenance.

## Updating

When bumping a version, update both the binary here **and** the `ZIZMOR_VERSION` pin in `skills/workflow-security-audit/SKILL.md` so the fallback pip-install path stays consistent:

```bash
# zizmor — download the linux/amd64 binary from the release page and replace
curl -Lo .audit-bin/zizmor https://github.com/zizmorcore/zizmor/releases/download/v<NEW>/zizmor-x86_64-unknown-linux-musl
chmod +x .audit-bin/zizmor

# actionlint — download and extract
curl -Lo /tmp/actionlint.tar.gz https://github.com/rhysd/actionlint/releases/download/v<NEW>/actionlint_<NEW>_linux_amd64.tar.gz
tar -xzf /tmp/actionlint.tar.gz -C .audit-bin actionlint
cp /tmp/actionlint.tar.gz .audit-bin/actionlint.tar.gz
```

Then update the `ZIZMOR_VERSION` variable in `skills/workflow-security-audit/SKILL.md` to match.
