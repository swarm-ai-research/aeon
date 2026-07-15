# .audit-bin — pre-bundled security scanners

Pre-downloaded static binaries for `workflow-security-audit`. The GitHub Actions sandbox
blocks `bash <(curl …)` pipe-install patterns, so these binaries are committed directly
to avoid falling back to hand-rolled regex coverage.

See `memory/notes/sandbox-blocks-piped-curl-installers.md` for the incident that prompted this.

## Pinned versions

| Binary | Version | Source |
|--------|---------|--------|
| `actionlint` | v1.7.12 | https://github.com/rhysd/actionlint/releases |
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |

`actionlint.tar.gz` is the original release archive kept alongside the extracted binary
so the checksum can be verified without re-downloading.

## Updating

1. Download the new release tarball for `actionlint` (linux-amd64) and replace
   `actionlint` + `actionlint.tar.gz`.
2. Download the new `zizmor` binary (linux-amd64) and replace `zizmor`.
3. `chmod +x actionlint zizmor`
4. Update the pinned version comment in `skills/workflow-security-audit/SKILL.md`
   (step 0b, `ZIZMOR_VERSION` and the actionlint `ACTIONLINT_VERSION` comment).
5. Commit with message `chore(audit-bin): bump actionlint to vX.Y.Z / zizmor to A.B.C`.
