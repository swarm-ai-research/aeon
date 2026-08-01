# .audit-bin — pre-cached security scanner binaries

Pre-built Linux (x86-64) binaries committed here so `workflow-security-audit` can run
on GitHub Actions runners without relying on outbound PyPI or curl installs, which are
blocked in the Aeon sandbox.

## Pinned versions

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | see tarball | https://github.com/rhysd/actionlint/releases |
| `actionlint.tar.gz` | (upstream release archive, kept for reference) | same |

## Upgrade procedure

**zizmor:**
1. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`.
2. Download the new Linux binary from the zizmor releases page.
3. Replace `.audit-bin/zizmor` and commit.

**actionlint:**
1. Download the new release tarball from the actionlint releases page.
2. Extract the `actionlint` binary and replace `.audit-bin/actionlint`.
3. Replace `.audit-bin/actionlint.tar.gz` with the new tarball.
4. Record the new version in the table above and in SKILL.md.

## Notes

- Both tools are offline-only static analyzers — no secrets or network access needed at scan time.
- The skill's Step 0b checks for these binaries first; network fallbacks only trigger when the binary is absent.
- Binaries are Linux x86-64. They will not work on macOS/ARM runners without replacement.
