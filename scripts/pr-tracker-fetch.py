#!/usr/bin/env python3
"""One-shot: run the pr-tracker GraphQL query and write the JSON payload to disk."""
import subprocess
import sys
from pathlib import Path

query_file = Path("/tmp/pr-tracker-query.graphql")
out_file = Path(".pending-notify-temp/pr-tracker-raw.json")
out_file.parent.mkdir(exist_ok=True)

result = subprocess.run(
    ["gh", "api", "graphql", "-F", f"query=@{query_file}"],
    capture_output=True, text=True,
)
if result.returncode != 0:
    sys.stderr.write(f"gh exit={result.returncode}\nstderr={result.stderr}\n")
    sys.exit(result.returncode)
out_file.write_text(result.stdout)
print(f"wrote {len(result.stdout)} bytes to {out_file}")
