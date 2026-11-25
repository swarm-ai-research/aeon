#!/bin/bash
set -u
mkdir -p /home/runner/work/aeon/aeon/.audit
cd /home/runner/work/aeon/aeon
export PATH="/home/runner/work/aeon/aeon/.audit-bin:$PATH"

capture_version() {
  local tool="$1" flag="$2"
  "$tool" "$flag" > ".audit/$tool.version" 2>&1 || echo "$tool version unavailable" > ".audit/$tool.version"
}

capture_version zizmor --version
capture_version actionlint -version
zizmor --format sarif --persona auditor .github/workflows > .audit/zizmor.sarif 2> .audit/zizmor.err
echo "zizmor_exit=$?" >> .audit/zizmor.err
actionlint -format '{{json .}}' > .audit/actionlint.json 2> .audit/actionlint.err
echo "actionlint_exit=$?" >> .audit/actionlint.err
wc -c .audit/zizmor.sarif .audit/actionlint.json
