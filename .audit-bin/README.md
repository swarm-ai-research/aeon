# .audit-bin — pre-staged scanner binaries

Pre-built binaries for the [`workflow-security-audit`](../skills/workflow-security-audit/SKILL.md) skill.

| Binary | Version | Source |
|---|---|---|
| `zizmor` | v1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GH Actions auditor |
| `actionlint` | v1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter |
| `actionlint.tar.gz` | v1.7.12 | Source archive; the extracted binary above is what the skill uses |

## Why these exist

The GitHub Actions sandbox blocks `bash <(curl …)` pipe-installers and silently drops `~/.local/bin` from PATH, so the skill's runtime install paths both fail. On 2026-06-21 the skill degraded to hand-rolled regex only (`WORKFLOW_AUDIT_TOOL_DEGRADED`). These binaries were committed so the skill can put `.audit-bin/` on PATH and pick them up without any network call.

See [`memory/notes/sandbox-blocks-piped-curl-installers.md`](../memory/notes/sandbox-blocks-piped-curl-installers.md) for the original incident note.

## How the skill uses them

In `0b. Install scanners`, the skill adds `.audit-bin/` to PATH before attempting pip/curl installs, so `command -v zizmor` resolves here first:

```bash
export PATH="$PWD/.audit-bin:$PATH"
```

## Updating the binaries

When bumping `ZIZMOR_VERSION` in the skill, replace `zizmor` here with the new release binary and update the version table above. For actionlint, download the new release tar, extract the binary, replace the files, and update the table.
