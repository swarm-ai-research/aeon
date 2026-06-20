# .audit-bin/

Pre-committed Linux x86-64 binaries for the `workflow-security-audit` skill.

GitHub Actions sandbox can block outbound network during the Claude Code phase, which prevents `pipx install zizmor` and the `curl | bash` actionlint installer from running. These binaries are the fast-path fallback: the skill checks for them before attempting a live download.

## Contents

| File | Tool | Version | Source |
|---|---|---|---|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) | 1.7.12 | release page (statically linked, no libc dep) |
| `actionlint.tar.gz` | same | 1.7.12 | original release tarball |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) | 1.25.2 | release page (dynamically linked, requires glibc ≥ 2.17) |

## Updating

When bumping `ZIZMOR_VERSION` or `actionlint` in the skill's `SKILL.md`:

1. Download the new Linux x86-64 release binary from the project's GitHub releases page.
2. Replace the file here (`chmod +x` after copying).
3. Update the version column in this table.
4. Commit together with the `ZIZMOR_VERSION` bump in `SKILL.md` so they stay in sync.

## Notes

- Only the `workflow-security-audit` skill uses these binaries; no other skill or script references `.audit-bin/`.
- The skill's install block checks `[ -x ".audit-bin/zizmor" ]` and `[ -x ".audit-bin/actionlint" ]` before falling back to live download.
- These binaries are committed as compiled artifacts, not source. Review release signatures before updating.
