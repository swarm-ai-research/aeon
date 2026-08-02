#!/usr/bin/env python3
"""Unit tests for hand-rolled regex patterns and severity-mapping logic.

Run: python3 .audit/test_handrolled_patterns.py

Tests the regexes in handrolled_checks.py and the severity mapping in
build_findings.py without invoking the scanner binaries or touching the
filesystem.
"""
import re
import sys

# ── replicate patterns from handrolled_checks.py ──────────────────────────────

TOJSON_RE = re.compile(r"echo\s+['\"]?\$\{\{\s*toJson\s*\(\s*github\.")
ENV_INJ_RE = re.compile(
    r'echo\s+["\']?[A-Za-z_]+=\$\{\{\s*(github\.event|inputs)\.[^}]+\}\}["\']?\s*>>\s*"?\$?\{?GITHUB_(ENV|OUTPUT)'
)
USES_RE = re.compile(r'uses:\s*([\w-]+)/([\w./-]+)@([\w./-]+)')

# ── replicate map_severity_zizmor from build_findings.py ──────────────────────

def map_severity_zizmor(level, conf, zsev):
    conf_high = (conf or '').lower() in ('high', 'critical')
    if level == 'error' and conf_high:
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and conf_high:
        return 'High'
    if level == 'warning':
        return 'Medium'
    if level == 'note':
        return 'Low'
    return 'Low'

# ── replicate mutable-ref check logic from handrolled_checks.py ───────────────

def is_mutable_ref(line):
    """Return True if the line uses a third-party action without SHA pinning."""
    m = USES_RE.search(line)
    if not m:
        return False
    owner, repo, ref = m.group(1), m.group(2), m.group(3)
    if owner == '.' or line.strip().startswith('uses: ./'):
        return False
    trusted = owner in ('actions', 'github', 'docker', 'aws-actions')
    is_sha = re.fullmatch(r'[0-9a-f]{40}', ref)
    return not trusted and not is_sha

# ── test harness ──────────────────────────────────────────────────────────────

passed = 0
failed = 0

def check(condition, label):
    global passed, failed
    if condition:
        passed += 1
        print(f'  ok  {label}')
    else:
        failed += 1
        print(f'  FAIL  {label}', file=sys.stderr)

# ── TOJSON_RE ─────────────────────────────────────────────────────────────────

print('TOJSON_RE:')

# should match
check(TOJSON_RE.search(r'echo ${{ toJson( github.event )}}'),
      'bare echo toJson github')
check(TOJSON_RE.search(r'echo "${{ toJson( github.context )}}"'),
      'double-quoted toJson github')
check(TOJSON_RE.search(r"echo '${{ toJson(github.event )}}'"),
      'single-quoted toJson github')
check(TOJSON_RE.search(r'  echo  ${{ toJson(  github.actor )}}'),
      'extra whitespace around toJson and github')

# should NOT match
check(not TOJSON_RE.search(r'echo ${{ toJson( inputs.foo )}}'),
      'inputs.foo is not a github. reference')
check(not TOJSON_RE.search(r'echo ${{ github.event }}'),
      'no toJson call')
check(not TOJSON_RE.search(r'echo hello world'),
      'plain echo')

# ── ENV_INJ_RE ────────────────────────────────────────────────────────────────

print('\nENV_INJ_RE:')

# should match — github.event
check(ENV_INJ_RE.search(r'echo "PAYLOAD=${{ github.event.action }}" >> "$GITHUB_ENV"'),
      'github.event.action to GITHUB_ENV')
check(ENV_INJ_RE.search(r'echo NAME=${{ github.event.issue.title }} >> $GITHUB_ENV'),
      'github.event.issue.title to GITHUB_ENV (bare)')
check(ENV_INJ_RE.search(r'echo KEY=${{ github.event.pull_request.body }} >> $GITHUB_OUTPUT'),
      'github.event.* to GITHUB_OUTPUT')

