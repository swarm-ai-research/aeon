# .audit-bin

Pre-built scanner binaries committed to the repo so `workflow-security-audit` can run offline on GitHub Actions runners where outbound PyPI/curl may be blocked.

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/woodruffw/zizmor) — SARIF-capable GH Actions auditor | v1.25.2 | `pip install zizmor==1.25.2` (linux/amd64) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | v1.7.12 | release tarball (linux/amd64) |
| `actionlint.tar.gz` | actionlint release archive | v1.7.12 | `https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz` |

## Updating

When bumping a version, update both the binary here **and** the version pin in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` / `ACTIONLINT_VERSION`).

```bash
# zizmor — download the linux/amd64 wheel and extract the binary
pip download zizmor==<NEW> --no-deps --platform linux_x86_64 --python-version 311 --only-binary :all: -d /tmp/zizmor-dl
unzip -p /tmp/zizmor-dl/zizmor-*.whl 'zizmor/zizmor' > .audit-bin/zizmor
chmod +x .audit-bin/zizmor

# actionlint — grab the release tarball and binary
curl -L "https://github.com/rhysd/actionlint/releases/download/v<NEW>/actionlint_<NEW>_linux_amd64.tar.gz" \
  -o .audit-bin/actionlint.tar.gz
tar xzf .audit-bin/actionlint.tar.gz -C .audit-bin actionlint
chmod +x .audit-bin/actionlint
```

Both tools are offline-only static analyzers — no secrets or network calls at scan time.
