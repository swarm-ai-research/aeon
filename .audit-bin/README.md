# .audit-bin — pre-cached security scanner binaries

Pre-built binaries for the `workflow-security-audit` skill. Committing them avoids
PyPI/curl installs that can be blocked in the GitHub Actions sandbox.

## Committed binaries

| Binary | Version | Platform | Source |
|---|---|---|---|
| `zizmor` | v1.25.2 | linux/amd64 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | v1.7.12 | linux/amd64 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | v1.7.12 | linux/amd64 | same — kept as the original archive |

## How to update

**zizmor** — download the `zizmor-x86_64-unknown-linux-gnu` binary from the
[releases page](https://github.com/zizmorcore/zizmor/releases), replace
`.audit-bin/zizmor`, `chmod +x`, and bump `ZIZMOR_VERSION` in
`skills/workflow-security-audit/SKILL.md`.

**actionlint** — download the `actionlint_*_linux_amd64.tar.gz` from the
[releases page](https://github.com/rhysd/actionlint/releases), extract the
`actionlint` binary into `.audit-bin/`, replace `actionlint.tar.gz` with the
new archive, and `chmod +x` the binary.

## Platform note

These are ELF 64-bit x86-64 binaries. They run on GitHub-hosted `ubuntu-*`
runners. They will not run on macOS or ARM runners without replacement.
