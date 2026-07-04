# .audit-bin — pre-shipped scanner binaries

Pre-compiled binaries committed to the repository so the `workflow-security-audit` skill
can run its scanners inside the GitHub Actions sandbox, where network-based installers
(`pipx install`, `bash <(curl ...)`) are blocked.

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | 1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | 1.7.12 | Original release archive (retained for provenance) |

## Why committed to git

The GitHub Actions sandbox blocks outbound installs at runtime. See
`memory/notes/sandbox-blocks-piped-curl-installers.md` for the incident that prompted
this. The `scripts/prefetch-vuln-scanner.sh` pattern (run before Claude, writes to `/tmp/bin/`)
was not feasible here because these binaries are large — committing them avoids re-downloading
on every run.

The `workflow-security-audit` SKILL.md prepends `.audit-bin/` to `$PATH` before attempting
any `pipx`/`pip` install, so the committed binaries take precedence.

## Updating

1. Download the new release archive from the project's GitHub releases page.
2. Extract and replace the binary in `.audit-bin/` (keep the `.tar.gz` alongside it).
3. Update the version table in this README.
4. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` (line ~29).
5. Open a PR — the binaries are tracked in git like any other committed asset.
