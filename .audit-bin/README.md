# .audit-bin — pre-built scanner binaries

Pre-built static binaries for the [`workflow-security-audit`](../skills/workflow-security-audit/SKILL.md) skill. These are committed to the repo as a **sandbox fallback**: GitHub-hosted runners sometimes block outbound network traffic, so `pipx install` and `curl`-based installers can fail. When that happens, the skill can use these binaries instead of failing the whole audit.

## Contents

| File | Tool | Version | Platform |
|------|------|---------|----------|
| `actionlint` | [actionlint](https://github.com/rhysd/actionlint) — GitHub Actions static analyzer | see binary (`./actionlint --version`) | linux/amd64, statically linked |
| `actionlint.tar.gz` | Source tarball for `actionlint` (kept for provenance) | matches `actionlint` binary | — |
| `zizmor` | [zizmor](https://github.com/zizmorcore/zizmor) — SARIF-capable GH Actions security auditor | 1.25.2 | linux/amd64 |

## Usage

The skill tries to install these tools via `pipx`/`pip`/`curl` first. If all network installs fail, add this directory to `PATH` before running the scanners:

```bash
export PATH="$PWD/.audit-bin:$PATH"
actionlint -format '{{json .}}' > .audit/actionlint.json 2> .audit/actionlint.err || true
zizmor --format sarif --persona auditor .github/workflows .github/actions > .audit/zizmor.sarif 2> .audit/zizmor.err || true
```

## Updating

When bumping scanner versions, replace both the binary and the version pin in SKILL.md:

- **zizmor:** Update `ZIZMOR_VERSION` in `SKILL.md` line 29, then download the matching linux/amd64 ELF from the [zizmor releases page](https://github.com/zizmorcore/zizmor/releases) and replace `.audit-bin/zizmor`.
- **actionlint:** Download the linux/amd64 tarball from the [actionlint releases page](https://github.com/rhysd/actionlint/releases), replace `.audit-bin/actionlint.tar.gz`, and extract the binary over `.audit-bin/actionlint`.

Keep the binary's execute bit set (`chmod +x`). These are the only files in this directory that should be committed — do not commit `.audit/` working files here.
