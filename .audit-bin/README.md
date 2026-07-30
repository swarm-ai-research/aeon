# .audit-bin — pre-built scanner binaries

Pre-built binaries committed here so `workflow-security-audit` can run on GitHub
Actions runners without hitting the sandbox's blocked-outbound-network restriction
(see [[sandbox-blocks-piped-curl-installers]] in `memory/notes/`).

## Bundled tools

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | 1.7.12 | https://github.com/rhysd/actionlint/releases |

`actionlint.tar.gz` — original release archive kept alongside the extracted binary
for provenance; the skill only uses the extracted `actionlint` executable.

## How the skill uses these

`skills/workflow-security-audit/SKILL.md` step 0b checks for `[ -x ".audit-bin/zizmor" ]`
and `[ -x ".audit-bin/actionlint" ]` first and prepends `.audit-bin/` to `$PATH`.
Network installs (pipx/pip for zizmor, curl-pipe for actionlint) are only attempted
as fallbacks if the committed binaries are absent.

## Updating

When bumping a version:

1. Download the new release binary for `linux/amd64` from the project's releases page.
2. Replace the file here (and the `.tar.gz` for actionlint).
3. Update the `ZIZMOR_VERSION` / `ACTIONLINT_VERSION` pin in `SKILL.md` step 0b to match.
4. Commit both the binary and the SKILL.md change together so the pin stays in sync.

## Platform note

These are `linux/amd64` ELF binaries built for GitHub-hosted Ubuntu runners.
They will not run on macOS or ARM runners without replacement.
