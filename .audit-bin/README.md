# .audit-bin — Pre-cached scanner binaries

Pre-built binaries committed to the repo so the `workflow-security-audit` skill can
run on GitHub Actions runners without needing network access to PyPI or curl-pipe
installers (both are unreliable inside the Aeon sandbox).

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GH Actions SARIF auditor | 1.25.2 | GitHub Releases |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | GitHub Releases |
| `actionlint.tar.gz` | Source tarball for the `actionlint` binary above | 1.7.12 | GitHub Releases |

## Why these are committed

The Aeon sandbox on GitHub Actions blocks:
- `bash <(curl …)` piped installers
- `pipx install` / `pip install --user` to PyPI in some runner configurations
- Execution of binaries installed to `~/.local/bin` (not on PATH)

Committing the binaries as `chmod +x` executables lets `workflow-security-audit`
export `$PWD/.audit-bin` onto `PATH` and skip all network installs. See
`memory/notes/sandbox-blocks-piped-curl-installers.md` for the incident that
motivated this.

## Updating

When bumping a version, replace the binary and update `skills/workflow-security-audit/SKILL.md`:

**zizmor:**
```bash
VERSION=1.x.y
curl -L "https://github.com/zizmorcore/zizmor/releases/download/v${VERSION}/zizmor-x86_64-unknown-linux-musl.tar.gz" \
  | tar -xz zizmor
chmod +x zizmor && mv zizmor .audit-bin/zizmor
```
Then update `ZIZMOR_VERSION` in SKILL.md.

**actionlint:**
```bash
VERSION=1.x.y
curl -L "https://github.com/rhysd/actionlint/releases/download/v${VERSION}/actionlint_${VERSION}_linux_amd64.tar.gz" \
  -o .audit-bin/actionlint.tar.gz
tar -xzf .audit-bin/actionlint.tar.gz -C .audit-bin actionlint
chmod +x .audit-bin/actionlint
```
Then update `ACTIONLINT_VERSION` in SKILL.md.
