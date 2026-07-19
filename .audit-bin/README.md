# `.audit-bin/` — pre-built scanner binaries

Pre-built binaries for the `workflow-security-audit` skill. They exist because the GitHub
Actions sandbox blocks outbound PyPI and `bash <(curl ...)` installs, so the skill falls
back to these committed executables on every run. See `memory/notes/sandbox-blocks-piped-curl-installers.md` for the incident that drove this.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits SARIF-capable GH Actions auditor) | 1.25.2 | Linux x86-64 (ELF, dynamically linked) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) (syntax-level workflow linter) | see below | Linux x86-64 (ELF, statically linked) |
| `actionlint.tar.gz` | original release archive used to extract `actionlint` | — | — |

Run `./actionlint --version` locally to confirm the actionlint version after updating.

**Platform note:** these binaries target `ubuntu-latest` GitHub Actions runners (Linux
x86-64). They will not run on macOS or Windows runners. If you switch runner OS, replace
with the matching platform binary from the release pages.

## Updating

When `ZIZMOR_VERSION` is bumped in `skills/workflow-security-audit/SKILL.md`:

1. Download the matching zizmor release from <https://github.com/zizmorcore/zizmor/releases>
   (pick the `x86_64-unknown-linux-gnu` asset).
2. Replace `.audit-bin/zizmor` and commit.

For actionlint, download the `linux-amd64` tarball from
<https://github.com/rhysd/actionlint/releases>, extract the binary, replace
`.audit-bin/actionlint` and `.audit-bin/actionlint.tar.gz`, and commit.
