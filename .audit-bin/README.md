# .audit-bin/

Pre-built scanner binaries committed directly to the repo so the `workflow-security-audit` skill can run on GitHub Actions runners where outbound PyPI/curl may be sandbox-blocked.

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | Trail of Bits SARIF-capable GH Actions auditor | 1.25.2 | https://github.com/woodruffw/zizmor/releases |
| `actionlint` | Rhymond's workflow syntax linter | 1.7.7 | https://github.com/rhysd/actionlint/releases |
| `actionlint.tar.gz` | Source archive for the actionlint binary above | 1.7.7 | same |

## Usage

`skills/workflow-security-audit/SKILL.md` adds this directory to `$PATH` before attempting any network installs:

```bash
if [ -x ".audit-bin/zizmor" ]; then
  export PATH="$PWD/.audit-bin:$PATH"
fi
```

## Updating

1. Download the new release binary from the source URLs above.
2. Replace the file here (keep executable bit: `chmod +x .audit-bin/<tool>`).
3. Update the version in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` / `ACTIONLINT_VERSION`).
4. Commit both the binary and the version bump together so the pin stays in sync.

The binaries are Linux `amd64` builds — match the GitHub Actions runner architecture (`ubuntu-latest`).
