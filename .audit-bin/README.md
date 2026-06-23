# .audit-bin/

Pre-built scanner binaries committed to the repo so `workflow-security-audit` can
run offline in the GitHub Actions sandbox without network calls at runtime.

## Contents

| Binary | Version | Purpose |
|--------|---------|---------|
| `zizmor` | 1.25.2 | Trail of Bits — SARIF-capable GitHub Actions security auditor |
| `actionlint` | — | Rhysd — syntax-level GitHub Actions workflow linter |
| `actionlint.tar.gz` | — | Original release archive (retained for re-extraction) |

## Why these live here

The GitHub Actions sandbox blocks `bash <(curl ...)` piped-installer patterns and does not
include `~/.local/bin` on PATH. On 2026-06-21, both install paths in the skill failed and
the run degraded to hand-rolled regex fallbacks (`WORKFLOW_AUDIT_TOOL_DEGRADED`). Shipping
the binaries directly in the repo solves both problems without requiring outbound network.

`skills/workflow-security-audit/SKILL.md` step 0b exports `$PWD/.audit-bin` as the first
entry on PATH, so `command -v zizmor` and `command -v actionlint` resolve here before the
`pipx` / `curl` install fallbacks run.

## Updating

**zizmor:** bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`, then:

```bash
pip install --target .audit-tools "zizmor==$NEW_VERSION"
cp .audit-tools/bin/zizmor .audit-bin/zizmor
```

**actionlint:** download the linux-amd64 release binary from
<https://github.com/rhysd/actionlint/releases> and replace `.audit-bin/actionlint`.
Update `.audit-bin/actionlint.tar.gz` to the matching release archive if desired.
