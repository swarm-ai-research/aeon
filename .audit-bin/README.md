# .audit-bin — pre-bundled scanner binaries

Pre-built Linux x86-64 binaries for the `workflow-security-audit` skill.

## Why

The GitHub Actions sandbox blocks `bash <(curl …)` pipe-installs and does not have
`~/.local/bin` on `PATH`, so the in-sandbox `pipx install zizmor` / curl-actionlint
paths both fail (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).
Bundling the binaries here lets `workflow-security-audit` find them without a
network call inside the Claude sandbox.

## Contents

| File | Tool | Version | Source |
|---|---|---|---|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) | v1.7.12 | official release, statically linked |
| `actionlint.tar.gz` | (source archive) | v1.7.12 | kept for checksum verification |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) | 1.25.2 | official release |

## How the skill uses them

`workflow-security-audit` step 0b checks `$REPO_ROOT/.audit-bin/` before falling
back to `pipx install` / curl-installer. The skill exports this directory onto
`PATH` so subsequent `command -v zizmor` / `command -v actionlint` checks succeed.

## Updating

When a new version ships:

1. Download the new Linux x86-64 release binary.
2. Replace the file here (`chmod +x` as needed).
3. Bump the version constant in `skills/workflow-security-audit/SKILL.md`
   (`ZIZMOR_VERSION` for zizmor; update the version comment for actionlint).
4. Commit both the binary and the SKILL.md change together.

**Do not update `.audit-bin/` and SKILL.md separately** — the skill's version
comment serves as the authoritative record; out-of-sync versions produce
confusing audit reports.
