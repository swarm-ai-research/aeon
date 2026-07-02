# .audit-bin/

Pre-seeded scanner binaries committed to let `workflow-security-audit` work inside the GitHub Actions Claude sandbox, which blocks `bash <(curl ...)` and `pipx install` calls at runtime (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).

## Contents

| Binary | Tool | Platform |
|--------|------|----------|
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) 1.25.2 — Trail of Bits SARIF-capable GHA auditor | linux/amd64 |
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — workflow syntax and security linter | linux/amd64 |
| `actionlint.tar.gz` | Source archive for the actionlint binary above | — |

## How the skill uses these

At the start of step 0b in `skills/workflow-security-audit/SKILL.md`, prepend this directory to `$PATH`:

```bash
export PATH="$PWD/.audit-bin:$PATH"
```

The `if ! command -v zizmor` and `if ! command -v actionlint` guards in step 0b then resolve immediately, skipping the network install entirely and keeping the run offline.

## Updating

When bumping scanner versions:
1. Download the new `zizmor` linux/amd64 binary from the [zizmorcore/zizmor releases page](https://github.com/zizmorcore/zizmor/releases) and replace the binary here.
2. Fetch a new `actionlint` binary using the download script referenced in `SKILL.md` step 0b and replace the binary here.
3. Update `ZIZMOR_VERSION` in `skills/workflow-security-audit/SKILL.md` to match the new zizmor binary.
4. Commit the binaries and the SKILL.md version bump together so they stay in sync.
