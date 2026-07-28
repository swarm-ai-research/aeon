# .audit-bin/

Pre-built binaries committed to the repo so `workflow-security-audit` can run on GitHub Actions runners without outbound network access (PyPI/curl may be sandbox-blocked).

| Binary | Tool | Version | Upstream |
|--------|------|---------|----------|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | linux/amd64 |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions security auditor | 1.25.2 | linux/amd64 |

`actionlint.tar.gz` is the original release archive for `actionlint`; the extracted binary is committed alongside it for convenience.

## Upgrading

1. Download the new release binary for `linux/amd64` from the upstream releases page.
2. Replace the file here and make it executable (`chmod +x`).
3. Bump the corresponding version pin in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` / `ACTIONLINT_VERSION`).
4. Commit both the binary and the SKILL.md change together so the pin always matches the committed binary.
