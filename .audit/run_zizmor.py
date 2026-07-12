import subprocess, pathlib, sys

targets = [".github/workflows", ".github/actions"]
# .github/actions may not exist; filter to existing
existing = [t for t in targets if pathlib.Path(t).exists()]
cmd = ["./.audit-bin/zizmor", "--format", "sarif", "--persona", "auditor"] + existing
r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
pathlib.Path(".audit/zizmor.sarif").write_text(r.stdout)
pathlib.Path(".audit/zizmor.err").write_text(r.stderr)
print("exit:", r.returncode, "sarif bytes:", len(r.stdout), "err bytes:", len(r.stderr))
