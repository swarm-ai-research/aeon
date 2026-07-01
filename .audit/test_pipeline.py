"""
Unit tests for the pure functions in the .audit/ processing pipeline.

Run with:  python3 .audit/test_pipeline.py
"""

import hashlib
import os
import unittest

# ── Functions under test ─────────────────────────────────────────────────────
# Copied verbatim from classify.py / extract_steps.py (identical in both).

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


def fp_delta(rule, fname, step):
    """Fingerprint scheme used by delta.py — step kept as-is."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def fp_trailer(rule, fname, step):
    """Fingerprint scheme used by gen_trailer.py — spaces in step → underscores."""
    base = os.path.basename(fname)
    s = f"{rule}|{base}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def apply_calibration(findings):
    """Calibration from delta.py / delta2.py: unpinned-uses Critical → High."""
    for f in findings:
        if f['short_rule'] == 'unpinned-uses' and f['severity'] == 'Critical':
            f['severity'] = 'High'
            f['calibrated'] = True
    return findings


# ── Tests ────────────────────────────────────────────────────────────────────

class TestOurSeverity(unittest.TestCase):

    def _f(self, level, confidence=''):
        return {'level': level, 'confidence': confidence}

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity(self._f('error', 'high')), 'Critical')

    def test_error_high_confidence_case_insensitive(self):
        # confidence is lowercased before comparison
        self.assertEqual(our_severity(self._f('error', 'High')), 'Critical')
        self.assertEqual(our_severity(self._f('error', 'HIGH')), 'Critical')

    def test_error_no_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', '')), 'High')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('error', 'medium')), 'High')

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity(self._f('warning', 'high')), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', 'medium')), 'Medium')

    def test_warning_no_confidence_is_medium(self):
        self.assertEqual(our_severity(self._f('warning', '')), 'Medium')

    def test_note_level_falls_through_to_low(self):
        # 'note' is not explicitly handled — falls through the if-chain to Low.
        self.assertEqual(our_severity(self._f('note', '')), 'Low')
        self.assertEqual(our_severity(self._f('note', 'high')), 'Low')

    def test_unknown_level_falls_through_to_low(self):
        self.assertEqual(our_severity(self._f('info', '')), 'Low')
        self.assertEqual(our_severity(self._f('', '')), 'Low')


class TestCalibration(unittest.TestCase):
    """unpinned-uses Critical → High downgrade, as applied in delta.py / delta2.py."""

    def test_unpinned_uses_critical_is_downgraded(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertTrue(findings[0].get('calibrated'))

    def test_unpinned_uses_high_is_unchanged(self):
        findings = [{'short_rule': 'unpinned-uses', 'severity': 'High'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertFalse(findings[0].get('calibrated', False))

    def test_other_critical_rule_is_unchanged(self):
        findings = [{'short_rule': 'template-injection', 'severity': 'Critical'}]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'Critical')
        self.assertFalse(findings[0].get('calibrated', False))

    def test_calibration_does_not_mutate_other_findings(self):
        findings = [
            {'short_rule': 'unpinned-uses', 'severity': 'Critical'},
            {'short_rule': 'artipacked', 'severity': 'Critical'},
        ]
        apply_calibration(findings)
        self.assertEqual(findings[0]['severity'], 'High')
        self.assertEqual(findings[1]['severity'], 'Critical')


class TestFingerprintFunctions(unittest.TestCase):
    """
    delta.py and gen_trailer.py use subtly different fingerprint schemes:
    gen_trailer.py replaces spaces in step names with underscores (matching the
    stored format in prior report trailers), while delta.py keeps the raw step
    string but tries both variants when reading prior fingerprints.
    """

    FILE = '.github/workflows/example.yml'
    RULE = 'template-injection'

    def test_no_spaces_in_step_both_match(self):
        self.assertEqual(
            fp_delta(self.RULE, self.FILE, 'CheckoutRepo'),
            fp_trailer(self.RULE, self.FILE, 'CheckoutRepo'),
        )

    def test_spaces_in_step_fingerprints_diverge(self):
        # Documents the intentional difference: gen_trailer.py stores with '_',
        # delta.py reads it back with the space version and tries both.
        self.assertNotEqual(
            fp_delta(self.RULE, self.FILE, 'Checkout repo'),
            fp_trailer(self.RULE, self.FILE, 'Checkout repo'),
        )

    def test_trailer_underscore_matches_delta_underscore_pass(self):
        # delta.py's second attempt (step2 = step with underscores) must equal
        # what gen_trailer.py wrote — that's how prior → current matching works.
        step = 'Checkout repo'
        fp_stored = fp_trailer(self.RULE, self.FILE, step)
        fp_reread = fp_delta(self.RULE, self.FILE, step.replace(' ', '_'))
        self.assertEqual(fp_stored, fp_reread)

    def test_basename_not_full_path(self):
        self.assertEqual(
            fp_delta(self.RULE, '.github/workflows/example.yml', 'step'),
            fp_delta(self.RULE, 'example.yml', 'step'),
        )
        self.assertEqual(
            fp_trailer(self.RULE, '.github/workflows/example.yml', 'step'),
            fp_trailer(self.RULE, 'example.yml', 'step'),
        )

    def test_fingerprints_are_16_hex_chars(self):
        fp = fp_delta(self.RULE, self.FILE, 'some step')
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in '0123456789abcdef' for c in fp))

    def test_different_rules_produce_different_fps(self):
        self.assertNotEqual(
            fp_delta('rule-a', self.FILE, 'step'),
            fp_delta('rule-b', self.FILE, 'step'),
        )

    def test_different_files_produce_different_fps(self):
        self.assertNotEqual(
            fp_delta(self.RULE, 'a.yml', 'step'),
            fp_delta(self.RULE, 'b.yml', 'step'),
        )


if __name__ == '__main__':
    unittest.main()
