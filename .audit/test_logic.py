"""Unit tests for .audit/ script logic — pure-function coverage.

The scripts in this directory are not importable (module-level side effects
read real files), so we duplicate the pure functions here and test them in
isolation. Tests cover all branches and critical edge cases.
"""

import hashlib
import os
import unittest


# ── Duplicated from classify.py / extract_steps.py (identical function) ──────

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


# ── Duplicated from gen_trailer.py ────────────────────────────────────────────

def _base(p):
    return os.path.basename(p)

def fp_trailer(rule, fname, step):
    """Fingerprint used in gen_trailer: spaces → underscores before hashing."""
    s = f"{rule}|{_base(fname)}|{step.replace(' ', '_')}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def trailer_status(severity):
    return 'manual' if severity in ('Critical', 'High') else 'open'


# ── Duplicated from delta.py ──────────────────────────────────────────────────

def fp_for(rule, fname, step):
    """Fingerprint used in delta: spaces are NOT replaced."""
    b = os.path.basename(fname)
    s = f"{rule}|{b}|{step}"
    return hashlib.sha256(s.encode()).hexdigest()[:16]


# ── Duplicated from delta2.py ─────────────────────────────────────────────────

def short_rule(s):
    return s.split('/')[-1]


# ══════════════════════════════════════════════════════════════════════════════

class TestOurSeverity(unittest.TestCase):
    """All branches of the severity mapping function."""

    # --- error level ---

    def test_error_high_confidence_is_critical(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'high'}), 'Critical')

    def test_error_medium_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'medium'}), 'High')

    def test_error_low_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'low'}), 'High')

    def test_error_empty_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'error', 'confidence': ''}), 'High')

    def test_error_missing_confidence_key_is_high(self):
        # No 'confidence' key at all — .get() must default to '' not raise
        self.assertEqual(our_severity({'level': 'error'}), 'High')

    # --- warning level ---

    def test_warning_high_confidence_is_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'high'}), 'High')

    def test_warning_medium_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'medium'}), 'Medium')

    def test_warning_low_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'low'}), 'Medium')

    def test_warning_empty_confidence_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': ''}), 'Medium')

    def test_warning_missing_confidence_key_is_medium(self):
        self.assertEqual(our_severity({'level': 'warning'}), 'Medium')

    # --- note / other levels → Low ---

    def test_note_high_confidence_is_low(self):
        # note-level findings are always Low regardless of confidence
        self.assertEqual(our_severity({'level': 'note', 'confidence': 'high'}), 'Low')

    def test_note_no_confidence_is_low(self):
        self.assertEqual(our_severity({'level': 'note'}), 'Low')

    def test_unknown_level_is_low(self):
        self.assertEqual(our_severity({'level': 'none', 'confidence': 'high'}), 'Low')

    def test_empty_level_is_low(self):
        self.assertEqual(our_severity({'level': '', 'confidence': 'high'}), 'Low')

    # --- confidence case-insensitivity ---

    def test_confidence_uppercase_HIGH_treated_as_high(self):
        # .lower() normalises — 'HIGH' should produce Critical for error level
        self.assertEqual(our_severity({'level': 'error', 'confidence': 'HIGH'}), 'Critical')

    def test_confidence_titlecase_High_treated_as_high(self):
        self.assertEqual(our_severity({'level': 'warning', 'confidence': 'High'}), 'High')


