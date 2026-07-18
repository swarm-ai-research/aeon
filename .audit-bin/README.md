# .audit-bin — pre-built scanner binaries

Pre-built static binaries committed here so `workflow-security-audit` can run without network access on GitHub Actions (the sandbox blocks `bash <(curl …)` installers and `~/.local/bin` is not on PATH).

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GH Actions SARIF auditor | 1.25.2 | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | see below | linux/amd64 |
| `actionlint.tar.gz` | actionlint release archive (source for the `actionlint` binary above) | — | linux/amd64 |

Run `actionlint --version` to confirm the exact actionlint version; the binary was extracted from the matching release tarball via the official install script.

## How to update

**zizmor:** bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`, then replace the binary:

```bash
ZIZMOR_VERSION="<new-version>"
curl -L "https://github.com/zizmorcore/zizmor/releases/download/v${ZIZMOR_VERSION}/zizmor-x86_64-unknown-linux-gnu.tar.gz" \
  | tar xz -C .audit-bin/ zizmor
chmod +x .audit-bin/zizmor
```

**actionlint:** download the latest release tarball from the [actionlint releases page](https://github.com/rhysd/actionlint/releases) (`actionlint_<ver>_linux_amd64.tar.gz`), extract the binary, and replace both files:

```bash
ACTIONLINT_VERSION="<new-version>"
curl -L "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz" \
  -o .audit-bin/actionlint.tar.gz
tar xzf .audit-bin/actionlint.tar.gz -C .audit-bin/ actionlint
chmod +x .audit-bin/actionlint
```

Both tools are offline-only static analyzers — no secrets or network access required at scan time.
