# .audit-bin/

Pre-built Linux x86-64 static binaries for the `workflow-security-audit` skill.

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `actionlint` | 1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | 1.7.12 | Source archive (kept alongside binary for reference) |
| `zizmor` | 1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) |

## Why these are committed

The GitHub Actions sandbox that Aeon runs in blocks outbound pip/pipx installs and
`bash <(curl …)` pipe installers at runtime. Committing pre-built binaries lets
`workflow-security-audit` add `.audit-bin/` to `PATH` and reach these tools without
any network access during the Claude step.

This follows the same prefetch pattern as `.xai-cache/` (described in `CLAUDE.md`
under "Sandbox Limitations").

## How the skill uses them

`workflow-security-audit`'s step 0b checks for `zizmor` and `actionlint` on `PATH`
before attempting pip/curl installs. Prepend `.audit-bin/` to `PATH` at the top of
the install block so these binaries are found first:

```bash
export PATH="$PWD/.audit-bin:$PATH"
```

## Updating

To upgrade a binary, download the new release for `linux-amd64` from the upstream
releases page, replace the file in this directory, and update the version in this
README and the `ZIZMOR_VERSION` pin in `skills/workflow-security-audit/SKILL.md`.
