#!/usr/bin/env python3
"""Tests for the our_severity() branch logic in classify.py.

Extracts the function via AST so file-level I/O in classify.py is never
executed — no .audit/parsed.json needed to run these tests.

Run: python3 .audit/test_classify.py
"""

import ast
import os
import sys

# ── Load our_severity without triggering classify.py's file reads ──────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_HERE, "classify.py")

with open(_SRC) as _f:
    _tree = ast.parse(_f.read(), filename=_SRC)

_func_nodes = [n for n in _tree.body if isinstance(n, ast.FunctionDef)]
_ns = {}
exec(  # noqa: S102  (intentional: load pure function from sibling script)
    compile(ast.Module(body=_func_nodes, type_ignores=[]), filename=_SRC, mode="exec"),
    _ns,
)
our_severity = _ns["our_severity"]

# ── Test cases ──────────────────────────────────────────────────────────────

def test_error_high_conf_is_critical():
    assert our_severity({"level": "error", "confidence": "high"}) == "Critical"

def test_error_medium_conf_is_high():
    assert our_severity({"level": "error", "confidence": "medium"}) == "High"

def test_error_low_conf_is_high():
    assert our_severity({"level": "error", "confidence": "low"}) == "High"

def test_error_empty_conf_is_high():
    assert our_severity({"level": "error", "confidence": ""}) == "High"

def test_error_missing_confidence_key_is_high():
    # confidence absent → f.get('confidence', '') returns '' → not 'high' → High
    assert our_severity({"level": "error"}) == "High"

def test_error_uppercase_high_conf_is_critical():
    # classify.py lowercases confidence before comparing, so 'HIGH' → 'high'
    assert our_severity({"level": "error", "confidence": "HIGH"}) == "Critical"

def test_warning_high_conf_is_high():
    assert our_severity({"level": "warning", "confidence": "high"}) == "High"

def test_warning_medium_conf_is_medium():
    assert our_severity({"level": "warning", "confidence": "medium"}) == "Medium"

def test_warning_no_confidence_is_medium():
    assert our_severity({"level": "warning"}) == "Medium"

def test_note_any_conf_is_low():
    # 'note' level falls through all branches → Low regardless of confidence
    assert our_severity({"level": "note", "confidence": "high"}) == "Low"

def test_unknown_level_is_low():
    # An unrecognised level (e.g. future SARIF extension) must not raise
    assert our_severity({"level": "none", "confidence": "high"}) == "Low"

# ── Runner ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        (name, obj)
        for name, obj in sorted(globals().items())
        if name.startswith("test_") and callable(obj)
    ]
    passed = failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"OK  {name}")
            passed += 1
        except AssertionError as exc:
            print(f"FAIL {name}: {exc}")
            failed += 1
        except Exception as exc:
            print(f"ERR  {name}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
