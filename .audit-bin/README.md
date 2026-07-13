# .audit-bin — vendored security-audit binaries

Pre-built Linux (x86-64) binaries committed here so `workflow-security-audit`
can run offline inside the GitHub Actions sandbox without hitting PyPI or
GitHub release servers.

| Binary | Tool | Source |
|--------|------|--------|
| `zizmor` | Trail of Bits GH Actions auditor | [github.com/zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) |
| `actionlint` | Rhymond workflow linter | [github.com/rhysd/actionlint](https://github.com/rhysd/actionlint/releases) |
| `actionlint.tar.gz` | actionlint release archive | same |

The SKILL.md installer prepends `.audit-bin/` to `PATH`, so these take
priority over any system-installed copies.

## Updating

1. Download the new release binaries for `linux-amd64` from the links above.
2. Replace the files in this directory.
3. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to
   match the new zizmor release.
4. Commit only the updated binaries and the SKILL.md version bump — do not
   commit the `.tar.gz` unless it is needed for reproducibility.

## Why committed, not downloaded at runtime

GitHub Actions runners can reach PyPI and GitHub release servers, but
sandbox policies and transient network failures make that path flaky.
Committing the binaries guarantees a clean run even when outbound traffic
is restricted. The binaries are static executables with no runtime
dependencies beyond the Linux kernel.
