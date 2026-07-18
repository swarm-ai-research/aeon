# .audit-bin/

Pre-built binaries for the `workflow-security-audit` skill, committed so the
skill can run offline on GitHub Actions runners where outbound package installs
(PyPI, curl) may be sandbox-blocked.

| Binary | Tool | Version | Architecture |
|--------|------|---------|--------------|
| `actionlint` | [rhysd/actionlint](https://github.com/rhysd/actionlint) — GitHub Actions workflow linter | v1.7.12 | linux/amd64 |
| `actionlint.tar.gz` | Same actionlint binary, tarball form | v1.7.12 | linux/amd64 |
| `zizmor` | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable security auditor | v1.25.2 | linux/amd64 |

## Updating

1. Check the latest releases:
   - actionlint: <https://github.com/rhysd/actionlint/releases>
   - zizmor: <https://github.com/zizmorcore/zizmor/releases>
2. Download the new `linux/amd64` binary from the release assets.
3. Replace the file(s) here and update the version comment in
   `skills/workflow-security-audit/SKILL.md` (step 0b).
4. For zizmor, also bump `ZIZMOR_VERSION` in that same step.
