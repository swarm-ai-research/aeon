# .audit-bin — pre-built scanner binaries

Pre-built executables cached here so `skills/workflow-security-audit` can run
without hitting the network inside the GitHub Actions sandbox, where outbound
`pip install` / `curl | sh` calls may be blocked.

## Contents

| Binary | Tool | Purpose |
|--------|------|---------|
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) | SARIF-capable GitHub Actions security auditor (Trail of Bits) |
| `actionlint.tar.gz` | [rhysd/actionlint](https://github.com/rhysd/actionlint) | Syntax-level workflow linter — source archive |
| `actionlint` | extracted from above | Compiled actionlint binary |

## Current versions

- **zizmor:** `1.25.2` — pinned via `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`
- **actionlint:** run `.audit-bin/actionlint --version` to check; not yet pinned

## Updating

1. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`.
2. Download the new binary:
   ```bash
   # zizmor
   pipx install "zizmor==<new-version>"
   cp "$(which zizmor)" .audit-bin/zizmor

   # actionlint
   bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash) <version>
   cp actionlint .audit-bin/actionlint
   # optionally re-archive: tar -czf .audit-bin/actionlint.tar.gz actionlint
   ```
3. Commit both the binary and the version-pin change together so they stay in sync.

These are committed binaries — keep them lean (one architecture: `linux/amd64`,
matching GitHub-hosted runners) and do **not** commit debug builds or
platform-specific extras.
