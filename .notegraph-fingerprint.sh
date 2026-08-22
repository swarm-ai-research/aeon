#!/bin/bash
set -e
find memory docs -name '*.md' \
  -not -path 'memory/logs/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  | sort | xargs sha1sum > /tmp/notegraph.files.sha
sha1sum scripts/notegraph.mjs >> /tmp/notegraph.files.sha
FINGERPRINT=$(sha1sum /tmp/notegraph.files.sha | cut -c1-40)
echo "$FINGERPRINT"
