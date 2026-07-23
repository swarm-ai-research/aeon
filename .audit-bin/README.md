# .audit-bin — pre-built scanner binaries

Pre-built static-analysis binaries committed here so `workflow-security-audit` can
run on GitHub Actions without hitting PyPI or curl — both are unreliable from the
GHA sandbox.  The skill's step 0b checks for these before attempting network installs.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions auditor | 1.25.2 | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | linux/amd64 |
| `actionlint.tar.gz` | source archive from which `actionlint` was extracted | 1.7.12 | linux/amd64 |

## Updating

When bumping a tool version, also update the version pin in
`skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` / `ACTIONLINT_VERSION`),
then replace the binary here:

```bash
# zizmor — download the linux/amd64 release binary
curl -sLO "https://github.com/zizmorcore/zizmor/releases/download/v${NEW_VERSION}/zizmor-x86_64-unknown-linux-musl.tar.gz"
tar xzf zizmor-*.tar.gz zizmor
chmod +x zizmor

# actionlint — use the official install script with an explicit version
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash) "${NEW_VERSION}"
chmod +x actionlint
```

Run `.audit-bin/zizmor --version` and `.audit-bin/actionlint --version` after
replacement to verify the version matches the pin before committing.
