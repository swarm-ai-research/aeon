# .audit-bin

Pre-fetched static binaries for the `workflow-security-audit` skill.

Committing them avoids the GitHub Actions sandbox restriction that blocks
`bash <(curl …)` and `pipx` installs at skill runtime. The skill prepends
this directory to `PATH` before attempting any dynamic installation.

| Binary | Tool | Source |
|--------|------|--------|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | GitHub releases |
| `actionlint.tar.gz` | Same, original release archive | GitHub releases |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions security auditor | GitHub releases |

## Upgrading

1. Download the new release binaries for `linux/amd64` from the upstream release pages.
2. Replace the files here.
3. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match the new zizmor version.
4. Commit as `chore(audit-bin): bump zizmor vX.Y.Z / actionlint vX.Y.Z`.
