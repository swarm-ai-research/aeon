#!/usr/bin/env bash
set -eu
export PATH=".audit-bin:$PATH"
zizmor --version > .audit/zizmor.version 2>&1 || echo "zizmor version fail: $?" >> .audit/zizmor.version
actionlint --version > .audit/actionlint.version 2>&1 || echo "actionlint version fail: $?" >> .audit/actionlint.version
zizmor --format sarif --persona auditor .github/workflows .github/actions \
  > .audit/zizmor.sarif 2> .audit/zizmor.err || true
actionlint -format '{{json .}}' > .audit/actionlint.json 2> .audit/actionlint.err || true
echo "done"
