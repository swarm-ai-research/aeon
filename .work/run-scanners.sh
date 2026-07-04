#!/usr/bin/env bash
# Runs all three remaining scanners against the cloned target and writes
# outputs to /home/runner/work/aeon/aeon/scan-out/*.
# Semgrep was already run separately (uses -o flag).
set -u

TARGET="/home/runner/work/aeon/aeon/.work/torlink"
OUT="/home/runner/work/aeon/aeon/scan-out"
BIN="/tmp/bin"

# TruffleHog filesystem (working-tree secrets, verified only)
"${BIN}/trufflehog" filesystem "${TARGET}" --only-verified --json \
  > "${OUT}/trufflehog.json" 2> "${OUT}/trufflehog.stderr"
echo "trufflehog.fs=$?"

# TruffleHog git history (past secrets, verified only)
"${BIN}/trufflehog" git "file://${TARGET}" --only-verified --json \
  > "${OUT}/trufflehog-git.json" 2> "${OUT}/trufflehog-git.stderr"
echo "trufflehog.git=$?"

# OSV-Scanner (dependency CVEs)
"${BIN}/osv-scanner" --format=json --recursive "${TARGET}" \
  > "${OUT}/osv.json" 2> "${OUT}/osv.stderr"
echo "osv=$?"
