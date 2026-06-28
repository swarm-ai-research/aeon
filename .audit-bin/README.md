# .audit-bin

Pre-built scanner binaries for the `workflow-security-audit` skill.

The GitHub Actions sandbox blocks `curl | bash` installers and pip network installs in
some runner configurations (see `memory/notes/sandbox-blocks-piped-curl-installers.md`
for the incident that motivated this). Committing the binaries here lets the skill run
fully offline: step 0b adds `.audit-bin/` to `PATH` before the `command -v` checks, so
the runtime install paths become no-ops.

## Contents

| File | Version | Purpose |
|------|---------|---------|
| `actionlint` | 1.7.12 | GitHub Actions workflow syntax linter (rhysd/actionlint) |
| `actionlint.tar.gz` | 1.7.12 | Source archive retained for integrity verification |
| `zizmor` | 1.25.2 | SARIF-capable GitHub Actions security auditor (zizmorcore/zizmor) |

## Updating

1. Download the new release binary from the project's GitHub releases page.
2. Replace the file in this directory (`chmod +x` if needed).
3. Bump the version constant in `skills/workflow-security-audit/SKILL.md`:
   - `ZIZMOR_VERSION="..."` for zizmor
   - The comment on the actionlint install block for actionlint
4. Commit both the binary and the SKILL.md change together so the version reference
   stays in sync with what's on disk.

## Platform note

These binaries target `linux/amd64` (GitHub-hosted `ubuntu-*` runners). They will not
work on macOS or ARM runners without replacement.
