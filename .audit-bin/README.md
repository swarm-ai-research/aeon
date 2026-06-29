# .audit-bin — pre-cached security scanner binaries

Pre-downloaded binaries for the `workflow-security-audit` skill. Committed to the repo so the skill works even when the GitHub Actions sandbox blocks outbound downloads to PyPI or GitHub releases.

| File | Tool | Version | Source |
|------|------|---------|--------|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level GitHub Actions linter | see `actionlint --version` | rhysd/actionlint releases |
| `actionlint.tar.gz` | same — archive used for extraction on targets without the binary in PATH | — | same |
| `zizmor` | [zizmor](https://docs.zizmor.sh) — SARIF-capable GitHub Actions security auditor | 1.25.2 (pinned in SKILL.md) | zizmorcore/zizmor releases |

## Why these are committed

The `workflow-security-audit` skill tries `pipx install zizmor` and `curl | bash` for actionlint at runtime. Both can be blocked by the GitHub Actions network sandbox. Having the binaries here lets the skill fall back to `PATH=".audit-bin:$PATH"` without any network call.

## Updating

1. Download the new release binaries from the respective release pages.
2. Replace the files here (keep the same filenames).
3. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
4. Commit with a message like `chore: bump audit-bin zizmor to X.Y.Z`.
