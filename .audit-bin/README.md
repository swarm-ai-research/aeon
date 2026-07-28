# .audit-bin — pre-built scanner binaries

Pre-built Linux x86-64 executables committed here so `workflow-security-audit` can run on GitHub Actions runners without needing outbound PyPI or curl access.

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GH Actions auditor | 1.25.2 | GitHub releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | 1.7.12 | GitHub releases |
| `actionlint.tar.gz` | Source archive for the `actionlint` binary | 1.7.12 | GitHub releases |

## Updating a binary

1. Download the new release for `linux_amd64` from the tool's GitHub releases page.
2. Replace the file(s) here: `cp <new-binary> .audit-bin/<name> && chmod +x .audit-bin/<name>`.
3. Update the version pin in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` / `ACTIONLINT_VERSION`).
4. Commit both the binary and the SKILL.md version bump together so the pin stays in sync.

## Why committed binaries?

The GitHub Actions sandbox intermittently blocks outbound network from bash `run:` steps, which makes `pipx install zizmor` and `curl …/download-actionlint.bash` unreliable. Committing the executables eliminates the network dependency and makes the scan reproducible at a known version.
