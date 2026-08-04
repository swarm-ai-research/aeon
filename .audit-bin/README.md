# .audit-bin — pre-built scanner binaries

Pre-built, committed executables used by the `workflow-security-audit` skill so that the skill does not need outbound network access to install tools on GitHub Actions runners.

| Binary | Version | Platform | Source |
|--------|---------|----------|--------|
| `zizmor` | 1.25.2 | linux/amd64 | [zizmorcore/zizmor releases](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | 1.7.12 | linux/amd64 | [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases) |

`actionlint.tar.gz` is the original release archive for `actionlint`; the extracted binary is kept alongside it for traceability.

## Updating

When bumping a version, update **both** the binary here **and** the version pin in `skills/workflow-security-audit/SKILL.md`.

**zizmor** — download the `zizmor-x86_64-unknown-linux-gnu` asset from the [release page](https://github.com/zizmorcore/zizmor/releases), replace `.audit-bin/zizmor`, and update `ZIZMOR_VERSION` in `SKILL.md`.

**actionlint** — download `actionlint_<version>_linux_amd64.tar.gz` from the [release page](https://github.com/rhysd/actionlint/releases), extract the binary, replace both `.audit-bin/actionlint` and `.audit-bin/actionlint.tar.gz`, and update `ACTIONLINT_VERSION` in `SKILL.md`.
