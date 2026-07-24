"""Tests for severity classification and fingerprinting logic in classify.py.

Runs classify.py as a subprocess with controlled input fixtures so we exercise
the real code rather than an inline copy of it.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

CLASSIFY_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classify.py')


def _finding(level, confidence=None, rule_id='zizmor/test-rule',
             filename='test.yml', snippet='run: echo test', line=10):
    return {
        'rule_id': rule_id,
        'level': level,
        'confidence': confidence if confidence is not None else '',
        'message': 'test finding',
        'file': filename,
        'line': line,
        'snippet': snippet,
    }


class TestClassifySeverity(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp(prefix='aeon-test-classify-')
        os.makedirs(os.path.join(self.work, '.audit'))

    def tearDown(self):
        shutil.rmtree(self.work, ignore_errors=True)

    def _run(self, findings):
        parsed = os.path.join(self.work, '.audit', 'parsed.json')
        with open(parsed, 'w') as f:
            json.dump(findings, f)
        import subprocess
        r = subprocess.run(
            [sys.executable, CLASSIFY_PY],
            cwd=self.work, capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, msg=r.stderr)
        classified = os.path.join(self.work, '.audit', 'classified.json')
        with open(classified) as f:
            return json.load(f)

    # --- severity mapping ---

    def test_error_high_confidence_is_critical(self):
        out = self._run([_finding('error', 'high')])
        self.assertEqual(out[0]['severity'], 'Critical')

    def test_error_medium_confidence_is_high(self):
        out = self._run([_finding('error', 'medium')])
        self.assertEqual(out[0]['severity'], 'High')

    def test_error_empty_confidence_is_high(self):
        # '' != 'high', so falls through to the bare 'error' branch
        out = self._run([_finding('error', '')])
        self.assertEqual(out[0]['severity'], 'High')

    def test_error_missing_confidence_key_is_high(self):
        # .get('confidence', '') returns '' when key absent — must not raise
        f = _finding('error')
        del f['confidence']
        out = self._run([f])
        self.assertEqual(out[0]['severity'], 'High')

    def test_warning_high_confidence_is_high(self):
        out = self._run([_finding('warning', 'high')])
        self.assertEqual(out[0]['severity'], 'High')

    def test_warning_low_confidence_is_medium(self):
        out = self._run([_finding('warning', 'low')])
        self.assertEqual(out[0]['severity'], 'Medium')

    def test_warning_missing_confidence_is_medium(self):
        f = _finding('warning')
        del f['confidence']
        out = self._run([f])
        self.assertEqual(out[0]['severity'], 'Medium')

    def test_note_level_is_low(self):
        # SARIF default level when a scanner doesn't emit error/warning
        out = self._run([_finding('note', 'high')])
        self.assertEqual(out[0]['severity'], 'Low')

    def test_unknown_level_is_low(self):
        out = self._run([_finding('none', 'high')])
        self.assertEqual(out[0]['severity'], 'Low')

    def test_confidence_uppercase_normalized(self):
        # our_severity calls .lower() so 'HIGH' must produce Critical, not High
        out = self._run([_finding('error', 'HIGH')])
        self.assertEqual(out[0]['severity'], 'Critical')

    # --- fingerprint properties ---

    def test_fingerprint_is_16_hex_chars(self):
        out = self._run([_finding('error', 'high')])
        fp = out[0]['fingerprint']
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_fingerprint_differs_by_rule(self):
        f1 = _finding('error', 'high', rule_id='zizmor/rule-a')
        f2 = _finding('error', 'high', rule_id='zizmor/rule-b')
        out = self._run([f1, f2])
        self.assertNotEqual(out[0]['fingerprint'], out[1]['fingerprint'])

    def test_fingerprint_whitespace_in_snippet_is_normalized(self):
        # re.sub(r'\s+', ' ', snippet) collapses multiple spaces to one
        f1 = _finding('error', 'high', snippet='run:  echo  foo')
        f2 = _finding('error', 'high', snippet='run: echo foo')
        out = self._run([f1, f2])
        self.assertEqual(out[0]['fingerprint'], out[1]['fingerprint'])

    def test_fingerprint_uses_basename_of_file(self):
        # classify.py hashes os.path.basename(file), so paths with different
        # directories but the same basename must produce the same fingerprint
        f1 = _finding('error', 'high', filename='.github/workflows/test.yml')
        f2 = _finding('error', 'high', filename='test.yml')
        out = self._run([f1, f2])
        self.assertEqual(out[0]['fingerprint'], out[1]['fingerprint'])

    # --- batch / empty cases ---

    def test_empty_input_produces_empty_output(self):
        out = self._run([])
        self.assertEqual(out, [])

    def test_multiple_findings_all_get_severity(self):
        findings = [
            _finding('error', 'high'),
            _finding('warning', 'low'),
            _finding('note', ''),
        ]
        out = self._run(findings)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[0]['severity'], 'Critical')
        self.assertEqual(out[1]['severity'], 'Medium')
        self.assertEqual(out[2]['severity'], 'Low')

    def test_short_rule_strips_prefix(self):
        # classify.py sets short_rule = rule_id.split('/')[-1]
        out = self._run([_finding('error', 'high', rule_id='zizmor/template-injection')])
        self.assertEqual(out[0]['short_rule'], 'template-injection')

    def test_short_rule_no_slash_is_rule_id_itself(self):
        out = self._run([_finding('error', 'high', rule_id='template-injection')])
        self.assertEqual(out[0]['short_rule'], 'template-injection')


if __name__ == '__main__':
    unittest.main()
