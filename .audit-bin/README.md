# .audit-bin/

Pre-cached scanner binaries for the `workflow-security-audit` skill. Committing them avoids
network installs on GitHub Actions runners where outbound PyPI/curl may be blocked.

The skill's `Step 0b` checks for these executables first and adds this directory to `$PATH`
before falling back to `pipx install` / `curl` installs.

## Binaries

| Binary | Source | Pinned version |
|--------|--------|----------------|
| `zizmor` | [zizmorcore/zizmor](https://github.com/woodruffw/zizmor) | `1.25.2` (matches `ZIZMOR_VERSION` in SKILL.md) |
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) | see tarball below |
| `actionlint.tar.gz` | same release as `actionlint` | original release archive |

## Updating

When bumping tool versions, replace the binary **and** update the version pin in
`skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` for zizmor).

```bash
# zizmor — replace with the new release binary from:
#   https://github.com/woodruffw/zizmor/releases

# actionlint — download the desired release from:
#   https://github.com/rhysd/actionlint/releases
# Replace both actionlint and actionlint.tar.gz, then update this README.
```

Both tools are offline-only static analyzers — no secrets or network access needed at scan time.
