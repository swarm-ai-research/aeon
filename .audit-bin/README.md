# .audit-bin — pre-built scanner binaries

Pre-compiled executables committed here so the `workflow-security-audit` skill can run offline on GitHub Actions runners without hitting sandbox-blocked PyPI or curl installers.

## Contents

| File | Tool | Version | Architecture |
|------|------|---------|--------------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GH Actions auditor | 1.25.2 | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | linux/amd64 |
| `actionlint.tar.gz` | actionlint release archive (source for the extracted binary above) | 1.7.12 | linux/amd64 |

## Updating

**zizmor:** download the `zizmor-x86_64-unknown-linux-musl` asset from the [zizmor releases page](https://github.com/zizmorcore/zizmor/releases), replace `.audit-bin/zizmor`, and bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`.

**actionlint:** download `actionlint_<version>_linux_amd64.tar.gz` from the [actionlint releases page](https://github.com/rhysd/actionlint/releases), replace both `actionlint.tar.gz` and the extracted `actionlint` binary, and bump `ACTIONLINT_VERSION` in `skills/workflow-security-audit/SKILL.md`.

After replacing either binary, `chmod +x` it so the `-x` executable check in the skill passes.
