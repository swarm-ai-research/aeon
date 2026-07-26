# .audit-bin — pre-built scanner binaries

Pre-built Linux x86-64 binaries committed here so the `workflow-security-audit` skill
can run offline on GitHub Actions runners without hitting PyPI or external download URLs.

| Binary | Version | Source |
|--------|---------|--------|
| `actionlint` | v1.7.12 | https://github.com/rhysd/actionlint/releases/tag/v1.7.12 |
| `zizmor` | v1.25.2 | https://github.com/woodruffw/zizmor/releases/tag/v1.25.2 |
| `actionlint.tar.gz` | v1.7.12 | original release tarball (kept for auditing) |

## Updating

1. Download the new release tarball from the upstream GitHub release page.
2. Extract and replace the binary in this directory.
3. Update the version constant in `skills/workflow-security-audit/SKILL.md`
   (`ZIZMOR_VERSION` for zizmor, `ACTIONLINT_VERSION` for actionlint).
4. Commit both the binary and the SKILL.md change together.

## Notes

- Both binaries are Linux x86-64 ELF executables — they will not run on macOS or Windows.
- `zizmor` is dynamically linked (requires glibc ≥ 3.2); `actionlint` is statically linked.
- The skill's step 0b checks for these binaries first, before attempting any network install,
  so they are the primary execution path on sandboxed runners.
