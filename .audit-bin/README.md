# .audit-bin — pre-cached scanner binaries

Pre-built binaries for the `workflow-security-audit` skill. Committed here so the
skill can run offline without hitting PyPI or GitHub release downloads on every
execution.

| Binary | Tool | Version |
|--------|------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GH Actions auditor | 1.25.2 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | latest-at-cache-time |
| `actionlint.tar.gz` | same binary, compressed (source tarball from release) | — |

## How the skill uses these

`skills/workflow-security-audit/SKILL.md` step 0b adds `.audit-bin/` to `$PATH`
before running `command -v zizmor` / `command -v actionlint`. If the binaries are
found, the dynamic install (pipx / curl) is skipped.

## Updating

Re-run `workflow-security-audit` on a runner with network access. The skill's
preflight downloads the tools if absent, and the resulting commit lands them here
for future offline runs. Bump `ZIZMOR_VERSION` in the SKILL.md before doing so.
