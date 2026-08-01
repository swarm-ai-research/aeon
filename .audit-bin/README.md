# .audit-bin/

Pre-built scanner binaries committed here so `workflow-security-audit` can run on GitHub
Actions without hitting sandbox-blocked network installs (PyPI curl-pipe is blocked; see
`memory/notes/sandbox-blocks-piped-curl-installers.md` for the original incident).

## Contents

| Binary | Version | Source |
|---|---|---|
| `zizmor` | 1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) (linux/amd64) |
| `actionlint` | 1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) (linux/amd64) |
| `actionlint.tar.gz` | 1.7.12 | Source archive kept alongside the binary for provenance |

## Updating

1. Download the new binary from the project's releases page (linux/amd64 build).
2. Replace the file and ensure it is executable: `chmod +x .audit-bin/<binary>`.
3. Update the version pin in `skills/workflow-security-audit/SKILL.md`:
   - zizmor: change `ZIZMOR_VERSION="..."`.
   - actionlint: update the version comment near the actionlint install block.
4. Update this README.
