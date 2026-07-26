#!/usr/bin/env bash
set -euo pipefail
{
  git ls-files -- 'skills/*/SKILL.md' | sort | xargs sha1sum
  sha1sum scripts/skillpacks.mjs
} | sha1sum | awk '{print $1}'
