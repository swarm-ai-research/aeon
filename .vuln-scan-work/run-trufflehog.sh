#!/usr/bin/env bash
set -uo pipefail
TARGET="$1"
OUT="$2"
LOG="$3"
/tmp/bin/trufflehog filesystem "$TARGET" --only-verified --json > "$OUT" 2> "$LOG"
exit 0
