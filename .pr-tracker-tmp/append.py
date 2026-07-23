#!/usr/bin/env python3
from pathlib import Path
log = Path("/home/runner/work/aeon/aeon/memory/logs/2026-07-23.md")
entry = Path("/home/runner/work/aeon/aeon/.pr-tracker-tmp/log_entry.md").read_text()
existing = log.read_text() if log.exists() else ""
log.write_text(existing + entry)
print(f"log now {len(log.read_text())} bytes")
