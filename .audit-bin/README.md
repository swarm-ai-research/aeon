# .audit-bin

Pre-built security scanner binaries committed here so the `workflow-security-audit` skill can run
without network installs on GitHub Actions runners where outbound PyPI/curl may be blocked.

| Binary | Tool | Version |
|--------|------|---------|
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions auditor (Trail of Bits) | 1.25.2 |
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | 1.7.12 |
| `actionlint.tar.gz` | Source tarball for the actionlint binary above | 1.7.12 |

All binaries target **Linux x86-64** (the GitHub-hosted runner architecture).

## Updating

When bumping a version in `skills/workflow-security-audit/SKILL.md`, replace the binary here with
the matching release artifact:

- **zizmor:** [releases page](https://github.com/zizmorcore/zizmor/releases) → download
  `zizmor-x86_64-unknown-linux-gnu.tar.gz`, extract, and replace `zizmor`.
- **actionlint:** [releases page](https://github.com/rhysd/actionlint/releases) → download
  `actionlint_X.Y.Z_linux_amd64.tar.gz`, extract the binary and the tarball, then replace both
  `actionlint` and `actionlint.tar.gz`.

After replacing, ensure the execute bit is set (`chmod +x zizmor actionlint`) and bump the
corresponding `*_VERSION` variable in the SKILL.md so the two stay in sync.
