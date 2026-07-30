# .audit-bin — pre-built scanner binaries

Pre-built binaries for the `workflow-security-audit` skill. Committed here so the skill can run on GitHub Actions without hitting PyPI or curl installers that the sandbox may block.

## Contents

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GitHub Actions auditor by Trail of Bits | 1.25.2 | `zizmorcore/zizmor` releases page |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | `rhysd/actionlint` download script |
| `actionlint.tar.gz` | actionlint release tarball (source for the binary above) | 1.7.12 | `rhysd/actionlint` releases page |

Both binaries are Linux x86-64 ELF executables. They are not used outside GitHub Actions runners.

## Updating

When bumping versions, update both the binary here **and** the version pin in `skills/workflow-security-audit/SKILL.md`.

**zizmor** — download the Linux x86-64 binary from the [releases page](https://github.com/zizmorcore/zizmor/releases), replace `.audit-bin/zizmor`, and update `ZIZMOR_VERSION` in SKILL.md.

**actionlint** — download the Linux x86-64 tarball from the [releases page](https://github.com/rhysd/actionlint/releases), extract the binary, replace `.audit-bin/actionlint` and `.audit-bin/actionlint.tar.gz`, and update `ACTIONLINT_VERSION` in SKILL.md.

After replacing either binary, `chmod +x .audit-bin/actionlint .audit-bin/zizmor` before committing.
