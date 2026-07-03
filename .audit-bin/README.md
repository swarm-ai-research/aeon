# .audit-bin

Pre-bundled static binaries for the `workflow-security-audit` skill.

## Why this exists

GitHub Actions sandboxes block `bash <(curl …)` installers and restrict `~/.local/bin` execution,
so the skill cannot download its own scanners at runtime. These binaries are committed directly
so the skill can find them at `$PWD/.audit-bin/` without any network calls.

See `memory/notes/sandbox-blocks-piped-curl-installers.md` for the incident that motivated this.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) | 1.7.12 | linux/amd64 (static) |
| `actionlint.tar.gz` | actionlint source archive | 1.7.12 | — |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) | 1.25.2 | linux/amd64 |

## Updating

1. Download the new release binaries for `linux/amd64` from each tool's GitHub releases page.
2. Replace the files here and update the version table above.
3. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match the new zizmor version.
4. Commit as `chore(audit-bin): bump actionlint to X.Y.Z / zizmor to X.Y.Z`.

Do not add binaries for other platforms — GHA runners are always `linux/amd64`.
