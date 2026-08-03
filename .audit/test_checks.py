#!/usr/bin/env python3
"""
Tests for pure logic in handrolled_checks.py, build_findings.py, and classify.py.

These scripts are not importable (they execute immediately and read files from CWD),
so the pure functions and regex patterns are re-defined here verbatim to test edge
cases without requiring the full audit file infrastructure.

Run: python3 .audit/test_checks.py
"""
import re
import unittest

# ── Patterns from handrolled_checks.py (verbatim) ──────────────────────────

TOJSON_RE = re.compile(r"echo\s+['\"]?\$\{\{\s*toJson\s*\(\s*github\.")
ENV_INJ_RE = re.compile(
    r'echo\s+["\']?[A-Za-z_]+=\$\{\{\s*(github\.event|inputs)\.[^}]+\}\}'
    r'["\']?\s*>>\s*"?\$?\{?GITHUB_(ENV|OUTPUT)'
)
USES_RE = re.compile(r'uses:\s*([\w-]+)/([\w./-]+)@([\w./-]+)')


def _is_mutable_ref(owner, ref):
    """Extracted from handrolled_checks.py lines 34-35."""
    trusted = owner in ('actions', 'github', 'docker', 'aws-actions')
    is_sha = re.fullmatch(r'[0-9a-f]{40}', ref)
    return not trusted and not is_sha


# ── Severity functions from build_findings.py (verbatim) ───────────────────

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


# ── Severity function from classify.py (verbatim) ──────────────────────────

def our_severity(f):
    level = f['level']
    conf = f.get('confidence', '').lower()
    if level == 'error' and conf == 'high':
        return 'Critical'
    if level == 'error':
        return 'High'
    if level == 'warning' and conf == 'high':
        return 'High'
    if level == 'warning':
        return 'Medium'
    return 'Low'


# ── Tests ───────────────────────────────────────────────────────────────────

class TestToJsonRe(unittest.TestCase):
    """TOJSON_RE — toJson-into-shell injection pattern."""

    def test_single_quoted_matches(self):
        line = "echo '${{ toJson(github.event.client_payload.message) }}' | jq -r '.'"
        self.assertIsNotNone(TOJSON_RE.search(line))

    def test_double_quoted_matches(self):
        line = 'echo "${{ toJson(github.event.client_payload) }}" | jq -r "."'
        self.assertIsNotNone(TOJSON_RE.search(line))

    def test_unquoted_matches(self):
        line = 'echo ${{ toJson(github.event) }} | jq'
        self.assertIsNotNone(TOJSON_RE.search(line))

    def test_inputs_tojson_not_matched(self):
        # Only github.* is tracked; inputs.* does not trigger this rule.
        line = "echo '${{ toJson(inputs.data) }}' | jq"
        self.assertIsNone(TOJSON_RE.search(line))

    def test_unrelated_echo_not_matched(self):
        self.assertIsNone(TOJSON_RE.search('echo "hello world"'))

    def test_tojson_without_echo_not_matched(self):
        # Expression in a `with:` block — not a shell injection via echo.
        self.assertIsNone(TOJSON_RE.search('run: ${{ toJson(github.event) }}'))


class TestEnvInjRe(unittest.TestCase):
    """ENV_INJ_RE — user-controlled data written to GITHUB_ENV / GITHUB_OUTPUT."""

    def test_github_event_to_env(self):
        line = 'echo "MSG=${{ github.event.client_payload.message }}" >> "$GITHUB_ENV"'
        self.assertIsNotNone(ENV_INJ_RE.search(line))

    def test_inputs_to_output(self):
        line = "echo 'RESULT=${{ inputs.value }}' >> $GITHUB_OUTPUT"
        self.assertIsNotNone(ENV_INJ_RE.search(line))

    def test_inputs_to_env_no_quotes(self):
        line = 'echo KEY=${{ inputs.token }} >> $GITHUB_ENV'
        self.assertIsNotNone(ENV_INJ_RE.search(line))

    def test_hardcoded_value_not_matched(self):
        line = 'echo "MSG=hello" >> "$GITHUB_ENV"'
        self.assertIsNone(ENV_INJ_RE.search(line))

    def test_github_sha_not_matched(self):
        # github.sha is not github.event.* — excluded by the regex.
        line = 'echo "SHA=${{ github.sha }}" >> "$GITHUB_ENV"'
        self.assertIsNone(ENV_INJ_RE.search(line))

    def test_github_actor_not_matched(self):
        # github.actor is not github.event.* — excluded.
        line = 'echo "ACTOR=${{ github.actor }}" >> "$GITHUB_OUTPUT"'
        self.assertIsNone(ENV_INJ_RE.search(line))


