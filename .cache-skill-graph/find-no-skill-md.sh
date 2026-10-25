#!/bin/bash
cd /home/runner/work/aeon/aeon
for d in skills/*/; do
  if ! test -f "$d/SKILL.md"; then
    echo "no SKILL.md: $d"
  fi
done
