# .audit-bin — pre-committed scanner binaries

Pre-fetched Linux x86-64 binaries for the `workflow-security-audit` skill.

| Binary | Purpose |
|---|---|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — GitHub Actions workflow linter (statically linked Go binary) |
| `actionlint.tar.gz` | Source archive used to produce the `actionlint` binary above |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GHA security auditor (dynamically linked Rust binary) |

## Why they're committed here

The GitHub Actions sandbox blocks `bash <(curl …)` pipe-installs and may not
have `pipx` / `pip` access to PyPI at runtime. Committing the binaries to the
repo pre-seeds them before Claude starts, exactly like `.xai-cache/` or the
`scripts/prefetch-*.sh` pattern used by other skills.

The `workflow-security-audit` SKILL.md step 0b uses `$PWD/.audit-bin` as its
first PATH entry, so these binaries are found before any download is attempted.

## Updating binaries

To bump to a newer version:

```bash
# zizmor — download the linux-amd64 release from zizmorcore/zizmor/releases
curl -sSfL -o .audit-bin/zizmor \
  https://github.com/zizmorcore/zizmor/releases/download/v<VERSION>/zizmor-x86_64-unknown-linux-gnu
chmod +x .audit-bin/zizmor

# actionlint — download from rhysd/actionlint/releases
curl -sSfL -o .audit-bin/actionlint.tar.gz \
  https://github.com/rhysd/actionlint/releases/download/v<VERSION>/actionlint_<VERSION>_linux_amd64.tar.gz
tar -xzf .audit-bin/actionlint.tar.gz -C .audit-bin actionlint
```

Also bump `ZIZMOR_VERSION` in the SKILL.md step 0b install block so the
fallback pip install targets the same version.