class TestUsesRe(unittest.TestCase):
    """USES_RE + mutable-ref classification."""

    def test_trusted_owner_actions_ok(self):
        m = USES_RE.search('uses: actions/checkout@v4')
        self.assertIsNotNone(m)
        self.assertFalse(_is_mutable_ref(m.group(1), m.group(3)))

    def test_trusted_owner_github_ok(self):
        m = USES_RE.search('uses: github/codeql-action/analyze@v3')
        self.assertIsNotNone(m)
        self.assertFalse(_is_mutable_ref(m.group(1), m.group(3)))

    def test_trusted_owner_docker_ok(self):
        m = USES_RE.search('uses: docker/build-push-action@v5')
        self.assertIsNotNone(m)
        self.assertFalse(_is_mutable_ref(m.group(1), m.group(3)))

    def test_sha_pinned_third_party_ok(self):
        sha = 'a' * 40
        m = USES_RE.search(f'uses: some-org/some-action@{sha}')
        self.assertIsNotNone(m)
        self.assertFalse(_is_mutable_ref(m.group(1), m.group(3)))

    def test_version_tag_mutable(self):
        m = USES_RE.search('uses: some-org/some-action@v1')
        self.assertIsNotNone(m)
        self.assertTrue(_is_mutable_ref(m.group(1), m.group(3)))

    def test_branch_ref_mutable(self):
        m = USES_RE.search('uses: some-org/some-action@main')
        self.assertIsNotNone(m)
        self.assertTrue(_is_mutable_ref(m.group(1), m.group(3)))

    def test_39_char_hex_is_mutable(self):
        # 39-char hex is NOT a valid SHA-40 — must not be treated as pinned.
        sha = 'a' * 39
        m = USES_RE.search(f'uses: some-org/some-action@{sha}')
        self.assertIsNotNone(m)
        self.assertTrue(_is_mutable_ref(m.group(1), m.group(3)))

    def test_41_char_hex_is_mutable(self):
        # 41 chars also fails fullmatch on [0-9a-f]{40}.
        sha = 'a' * 41
        m = USES_RE.search(f'uses: some-org/some-action@{sha}')
        self.assertIsNotNone(m)
        self.assertTrue(_is_mutable_ref(m.group(1), m.group(3)))


class TestMapSeverityZizmor(unittest.TestCase):
    """map_severity_zizmor from build_findings.py."""

    def test_error_high_conf_critical(self):
        self.assertEqual(map_severity_zizmor('error', 'high', ''), 'Critical')

    def test_error_critical_conf_critical(self):
        # 'critical' is treated the same as 'high' by conf_high check.
        self.assertEqual(map_severity_zizmor('error', 'critical', ''), 'Critical')

    def test_error_low_conf_high(self):
        self.assertEqual(map_severity_zizmor('error', 'low', ''), 'High')

    def test_error_medium_conf_high(self):
        self.assertEqual(map_severity_zizmor('error', 'medium', ''), 'High')

    def test_error_none_conf_high(self):
        self.assertEqual(map_severity_zizmor('error', None, ''), 'High')

    def test_warning_high_conf_high(self):
        self.assertEqual(map_severity_zizmor('warning', 'high', ''), 'High')

    def test_warning_medium_conf_medium(self):
        self.assertEqual(map_severity_zizmor('warning', 'medium', ''), 'Medium')

    def test_note_low(self):
        self.assertEqual(map_severity_zizmor('note', '', ''), 'Low')

    def test_unknown_level_low(self):
        self.assertEqual(map_severity_zizmor('info', '', ''), 'Low')


class TestOurSeverity(unittest.TestCase):
    """our_severity from classify.py — note the narrower 'high'-only Critical gate."""

    def test_error_high_conf_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_critical_conf_not_critical(self):
        # classify.py only checks conf == 'high', unlike build_findings.py which
        # also accepts 'critical'. So 'critical' confidence → High here.
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'critical'}), 'High')

    def test_error_low_conf_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_missing_conf_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_conf_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_conf_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_note_low(self):
        self.assertEqual(our_severity({'level': 'note', 'confidence': ''}), 'Low')


if __name__ == '__main__':
    unittest.main(verbosity=2)
