# .audit-bin

Pre-built scanner binaries committed for offline use by `workflow-security-audit`.
These take priority over network installs on GitHub Actions runners where PyPI/curl may be blocked.

## Versions

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | v1.25.2 | [zizmorcore/zizmor releases](https://github.com/woodruffw/zizmor/releases) |
| `actionlint` | v1.7.12 | [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases) |

`actionlint.tar.gz` is the upstream release tarball for `actionlint` (kept alongside the binary as the version reference).

## Upgrading

When bumping either tool:
1. Replace the binary (and tarball for actionlint) with the new release.
2. Update the version row in this table.
3. For `zizmor`, also update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
