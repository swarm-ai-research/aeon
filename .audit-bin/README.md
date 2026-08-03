# .audit-bin

Pre-built static binaries committed for the `workflow-security-audit` skill.

## Why committed

GitHub Actions runners block outbound PyPI and piped-curl installs inside the Claude Code sandbox. Committing binaries here lets the skill skip the network entirely and use `export PATH="$PWD/.audit-bin:$PATH"` as the primary bootstrap path.

## Contents

| Binary | Source | Purpose |
|--------|--------|---------|
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits) | SARIF-capable security auditor for GitHub Actions workflows |
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) | Syntax-level linter for GitHub Actions workflow files |
| `actionlint.tar.gz` | same | Source archive kept alongside the binary for provenance |

## Pinned version

`zizmor` is pinned to **1.25.2** in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION`). When upgrading:

1. Download the new release binary for `linux/amd64` from the project's releases page.
2. Replace `.audit-bin/zizmor` with the new binary (`chmod +x`).
3. Update `ZIZMOR_VERSION` in `SKILL.md` to match.

`actionlint` follows the same pattern — replace `.audit-bin/actionlint` and update any version comment in `SKILL.md`.
