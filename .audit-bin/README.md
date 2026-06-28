# .audit-bin — pre-shipped scanner binaries

Pre-downloaded static binaries for the `workflow-security-audit` skill.

The GitHub Actions sandbox blocks `bash <(curl …)` installers and `pipx`/`pip` installs at
runtime (see `memory/notes/sandbox-blocks-piped-curl-installers.md`). These binaries are
committed to the repo so the skill can reference them directly without network access during
the Claude step.

## Contents

| File | Tool | Notes |
|------|------|-------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GHA auditor | Linux x86-64 ELF; pinned in SKILL.md as `ZIZMOR_VERSION` |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | Linux x86-64 ELF; extracted from `actionlint.tar.gz` |
| `actionlint.tar.gz` | actionlint release archive | Source tarball; keep alongside the extracted binary for provenance |

## How to update

1. Download the new release archives from the respective GitHub releases pages.
2. Extract and replace the binaries in this directory (`chmod +x` after extraction).
3. Bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
4. Commit the updated binaries and open a PR.

## Usage in the skill

The `workflow-security-audit` SKILL.md's install step (§0b) prepends `.audit-bin` to `PATH`
so these binaries are found before any system-installed versions:

```bash
export PATH="$PWD/.audit-bin:$PATH"
```
