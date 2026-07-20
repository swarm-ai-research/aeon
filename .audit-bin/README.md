# .audit-bin

Pre-built scanner binaries committed to the repo so the `workflow-security-audit` skill can run inside GitHub Actions without hitting sandbox-blocked network installs.

## Tools

| Binary | Tool | Version | Source |
|---|---|---|---|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions security auditor (Trail of Bits) | 1.25.2 | PyPI / release tarball |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — syntax-level workflow linter | see note | download-actionlint.bash |
| `actionlint.tar.gz` | Original download archive for `actionlint` | same | GitHub releases |

**actionlint version note:** actionlint was installed via `download-actionlint.bash` which fetches the latest release at download time. Run `./actionlint --version` to confirm the pinned version and record it here when upgrading.

## Why committed binaries?

The GitHub Actions sandbox may block outbound requests to PyPI and arbitrary curl targets. Shipping the binaries removes the install step and makes every skill run hermetic.

## Updating

When `ZIZMOR_VERSION` is bumped in `skills/workflow-security-audit/SKILL.md`:

```bash
# Replace zizmor (x86-64 Linux)
ZIZMOR_VERSION="<new version>"
curl -L "https://github.com/zizmorcore/zizmor/releases/download/v${ZIZMOR_VERSION}/zizmor-x86_64-unknown-linux-gnu.tar.gz" \
  | tar xz zizmor
mv zizmor .audit-bin/zizmor
chmod +x .audit-bin/zizmor

# Replace actionlint (fetches latest)
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
mv actionlint .audit-bin/actionlint
cp actionlint.tar.gz .audit-bin/actionlint.tar.gz
chmod +x .audit-bin/actionlint
```

Commit both binaries together with the version-bump commit so the pin and the binary stay in sync.

## Platform

Both binaries target **x86-64 Linux** (the GitHub-hosted `ubuntu-*` runner architecture). They will not run on macOS or ARM.
