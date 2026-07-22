"""
Unit tests for the severity-mapping and fingerprint helpers used by classify.py,
finalize.py, and gen_trailer.py — the analysis pipeline for the workflow-security-audit
skill that calls .audit-bin/zizmor and .audit-bin/actionlint.

Run: python -m unittest .audit.test_severity  (from repo root)
  or: python .audit/test_severity.py
"""
import hashlib
import os
import unittest


# ── replicated from classify.py (module-level code in original makes it
#    non-importable without triggering the json.load call) ────────────────
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


# ── replicated from gen_trailer.py ──────────────────────────────────────
def _base(p):
    return os.path.basename(p)


def fingerprint(rule, fname, step):
    """sha256(rule|basename(file)|step_underscored)[:16]"""
    s = f"{rule}|{_base(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── calibration override replicated from finalize.py / delta.py ─────────
def apply_calibration(finding):
    """Return severity after policy-driven calibration overrides."""
    sev = finding['severity']
    rule = finding.get('short_rule', '')
    # unpinned-uses: zizmor --persona auditor uplifts to error+high (Critical),
    # but the prior audit graded it High (policy-driven, not exploit-driven).
    if rule == 'unpinned-uses' and sev == 'Critical':
        return 'High'
    # secrets-outside-env High -> Medium (GitHub Environments hardening noise)
    if rule == 'secrets-outside-env' and sev == 'High':
        return 'Medium'
    return sev


class TestOurSeverity(unittest.TestCase):

    def _f(self, level, confidence=None):
        d = {'level': level}
        if confidence is not None:
            d['confidence'] = confidence
        return d

    # ── main paths ──────────────────────────────────────────────────────

    def test_error_high_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_medium_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_error_low_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'low')), 'High')

    def test_warning_high_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_medium_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_note_any_confidence_is_low(self):
        # note-level never escalates above Low, even with high confidence
        self.assertEqual(our_severity(self._f('note', 'high')), 'Low')
        self.assertEqual(our_severity(self._f('note', 'medium')), 'Low')
        self.assertEqual(our_severity(self._f('note')), 'Low')

    # ── edge cases ──────────────────────────────────────────────────────

    def test_missing_confidence_key_error_is_high_not_critical(self):
        # When zizmor omits confidence, error-level must not become Critical
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    def test_confidence_case_normalized(self):
        # zizmor emits lowercase but guard against mixed-case values
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')
        self.assertEqual(our_severity(self._f('error', 'High')), 'Critical')
        self.assertEqual(our_severity(self._f('warning', 'HIGH')), 'High')

    def test_empty_confidence_string_error_is_high(self):
        self.assertEqual(our_severity(self._f('error', '')), 'High')

    def test_empty_confidence_string_warning_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', '')), 'Medium')

    def test_unknown_level_falls_through_to_low(self):
        # Any level not explicitly handled (e.g. future 'info') → Low
        self.assertEqual(our_severity(self._f('info', 'high')), 'Low')
        self.assertEqual(our_severity(self._f('debug')), 'Low')


class TestFingerprint(unittest.TestCase):

    def test_output_is_16_hex_chars(self):
        fp = fingerprint('template-injection', 'aeon.yml', 'Run script')
        self.assertEqual(len(fp), 16)
        self.assertRegex(fp, r'^[0-9a-f]{16}$')

    def test_full_path_uses_basename(self):
        fp_abs = fingerprint('rule', '.github/workflows/aeon.yml', 'step')
        fp_base = fingerprint('rule', 'aeon.yml', 'step')
        self.assertEqual(fp_abs, fp_base)

    def test_step_spaces_become_underscores(self):
        fp_space = fingerprint('rule', 'aeon.yml', 'Setup Node')
        fp_under = fingerprint('rule', 'aeon.yml', 'Setup_Node')
        self.assertEqual(fp_space, fp_under)

    def test_different_rules_produce_different_fingerprints(self):
        fp1 = fingerprint('template-injection', 'aeon.yml', 'Run')
        fp2 = fingerprint('unpinned-uses', 'aeon.yml', 'Run')
        self.assertNotEqual(fp1, fp2)

    def test_deterministic(self):
        fp1 = fingerprint('rule', 'file.yml', 'step')
        fp2 = fingerprint('rule', 'file.yml', 'step')
        self.assertEqual(fp1, fp2)


class TestCalibration(unittest.TestCase):

    def _finding(self, rule, severity):
        return {'short_rule': rule, 'severity': severity}

    def test_unpinned_uses_critical_becomes_high(self):
        # zizmor --persona auditor uplifts unpinned-uses to error+high → Critical,
        # but policy maps it back to High to match prior audit grading.
        f = self._finding('unpinned-uses', 'Critical')
        self.assertEqual(apply_calibration(f), 'High')

    def test_unpinned_uses_high_unchanged(self):
        f = self._finding('unpinned-uses', 'High')
        self.assertEqual(apply_calibration(f), 'High')

    def test_secrets_outside_env_high_becomes_medium(self):
        f = self._finding('secrets-outside-env', 'High')
        self.assertEqual(apply_calibration(f), 'Medium')

    def test_secrets_outside_env_medium_unchanged(self):
        f = self._finding('secrets-outside-env', 'Medium')
        self.assertEqual(apply_calibration(f), 'Medium')

    def test_template_injection_critical_unchanged(self):
        # template-injection Critical has no override — stays Critical
        f = self._finding('template-injection', 'Critical')
        self.assertEqual(apply_calibration(f), 'Critical')

    def test_unknown_rule_passes_through(self):
        f = self._finding('new-rule', 'High')
        self.assertEqual(apply_calibration(f), 'High')


if __name__ == '__main__':
    unittest.main()
