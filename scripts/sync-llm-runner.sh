#!/usr/bin/env bash
# Sync the canonical shared/llm-runner.ts into each TS consumer that runs LLMs.
# Run after editing shared/llm-runner.ts; commit the regenerated copies alongside.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL="$REPO_ROOT/shared/llm-runner.ts"

TARGETS=(
  "$REPO_ROOT/mcp-server/src/llm-runner.ts"
  "$REPO_ROOT/a2a-server/src/llm-runner.ts"
)

for target in "${TARGETS[@]}"; do
  mkdir -p "$(dirname "$target")"
  cp "$CANONICAL" "$target"
  echo "wrote $target"
done
