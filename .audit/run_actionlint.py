import subprocess, pathlib
r = subprocess.run(["./.audit-bin/actionlint", "-format", "{{json .}}"], capture_output=True, text=True, timeout=120)
pathlib.Path(".audit/actionlint.json").write_text(r.stdout)
pathlib.Path(".audit/actionlint.err").write_text(r.stderr)
print("exit:", r.returncode, "json bytes:", len(r.stdout), "err bytes:", len(r.stderr))
