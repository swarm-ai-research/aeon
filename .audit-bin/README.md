# .audit-bin — Pre-cached scanner binaries

These executables are committed so `workflow-security-audit` can run without
hitting the network on GitHub Actions runners where PyPI and
`raw.githubusercontent.com` may be blocked.

## Contents

| File | Tool | Version | Source |
|------|------|---------|--------|
| `zizmor` | SARIF-capable GH Actions auditor | **1.25.2** | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits) |
| `actionlint` | Workflow syntax + shellcheck linter | run `./actionlint --version` | [rhysd/actionlint](https://github.com/rhysd/actionlint) |
| `actionlint.tar.gz` | Original release tarball | — | kept for reference / re-extraction |

Both binaries are `linux/amd64` — built for GitHub-hosted `ubuntu-*` runners.

## Updating

**zizmor** — bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`,
then download the matching `zizmor-x86_64-unknown-linux-gnu` binary from the
[releases page](https://github.com/zizmorcore/zizmor/releases) and replace
`.audit-bin/zizmor`. `chmod +x` it before committing.

**actionlint** — run the upstream download script to get the latest release:

```bash
cd .audit-bin
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
# rename the produced tarball and binary in place
mv actionlint_*.tar.gz actionlint.tar.gz
chmod +x actionlint
```

Then update the version note in `skills/workflow-security-audit/SKILL.md`'s
`## Sandbox note` to reflect the new version.
