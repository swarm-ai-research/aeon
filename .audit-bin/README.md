# .audit-bin — pre-cached security scanner binaries

Pre-built executables committed here so `workflow-security-audit` can run offline on GitHub Actions
runners where outbound PyPI / curl installs may be sandbox-blocked.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GH Actions auditor | 1.25.2 | Linux x86-64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | 1.7.12 | Linux x86-64 |
| `actionlint.tar.gz` | actionlint release tarball (source for the binary above) | 1.7.12 | Linux x86-64 |

## Updating

Both the binary **and** the version pin in `skills/workflow-security-audit/SKILL.md` must be bumped together:

### zizmor
1. Download the new release binary from https://github.com/woodruffw/zizmor/releases
2. Replace `.audit-bin/zizmor` with the Linux x86-64 build and `chmod +x` it
3. Update `ZIZMOR_VERSION` in `SKILL.md` step 0b to match

### actionlint
1. Download the new release tarball from https://github.com/rhysd/actionlint/releases
2. Extract the binary, replace `.audit-bin/actionlint` and `chmod +x` it
3. Replace `.audit-bin/actionlint.tar.gz` with the new tarball
4. Update `ACTIONLINT_VERSION` in `SKILL.md` step 0b to match
