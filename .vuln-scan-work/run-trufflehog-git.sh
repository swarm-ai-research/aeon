#!/usr/bin/env bash
set -uo pipefail
TARGET="$1"
OUT="$2"
LOG="$3"
/tmp/bin/trufflehog git "file://$TARGET" --only-verified --json > "$OUT" 2> "$LOG"
exit 0
