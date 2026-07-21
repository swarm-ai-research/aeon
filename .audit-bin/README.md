# .audit-bin — pre-built scanner binaries

Pre-built binaries for the `workflow-security-audit` skill. They are committed here because the GitHub Actions sandbox blocks outbound `curl`/`pipx`/`pip` installs at runtime, so the skill falls back to these cached executables as the primary source.

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GHA security auditor (Trail of Bits) | 1.25.2 | `zizmorcore/zizmor` releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | `rhysd/actionlint` releases |
| `actionlint.tar.gz` | actionlint release tarball (kept as provenance artifact) | 1.7.12 | same |

## How to update

1. Download the new release binary from GitHub releases for the tool you're bumping.
2. Replace the file here (`zizmor` or `actionlint`). Make sure the replacement is executable (`chmod +x`).
3. For zizmor, update `actionlint.tar.gz` with the corresponding release tarball.
4. Bump the matching version pin in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` or `ACTIONLINT_VERSION`).
5. Commit both the binary and the SKILL.md change together so the pin stays in sync with the file.

## Why committed binaries

See `memory/notes/sandbox-blocks-piped-curl-installers.md` for the full incident note. Short version: `bash <(curl …)` and `pipx install` are blocked inside the Aeon GHA sandbox. Without pre-cached binaries the skill degrades to hand-rolled regex checks only.
