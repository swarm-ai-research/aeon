# .audit-bin — pre-cached scanner binaries

Pre-built binaries for the `workflow-security-audit` skill. Committed here so the skill can run on GitHub Actions runners without hitting the network — the sandbox blocks `bash <(curl …)` installers and PyPI installs in some configurations (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).

The skill's `0b. Install scanners` step checks for these before attempting any network install.

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GH Actions auditor | 1.25.2 | `linux-x86_64` release binary |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | 1.7.12 | `linux-amd64` release binary |
| `actionlint.tar.gz` | actionlint release archive (source of the binary above) | 1.7.12 | rhysd/actionlint releases |

## Updating

When `skills/workflow-security-audit/SKILL.md` bumps a version pin, replace the corresponding binary here:

**zizmor:**
```bash
VERSION=1.25.2   # bump to new version
curl -sSL "https://github.com/zizmorcore/zizmor/releases/download/v${VERSION}/zizmor-x86_64-unknown-linux-gnu.tar.gz" \
  | tar -xz -C .audit-bin/ zizmor
chmod +x .audit-bin/zizmor
```

**actionlint:**
```bash
VERSION=1.7.12   # bump to new version
curl -sSL "https://github.com/rhysd/actionlint/releases/download/v${VERSION}/actionlint_${VERSION}_linux_amd64.tar.gz" \
  -o .audit-bin/actionlint.tar.gz
tar -xz -C .audit-bin/ -f .audit-bin/actionlint.tar.gz actionlint
chmod +x .audit-bin/actionlint
```

After replacing binaries, commit the updated files and update the version pins in `SKILL.md`.

Both tools are offline-only static analyzers — no secrets or network access required at runtime.
