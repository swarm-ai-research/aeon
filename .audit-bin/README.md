# .audit-bin — pre-built scanner binaries

Pre-built Linux x86-64 executables committed for the `workflow-security-audit` skill.
They are the primary tool source on GitHub Actions runners, where outbound network
(PyPI / curl) may be sandbox-blocked.

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | Trail of Bits SARIF-capable GH Actions auditor | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | rhysd syntax-level workflow linter | 1.26.1 | https://github.com/rhysd/actionlint/releases |

`actionlint.tar.gz` is the original release archive; the extracted `actionlint` binary
next to it is what the skill uses at runtime.

## Updating

When bumping a tool version:

1. Download the new Linux x86-64 binary from the tool's GitHub releases page.
2. Replace the file here (`zizmor` or `actionlint` + `actionlint.tar.gz`).
3. Update the matching version pin in `skills/workflow-security-audit/SKILL.md`
   (`ZIZMOR_VERSION` or `ACTIONLINT_VERSION`).
4. Commit all three changes together so the binary and the pin stay in sync.
