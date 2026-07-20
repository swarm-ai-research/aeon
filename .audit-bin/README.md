# .audit-bin — pre-committed scanner binaries

Pre-built executables committed here so the `workflow-security-audit` skill can
run on GitHub Actions runners without requiring outbound PyPI or GitHub downloads
(which the GHA sandbox blocks intermittently).

## Contents

| File | Tool | Version |
|------|------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — Trail of Bits SARIF-capable GHA auditor | 1.25.2 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — Rhymond's workflow syntax linter | see commit message |
| `actionlint.tar.gz` | actionlint release archive (source for the binary above) | — |

## How the skill uses these

`skills/workflow-security-audit/SKILL.md` step 0b checks for `PATH`-executable
`zizmor` / `actionlint` here first, before falling back to `pipx` / `pip` /
`curl` network installs.  On a clean GHA runner this cache is the primary path.

## Updating

1. Download the new release binary from the tool's GitHub releases page.
2. Replace the file: `cp /path/to/new-binary .audit-bin/<tool>` and `chmod +x`.
3. Bump `ZIZMOR_VERSION` (or note the actionlint version) in
   `skills/workflow-security-audit/SKILL.md` step 0b.
4. Commit both changes together so the pin and binary stay in sync.

> **Platform:** binaries are built for `linux/amd64` to match GitHub-hosted
> `ubuntu-*` runners.  They will not run on macOS or Windows runner images.
