# .audit-bin — pre-built scanner binaries

Pre-built binaries committed here so `workflow-security-audit` can run offline on GitHub Actions runners where outbound installs (PyPI, curl) may be sandbox-blocked. See `skills/workflow-security-audit/SKILL.md` for usage.

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GH Actions security auditor | **1.25.2** | zizmorcore/zizmor releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | see binary (`actionlint --version`) | rhysd/actionlint releases |
| `actionlint.tar.gz` | source tarball for actionlint (used to extract the binary above) | matches binary | rhysd/actionlint releases |

## Updating

**zizmor:** bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` step 0b, download the matching release binary for `linux-x86_64`, replace `.audit-bin/zizmor`, and update the version cell above.

**actionlint:** download the new release tarball from `rhysd/actionlint/releases`, extract the binary, replace both `.audit-bin/actionlint` and `.audit-bin/actionlint.tar.gz`, and update the version cell above.

Both binaries must be executable (`chmod +x`). Neither tool requires network access at scan time — they are pure static analyzers.
