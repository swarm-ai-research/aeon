#!/bin/bash
set -euo pipefail
{
  find memory docs -name '*.md' \
    -not -path 'memory/logs/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/.git/*' \
    | sort | xargs sha1sum
  sha1sum scripts/notegraph.mjs
} | sha1sum | awk '{print $1}'
