"""Tests for the our_severity() branch logic in classify.py.

Run: python .audit/test_classify.py
"""
import importlib.util
import os
import sys
from unittest.mock import patch, MagicMock

# Load classify.py with all I/O patched so module-level code doesn't fail.
with patch("builtins.open", MagicMock()), \
     patch("json.load", return_value=[]), \
     patch("json.dump"), \
     patch("builtins.print"):
    _spec = importlib.util.spec_from_file_location(
        "classify",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "classify.py"),
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)

our_severity = _mod.our_severity

# ---------------------------------------------------------------------------
passed = 0
failed = 0


def check(label, got, want):
    global passed, failed
    if got == want:
        passed += 1
        print(f"  PASS  {label}")
    else:
        failed += 1
        print(f"  FAIL  {label}: got {got!r}, want {want!r}")


# Branch 1: error + high confidence → Critical
check("error+high → Critical", our_severity({"level": "error", "confidence": "high"}), "Critical")
# .lower() normalises uppercase confidence strings
check("error+High (caps) → Critical", our_severity({"level": "error", "confidence": "High"}), "Critical")
check("error+HIGH → Critical", our_severity({"level": "error", "confidence": "HIGH"}), "Critical")

# Branch 2: error + any other confidence → High
check("error+medium → High", our_severity({"level": "error", "confidence": "medium"}), "High")
check("error+low → High", our_severity({"level": "error", "confidence": "low"}), "High")
check("error+empty conf → High", our_severity({"level": "error", "confidence": ""}), "High")
# Missing 'confidence' key falls back to '' via .get('confidence', '')
check("error+missing conf → High", our_severity({"level": "error"}), "High")

# Branch 3: warning + high confidence → High
check("warning+high → High", our_severity({"level": "warning", "confidence": "high"}), "High")
check("warning+High (caps) → High", our_severity({"level": "warning", "confidence": "High"}), "High")

# Branch 4: warning + non-high confidence → Medium
check("warning+medium → Medium", our_severity({"level": "warning", "confidence": "medium"}), "Medium")
check("warning+low → Medium", our_severity({"level": "warning", "confidence": "low"}), "Medium")
check("warning+empty → Medium", our_severity({"level": "warning", "confidence": ""}), "Medium")
check("warning+missing conf → Medium", our_severity({"level": "warning"}), "Medium")

# Branch 5: note / any other level → Low, even with high confidence
check("note+high conf → Low", our_severity({"level": "note", "confidence": "high"}), "Low")
check("note+empty → Low", our_severity({"level": "note", "confidence": ""}), "Low")
check("unknown level+high → Low", our_severity({"level": "open", "confidence": "high"}), "Low")
check("none level → Low", our_severity({"level": "none", "confidence": ""}), "Low")

# ---------------------------------------------------------------------------
print(f"\n{passed} passed, {failed} failed")
if failed:
    sys.exit(1)
