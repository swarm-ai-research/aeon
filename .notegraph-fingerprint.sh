#!/bin/bash
set -e
find memory docs -name '*.md' \
  -not -path 'memory/logs/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  | LC_ALL=C sort | xargs sha1sum > /tmp/hashes.txt
sha1sum scripts/notegraph.mjs >> /tmp/hashes.txt
sha1sum /tmp/hashes.txt | awk '{print $1}'
