#!/usr/bin/env python3
"""Invoke zizmor and actionlint, capture outputs to files."""
import os, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
os.chdir(ROOT.parent)

BIN = ROOT.parent / ".audit-bin"

def run(cmd, out_path, err_path):
    with open(out_path, "wb") as out, open(err_path, "wb") as err:
        p = subprocess.run(cmd, stdout=out, stderr=err)
        return p.returncode

rc_z = run(
    [str(BIN / "zizmor"), "--format", "sarif", "--persona", "auditor",
     ".github/workflows"],
    ROOT / "zizmor.sarif", ROOT / "zizmor.err"
)
print(f"zizmor_rc={rc_z}", file=sys.stderr)

rc_a = run(
    [str(BIN / "actionlint"), "-format", "{{json .}}"],
    ROOT / "actionlint.json", ROOT / "actionlint.err"
)
print(f"actionlint_rc={rc_a}", file=sys.stderr)
