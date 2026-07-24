# .audit-bin — pre-built scanner binaries

Pre-built executables committed here so `workflow-security-audit` can run on
GitHub Actions runners without hitting the network. The sandbox may block
outbound PyPI and arbitrary curl installs; these binaries bypass that.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | v1.7.12 | linux/amd64 |
| `actionlint.tar.gz` | original release tarball (kept for checksum verification) | v1.7.12 | linux/amd64 |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable security auditor | v1.25.2 | linux/amd64 |

## Upgrading

1. Download the new release binary for `linux/amd64` from the tool's GitHub
   releases page.
2. Replace the file in `.audit-bin/` and `chmod +x` it.
3. Update the matching version variable in `skills/workflow-security-audit/SKILL.md`
   (`ZIZMOR_VERSION` or `ACTIONLINT_VERSION`).
4. Keep `actionlint.tar.gz` in sync with the `actionlint` binary so the
   tarball can be used to verify the binary's integrity.

Both tools are offline-only static analyzers — no new secrets or network
access are needed at scan time.
