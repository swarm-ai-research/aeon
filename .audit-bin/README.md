# .audit-bin/

Pre-built scanner binaries committed to the repo so the `workflow-security-audit` skill works on GitHub Actions runners where outbound network access to PyPI and release CDNs may be blocked.

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GitHub Actions auditor (Trail of Bits) | 1.25.2 | `zizmorcore/zizmor` releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | see `./actionlint --version` | `rhysd/actionlint` releases |
| `actionlint.tar.gz` | Source archive for the `actionlint` binary above | — | used to build the committed binary |

## Updating

When `ZIZMOR_VERSION` is bumped in `skills/workflow-security-audit/SKILL.md`, replace the `zizmor` binary here:

```bash
# Download the new zizmor binary for linux/amd64 (GitHub Actions default runner)
VERSION=1.x.y   # match ZIZMOR_VERSION in SKILL.md
curl -L "https://github.com/zizmorcore/zizmor/releases/download/v${VERSION}/zizmor-x86_64-unknown-linux-musl.tar.gz" \
  | tar -xz -O zizmor > .audit-bin/zizmor
chmod +x .audit-bin/zizmor
```

For `actionlint`, download the latest release tarball from [rhysd/actionlint/releases](https://github.com/rhysd/actionlint/releases), extract the binary to `.audit-bin/actionlint`, and keep the tarball as `actionlint.tar.gz`.

Both binaries must be `linux/amd64` (the architecture used by GitHub-hosted `ubuntu-*` runners).
