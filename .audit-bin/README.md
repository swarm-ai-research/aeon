# .audit-bin

Pre-built tool binaries committed to the repo so the `workflow-security-audit` skill
can run offline on GitHub Actions runners where outbound PyPI/curl installs may be blocked.

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GitHub Actions auditor | 1.25.2 | GitHub releases |
| `zizmor.tar.gz` | — | — | — |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | see binary | GitHub releases |
| `actionlint.tar.gz` | Source archive for the actionlint binary above | — | GitHub releases |

## How the skill uses these

`skills/workflow-security-audit/SKILL.md` step 0b checks for these executables first:

```bash
if [ -x ".audit-bin/zizmor" ]; then
  export PATH="$PWD/.audit-bin:$PATH"
fi
```

If the binary is present and executable, no network install is attempted. This is the
primary path on GitHub Actions runners where outbound PyPI and curl installers may fail.

## Updating

1. Download the new release binary from the tool's GitHub releases page.
2. Replace the file here (keep the same filename).
3. Bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
4. Commit `.audit-bin/` and the SKILL.md together so the version pin stays in sync.

The SKILL.md comment near the version pin reads:
> When auditing this skill, verify ZIZMOR_VERSION is still on the latest stable and bump
> if a patch/minor is out. Also update the binary in .audit-bin/ when bumping the version pin.
