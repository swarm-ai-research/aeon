# .audit-bin — Pre-built scanner binaries

Pre-built executables committed to the repo so `workflow-security-audit` can run on GitHub
Actions runners where outbound PyPI/curl is sandboxed.

## Contents

| File | Tool | Version | Source |
|---|---|---|---|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GHA security auditor | 1.25.2 | `zizmorcore/zizmor` releases (linux-x86_64) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax/correctness linter | v1.7.12 | `rhysd/actionlint` releases (linux-amd64) |
| `actionlint.tar.gz` | Source tarball for the actionlint binary above | v1.7.12 | Same release page |

## Why committed binaries?

The GHA sandbox blocks `bash <(curl …)` piped installers and `pipx install` calls made during
the Claude Code run. Without pre-cached binaries the skill degrades to hand-rolled regex
fallbacks. The binaries let the full SARIF-based scan run without any outbound network access.

See `memory/notes/sandbox-blocks-piped-curl-installers.md` for the incident that motivated this.

## Updating

1. Download the new release for `linux-x86_64` / `linux-amd64` from the respective GitHub
   releases page.
2. Replace the binary (and tarball for actionlint) here.
3. Update the version pin in `skills/workflow-security-audit/SKILL.md`:
   - `ZIZMOR_VERSION` near step 0b for zizmor.
   - `ACTIONLINT_VERSION` near step 0b for actionlint.
4. Commit both the binary and the SKILL.md version-pin change together so they stay in sync.
