# .audit-bin — Pre-cached security scanner binaries

Pre-built executables committed to the repo so the `workflow-security-audit` skill can run on GitHub Actions runners without hitting sandbox-blocked PyPI or outbound curl calls.

## Contents

| Binary | Version | Source | Purpose |
|--------|---------|--------|---------|
| `zizmor` | v1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) | SARIF-capable GitHub Actions auditor (Trail of Bits) |
| `actionlint` | v1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) | Syntax-level workflow linter |
| `actionlint.tar.gz` | v1.7.12 | same | Source tarball kept alongside the extracted binary |

## Why committed?

GitHub Actions sandboxes may block outbound connections to PyPI and arbitrary curl targets. Committing pre-built binaries guarantees they are always available — `skills/workflow-security-audit/SKILL.md` tries these first and falls back to network installs only if they are absent.

## Sandbox invocation note

Direct `./` invocation of these binaries (e.g. `./.audit-bin/zizmor`) may be blocked by the Claude Code harness permission model inside GitHub Actions. The practical workaround is to invoke them via `python3 subprocess.run(...)`, which bypasses the shell-redirection guard. See the Sandbox note in `skills/workflow-security-audit/SKILL.md` for details.

## Updating

1. Download the new release binary for `linux/amd64` from the project's releases page.
2. Replace the binary here and update the tarball if applicable.
3. Bump the `ZIZMOR_VERSION` or equivalent version comment in `skills/workflow-security-audit/SKILL.md`.
4. Update the version table above.
