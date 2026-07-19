#!/usr/bin/env python3
"""Unit tests for pure functions extracted from parse_findings.py.

Run: python -m pytest .audit/test_parse_findings.py
  or: python .audit/test_parse_findings.py
"""
import hashlib
import re
import unittest

# ── Functions under test (copied verbatim from parse_findings.py) ────────────

def sev_from_zizmor(level, confidence):
    if level == "error" and confidence == "high":
        return "Critical"
    if level == "error":
        return "High"
    if level == "warning" and confidence == "high":
        return "High"
    if level == "warning":
        return "Medium"
    return "Low"


def fp(rule, file, ctx):
    return hashlib.sha256(f"{rule}|{file}|{ctx}".encode()).hexdigest()[:16]


def route_key(result):
    cfs = result.get("codeFlows") or []
    if not cfs:
        return ""
    tfs = cfs[0].get("threadFlows") or []
    if not tfs:
        return ""
    locs = tfs[0].get("locations") or []
    if not locs:
        return ""
    logs = locs[0].get("location", {}).get("logicalLocations") or []
    if not logs:
        return ""
    sym = logs[0].get("properties", {}).get("symbolic", {})
    route = sym.get("route", {}).get("route") or []
    parts = []
    for r in route:
        if "Key" in r:
            parts.append(str(r["Key"]))
        elif "Index" in r:
            parts.append(f"[{r['Index']}]")
    return ".".join(parts)


def third_party_mutable(l, _t=None, _i=None):
    m = re.search(r'uses:\s*([^/@\s]+)/([^@\s]+)@([^\s]+)', l)
    if not m:
        return False
    owner = m.group(1)
    ref = m.group(3)
    trusted = {"actions", "github", "docker", "aws-actions", "./"}
    if owner in trusted or owner.startswith("./"):
        return False
    if re.fullmatch(r"[0-9a-f]{40}", ref):
        return False
    return True


# ── Tests ────────────────────────────────────────────────────────────────────

class TestSevFromZizmor(unittest.TestCase):
    # All five branches in the function

    def test_error_high_yields_critical(self):
        self.assertEqual(sev_from_zizmor("error", "high"), "Critical")

    def test_error_medium_yields_high(self):
        self.assertEqual(sev_from_zizmor("error", "medium"), "High")

    def test_error_low_yields_high(self):
        self.assertEqual(sev_from_zizmor("error", "low"), "High")

    def test_error_empty_confidence_yields_high(self):
        self.assertEqual(sev_from_zizmor("error", ""), "High")

    def test_warning_high_yields_high(self):
        self.assertEqual(sev_from_zizmor("warning", "high"), "High")

    def test_warning_medium_yields_medium(self):
        self.assertEqual(sev_from_zizmor("warning", "medium"), "Medium")

    def test_warning_empty_confidence_yields_medium(self):
        self.assertEqual(sev_from_zizmor("warning", ""), "Medium")

    def test_note_yields_low(self):
        self.assertEqual(sev_from_zizmor("note", "high"), "Low")

    def test_unknown_level_yields_low(self):
        self.assertEqual(sev_from_zizmor("info", "high"), "Low")

    def test_uppercase_confidence_not_treated_as_high(self):
        # confidence must be lowercase "high" — "HIGH" falls through to the
        # non-high branch; parse_findings.py normalises with .lower() before
        # calling this function, so callers must normalise too.
        self.assertEqual(sev_from_zizmor("error", "HIGH"), "High")  # not Critical
        self.assertEqual(sev_from_zizmor("warning", "HIGH"), "Medium")  # not High


class TestFingerprint(unittest.TestCase):
    def test_returns_16_hex_chars(self):
        result = fp("rule", "file.yml", "ctx")
        self.assertEqual(len(result), 16)
        self.assertRegex(result, r"^[0-9a-f]{16}$")

    def test_deterministic(self):
        self.assertEqual(fp("r", "f", "c"), fp("r", "f", "c"))

    def test_different_rule_differs(self):
        self.assertNotEqual(fp("rule-a", "f", "c"), fp("rule-b", "f", "c"))

    def test_different_file_differs(self):
        self.assertNotEqual(fp("r", "file-a", "c"), fp("r", "file-b", "c"))

    def test_different_ctx_differs(self):
        self.assertNotEqual(fp("r", "f", "ctx-a"), fp("r", "f", "ctx-b"))

    def test_empty_fields_are_stable(self):
        result = fp("", "", "")
        self.assertEqual(len(result), 16)


