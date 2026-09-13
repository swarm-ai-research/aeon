#!/bin/bash
set -u
mkdir -p /home/runner/work/aeon/aeon/.audit
cd /home/runner/work/aeon/aeon
export PATH="/home/runner/work/aeon/aeon/.audit-bin:$PATH"
zizmor --version > .audit/zizmor.version 2>&1 || echo "zizmor version unavailable" > .audit/zizmor.version
actionlint -version > .audit/actionlint.version 2>&1 || echo "actionlint version unavailable" > .audit/actionlint.version
zizmor --format sarif --persona auditor .github/workflows > .audit/zizmor.sarif 2> .audit/zizmor.err
echo "zizmor_exit=$?" >> .audit/zizmor.err
actionlint -format '{{json .}}' > .audit/actionlint.json 2> .audit/actionlint.err
echo "actionlint_exit=$?" >> .audit/actionlint.err
wc -c .audit/zizmor.sarif .audit/actionlint.json
