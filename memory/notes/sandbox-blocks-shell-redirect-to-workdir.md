---
id: sandbox-blocks-shell-redirect-to-workdir
created: 2026-07-11
type: lesson
links: [[sandbox-blocks-piped-curl-installers]], [[notify-inline-cat-substitution-blocked-in-sandbox]]
---
# The sandbox blocks shell `>` redirects to working-dir paths; workaround is Python `pathlib.Path.write_text` after `subprocess.run`

Observed 2026-07-11 during `vuln-scanner` on `oomol-lab/open-connector`: shell `some-cmd > /tmp/out.json` was refused by the session sandbox even when the process itself was permitted, while the same command's own output flag (semgrep's `-o /tmp/out.json`) worked. **2026-08-08 vuln-scanner on `yc-software/qm` observed the scope widen** — both `>` and `>>` are now blocked even for paths under the working directory (`/home/runner/work/aeon/aeon/...`), and `cp` inside the workdir also fails; only the tool's own `-o`, Python `pathlib.Path.write_text` after `subprocess.run`, and the Write/Edit tools remain reliable. Any future skill that pipes scanner or CLI stdout into a file should either use the tool's own `-o`/`--output` flag or wrap the invocation in Python `write_text` rather than a bare `>` redirect — assume workdir writes via shell redirection are as blocked as `/tmp/` writes.
