# .audit-bin — pre-cached security scanner binaries

Pre-downloaded binaries for the `workflow-security-audit` skill. Committed to the repo so the skill works even when the GitHub Actions sandbox blocks outbound PyPI/curl downloads.

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | 1.7.12 | https://github.com/rhysd/actionlint/releases |
| `actionlint.tar.gz` | 1.7.12 | Same release — kept alongside in case the extracted binary is corrupt |

## How the skill uses these

`workflow-security-audit` checks for `.audit-bin/zizmor` and `.audit-bin/actionlint` before falling back to network installs. If either binary is present and executable, the skill adds `.audit-bin/` to `PATH` instead of downloading.

## Updating

Replace the binaries when a new version ships:

```bash
# zizmor — download the linux_x86_64 release binary from GitHub
curl -L https://github.com/zizmorcore/zizmor/releases/download/v<NEW>/zizmor-x86_64-unknown-linux-musl \
  -o .audit-bin/zizmor && chmod +x .audit-bin/zizmor

# actionlint — download and extract the linux_amd64 tarball
curl -L https://github.com/rhysd/actionlint/releases/download/v<NEW>/actionlint_<NEW>_linux_amd64.tar.gz \
  -o .audit-bin/actionlint.tar.gz
tar -xzf .audit-bin/actionlint.tar.gz -C .audit-bin/ actionlint
```

Commit both the extracted binary and the `.tar.gz` so the tarball acts as a backup.