class TestFpTrailer(unittest.TestCase):
    """gen_trailer.fp(): spaces become underscores before hashing."""

    def test_returns_16_hex_chars(self):
        result = fp_trailer('rule', 'ci.yml', 'Build')
        self.assertEqual(len(result), 16)
        self.assertRegex(result, r'^[0-9a-f]{16}$')

    def test_space_and_underscore_produce_same_fingerprint(self):
        # "Set up Node" and "Set_up_Node" must hash identically
        self.assertEqual(
            fp_trailer('rule', 'ci.yml', 'Set up Node'),
            fp_trailer('rule', 'ci.yml', 'Set_up_Node'),
        )

    def test_multiple_internal_spaces_normalised(self):
        self.assertEqual(
            fp_trailer('rule', 'ci.yml', 'Install and build packages'),
            fp_trailer('rule', 'ci.yml', 'Install_and_build_packages'),
        )

    def test_uses_basename_not_full_path(self):
        self.assertEqual(
            fp_trailer('rule', '.github/workflows/ci.yml', 'Build'),
            fp_trailer('rule', 'ci.yml', 'Build'),
        )

    def test_different_rules_differ(self):
        self.assertNotEqual(
            fp_trailer('unpinned-uses', 'ci.yml', 'Build'),
            fp_trailer('template-injection', 'ci.yml', 'Build'),
        )

    def test_different_files_differ(self):
        self.assertNotEqual(
            fp_trailer('rule', 'ci.yml', 'Build'),
            fp_trailer('rule', 'cd.yml', 'Build'),
        )

    def test_empty_step_is_stable(self):
        result = fp_trailer('rule', 'ci.yml', '')
        self.assertEqual(len(result), 16)

    def test_deterministic(self):
        self.assertEqual(
            fp_trailer('rule', 'ci.yml', 'Build'),
            fp_trailer('rule', 'ci.yml', 'Build'),
        )


class TestFpFor(unittest.TestCase):
    """delta.fp_for(): spaces are NOT replaced — different from gen_trailer.fp."""

    def test_returns_16_hex_chars(self):
        result = fp_for('rule', 'ci.yml', 'Build')
        self.assertEqual(len(result), 16)
        self.assertRegex(result, r'^[0-9a-f]{16}$')

    def test_spaces_not_replaced(self):
        # This is the key difference from gen_trailer.fp
        self.assertNotEqual(
            fp_for('rule', 'ci.yml', 'Set up Node'),
            fp_for('rule', 'ci.yml', 'Set_up_Node'),
        )

    def test_uses_basename(self):
        self.assertEqual(
            fp_for('rule', '.github/workflows/ci.yml', 'Build'),
            fp_for('rule', 'ci.yml', 'Build'),
        )

    def test_deterministic(self):
        self.assertEqual(fp_for('r', 'f.yml', 's'), fp_for('r', 'f.yml', 's'))

    def test_different_from_fp_trailer_for_spaced_step(self):
        # fp_for and fp_trailer diverge when step contains a space
        self.assertNotEqual(
            fp_for('rule', 'ci.yml', 'Set up Node'),
            fp_trailer('rule', 'ci.yml', 'Set up Node'),
        )


class TestTrailerStatus(unittest.TestCase):
    """gen_trailer status field: Critical/High → 'manual', else → 'open'."""

    def test_critical_is_manual(self):
        self.assertEqual(trailer_status('Critical'), 'manual')

    def test_high_is_manual(self):
        self.assertEqual(trailer_status('High'), 'manual')

    def test_medium_is_open(self):
        self.assertEqual(trailer_status('Medium'), 'open')

    def test_low_is_open(self):
        self.assertEqual(trailer_status('Low'), 'open')

    def test_unexpected_value_defaults_to_open(self):
        self.assertEqual(trailer_status('Info'), 'open')
        self.assertEqual(trailer_status(''), 'open')


class TestShortRule(unittest.TestCase):
    """delta2.short_rule(): splits on '/' and returns the last segment."""

    def test_namespaced_rule_id(self):
        self.assertEqual(short_rule('zizmor/unpinned-uses'), 'unpinned-uses')

    def test_plain_rule_id_unchanged(self):
        self.assertEqual(short_rule('unpinned-uses'), 'unpinned-uses')

    def test_multi_segment_path(self):
        self.assertEqual(short_rule('org/tool/template-injection'), 'template-injection')

    def test_empty_string(self):
        self.assertEqual(short_rule(''), '')


if __name__ == '__main__':
    unittest.main()
