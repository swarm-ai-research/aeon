#!/usr/bin/env python3
"""Queue the notify message directly to .pending-notify/ (skill 'Standardize
notification emission' preference per memory: direct write, no `./notify -f`)."""
import pathlib, subprocess

msg = pathlib.Path(".audit/notify_msg.txt").read_text()
ts = subprocess.check_output(["date", "-u", "+%s"]).decode().strip()
pending = pathlib.Path(".pending-notify")
pending.mkdir(exist_ok=True)
out = pending / f"{ts}-workflow-security-audit.md"
out.write_text(msg)
print(f"queued: {out} ({len(msg)} bytes)")
