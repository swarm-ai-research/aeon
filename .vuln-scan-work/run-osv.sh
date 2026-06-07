#!/usr/bin/env bash
set -uo pipefail
TARGET="$1"
OUT="$2"
LOG="$3"
/tmp/bin/osv-scanner --format=json --recursive "$TARGET" > "$OUT" 2> "$LOG"
exit 0
