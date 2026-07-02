# .audit-bin

Pre-seeded static binaries for the `workflow-security-audit` skill.

## Purpose

GitHub Actions sandboxes can block outbound `curl`/`pip`/`pipx` calls at
runtime. Committing these binaries ensures the audit runs even when the network
is unavailable, and makes results reproducible without live downloads.

## Contents

| File | Tool | Notes |
|------|------|-------|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — GH Actions syntax/semantic linter | Statically linked x86-64 Linux ELF |
| `actionlint.tar.gz` | Source archive shipped alongside the binary | Used for integrity cross-checking |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions security auditor | x86-64 Linux ELF |

## How the skill uses them

`workflow-security-audit` (step 0b) prepends `.audit-bin/` to `PATH` before
attempting live installs via `pipx`/`pip` or `curl`. If the binaries here are
present and executable, no network calls are needed for tool setup.

## Updating

When upgrading, replace the binary and bump `ZIZMOR_VERSION` in
`skills/workflow-security-audit/SKILL.md` in the same commit:

1. Download the target release for `linux_amd64` from the tool's GitHub Releases page.
2. Copy the extracted binary to `.audit-bin/` (overwrite in place).
3. Update `actionlint.tar.gz` to match the new `actionlint` binary if rebuilding actionlint.
4. Bump `ZIZMOR_VERSION="X.Y.Z"` in `skills/workflow-security-audit/SKILL.md` to match.
5. Verify both binaries are executable (`chmod +x .audit-bin/actionlint .audit-bin/zizmor`).
