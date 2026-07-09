"""Tests for pure logic functions in classify.py, delta.py, and parse_sarif.py.

Run with: python .audit/test_audit_logic.py
"""

import hashlib
import os
import unittest

# --- Functions under test (inlined from classify.py and delta.py) ---

def our_severity(f):
    """Severity mapping from classify.py."""
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


def fp_for(rule, fname, step):
    """Fingerprint builder from delta.py."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def resolve_zizmor_severity(props):
    """Severity chain from parse_sarif.py."""
    return props.get('problem.severity') or props.get('zizmor/severity') or props.get('security-severity', '')


def is_high_candidate_al(f):
    """HIGH-CANDIDATE detection from summarize_al.py."""
    msg = f.get('message', '')
    return ('SC2086' in msg or 'SC2046' in msg) and 'github.' in msg.lower()


def apply_calibration(findings):
    """Calibration override from delta.py: unpinned-uses Critical → High."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


# --- Tests ---

class TestOurSeverity(unittest.TestCase):
    def test_error_high_conf_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_high_conf_case_insensitive(self):
        # Confidence is lowercased before comparison
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_error_medium_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_empty_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_conf_key_is_high(self):
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_warning_high_conf_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_conf_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_level_with_high_conf_is_low(self):
        # 'note' hits the final else branch regardless of confidence
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'informational'}), 'Low')

    def test_none_string_level_is_low(self):
        self.assertEqual(our_severity({'level': 'none'}), 'Low')


class TestFpFor(unittest.TestCase):
    def test_output_is_16_hex_chars(self):
        fp = fp_for('some-rule', 'file.yml', 'step name')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_basename_stripped_from_path(self):
        # Full path and bare filename should produce the same fingerprint
        fp_full = fp_for('rule', '.github/workflows/ci.yml', 'step')
        fp_base = fp_for('rule', 'ci.yml', 'step')
        self.assertEqual(fp_full, fp_base)

    def test_different_rules_differ(self):
        self.assertNotEqual(fp_for('rule-a', 'f.yml', 's'), fp_for('rule-b', 'f.yml', 's'))

    def test_different_files_differ(self):
        self.assertNotEqual(fp_for('rule', 'a.yml', 's'), fp_for('rule', 'b.yml', 's'))

    def test_underscore_vs_space_step_differ(self):
        # delta.py normalises prior 'Setup_Node' → 'Setup Node'; both fps are
        # inserted into prior_fp_set precisely because they differ
        self.assertNotEqual(
            fp_for('rule', 'f.yml', 'Setup_Node'),
            fp_for('rule', 'f.yml', 'Setup Node'),
        )

    def test_deterministic(self):
        self.assertEqual(fp_for('r', 'f.yml', 's'), fp_for('r', 'f.yml', 's'))

    def test_empty_inputs_do_not_crash(self):
        fp = fp_for('', '', '')
        self.assertEqual(len(fp), 16)


class TestResolveZizmirSeverity(unittest.TestCase):
    def test_problem_severity_wins(self):
        props = {'problem.severity': 'high', 'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(resolve_zizmor_severity(props), 'high')

    def test_falls_back_to_zizmor_severity(self):
        props = {'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(resolve_zizmor_severity(props), 'medium')

    def test_falls_back_to_security_severity(self):
        self.assertEqual(resolve_zizmor_severity({'security-severity': 'low'}), 'low')

    def test_empty_props_returns_empty_string(self):
        self.assertEqual(resolve_zizmor_severity({}), '')

    def test_empty_string_problem_severity_falls_through(self):
        # '' is falsy — the `or` chain should skip it and use the next key
        props = {'problem.severity': '', 'zizmor/severity': 'medium'}
        self.assertEqual(resolve_zizmor_severity(props), 'medium')

    def test_none_problem_severity_falls_through(self):
        props = {'problem.severity': None, 'zizmor/severity': 'high'}
        self.assertEqual(resolve_zizmor_severity(props), 'high')


class TestHighCandidateAL(unittest.TestCase):
    def test_sc2086_with_github_is_candidate(self):
        self.assertTrue(is_high_candidate_al({'message': 'ShellCheck (SC2086): github.com token expansion'}))

    def test_sc2046_with_github_is_candidate(self):
        self.assertTrue(is_high_candidate_al({'message': 'ShellCheck (SC2046): github.event.inputs ref'}))

    def test_sc2086_without_github_not_candidate(self):
        self.assertFalse(is_high_candidate_al({'message': 'ShellCheck (SC2086): unquoted variable'}))

    def test_other_shellcheck_code_with_github_not_candidate(self):
        self.assertFalse(is_high_candidate_al({'message': 'ShellCheck (SC2153): github.context value'}))

    def test_github_uppercase_matched_case_insensitively(self):
        self.assertTrue(is_high_candidate_al({'message': 'SC2086 GITHUB.TOKEN may be unquoted'}))

    def test_missing_message_key_does_not_crash(self):
        self.assertFalse(is_high_candidate_al({}))

    def test_empty_message_not_candidate(self):
        self.assertFalse(is_high_candidate_al({'message': ''}))


class TestCalibrationOverride(unittest.TestCase):
    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        result = apply_calibration(findings)[0]
        self.assertEqual(result['severity'], 'High')
        self.assertTrue(result.get('calibrated'))

    def test_unpinned_uses_already_high_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        result = apply_calibration(findings)[0]
        self.assertEqual(result['severity'], 'High')
        self.assertNotIn('calibrated', result)

    def test_other_rule_critical_not_downgraded(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        result = apply_calibration(findings)[0]
        self.assertEqual(result['severity'], 'Critical')
        self.assertNotIn('calibrated', result)

    def test_unpinned_uses_low_not_touched(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Low'}]
        result = apply_calibration(findings)[0]
        self.assertEqual(result['severity'], 'Low')
        self.assertNotIn('calibrated', result)

    def test_multiple_findings_only_matching_ones_changed(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'unpinned-uses', 'severity': 'High'},
            {'short_rule': 'other-rule', 'severity': 'Critical'},
        ]
        result = apply_calibration(findings)
        self.assertEqual(result[0]['severity'], 'High')
        self.assertTrue(result[0].get('calibrated'))
        self.assertEqual(result[1]['severity'], 'High')
        self.assertNotIn('calibrated', result[1])
        self.assertEqual(result[2]['severity'], 'Critical')
        self.assertNotIn('calibrated', result[2])


if __name__ == '__main__':
    unittest.main()