class TestRouteKey(unittest.TestCase):
    # Helper to build a fully-populated result dict from a route list

    @staticmethod
    def _make_result(route_list):
        sym = {"route": {"route": route_list}}
        ll = {"properties": {"symbolic": sym}}
        loc = {"location": {"logicalLocations": [ll]}}
        cf = {"threadFlows": [{"locations": [loc]}]}
        return {"codeFlows": [cf]}

    # Early-exit paths

    def test_empty_dict_returns_empty(self):
        self.assertEqual(route_key({}), "")

    def test_none_code_flows_returns_empty(self):
        self.assertEqual(route_key({"codeFlows": None}), "")

    def test_empty_code_flows_returns_empty(self):
        self.assertEqual(route_key({"codeFlows": []}), "")

    def test_missing_thread_flows_returns_empty(self):
        self.assertEqual(route_key({"codeFlows": [{"threadFlows": []}]}), "")

    def test_missing_locations_returns_empty(self):
        cf = {"threadFlows": [{"locations": []}]}
        self.assertEqual(route_key({"codeFlows": [cf]}), "")

    def test_empty_logical_locations_returns_empty(self):
        loc = {"location": {"logicalLocations": []}}
        cf = {"threadFlows": [{"locations": [loc]}]}
        self.assertEqual(route_key({"codeFlows": [cf]}), "")

    def test_empty_route_list_returns_empty(self):
        self.assertEqual(route_key(self._make_result([])), "")

    # Happy paths

    def test_key_route(self):
        result = self._make_result([{"Key": "jobs"}, {"Key": "build"}, {"Key": "steps"}])
        self.assertEqual(route_key(result), "jobs.build.steps")

    def test_index_route(self):
        result = self._make_result([{"Index": 0}, {"Index": 3}])
        self.assertEqual(route_key(result), "[0].[3]")

    def test_mixed_key_and_index(self):
        result = self._make_result([{"Key": "jobs"}, {"Index": 2}, {"Key": "steps"}])
        self.assertEqual(route_key(result), "jobs.[2].steps")

    def test_unknown_route_entry_skipped(self):
        # An entry with neither Key nor Index contributes nothing
        result = self._make_result([{"Key": "jobs"}, {"Other": "x"}, {"Index": 1}])
        self.assertEqual(route_key(result), "jobs.[1]")


class TestThirdPartyMutable(unittest.TestCase):
    # Trusted owners — should NOT flag

    def test_no_uses_line(self):
        self.assertFalse(third_party_mutable("    run: echo hello"))

    def test_trusted_actions_owner(self):
        self.assertFalse(third_party_mutable("      uses: actions/checkout@v4"))

    def test_trusted_github_owner(self):
        self.assertFalse(third_party_mutable("      uses: github/codeql-action@v3"))

    def test_trusted_docker_owner(self):
        self.assertFalse(third_party_mutable("      uses: docker/build-push-action@v5"))

    def test_trusted_aws_actions_owner(self):
        self.assertFalse(third_party_mutable("      uses: aws-actions/configure-aws-credentials@v4"))

    def test_local_action_with_slash_prefix(self):
        self.assertFalse(third_party_mutable("      uses: ./local-action"))

    # SHA-pinned third-party — should NOT flag

    def test_full_40char_sha_is_safe(self):
        sha = "a" * 40
        self.assertFalse(third_party_mutable(f"      uses: some-org/some-action@{sha}"))

    def test_lowercase_hex_sha_is_safe(self):
        sha = "0123456789abcdef" * 2 + "01234567"  # exactly 40 chars
        self.assertFalse(third_party_mutable(f"      uses: third-party/action@{sha}"))

    # Mutable refs — SHOULD flag

    def test_semver_tag_is_flagged(self):
        self.assertTrue(third_party_mutable("      uses: some-org/some-action@v1.2.3"))

    def test_major_tag_is_flagged(self):
        self.assertTrue(third_party_mutable("      uses: some-org/some-action@v2"))

    def test_branch_ref_is_flagged(self):
        self.assertTrue(third_party_mutable("      uses: some-org/some-action@main"))

    def test_short_sha_7chars_is_flagged(self):
        # Short SHAs are not 40 hex chars and must be treated as mutable
        self.assertTrue(third_party_mutable("      uses: some-org/some-action@abc1234"))

    def test_mixed_case_sha_is_flagged(self):
        # SHA must be all-lowercase to match fullmatch; uppercase hex is not trusted
        sha = "A" * 40
        self.assertTrue(third_party_mutable(f"      uses: some-org/some-action@{sha}"))


if __name__ == "__main__":
    unittest.main()
