# .audit-bin

Pre-built scanner binaries committed directly to the repo so `workflow-security-audit` can run them on GitHub Actions without hitting the network.

## Why committed binaries?

The GitHub Actions sandbox used by Aeon blocks outbound installs at runtime — `bash <(curl …)` and `pipx install` both fail. Committing the binaries here lets the skill skip those install paths entirely and fall back to them as a first resort rather than last.

See `memory/notes/sandbox-blocks-piped-curl-installers.md` for the incident that prompted this.

## Current versions

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | 1.7.12 | https://github.com/rhysd/actionlint/releases |
| `actionlint.tar.gz` | 1.7.12 | Original release tarball (kept alongside binary) |

## Updating

When bumping a version, update **both** the binary here and the version pin in `skills/workflow-security-audit/SKILL.md`.

```bash
# zizmor — download the linux-x86_64 binary from the release page and replace .audit-bin/zizmor
# actionlint — download the linux-x86_64 tarball, extract, and replace .audit-bin/actionlint + actionlint.tar.gz
chmod +x .audit-bin/zizmor .audit-bin/actionlint
```

Both binaries must be executable (`chmod +x`) after replacement.