# should match — inputs.*
check(ENV_INJ_RE.search(r'echo VALUE=${{ inputs.my_param }} >> $GITHUB_ENV'),
      'inputs.my_param to GITHUB_ENV')
check(ENV_INJ_RE.search(r'echo VAL=${{ inputs.target }} >> $GITHUB_OUTPUT'),
      'inputs.target to GITHUB_OUTPUT')

# should NOT match
check(not ENV_INJ_RE.search(r'echo SHA=${{ github.sha }} >> $GITHUB_ENV'),
      'github.sha (not github.event) should not match')
check(not ENV_INJ_RE.search(r'echo KEY=${{ env.VALUE }} >> $GITHUB_ENV'),
      'env.VALUE is not github.event or inputs')
check(not ENV_INJ_RE.search(r'echo KEY=${{ github.event.action }}'),
      'missing >> GITHUB_ENV redirection')

# ── USES_RE + mutable-ref logic ───────────────────────────────────────────────

print('\nMutable third-party ref:')

# trusted owners — no finding
check(not is_mutable_ref('        uses: actions/checkout@v4'),
      'actions/checkout@v4 is trusted — no finding')
check(not is_mutable_ref('        uses: docker/build-push-action@v5'),
      'docker/* is trusted — no finding')
check(not is_mutable_ref('        uses: aws-actions/configure-aws-credentials@v4'),
      'aws-actions/* is trusted — no finding')
check(not is_mutable_ref('        uses: github/codeql-action/analyze@v3'),
      'github/* is trusted — no finding')

# SHA-pinned third-party — no finding
check(not is_mutable_ref(
      '        uses: random-org/my-action@a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2'),
      'SHA-pinned third-party — no finding')

# local action — no finding
check(not is_mutable_ref('        uses: ./local-action'),
      'local ./ action — no finding')

# mutable third-party — finding
check(is_mutable_ref('        uses: random-org/my-action@v1.0'),
      'third-party with mutable tag — finding')
check(is_mutable_ref('        uses: some-user/helper@main'),
      'third-party pinned to branch name — finding')
check(is_mutable_ref('        uses: acme-corp/deploy@1.2.3'),
      'third-party with semver tag — finding')

# short SHA (not 40 chars) is NOT accepted as a pin
check(is_mutable_ref('        uses: acme-corp/deploy@abcdef1'),
      'short SHA (7 chars) treated as mutable — finding')

# ── map_severity_zizmor ───────────────────────────────────────────────────────

print('\nmap_severity_zizmor:')

check(map_severity_zizmor('error', 'high', '') == 'Critical',
      'error + high confidence → Critical')
check(map_severity_zizmor('error', 'critical', '') == 'Critical',
      'error + critical confidence → Critical (treated as high)')
check(map_severity_zizmor('error', 'low', '') == 'High',
      'error + low confidence → High')
check(map_severity_zizmor('error', '', '') == 'High',
      'error + empty confidence → High')
check(map_severity_zizmor('error', None, '') == 'High',
      'error + None confidence → High')
check(map_severity_zizmor('warning', 'high', '') == 'High',
      'warning + high confidence → High')
check(map_severity_zizmor('warning', 'critical', '') == 'High',
      'warning + critical confidence → High')
check(map_severity_zizmor('warning', 'low', '') == 'Medium',
      'warning + low confidence → Medium')
check(map_severity_zizmor('warning', '', '') == 'Medium',
      'warning + empty confidence → Medium')
check(map_severity_zizmor('note', 'high', '') == 'Low',
      'note → Low regardless of confidence')
check(map_severity_zizmor('note', '', '') == 'Low',
      'note + empty → Low')
check(map_severity_zizmor('unknown', 'high', '') == 'Low',
      'unknown level falls through to Low')
check(map_severity_zizmor('', '', '') == 'Low',
      'empty level falls through to Low')

# ── results ───────────────────────────────────────────────────────────────────

print(f'\n{passed} passed, {failed} failed')
if failed:
    sys.exit(1)
