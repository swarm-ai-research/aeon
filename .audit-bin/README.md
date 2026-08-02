# .audit-bin

Pre-built scanner binaries committed to the repo so the `workflow-security-audit` skill can run inside GitHub Actions without hitting outbound network restrictions.

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits, SARIF-capable GH Actions security auditor | 1.25.2 | GitHub Releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | GitHub Releases |
| `actionlint.tar.gz` | source archive for the actionlint binary above | 1.7.12 | GitHub Releases |

Both binaries target linux/amd64 to match GitHub-hosted runners.

## Updating

When bumping a version:

1. Download the new release binary from the tool's GitHub Releases page.
2. Replace the file here (e.g. `cp ~/Downloads/zizmor .audit-bin/zizmor && chmod +x .audit-bin/zizmor`).
3. Update the version comment in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` variable for zizmor; inline comment for actionlint).
4. Commit both the binary and the SKILL.md change together so the pin and the binary stay in sync.

## Why committed binaries?

The GitHub Actions sandbox used by Aeon blocks `bash <(curl …)` style installers and may restrict outbound PyPI access. Shipping the binaries in the repo guarantees they load on every run without any network dependency.
