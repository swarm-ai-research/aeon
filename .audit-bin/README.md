# .audit-bin — pre-cached audit tool binaries

Pre-downloaded binaries for the `workflow-security-audit` skill. Committed here
so the skill can run in the GitHub Actions sandbox, which blocks outbound
`curl`/`pip` in the Claude Code execution environment.

## Contents

| File | Tool | Version |
|------|------|---------|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | v1.7.12 |
| `actionlint.tar.gz` | Source tarball for the above | v1.7.12 |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions security auditor | see SKILL.md `ZIZMOR_VERSION` |

## How the skill uses these

`workflow-security-audit/SKILL.md` step 0b checks whether each tool is already
on `PATH`. If not, it falls back to `pipx`/`pip` for zizmor and a curl installer
for actionlint. When those are blocked by the sandbox, the skill can resolve the
binary from this directory by prepending it to `PATH`:

```bash
export PATH="$REPO_ROOT/.audit-bin:$PATH"
```

## Updating

To update the binaries:
1. Download the new release from the project's GitHub releases page.
2. Replace the file here (`chmod +x` after replacing `actionlint`).
3. Update the version table above and `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`.
4. Commit and open a PR — do not push directly to main.
