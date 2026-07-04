# .audit-bin/

Pre-built Linux amd64 scanner binaries committed to the repo so the
`workflow-security-audit` skill can run inside the GitHub Actions sandbox
without any network access.

The GHA sandbox blocks `bash <(curl …)` installer patterns and often blocks
`pip install` to PyPI. These binaries bypass that limitation — the skill
prepends `.audit-bin/` to `PATH` before attempting any network fallback.

| Binary | Tool | Source |
|--------|------|--------|
| `zizmor` | Trail of Bits SARIF-capable GH Actions auditor | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | Rhysd's workflow syntax linter | https://github.com/rhysd/actionlint/releases |
| `actionlint.tar.gz` | Archive used to extract the `actionlint` binary | same |

**To update:** download the new release binary for your target platform
(`linux_amd64`), replace the file here, and bump the `ZIZMOR_VERSION`
constant in `skills/workflow-security-audit/SKILL.md` to match.
