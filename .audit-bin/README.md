# .audit-bin/

Pre-built scanner binaries shipped with the repo so that `workflow-security-audit` can run on GitHub Actions without network installs (PyPI and curl-pipe installers are blocked in the sandbox).

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GitHub Actions auditor by Trail of Bits | 1.25.2 | [Releases](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter by rhysd | 1.7.12 | [Releases](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | Source archive from the actionlint release tarball (linux_amd64) | 1.7.12 | — |

## Updating

When bumping a version:

1. Update the corresponding `*_VERSION` pin in `skills/workflow-security-audit/SKILL.md`.
2. Replace the binary here with the new release build for `linux/amd64`.
3. Ensure the binary is executable (`chmod +x .audit-bin/<tool>`).
4. Update the version table above.

**zizmor:** download the `zizmor-x86_64-unknown-linux-musl` asset from https://github.com/zizmorcore/zizmor/releases.

**actionlint:** download the `actionlint_<version>_linux_amd64.tar.gz` asset from https://github.com/rhysd/actionlint/releases, extract the `actionlint` binary, and keep the tar.gz alongside it as a provenance artifact.
