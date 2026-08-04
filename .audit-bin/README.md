# .audit-bin/

Pre-built scanner binaries committed here so `workflow-security-audit` can run on GitHub
Actions runners without relying on network installs. The GHA sandbox blocks PyPI and
curl-piped installers — see `memory/notes/sandbox-blocks-piped-curl-installers.md` for
the incident that motivated this approach.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GH Actions auditor | 1.25.2 | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | 1.7.12 | linux/amd64 |
| `actionlint.tar.gz` | Source tarball for the actionlint binary above (kept for provenance) | 1.7.12 | — |

## Updating

**zizmor** — when `skills/workflow-security-audit/SKILL.md` bumps `ZIZMOR_VERSION`:

```bash
VERSION=<new-version>
curl -Lo .audit-bin/zizmor \
  "https://github.com/zizmorcore/zizmor/releases/download/v${VERSION}/zizmor-x86_64-unknown-linux-musl"
chmod +x .audit-bin/zizmor
```

**actionlint** — when the pin comment in SKILL.md is bumped:

```bash
VERSION=<new-version>
curl -Lo .audit-bin/actionlint.tar.gz \
  "https://github.com/rhysd/actionlint/releases/download/v${VERSION}/actionlint_${VERSION}_linux_amd64.tar.gz"
tar -xzf .audit-bin/actionlint.tar.gz -C .audit-bin/ actionlint
chmod +x .audit-bin/actionlint
```

Both binaries must be executable before committing. Update the version table above and the
pin comment in SKILL.md to match.
