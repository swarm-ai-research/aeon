# .audit-bin — pre-built scanner binaries

Pre-built static binaries committed here so the `workflow-security-audit` skill can run on GitHub Actions runners without hitting sandbox-blocked network installs (PyPI, curl to remote hosts).

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions security auditor | 1.25.2 | `zizmorcore/zizmor` releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | 1.7.12 | `rhysd/actionlint` releases |
| `actionlint.tar.gz` | actionlint source archive (kept alongside the binary for reproducibility checks) | 1.7.12 | same release |

## Updating

When `skills/workflow-security-audit/SKILL.md` bumps `ZIZMOR_VERSION` or `ACTIONLINT_VERSION`:

1. Download the new binary for `linux/amd64` from the respective releases page.
2. Replace the file here (`chmod +x` if needed).
3. Update the version table above.
4. Commit alongside the SKILL.md change so the binary and the version pin stay in sync.
