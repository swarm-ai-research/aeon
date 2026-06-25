# .audit-bin — Pre-bundled scanner binaries

Pre-compiled binaries for the `workflow-security-audit` skill, committed here to
work around the GitHub Actions sandbox restriction that blocks `bash <(curl …)` pipe
installations (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `actionlint` | v1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) — Linux amd64, statically linked |
| `actionlint.tar.gz` | v1.7.12 | Original release archive (retained for checksum verification) |
| `zizmor` | v1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) — Linux amd64 |

## Usage

The `workflow-security-audit` skill prepends `.audit-bin/` to `PATH` at the start of
the scanner bootstrap step, so both tools resolve here before any network install is
attempted:

```bash
export PATH="$PWD/.audit-bin:$PATH"
```

## Updating

1. Download the new Linux amd64 release binary from the upstream release page.
2. Replace the binary (and `actionlint.tar.gz` if updating actionlint).
3. Update the version comment in `skills/workflow-security-audit/SKILL.md`
   (`ZIZMOR_VERSION` var and the actionlint version note in step 0b).
4. Commit: `chore(audit-bin): bump <tool> to vX.Y.Z`.

Both tools are offline-only static analyzers — no secrets or network access needed
at scan time.
