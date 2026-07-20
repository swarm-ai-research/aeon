"""
Tests for .audit/ pipeline scripts: classify.py and summarize_al.py.

Run from repo root:
  python -m pytest .audit/tests/test_audit_scripts.py -v
  # or without pytest:
  python .audit/tests/test_audit_scripts.py
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AUDIT_DIR = Path(__file__).resolve().parent.parent
CLASSIFY_PY = AUDIT_DIR / "classify.py"
SUMMARIZE_AL_PY = AUDIT_DIR / "summarize_al.py"


def _run(script, cwd, env=None):
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env or os.environ.copy(),
    )


class TestClassify(unittest.TestCase):
    """classify.py: our_severity() branches + fingerprint generation."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, ".audit"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _classify(self, findings):
        parsed_path = os.path.join(self.tmp, ".audit", "parsed.json")
        with open(parsed_path, "w") as f:
            json.dump(findings, f)
        result = _run(CLASSIFY_PY, cwd=self.tmp)
        self.assertEqual(result.returncode, 0, result.stderr)
        out_path = os.path.join(self.tmp, ".audit", "classified.json")
        with open(out_path) as f:
            return json.load(f)

    def _finding(self, level, confidence, rule_id="test/rule",
                  file=".github/workflows/ci.yml", snippet="", line=1):
        return {
            "rule_id": rule_id,
            "level": level,
            "severity_zizmor": "",
            "confidence": confidence,
            "message": "test message",
            "file": file,
            "line": line,
            "snippet": snippet,
        }

    # ── our_severity branches ─────────────────────────────────────────────────

    def test_error_high_confidence_is_critical(self):
        out = self._classify([self._finding("error", "high")])
        self.assertEqual(out[0]["severity"], "Critical")

    def test_error_medium_confidence_is_high(self):
        out = self._classify([self._finding("error", "medium")])
        self.assertEqual(out[0]["severity"], "High")

    def test_error_empty_confidence_is_high(self):
        out = self._classify([self._finding("error", "")])
        self.assertEqual(out[0]["severity"], "High")

    def test_warning_high_confidence_is_high(self):
        out = self._classify([self._finding("warning", "high")])
        self.assertEqual(out[0]["severity"], "High")

    def test_warning_medium_confidence_is_medium(self):
        out = self._classify([self._finding("warning", "medium")])
        self.assertEqual(out[0]["severity"], "Medium")

    def test_warning_empty_confidence_is_medium(self):
        out = self._classify([self._finding("warning", "")])
        self.assertEqual(out[0]["severity"], "Medium")

    def test_note_is_low(self):
        out = self._classify([self._finding("note", "high")])
        self.assertEqual(out[0]["severity"], "Low")

    def test_unknown_level_is_low(self):
        out = self._classify([self._finding("info", "high")])
        self.assertEqual(out[0]["severity"], "Low")

    # ── fingerprint properties ────────────────────────────────────────────────

    def test_fingerprint_is_16_hex_chars(self):
        out = self._classify([self._finding("error", "high")])
        fp = out[0]["fingerprint"]
        self.assertEqual(len(fp), 16)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))

    def test_fingerprint_uses_basename_not_full_path(self):
        # Same rule + basename + snippet → same fingerprint, even if dir differs
        f1 = self._finding("warning", "high", file=".github/workflows/aeon.yml")
        f2 = self._finding("warning", "high", file="other/path/aeon.yml")
        out = self._classify([f1, f2])
        self.assertEqual(out[0]["fingerprint"], out[1]["fingerprint"])

    def test_fingerprint_differs_for_different_rules(self):
        f1 = self._finding("error", "high", rule_id="rule/alpha")
        f2 = self._finding("error", "high", rule_id="rule/beta")
        out = self._classify([f1, f2])
        self.assertNotEqual(out[0]["fingerprint"], out[1]["fingerprint"])

    def test_short_rule_strips_namespace(self):
        # rule_id "namespace/short-name" → short_rule "short-name"
        out = self._classify([self._finding("error", "high", rule_id="zizmor/unpinned-uses")])
        self.assertEqual(out[0]["short_rule"], "unpinned-uses")

    def test_empty_findings_does_not_crash(self):
        out = self._classify([])
        self.assertEqual(out, [])


class TestSummarizeAl(unittest.TestCase):
    """summarize_al.py: shellcheck code matching + HIGH-CANDIDATE detection."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, ".audit"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _summarize(self, findings):
        path = os.path.join(self.tmp, ".audit", "actionlint.json")
        with open(path, "w") as f:
            json.dump(findings, f)
        result = _run(SUMMARIZE_AL_PY, cwd=self.tmp)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def _finding(self, message, filepath="ci.yml", line=1):
        return {"message": message, "filepath": filepath, "line": line}

    # ── shellcheck code matching ──────────────────────────────────────────────

    def test_sc2086_counted(self):
        out = self._summarize([self._finding("SC2086: double-quote to prevent globbing")])
        self.assertIn("'SC2086': 1", out)

    def test_sc2046_counted(self):
        out = self._summarize([self._finding("SC2046 word-splitting risk")])
        self.assertIn("'SC2046': 1", out)

    def test_sc2155_counted(self):
        out = self._summarize([self._finding("SC2155: declare and assign separately")])
        self.assertIn("'SC2155': 1", out)

    def test_unknown_code_goes_to_other(self):
        out = self._summarize([self._finding("SC9999: some unknown error")])
        self.assertIn("'other': 1", out)

    def test_first_match_wins_on_multi_code_message(self):
        # SC2086 appears before SC2046 in the priority list; only SC2086 incremented
        out = self._summarize([self._finding("SC2086 and SC2046 both present")])
        self.assertIn("'SC2086': 1", out)
        self.assertNotIn("'SC2046'", out)

    def test_empty_findings_does_not_crash(self):
        out = self._summarize([])
        self.assertIn("shellcheck codes:", out)

    # ── HIGH-CANDIDATE detection ──────────────────────────────────────────────

    def test_sc2086_with_github_is_high_candidate(self):
        out = self._summarize([self._finding("SC2086: ${{ github.event.inputs.value }}")])
        self.assertIn("HIGH-CANDIDATE:", out)

    def test_sc2046_with_github_is_high_candidate(self):
        out = self._summarize([self._finding("SC2046 unquoted ${{ github.ref }}")])
        self.assertIn("HIGH-CANDIDATE:", out)

    def test_sc2086_without_github_is_not_high_candidate(self):
        out = self._summarize([self._finding("SC2086: $MY_VAR unquoted")])
        self.assertNotIn("HIGH-CANDIDATE:", out)

    def test_github_check_is_case_insensitive(self):
        # .lower() applied before 'github.' check, so GITHUB. also triggers
        out = self._summarize([self._finding("SC2086: ${{ GITHUB.repository }}")])
        self.assertIn("HIGH-CANDIDATE:", out)

    def test_non_sc2086_sc2046_with_github_not_high_candidate(self):
        # SC2155 mentioning github. should not fire the HIGH-CANDIDATE path
        out = self._summarize([self._finding("SC2155: export in github.ref context")])
        self.assertNotIn("HIGH-CANDIDATE:", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
