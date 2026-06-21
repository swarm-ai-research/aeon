---
id: gha-inputs-unquoted-shell-rce
created: 2026-06-21
type: lesson
links: [[github-actions-cannot-create-prs]]
---
# Workflow `inputs.*` values flowing unquoted into shell commands are an RCE channel on write-access dispatch

The 2026-06-21 workflow-security-audit caught `inputs.agent` in `fleet-runner.yml` flowing unquoted into `--agent $AGENT` and `node ... once $ARGS`; any actor with workflow-dispatch write can run arbitrary code on the runner. The fix is the standard 4-line shell-array refactor — assign the input to a quoted env var, then expand as `"$VAR"` (or `"${ARGS[@]}"` for argv) inside `run:`. Sweep any other `run:` block that splices `${{ inputs.X }}` directly into a shell command before passing the input as an env.
