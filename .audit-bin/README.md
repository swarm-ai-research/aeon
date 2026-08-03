# .audit-bin — pre-cached audit binaries

Pre-built executables for the `workflow-security-audit` skill. Committed here so
GitHub Actions runners can run the scanners without hitting PyPI or outbound curl
(both are blocked in the sandbox on some runner configurations).

## Contents

| File | Tool | Version | Purpose |
|------|------|---------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) | 1.25.2 | SARIF-capable security auditor for GitHub Actions workflows (Trail of Bits) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) | 1.7.12 | Static syntax/type linter for GitHub Actions workflow files |
| `actionlint.tar.gz` | — | 1.7.12 | Source tarball for the `actionlint` binary above |

## How the skill uses these

`skills/workflow-security-audit/SKILL.md` (step 0b) checks for these binaries
before falling back to network installs:

```bash
if [ -x ".audit-bin/zizmor" ]; then
  export PATH="$PWD/.audit-bin:$PATH"
fi
if [ -x ".audit-bin/actionlint" ]; then
  export PATH="$PWD/.audit-bin:$PATH"
fi
```

## Updating

When bumping the version pin in `SKILL.md` (`ZIZMOR_VERSION`), replace the
binary here to keep the committed copy in sync:

```bash
# zizmor — download the linux-x86_64 release from zizmorcore/zizmor releases
# actionlint — use its install script:
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash) <version>
cp actionlint .audit-bin/
tar -czf .audit-bin/actionlint.tar.gz -C .audit-bin actionlint
```

Commit both the binary and the tarball together with a message like
`chore: bump actionlint to X.Y.Z in .audit-bin`.
