#!/usr/bin/env bash
set -euo pipefail
MSG=$(cat .pending-notify-temp/surplus-pulse-2026-05-29.md)
./notify "$MSG"
