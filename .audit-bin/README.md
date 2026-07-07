# .audit-bin/

Pre-cached static binaries for the `workflow-security-audit` skill.

Both `zizmor` and `actionlint` are committed here because the GitHub Actions
sandbox blocks `bash <(curl …)` piped installs and does not have `~/.local/bin`
on PATH, causing the skill to degrade to hand-rolled regex-only coverage.

The `workflow-security-audit` SKILL.md prepends this directory to PATH first;
network installs are only attempted if a binary is missing from here.

## Updating

Replace the binaries here and bump `ZIZMOR_VERSION` in the SKILL.md `0b` step:

- **zizmor** — download the `x86_64-unknown-linux-musl` release asset from
  `https://github.com/zizmorcore/zizmor/releases` and replace `zizmor`.
- **actionlint** — download the `linux_amd64` release asset from
  `https://github.com/rhysd/actionlint/releases`, extract it, and replace
  `actionlint`. The `actionlint.tar.gz` here is the original archive for
  reference; it does not need to be updated separately.

Both binaries must be `chmod +x` after replacement.
