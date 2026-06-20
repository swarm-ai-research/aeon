#!/usr/bin/env bash
set -e
./.audit-tools/bin/zizmor --format sarif --persona auditor .github/workflows --output .audit/zizmor.sarif
