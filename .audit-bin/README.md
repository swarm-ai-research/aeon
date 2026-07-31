# .audit-bin — pre-built scanner binaries

These binaries are committed so `workflow-security-audit` can run on GitHub Actions
without hitting network restrictions that block `pipx`/`pip` installs and
`bash <(curl …)` installer patterns in the sandbox.

## Contents

| File | Tool | Pinned version |
|------|------|----------------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — GH Actions security auditor | 1.25.2 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | see tarball |
| `actionlint.tar.gz` | source tarball for the `actionlint` binary above | — |

Both binaries are Linux amd64 executables, matching the GitHub-hosted `ubuntu-*` runner
architecture.

## How the skill uses these

`workflow-security-audit` step 0b checks for `.audit-bin/zizmor` and
`.audit-bin/actionlint` before attempting any network install. If the executables are
present and executable (`-x`), it prepends `.audit-bin/` to `$PATH` and proceeds
without touching the network.

## Upgrading

**zizmor:** bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`, then
replace this binary:

```bash
# Download the new release (linux-x86_64 asset from zizmorcore/zizmor releases)
curl -Lo .audit-bin/zizmor \
  "https://github.com/zizmorcore/zizmor/releases/download/v<NEW>/zizmor-x86_64-unknown-linux-musl"
chmod +x .audit-bin/zizmor
```

**actionlint:** download the release tarball from [rhysd/actionlint releases](https://github.com/rhysd/actionlint/releases), extract the binary, and replace both files:

```bash
curl -Lo .audit-bin/actionlint.tar.gz \
  "https://github.com/rhysd/actionlint/releases/download/v<NEW>/actionlint_<NEW>_linux_amd64.tar.gz"
tar -xzf .audit-bin/actionlint.tar.gz -C .audit-bin/ actionlint
chmod +x .audit-bin/actionlint
```

Commit both the binary and the tarball together so the tarball stays in sync with the
executable.
