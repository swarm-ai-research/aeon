# .audit-bin — pre-cached scanner binaries

Pre-built executables for the `workflow-security-audit` skill. Committed to the repo so the skill
can run on GitHub Actions runners where outbound PyPI/curl installs are sandbox-blocked.

## Contents

| File | Tool | Version |
|------|------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits SARIF-capable GH Actions auditor) | 1.25.2 (matches `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`) |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) (syntax-level workflow linter) | see `actionlint.tar.gz` |
| `actionlint.tar.gz` | source tarball for `actionlint` | same release as the binary above |

## Updating

When bumping scanner versions, replace both the binary and the version pin together:

**zizmor:**
1. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`.
2. Download the matching Linux x86_64 binary from the [zizmor releases page](https://github.com/zizmorcore/zizmor/releases) and replace `.audit-bin/zizmor`.
3. `chmod +x .audit-bin/zizmor`

**actionlint:**
1. Download the matching release tarball from the [actionlint releases page](https://github.com/rhysd/actionlint/releases).
2. Extract the binary and replace `.audit-bin/actionlint`; keep the tarball as `.audit-bin/actionlint.tar.gz`.
3. `chmod +x .audit-bin/actionlint`
4. Update the version comment in `skills/workflow-security-audit/SKILL.md` (near the actionlint install block).

## Why committed binaries?

The GitHub Actions sandbox used by Aeon blocks `bash <(curl …)` piped installs and may restrict
outbound PyPI access. Committing the binaries lets `SKILL.md`'s step 0b pick them up first, before
falling back to network installs. See `memory/notes/sandbox-blocks-piped-curl-installers.md` for
the incident that motivated this pattern.
