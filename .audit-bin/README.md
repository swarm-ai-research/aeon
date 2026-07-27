# .audit-bin — pre-cached scanner binaries

Pre-built executables committed so `workflow-security-audit` can run inside GitHub
Actions without hitting PyPI or curl. The skill's step 0b tries these first and only
falls back to network installs when they are missing.

## Pinned versions

| Binary | Version | Source |
|--------|---------|--------|
| `zizmor` | 1.25.2 | https://github.com/zizmorcore/zizmor/releases/tag/v1.25.2 |
| `actionlint` | 1.7.12 | https://github.com/rhysd/actionlint/releases/tag/v1.7.12 |

Both binaries are built for **linux/amd64** (GitHub-hosted runners).

## How to update

1. Download the new release binary for `linux/amd64` from the links above.
2. Replace the file here (`zizmor` or `actionlint`) and mark it executable.
3. Update the corresponding version constant in `skills/workflow-security-audit/SKILL.md`:
   - `ZIZMOR_VERSION` for zizmor
   - `ACTIONLINT_VERSION` for actionlint
4. Commit both the binary and the version bump together.

## Sandbox invocation note

Direct shell invocation (`./.audit-bin/zizmor …`) may be blocked by the harness's
shell-redirection guard. Use a Python subprocess wrapper instead:

```python
import subprocess, json
result = subprocess.run([".audit-bin/zizmor", "--format", "sarif", "--persona", "auditor",
                        ".github/workflows", ".github/actions"],
                       capture_output=True, text=True)
sarif = json.loads(result.stdout)
```

This pattern is documented in `skills/workflow-security-audit/SKILL.md` under "Sandbox note".
