# .audit-bin — Pre-built scanner binaries

Pre-built, statically-linked Linux x86-64 binaries committed here so the
`workflow-security-audit` skill can run without network access. The GitHub
Actions sandbox used by Aeon blocks `bash <(curl …)` piped installers and
does not guarantee `~/.local/bin` is on `PATH`, so on-the-fly installation
is unreliable (see `memory/notes/sandbox-blocks-piped-curl-installers.md`).

## Contents

| Binary | Version | Source |
|--------|---------|--------|
| `actionlint` | 1.7.12 | <https://github.com/rhysd/actionlint/releases> |
| `actionlint.tar.gz` | 1.7.12 | original release archive (kept for verification) |
| `zizmor` | 1.25.2 | <https://github.com/zizmorcore/zizmor/releases> |

## Usage

The `workflow-security-audit` SKILL.md install section falls back to these
binaries when `pip`/`pipx` and `curl` installs are unavailable:

```bash
export PATH="$REPO_ROOT/.audit-bin:$PATH"
```

After that, `zizmor` and `actionlint` resolve without any download.

## Updating

To upgrade, replace the binary and update the version pins in:
- This README
- `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` var and the
  comment pinning actionlint)
