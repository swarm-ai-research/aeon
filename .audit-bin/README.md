# .audit-bin

Pre-downloaded audit tool binaries. The `workflow-security-audit` skill installs
these tools at runtime, but if the GitHub Actions sandbox blocks outbound network
access, adding `.audit-bin` to `$PATH` before the install step lets the skill use
these cached copies instead.

## Contents

| File | Tool | Version |
|---|---|---|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — GitHub Actions workflow linter | 1.7.12 |
| `actionlint.tar.gz` | Source tarball for `actionlint` | 1.7.12 |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits GHA security auditor | 1.25.2 |

## Updating

Download replacement binaries from each project's releases page and overwrite the
files here. Update the version table above and the `ZIZMOR_VERSION` pin in
`skills/workflow-security-audit/SKILL.md`.
