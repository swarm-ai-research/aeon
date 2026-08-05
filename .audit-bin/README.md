# .audit-bin

Pre-built scanner binaries committed for use inside the GitHub Actions sandbox, where outbound
PyPI and `bash <(curl …)` installs are blocked. `workflow-security-audit` (step 0b) checks for
these before attempting any network install.

| Binary | Tool | Version |
|---|---|---|
| `zizmor` | [zizmorcore/zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GH Actions auditor by Trail of Bits | 1.25.2 |
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | see git log |
| `actionlint.tar.gz` | actionlint source tarball (kept alongside the binary for reference) | — |

## Updating

1. Download the new release binary for `linux/amd64` from the project's GitHub Releases page.
2. Replace the file here and commit it.
3. For zizmor, also bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
4. For actionlint, update the version note in this table.

Binaries must be executable (`chmod +x`). The SKILL.md Sandbox note has more context on why
these are committed rather than installed at runtime.
