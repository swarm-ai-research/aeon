# .audit-bin

Pre-built scanner binaries committed here so `workflow-security-audit` can run on GitHub Actions runners where outbound PyPI/curl installs are sandbox-blocked (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions auditor | 1.25.2 | [zizmorcore/zizmor releases](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | run `actionlint --version` | [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | Original release tarball for `actionlint`, kept for reproducibility and verification | same as binary | same |

## Upgrading a binary

1. Download the new linux/amd64 release tarball from the source link above.
2. Extract the binary and replace the file here.
3. Keep `actionlint.tar.gz` in sync — replace it with the new tarball.
4. Update the version pin in `skills/workflow-security-audit/SKILL.md`:
   - zizmor: bump `ZIZMOR_VERSION="..."` in step 0b.
   - actionlint: update the `# Cached version:` comment in step 0b.
5. Ensure the binary is executable: `chmod +x .audit-bin/actionlint .audit-bin/zizmor`.

Both tools are offline-only static analyzers — no secrets or network access required at scan time.
