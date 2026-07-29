# .audit-bin/

Pre-built static binaries committed so `workflow-security-audit` runs without network
access on GitHub Actions runners where outbound PyPI/curl may be sandbox-blocked.

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | 1.7.12 | https://github.com/rhysd/actionlint/releases |

`actionlint.tar.gz` is the upstream release archive kept alongside the extracted binary
for provenance — the binary inside matches the extracted `actionlint` executable.

## Updating

When bumping a version, replace both the binary here **and** the matching version
constant in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` /
`ACTIONLINT_VERSION`) so the fallback network-install path stays in sync.

For zizmor: download the `x86_64-unknown-linux-gnu` release binary from the releases page.
For actionlint: download the `linux_amd64` tarball, extract, and drop `actionlint` here.
