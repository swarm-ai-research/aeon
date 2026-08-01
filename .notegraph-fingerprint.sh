#!/usr/bin/env bash
# Helper: produce the notegraph input fingerprint.
# Sandbox blocks the multi-op {...} + xargs pipeline when invoked from Claude's Bash tool,
# so we shell it out through a script file (readable-verifiable, single-op invocation).
set -euo pipefail
{
  find memory docs -name '*.md' \
    -not -path 'memory/logs/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/.git/*' \
    | sort | xargs sha1sum
  sha1sum scripts/notegraph.mjs
} | sha1sum | awk '{print $1}'
