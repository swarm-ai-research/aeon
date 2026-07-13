# .audit-bin/

Pre-built offline binaries used by the `workflow-security-audit` skill as a fallback when the GitHub Actions sandbox blocks network-based installation.

| File | Tool | Arch |
|------|------|------|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — GitHub Actions workflow linter | Linux x86-64 |
| `actionlint.tar.gz` | Source archive for the actionlint binary above | — |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — security auditor for GitHub Actions (SARIF output) | Linux x86-64 |

## Usage

The skill's step 0b adds this directory to `$PATH` before falling back to `pipx`/`pip`/`curl` installs. On runners where the binaries are executable (Linux x86-64), no network access is needed for the scanner install step.

## Updating

When bumping the pinned `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`, replace `zizmor` here with the matching release binary from the [zizmorcore/zizmor releases page](https://github.com/zizmorcore/zizmor/releases). Similarly, replace `actionlint` and `actionlint.tar.gz` when the actionlint version is bumped.
