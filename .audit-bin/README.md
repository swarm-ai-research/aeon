# .audit-bin — pre-built scanner cache

Pre-built binaries for the `workflow-security-audit` skill. Committed here so the
skill can run on GitHub Actions runners without hitting PyPI or remote install
scripts, which are intermittently blocked in the sandbox.

## Contents

| Binary | Tool | Version | Platform |
|--------|------|---------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GH Actions auditor | 1.25.2 | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — Rhysd's workflow linter | latest at cache time | linux/amd64 |
| `actionlint.tar.gz` | actionlint original tarball | — | linux/amd64 |

## How the skill uses these

Step 0b of `skills/workflow-security-audit/SKILL.md` checks for executable binaries
here before falling back to `pipx install` / `pip install --user` (zizmor) or the
`download-actionlint.bash` script (actionlint). Pre-cached binaries take priority.

## Updating

**zizmor:** bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`, then
replace this binary with the matching release from
<https://github.com/zizmorcore/zizmor/releases> (linux x86_64 asset).

**actionlint:** download the latest release from
<https://github.com/rhysd/actionlint/releases> (linux amd64 tar.gz), extract the
binary, replace `actionlint` and `actionlint.tar.gz` here, and note the version in
this table.

Both tools are offline-only static analyzers — no secrets or network access needed
at scan time.
