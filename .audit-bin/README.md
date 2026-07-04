# .audit-bin — pre-bundled scanner binaries

Pre-compiled static binaries for the `workflow-security-audit` skill.

## Why these exist

The GHA sandbox blocks `bash <(curl …)` pipe-installers and doesn't expose
`~/.local/bin` on PATH, so runtime installs of `zizmor` and `actionlint`
reliably fail (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).
Committing the binaries here lets the skill run without any network fetching.

## Contents

| File | Tool | Platform | Notes |
|------|------|----------|-------|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) | linux/amd64 | statically linked |
| `actionlint.tar.gz` | actionlint (source archive) | — | keep alongside the binary for reference |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) | linux/amd64 | dynamically linked (glibc) |

Pinned versions are recorded in `SKILL.md` (`ZIZMOR_VERSION`, `ACTIONLINT_VERSION`).

## Updating

1. Download the new release binary for linux/amd64 from the project's GitHub
   Releases page.
2. Replace the binary in `.audit-bin/`.
3. Update the version constant in `skills/workflow-security-audit/SKILL.md`.
4. Open a PR — the binaries are tracked in git so diffs are visible.
