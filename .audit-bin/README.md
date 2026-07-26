# .audit-bin

Pre-built scanner binaries committed for reproducible, offline-friendly runs on GitHub Actions,
where outbound `bash <(curl …)` installs and PyPI may be blocked by the sandbox.

## Contents

| File | Tool | Version | Platform | Source |
|---|---|---|---|---|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — GH Actions security auditor (Trail of Bits) | 1.25.2 | Linux x86-64 | [Releases](https://github.com/zizmorcore/zizmor/releases/tag/v1.25.2) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | Linux x86-64 | [Releases](https://github.com/rhysd/actionlint/releases/tag/v1.7.12) |
| `actionlint.tar.gz` | actionlint source archive (kept for provenance) | 1.7.12 | — | same release page |

## Updating a binary

1. Download the new `linux_amd64` binary from the tool's GitHub Releases page.
2. Replace the file here and ensure it is executable (`chmod +x`).
3. Update the version pin in `skills/workflow-security-audit/SKILL.md`
   (`ZIZMOR_VERSION` for zizmor, `ACTIONLINT_VERSION` for actionlint).
4. Update the version column in the table above.

## Why committed binaries?

The GitHub Actions sandbox used by this repo blocks `bash <(curl …)` pipe installs
and may block PyPI. Committing the binaries avoids install-time failures and keeps
`workflow-security-audit` reproducible without outbound network access.
The `workflow-security-audit` SKILL.md (step 0b) tries these binaries first and
falls back to network installs only when they are absent.
