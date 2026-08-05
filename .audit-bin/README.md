# .audit-bin

Pre-built scanner binaries committed to the repo so the `workflow-security-audit` skill can run on GitHub Actions runners without hitting PyPI or outbound curl.

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | [zizmorcore/zizmor](https://github.com/zizmorcore/zizmor/releases) — Trail of Bits SARIF-capable GH Actions auditor |
| `actionlint` | 1.7.12 | [rhysd/actionlint](https://github.com/rhysd/actionlint/releases) — syntax-level workflow linter |

`actionlint.tar.gz` is the upstream release tarball from which the `actionlint` binary was extracted.

## Updating

1. Download the new release binary for `linux/amd64` from the upstream release page.
2. Replace the file in this directory (`chmod +x` the binary).
3. Update the version pin in `skills/workflow-security-audit/SKILL.md` (`ZIZMOR_VERSION` for zizmor; update the comment for actionlint).
4. Commit both together so the pin and binary stay in sync.

The skill's `0b. Install scanners` step checks for these binaries first; network installs (`pipx`/`curl`) are only attempted if they're missing.
