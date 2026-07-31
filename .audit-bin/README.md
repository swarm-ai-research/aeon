# .audit-bin — pre-built scanner binaries

Committed executables used by `workflow-security-audit` to avoid network installs on GitHub Actions runners where outbound PyPI and curl-pipe installs are blocked.

## Contents

| File | Tool | Notes |
|------|------|-------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits) — SARIF-capable GitHub Actions auditor | Pinned to the version in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION`) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | Extracted from `actionlint.tar.gz` below |
| `actionlint.tar.gz` | Original release archive for `actionlint` | Kept alongside the binary as the canonical source; re-extract if the binary is corrupted |

## Updating

**zizmor:** bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`, then replace the binary:

```bash
ZIZMOR_VERSION="<new-version>"
curl -L "https://github.com/zizmorcore/zizmor/releases/download/v${ZIZMOR_VERSION}/zizmor-x86_64-unknown-linux-musl.tar.gz" \
  | tar -xz --strip-components=1 -C .audit-bin zizmor
chmod +x .audit-bin/zizmor
```

**actionlint:** download the latest release tarball from [github.com/rhysd/actionlint/releases](https://github.com/rhysd/actionlint/releases), replace both `actionlint` and `actionlint.tar.gz`:

```bash
ACTIONLINT_VERSION="<new-version>"
curl -L "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz" \
  -o .audit-bin/actionlint.tar.gz
tar -xz -C .audit-bin -f .audit-bin/actionlint.tar.gz actionlint
chmod +x .audit-bin/actionlint
```

Commit both the binary and the tarball together so the archive stays in sync with the extracted binary.

## Sandbox note

The `workflow-security-audit` skill checks `.audit-bin/` first (`[ -x ".audit-bin/zizmor" ]`) before falling back to `pipx`/`pip` installs or the curl-pipe bootstrap. See `skills/workflow-security-audit/SKILL.md` § *0b. Install scanners* for the full fallback chain.
