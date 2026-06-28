# .audit-bin — pre-cached scanner binaries

Pre-downloaded binaries for the `workflow-security-audit` skill. Committed to the repo so the skill can run without network access when the GitHub Actions sandbox blocks `curl`/`pip` installers.

## Contents

| Binary | Tool | Version | Source |
|--------|------|---------|--------|
| `zizmor` | [zizmor](https://docs.zizmor.sh) — SARIF-capable GH Actions auditor | 1.25.2 | `pip install zizmor==1.25.2` |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax linter | see binary | rhysd/actionlint download script |
| `actionlint.tar.gz` | actionlint source archive | see above | original tarball |

## Usage

The skill adds `.audit-bin/` to `PATH` at step 0b before attempting any network install:

```bash
export PATH="$PWD/.audit-bin:$PATH"
```

## Refreshing the cache

To update a binary, download the new version locally and replace the file here, then commit:

```bash
# Update zizmor (replace 1.25.2 with the new version)
pip download --no-deps --dest /tmp/zizmor-dl zizmor==<NEW_VERSION>
# Extract the linux x86-64 binary and copy to .audit-bin/zizmor

# Update actionlint
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
cp actionlint .audit-bin/actionlint
tar czf .audit-bin/actionlint.tar.gz actionlint
```

Also bump `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` when upgrading zizmor.
