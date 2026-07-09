"""
Unit tests for the logic in classify.py, delta.py, and parse_sarif.py.
Run with: python -m pytest .audit/test_audit_scripts.py  (or python -m unittest)

These files are standalone scripts, so we replicate the pure functions here
rather than importing them (which would execute file I/O on load).
"""
import hashlib
import os
import unittest


# ── Logic from classify.py ────────────────────────────────────────────────────

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


class TestOurSeverity(unittest.TestCase):
    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_missing_confidence_is_high(self):
        # confidence key absent — must not raise, must return High not Critical
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_confidence_case_insensitive_HIGH_critical(self):
        # zizmor may emit 'HIGH' uppercase — .lower() normalises it
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    def test_note_with_high_confidence_is_low(self):
        # note-level should always be Low regardless of confidence
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'unknown_level'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': ''}), 'Low')


# ── Logic from delta.py ───────────────────────────────────────────────────────

def fp_for(rule, fname, step):
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class TestFpFor(unittest.TestCase):
    def test_deterministic(self):
        a = fp_for('unpinned-uses', '.github/workflows/foo.yml', 'Build')
        b = fp_for('unpinned-uses', '.github/workflows/foo.yml', 'Build')
        self.assertEqual(a, b)

    def test_length_16_hex(self):
        fp = fp_for('some-rule', 'file.yml', 'step')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_different_rules_differ(self):
        a = fp_for('rule-a', 'file.yml', 'step')
        b = fp_for('rule-b', 'file.yml', 'step')
        self.assertNotEqual(a, b)

    def test_different_files_differ(self):
        a = fp_for('rule', 'workflows/foo.yml', 'step')
        b = fp_for('rule', 'workflows/bar.yml', 'step')
        self.assertNotEqual(a, b)

    def test_basename_only_path_ignored(self):
        # classify.py strips dirname; delta.py must agree
        a = fp_for('rule', 'deep/nested/file.yml', 'step')
        b = fp_for('rule', 'file.yml', 'step')
        self.assertEqual(a, b)

    def test_underscore_vs_space_step_differ(self):
        # delta.py normalises underscores → spaces BEFORE calling fp_for.
        # Confirm the raw function treats them as distinct (normalisation is the caller's job).
        a = fp_for('rule', 'file.yml', 'Setup_Node')
        b = fp_for('rule', 'file.yml', 'Setup Node')
        self.assertNotEqual(a, b)

    def test_empty_step(self):
        fp = fp_for('rule', 'file.yml', '')
        self.assertEqual(len(fp), 16)


# ── Logic from delta.py: calibration override ─────────────────────────────────

def apply_calibration(findings):
    """Mirror of the calibration loop in delta.py."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


class TestCalibration(unittest.TestCase):
    def test_unpinned_uses_critical_downgraded_to_high(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_unpinned_uses_high_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertNotIn('calibrated', findings[0])

    def test_other_critical_not_downgraded(self):
        findings = [{'short_rule': 'injection', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')

    def test_empty_findings_no_error(self):
        self.assertEqual(apply_calibration([]), [])


# ── Logic from parse_sarif.py: severity fallback chain ───────────────────────

def extract_severity(props):
    """Mirror of the severity extraction in parse_sarif.py."""
    return (
        props.get('problem.severity')
        or props.get('zizmor/severity')
        or props.get('security-severity', '')
    )


class TestExtractSeverity(unittest.TestCase):
    def test_problem_severity_takes_precedence(self):
        props = {
            'problem.severity': 'high',
            'zizmor/severity': 'medium',
            'security-severity': 'low',
        }
        self.assertEqual(extract_severity(props), 'high')

    def test_falls_back_to_zizmor_severity(self):
        props = {'zizmor/severity': 'medium', 'security-severity': 'low'}
        self.assertEqual(extract_severity(props), 'medium')

    def test_falls_back_to_security_severity(self):
        props = {'security-severity': 'low'}
        self.assertEqual(extract_severity(props), 'low')

    def test_empty_props_returns_empty_string(self):
        self.assertEqual(extract_severity({}), '')

    def test_falsy_problem_severity_skips_to_next(self):
        # An empty string is falsy — the `or` chain should skip it
        props = {'problem.severity': '', 'zizmor/severity': 'medium'}
        self.assertEqual(extract_severity(props), 'medium')


# ── Logic from parse_sarif.py: location extraction ───────────────────────────

def extract_location(result):
    """Mirror of location extraction in parse_sarif.py."""
    locs = result.get('locations', [])
    if locs:
        phys = locs[0].get('physicalLocation', {})
        uri = phys.get('artifactLocation', {}).get('uri', '')
        region = phys.get('region', {})
        line = region.get('startLine', 0)
        snippet = region.get('snippet', {}).get('text', '')
    else:
        uri = ''
        line = 0
        snippet = ''
    return uri, line, snippet


class TestExtractLocation(unittest.TestCase):
    def test_no_locations_returns_defaults(self):
        uri, line, snippet = extract_location({'locations': []})
        self.assertEqual(uri, '')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    def test_missing_locations_key_returns_defaults(self):
        uri, line, snippet = extract_location({})
        self.assertEqual(uri, '')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    def test_first_location_used(self):
        result = {
            'locations': [
                {'physicalLocation': {'artifactLocation': {'uri': 'first.yml'}, 'region': {'startLine': 10, 'snippet': {'text': 'abc'}}}},
                {'physicalLocation': {'artifactLocation': {'uri': 'second.yml'}, 'region': {'startLine': 20}}},
            ]
        }
        uri, line, snippet = extract_location(result)
        self.assertEqual(uri, 'first.yml')
        self.assertEqual(line, 10)
        self.assertEqual(snippet, 'abc')

    def test_missing_region_fields_default(self):
        result = {
            'locations': [{'physicalLocation': {'artifactLocation': {'uri': 'foo.yml'}, 'region': {}}}]
        }
        uri, line, snippet = extract_location(result)
        self.assertEqual(uri, 'foo.yml')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')

    def test_missing_physical_location_defaults(self):
        result = {'locations': [{}]}
        uri, line, snippet = extract_location(result)
        self.assertEqual(uri, '')
        self.assertEqual(line, 0)
        self.assertEqual(snippet, '')


if __name__ == '__main__':
    unittest.main()
