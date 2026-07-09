# .audit-bin — pre-bundled audit scanner binaries

This directory ships static binaries for the two tools used by `workflow-security-audit`:

| Binary | Tool | Purpose |
|--------|------|---------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) (Trail of Bits) | SARIF-capable security auditor for GitHub Actions workflows |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) | Syntax-level linter for GitHub Actions workflow files |
| `actionlint.tar.gz` | actionlint release archive | Source tarball kept alongside the extracted binary |

## Why these are committed

The GitHub Actions sandbox blocks outbound network from `bash`, so the SKILL.md's
`pipx install zizmor` and `bash <(curl …)` download paths both fail at runtime.
Shipping the binaries here lets the skill resolve them without any network call —
just add `.audit-bin/` to `$PATH` before running the scanners.

## Versions

Run the binaries to confirm their exact versions:

```bash
.audit-bin/zizmor --version
.audit-bin/actionlint --version
```

The `ZIZMOR_VERSION` pin in `skills/workflow-security-audit/SKILL.md` (step 0b)
should always match the version of the `zizmor` binary here.

## Updating

1. Download the new release binary for `linux/amd64` from the tool's GitHub releases page.
2. Replace the binary here and mark it executable (`chmod +x`).
3. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match.
4. Commit all three together so SKILL.md and the binary stay in sync.
