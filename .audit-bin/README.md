# .audit-bin — Pre-committed scanner binaries

Pre-built binaries for the `workflow-security-audit` skill. They exist to avoid
the GitHub Actions sandbox blocking `bash <(curl …)` and `pipx install` at
runtime (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | 1.7.12 | https://github.com/rhysd/actionlint/releases |

The skill prepends this directory to `$PATH` before attempting any network
install, so these binaries are picked up first when the sandbox blocks
outbound downloads.

## Updating

1. Download the new release binary from the project's GitHub releases page.
2. Replace the binary file here (keep it executable: `chmod +x .audit-bin/<name>`).
3. Update the version table above.
4. If changing zizmor, also bump `ZIZMOR_VERSION` in
   `skills/workflow-security-audit/SKILL.md`.
