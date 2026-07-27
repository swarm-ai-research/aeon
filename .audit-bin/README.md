# .audit-bin — pre-cached scanner binaries

Pre-built binaries committed to avoid sandbox-blocked network installs on GitHub Actions runners.
The `workflow-security-audit` skill checks here first before attempting PyPI/curl installs.

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | v1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) — Trail of Bits, SARIF-capable GH Actions auditor |
| `actionlint` | v1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) — syntax-level workflow linter |
| `actionlint.tar.gz` | v1.7.12 | Original release archive for the `actionlint` binary above |

## Updating

When `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` is bumped, replace the binary here:

```bash
# Download the linux-amd64 release binary for the new version
curl -L https://github.com/zizmorcore/zizmor/releases/download/v<VERSION>/zizmor-x86_64-unknown-linux-gnu.tar.gz \
  | tar xz -O zizmor > .audit-bin/zizmor
chmod +x .audit-bin/zizmor
```

For actionlint, download the matching release from `rhysd/actionlint/releases` (linux-amd64 zip),
extract the binary, and update both `actionlint` and `actionlint.tar.gz` here. Update the version
comment in `skills/workflow-security-audit/SKILL.md` to match.

## Why committed binaries?

GitHub Actions runners allow outbound access to PyPI and GitHub releases, but it can be flaky.
Committing the binaries guarantees the audit skill works even when network fetches fail mid-run.
The `.gitignore` already excludes `.audit-tmp/` and `.audit*.py` scratch files — only the
production binaries in this directory are tracked.
