#!/usr/bin/env python3
"""Hand-rolled security checks, backstopping zizmor gaps for this repo."""
import glob
import hashlib
import json
import re

WFS = sorted(glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml'))
ACT = sorted(glob.glob('.github/actions/**/action.yml', recursive=True) +
             glob.glob('.github/actions/**/action.yaml', recursive=True))
TARGETS = WFS + ACT

findings = []


def emit(sev, rule, file, line, step, pattern, source='hand-rolled'):
    fp_input = f"{rule}|{file}|{step}"
    fp = hashlib.sha256(fp_input.encode()).hexdigest()[:16]
    findings.append({
        'fingerprint': fp,
        'severity': sev,
        'rule_id': rule,
        'file': file,
        'line': line,
        'step': step,
        'pattern': pattern[:200],
        'source': source,
    })


def find_step_name(lines, idx):
    """Walk backward from line idx to find the enclosing step's name (0-indexed)."""
    for i in range(idx, -1, -1):
        m = re.match(r'\s*-?\s*name:\s*(.+)$', lines[i])
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return f'line-{idx+1}'


for fn in TARGETS:
    try:
        text = open(fn).read()
    except Exception:
        continue
    lines = text.split('\n')
    trigger_block = ''
    m = re.search(r'^on:\s*(.*?)(?=^\S|\Z)', text, re.MULTILINE | re.DOTALL)
    if m:
        trigger_block = m.group(0)

    # 1) toJson-into-shell injection: echo '${{ toJson(github.event...)' | jq ...
    for idx, ln in enumerate(lines):
        if re.search(r"""echo\s+['"]\s*\$\{\{\s*toJson\(github\.event""", ln) \
           or re.search(r"""\$\(echo\s+['"]\s*\$\{\{\s*toJson\(""", ln):
            step = find_step_name(lines, idx)
            emit('Critical', 'handrolled/tojson-into-shell', fn, idx + 1, step, ln.strip())

    # 2) persist-credentials: true (or default) + head.sha checkout on pr_target / workflow_run
    is_pr_target = 'pull_request_target' in trigger_block
    is_workflow_run = 'workflow_run' in trigger_block
    if is_pr_target or is_workflow_run:
        # Scan for actions/checkout with head.sha / head.ref
        for idx, ln in enumerate(lines):
            if 'actions/checkout' in ln:
                # look at the next 20 lines for `ref:` and `persist-credentials:`
                blk = '\n'.join(lines[idx:idx + 30])
                if re.search(r'ref:\s*\$\{\{\s*github\.event\.pull_request\.head\.(sha|ref)', blk) \
                   and not re.search(r'persist-credentials:\s*false', blk):
                    sev = 'Critical' if is_pr_target else 'High'
                    step = find_step_name(lines, idx)
                    emit(sev, 'handrolled/poisoned-pipeline-checkout', fn, idx + 1, step, ln.strip())

    # 3) GITHUB_ENV / GITHUB_OUTPUT writes with user-controlled interpolation
    for idx, ln in enumerate(lines):
        # echo "X=${{ github.event.* }}" >> "$GITHUB_ENV"
        if re.search(r'>>\s*["\']?\$?\{?GITHUB_(ENV|OUTPUT)', ln) \
           and re.search(r'\$\{\{\s*github\.event\.[^}]+\}\}', ln):
            step = find_step_name(lines, idx)
            emit('High', 'handrolled/github-env-injection', fn, idx + 1, step, ln.strip())

    # 4) Fleet-specific: gh workflow run / gh api /dispatches with inputs.* verbatim in same shell
    for idx, ln in enumerate(lines):
        if re.search(r'gh\s+(workflow\s+run|api\s+repos/.*/dispatches)', ln) \
           and re.search(r'\$\{\{\s*inputs\.[^}]+\}\}', ln):
            step = find_step_name(lines, idx)
            emit('High', 'handrolled/fleet-dispatch-inputs-inline', fn, idx + 1, step, ln.strip())

    # 5) Mutable ref on third-party action: uses: owner/action@branch or @vN where owner ∉ {actions,github,docker,aws-actions}
    trusted = {'actions', 'github', 'docker', 'aws-actions'}
    for idx, ln in enumerate(lines):
        m = re.search(r'uses:\s*([^/]+)/([^@\s]+)@(\S+)', ln)
        if not m:
            continue
        owner, action, ref = m.groups()
        if owner in trusted:
            continue
        # SHA pin = 40 hex chars
        if re.fullmatch(r'[0-9a-f]{40}', ref):
            continue
        step = find_step_name(lines, idx)
        emit('Medium', 'handrolled/mutable-third-party-ref', fn, idx + 1, step,
             f'uses: {owner}/{action}@{ref}')

# Idempotency-flagged: template-injection targets that already have env intermediary
# (For each zizmor template-injection finding, check if the enclosing step already has _ env vars.)
# Skipped here — we'll do idempotency check inline when auto-fixing.

by_rule = {}
for f in findings:
    by_rule[f['rule_id']] = by_rule.get(f['rule_id'], 0) + 1
print("hand-rolled findings:")
for k, v in by_rule.items():
    print(f"  {v:3d} {k}")
print(f"total: {len(findings)}")
for f in findings:
    print(f"  [{f['severity']}] {f['rule_id']} {f['file']}:{f['line']} step={f['step']!r}")

open('.audit/handrolled.json', 'w').write(json.dumps(findings, indent=2))
