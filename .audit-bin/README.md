# .audit-bin — pre-committed scanner binaries

Pre-compiled binaries for the `workflow-security-audit` skill. Committed to the repo so the skill can run offline inside the Claude Code GitHub Actions sandbox, which blocks piped-curl installers and may not find runtime-installed binaries on `$PATH`.

## Contents

| File | Tool | Version |
|---|---|---|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GH Actions SARIF auditor | 1.25.2 |
| `zizmor.tar.gz` | Source archive for the zizmor binary above | 1.25.2 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | see binary |

## How to update

When bumping `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`:

1. Download the new `zizmor` release binary for `linux_amd64` from the [zizmor releases page](https://github.com/zizmorcore/zizmor/releases).
2. Replace `.audit-bin/zizmor` with the new binary (`chmod +x` it).
3. Replace `.audit-bin/zizmor.tar.gz` with the corresponding source tarball.
4. Update the version row in this table.
5. Commit both files together with the `ZIZMOR_VERSION` bump.

For `actionlint`, download the latest `linux_amd64` release from the [actionlint releases page](https://github.com/rhysd/actionlint/releases) and replace the binary the same way.

## Why not a prefetch script?

A `scripts/prefetch-*.sh` would install at workflow start but still requires outbound network access, which the sandbox restricts. Committing the binaries directly is the most reliable option: no network, no install, no fail path.
