# .audit-bin/

Pre-fetched static binaries for the `workflow-security-audit` skill.

Committed here because the GitHub Actions sandbox blocks `bash <(curl ...)` and
`pipx install` — the two runtime install paths the skill would otherwise use.
The preflight in `skills/workflow-security-audit/SKILL.md` prepends this directory
to `$PATH` before attempting any network-based install, so these binaries are
picked up silently without network access.

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | <https://github.com/zizmorcore/zizmor/releases> |
| `actionlint` | 1.7.12 | <https://github.com/rhysd/actionlint/releases> |
| `actionlint.tar.gz` | 1.7.12 | Original release tarball (kept for provenance) |

All binaries are `linux/amd64` ELF executables targeting GitHub-hosted runners.

## Updating

1. Download the new `linux_amd64` release from the project's releases page.
2. Replace the binary and, for actionlint, the `.tar.gz` alongside it.
3. Bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
4. Commit the replacement — large binary diffs are expected here.
