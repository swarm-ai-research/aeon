#!/usr/bin/env bash
set -euo pipefail
cd /home/runner/work/aeon/aeon
MSG=$(cat .pending-notify-temp/skill-health-2026-06-26.md)
./notify "$MSG"
