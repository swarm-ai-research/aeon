# .audit-bin — pre-built scanner binaries

Pre-built binaries committed to the repo so `workflow-security-audit` can run on GitHub Actions without hitting the network. The GHA sandbox blocks `bash <(curl …)` pipe installs, so these serve as the primary scanner source. The skill falls through to a network install only when both binaries are absent.

## Contents

| File | Tool | Platform |
|------|------|----------|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — Trail of Bits SARIF-capable GHA auditor | x86-64 Linux (ubuntu-latest runner) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | x86-64 Linux (ubuntu-latest runner) |
| `actionlint.tar.gz` | actionlint release tarball (source for the `actionlint` binary above) | — |

## Version pins

- **zizmor**: pinned to `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` (currently `1.25.2`).
- **actionlint**: no explicit version pin; binary should be updated alongside zizmor bumps.

## Updating

When bumping `ZIZMOR_VERSION` in the skill:

```bash
# zizmor — download the new linux-x86_64 binary from the zizmor releases page
# https://github.com/woodruffw/zizmor/releases
curl -Lo .audit-bin/zizmor \
  "https://github.com/woodruffw/zizmor/releases/download/v${NEW_VERSION}/zizmor-x86_64-unknown-linux-gnu"
chmod +x .audit-bin/zizmor

# actionlint — download and unpack the linux-amd64 tarball
ACTIONLINT_VERSION="1.7.x"  # replace with the target version
curl -Lo .audit-bin/actionlint.tar.gz \
  "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz"
tar -xzf .audit-bin/actionlint.tar.gz -C .audit-bin actionlint
chmod +x .audit-bin/actionlint
```

Commit both changed binaries and the updated `ZIZMOR_VERSION` string in the same PR.
