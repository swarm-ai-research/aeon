# .audit-bin/

Pre-built scanner binaries committed for offline use on GitHub Actions runners,
where outbound network calls to PyPI or the actionlint download script may be
blocked by the sandbox.

`workflow-security-audit` tries these before any network install (see Step 0b in
`skills/workflow-security-audit/SKILL.md`).

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GH Actions auditor | 1.25.2 | GitHub Releases |
| `actionlint.tar.gz` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter (archive) | 1.7.12 | GitHub Releases |
| `actionlint` | actionlint (extracted from the tarball above) | 1.7.12 | extracted |

## Updating

When bumping either tool, replace the binary here **and** update the version
variable in `skills/workflow-security-audit/SKILL.md` so the fallback pip/curl
install uses the same version.

```bash
# zizmor — download the linux-x86_64 binary from the releases page and chmod +x
# https://github.com/zizmorcore/zizmor/releases

# actionlint — download the linux-x86_64 tarball, extract, and commit both
# https://github.com/rhysd/actionlint/releases
```

Both binaries must be committed with execute permission (`chmod +x`).
