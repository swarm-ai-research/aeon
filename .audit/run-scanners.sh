#!/bin/bash
set -u
cd "$(dirname "$0")/.."
export PATH="$PWD/.audit-bin:$PATH"

echo "=== zizmor ==="
zizmor --format sarif --persona auditor .github/workflows > .audit/zizmor.sarif 2> .audit/zizmor.err
echo "zizmor_exit=$?"

echo "=== actionlint ==="
actionlint -format '{{json .}}' > .audit/actionlint.json 2> .audit/actionlint.err
echo "actionlint_exit=$?"

echo "=== sizes ==="
wc -c .audit/zizmor.sarif .audit/zizmor.err .audit/actionlint.json .audit/actionlint.err 2>/dev/null
