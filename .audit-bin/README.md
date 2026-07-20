# .audit-bin — pre-built audit tool binaries

These binaries are committed so that the `workflow-security-audit` skill can run on GitHub Actions runners without relying on outbound network installs (PyPI and curl are blocked in the Aeon sandbox).

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GitHub Actions security auditor | 1.25.2 | Trail of Bits |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | check: `actionlint --version` | rhysd |
| `actionlint.tar.gz` | source tarball for the `actionlint` binary above | same as binary | rhysd |

## Updating

When bumping a version pin in `skills/workflow-security-audit/SKILL.md`, replace the corresponding binary here:

**zizmor** — download the Linux amd64 release binary from
`https://github.com/woodruffw/zizmor/releases/tag/v<version>` and replace `.audit-bin/zizmor`.
Then update `ZIZMOR_VERSION` in the SKILL.md.

**actionlint** — run `bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)` locally to get the tarball and binary, then replace both `.audit-bin/actionlint` and `.audit-bin/actionlint.tar.gz`.
Update the `ACTIONLINT_VERSION` comment in the SKILL.md to match.

Both binaries must be executable (`chmod +x`). The skill's step 0b checks for executability before falling back to a network install.
