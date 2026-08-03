# .audit-bin — pre-cached scanner binaries

Pre-built executables committed to the repo so `workflow-security-audit` can run without network access inside the GitHub Actions sandbox (where `bash <(curl …)` and PyPI installs are blocked).

## Contents

| Binary | Version | Platform | Source |
|--------|---------|----------|--------|
| `zizmor` | v1.25.2 | linux/amd64 | [zizmorcore/zizmor releases](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | v1.7.12 | linux/amd64 | [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | v1.7.12 | linux/amd64 | same release tarball (kept for reference) |

## Updating

When bumping a version, replace both the binary and the version pin in `skills/workflow-security-audit/SKILL.md`:

```bash
# zizmor — download the linux_amd64 binary from the releases page:
# https://github.com/zizmorcore/zizmor/releases
# Verify the SHA-256 checksum from the release page before committing.
curl -L https://github.com/zizmorcore/zizmor/releases/download/v<NEW>/zizmor-x86_64-unknown-linux-gnu \
  -o .audit-bin/zizmor && chmod +x .audit-bin/zizmor
# Then update ZIZMOR_VERSION in SKILL.md.

# actionlint — download the linux_amd64 tarball:
# https://github.com/rhysd/actionlint/releases
curl -L https://github.com/rhysd/actionlint/releases/download/v<NEW>/actionlint_<NEW>_linux_amd64.tar.gz \
  -o .audit-bin/actionlint.tar.gz
tar -xzf .audit-bin/actionlint.tar.gz -C .audit-bin actionlint && chmod +x .audit-bin/actionlint
# Then update ACTIONLINT_VERSION in SKILL.md.
```

Both tools are offline-only static analyzers — no extra secrets required.
