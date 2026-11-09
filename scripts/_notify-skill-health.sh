#!/usr/bin/env bash
set -euo pipefail
BODY=$(cat .pending-notify/1794272482-skill-health.md)
./notify "$BODY"
