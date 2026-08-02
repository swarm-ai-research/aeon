#!/usr/bin/env python3
"""Hand-rolled security pattern checks for workflow-security-audit skill."""
import re, glob, json

targets = sorted(glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml'))
findings = []

TOJSON_RE = re.compile(r"echo\s+['\"]?\$\{\{\s*toJson\s*\(\s*github\.")
ENV_INJ_RE = re.compile(r'echo\s+["\']?[A-Za-z_]+=\$\{\{\s*(github\.event|inputs)\.[^}]+\}\}["\']?\s*>>\s*"?\$?\{?GITHUB_(ENV|OUTPUT)')
USES_RE = re.compile(r'uses:\s*([\w-]+)/([\w./-]+)@([\w./-]+)')

for f in targets:
    lines = open(f).read().splitlines()
    for i, line in enumerate(lines, 1):
        if TOJSON_RE.search(line):
            findings.append({
                'rule_id': 'hand-rolled/toJson-shell-injection',
                'severity': 'Critical',
                'file': f, 'line': i, 'pattern': line.strip()[:120],
                'source': 'hand-rolled',
            })
        if ENV_INJ_RE.search(line):
            findings.append({
                'rule_id': 'hand-rolled/github-env-injection',
                'severity': 'High',
                'file': f, 'line': i, 'pattern': line.strip()[:120],
                'source': 'hand-rolled',
            })
        m = USES_RE.search(line)
        if m:
            owner, repo, ref = m.group(1), m.group(2), m.group(3)
            if owner == '.' or line.strip().startswith('uses: ./'):
                continue
            trusted = owner in ('actions', 'github', 'docker', 'aws-actions')
            is_sha = re.fullmatch(r'[0-9a-f]{40}', ref)
            if not trusted and not is_sha:
                findings.append({
                    'rule_id': 'hand-rolled/mutable-third-party-ref',
                    'severity': 'Medium',
                    'file': f, 'line': i, 'pattern': f'{owner}/{repo}@{ref}',
                    'source': 'hand-rolled',
                })

# poisoned pipeline execution pattern
for f in targets:
    text = open(f).read()
    if 'pull_request_target' in text or 'workflow_run' in text:
        if re.search(r'ref:\s*\$\{\{\s*github\.event\.pull_request\.head\.(sha|ref)\s*\}\}', text):
            for m in re.finditer(r'uses:\s*actions/checkout[^\n]*\n((?:[^\S\n]+[^\n]*\n){0,10})', text):
                block = m.group(0)
                if 'persist-credentials: false' not in block:
                    line_num = text[:m.start()].count('\n') + 1
                    severity = 'Critical' if 'pull_request_target' in text else 'High'
                    findings.append({
                        'rule_id': 'hand-rolled/poisoned-pipeline-execution',
                        'severity': severity,
                        'file': f, 'line': line_num,
                        'pattern': 'checkout head.sha without persist-credentials: false',
                        'source': 'hand-rolled',
                    })
                    break

# fleet-specific: gh workflow run / dispatches / gh api with inputs.* directly
for f in targets:
    if 'chain-runner' in f or 'fleet' in f or 'spawn-instance' in f:
        lines = open(f).read().splitlines()
        for i, line in enumerate(lines, 1):
            if re.search(r'gh\s+(workflow\s+run|api\s+repos?/[^\s]*/dispatches)', line):
                if '${{' in line and 'inputs.' in line:
                    findings.append({
                        'rule_id': 'hand-rolled/fleet-input-shell-passthrough',
                        'severity': 'High',
                        'file': f, 'line': i, 'pattern': line.strip()[:120],
                        'source': 'hand-rolled',
                    })

print(f'Hand-rolled findings: {len(findings)}')
for x in findings:
    print(f"  [{x['severity']}] {x['file']}:{x['line']}  {x['rule_id']}")
open('.audit/handrolled.json', 'w').write(json.dumps(findings, indent=2))
