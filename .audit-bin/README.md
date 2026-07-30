# .audit-bin/

Pre-built static binaries for the `workflow-security-audit` skill. Committed here so the skill runs on GitHub Actions runners without needing outbound network access to PyPI or GitHub releases (both can be blocked in the sandbox).

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | Trail of Bits GH Actions security auditor | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | rhysd workflow syntax linter | 1.7.12 | https://github.com/rhysd/actionlint/releases |
| `actionlint.tar.gz` | actionlint release tarball | 1.7.12 | same as above |

## Updating a binary

1. Bump the version pin in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` or `ACTIONLINT_VERSION`).
2. Download the new release binary for `linux/amd64` from the source URL above.
3. Replace the binary here and update the version in this table.
4. Commit both changes together so the pin and the binary stay in sync.

The skill always tries `.audit-bin/` first; it falls back to a network install only when the cached binary is absent.
