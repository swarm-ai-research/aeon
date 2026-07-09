# .audit-bin — pre-fetched scanner binaries

This directory holds pre-downloaded scanner binaries so `workflow-security-audit`
can run without any outbound network access (sandbox-safe fallback).

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases |
| `actionlint` | latest at time of fetch | https://github.com/rhysd/actionlint/releases |

The skill's `preflight` step (Step 0b) prepends this directory to `$PATH` before
attempting `pipx install` or curl-based installs, so these binaries act as an
offline cache when the runner sandbox blocks outbound traffic.

## Updating

When bumping `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md`:

1. Download the matching binary for `linux-amd64` from the zizmor releases page.
2. Replace `.audit-bin/zizmor` with the new binary (`chmod +x` it).
3. Update the version row in this table.

For `actionlint`, re-run:
```bash
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
mv actionlint .audit-bin/actionlint
```

Do not commit `.audit-bin/*.tar.gz` — only the extracted executable is needed.
