# .audit-bin

Pre-built scanner binaries committed for sandbox-safe use by the `workflow-security-audit` skill.

## Contents

| Binary | Version | Source |
|---|---|---|
| `zizmor` | v1.25.2 | https://github.com/zizmorcore/zizmor |
| `actionlint` | v1.7.12 | https://github.com/rhysd/actionlint |
| `actionlint.tar.gz` | v1.7.12 | Source archive shipped with the actionlint release |

## Why committed

GitHub Actions runners may block outbound PyPI / `curl` installs. Committing the binaries as executables lets the skill run without network access to package registries. The skill's step 0b checks for these files first and only falls back to network installs when they are absent.

## Updating

When bumping versions, keep the binary, the archive, and the version constants in `skills/workflow-security-audit/SKILL.md` in sync — all three should be updated in the same commit:

1. Download the new release binary (and `.tar.gz` for actionlint) from the upstream GitHub releases page.
2. Replace the corresponding file(s) in this directory.
3. Update `ZIZMOR_VERSION` / `ACTIONLINT_VERSION` in the SKILL.md.
