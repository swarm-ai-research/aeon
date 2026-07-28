# .audit-bin

Pre-built Linux/amd64 binaries committed here so `workflow-security-audit` can run on GitHub Actions runners without network installs.

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | 1.7.12 | https://github.com/rhysd/actionlint/releases |

`actionlint.tar.gz` is the upstream release archive kept alongside the extracted binary for provenance.

## Updating

1. Download the new Linux/amd64 release from the links above.
2. Replace `zizmor` or `actionlint` (and `actionlint.tar.gz`) with the new binary, keeping it executable (`chmod +x`).
3. Bump the version comment in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION=` or the `# Committed binary is vX.Y.Z` line for actionlint).
4. Open a PR — the next `workflow-security-audit` run will pick up the new binary automatically.
