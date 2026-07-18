# .audit-bin/

Pre-built binaries for the `workflow-security-audit` skill. Committed here so the skill works on GitHub Actions runners where outbound network access may be blocked (PyPI, curl installs, etc.).

## Contents

| File | Tool | Purpose |
|------|------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits) | SARIF-capable GitHub Actions security auditor |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) | GitHub Actions workflow syntax and correctness linter |
| `actionlint.tar.gz` | — | Source tarball actionlint was extracted from (kept for provenance) |

## Current version pins

- **zizmor:** `1.25.2` (pinned in `skills/workflow-security-audit/SKILL.md` as `ZIZMOR_VERSION`)
- **actionlint:** see binary; no explicit version pin in SKILL.md

## Updating

When bumping a version pin in `SKILL.md`, replace the corresponding binary here:

```bash
# zizmor — download the Linux x86-64 binary from the zizmorcore/zizmor releases page
# actionlint — run the upstream install script and copy the resulting binary:
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
cp actionlint .audit-bin/actionlint
```

Commit both the updated binary and the version pin change together so they stay in sync.

## Platform

These binaries target **Linux x86-64** (the default GitHub Actions runner architecture).
