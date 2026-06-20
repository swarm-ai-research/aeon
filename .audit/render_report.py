"""Render the markdown audit report and the fingerprint trailer."""
import json
from collections import Counter, defaultdict

data = json.load(open('.audit/canonical.json'))
findings = data['findings']
s = data['summary']
today = data['today']
verdict = data['verdict']
exit_mode = data['exit_mode']

workflow_count = 7
action_count = 0
file_count = workflow_count + action_count

# Group by severity for rendering
high = [f for f in findings if f['severity'] == 'High']
medium = [f for f in findings if f['severity'] == 'Medium']
low = [f for f in findings if f['severity'] in ('Low', 'Informational')]

# Subgroup unpinned-uses vs secrets-outside-env in High
by_rule = defaultdict(list)
for f in high:
    by_rule[f['short_rule']].append(f)

# Build attack-chain text for High findings (grouped by rule to avoid 60 dupes)

attack_chains = []

# Unpinned actions/* uses (16 findings)
unpinned = by_rule.get('unpinned-uses', [])
if unpinned:
    files_lines = sorted({(f['file'], f['line'], f['snippet'].split('@')[-1].split()[0] if '@' in f['snippet'] else '?') for f in unpinned})
    locs = ', '.join(f"`{fname}:{ln}` (@{tag})" for fname, ln, tag in files_lines[:10])
    if len(files_lines) > 10:
        locs += f', +{len(files_lines)-10} more'
    chain = f"""### [HIGH] unpinned-uses — first-party `actions/*` referenced by mutable major tag
**Count:** {len(unpinned)} across {len({f['file'] for f in unpinned})} files
**Locations:** {locs}
**Pattern:**
```yaml
uses: actions/checkout@v5     # mutable — points to whatever v5.* publishes today
uses: actions/setup-node@v5   # same
uses: actions/checkout@v4     # same on v4
```

**Attack chain:**
1. **Entry:** any push, schedule, or dispatch event → all jobs check out via the unpinned tag.
2. **Vector:** GitHub re-points the `v5` tag if `actions/checkout` repo is compromised, or if a maintainer pushes a malicious commit and re-tags. The workflow grabs whatever code the tag points to *at runtime*.
3. **Sink:** the action runs inside the job with the same `permissions:` and `secrets:` as everything else in the job — including `contents: write`, `pull-requests: write`, and any auth tokens (`GH_GLOBAL`, `AEON_PRIVATE_PAT`, `CLAUDE_CODE_OAUTH_TOKEN`).
4. **Reachable secrets:** every secret referenced anywhere in the job (44 secret-references in this audit; see secrets-outside-env section).
5. **Blast radius:** full repo write (push to main, force-push, delete branches), cross-repo dispatch (chain-runner triggers other workflows), private-mirror sync (AEON_PRIVATE_PAT writes to the private aeon repo). A compromised `actions/checkout` would be a worst-case event for this repo.

**Trade-off:** SHA-pinning trades supply-chain protection for dependency drift cost (you must bump pins to get security patches). For first-party `actions/*`, the GitHub-attested supply chain is the strongest in the ecosystem — but pinning is still policy-recommended and is what zizmor's auditor persona enforces.

**Fix:** Replace each `actions/*@vN` with `actions/*@<full-40-char-sha> # vN.N.N` and bump quarterly. Renovate or Dependabot can manage the pin updates.

**Status:** Manual required — operator must select the exact commit SHA per pin; the skill does not auto-pin (matches the `Never auto-fix pinning` constraint)."""
    attack_chains.append(chain)

# secrets-outside-env (44 findings)
soe = by_rule.get('secrets-outside-env', [])
if soe:
    secrets_used = sorted({f['snippet'].split('.')[-1].rstrip() for f in soe if 'secrets.' in f['snippet']})
    files_count = Counter(f['file'] for f in soe)
    file_summary = ', '.join(f"`{fn}`({n})" for fn, n in files_count.most_common())
    chain = f"""### [HIGH] secrets-outside-env — secrets referenced outside a GitHub Actions Environment
**Count:** {len(soe)} across {len(files_count)} files
**Files:** {file_summary}
**Secrets referenced:** {', '.join('`' + sn + '`' for sn in secrets_used)}
**Pattern:**
```yaml
jobs:
  run:
    runs-on: ubuntu-latest
    # no `environment: prod-deploy` declaration → secret access is unscoped
    steps:
      - name: Run chain
        env:
          GH_TOKEN: ${{{{ secrets.GH_GLOBAL }}}}    # unscoped secret use
```

**Attack chain:**
1. **Entry:** every job has unrestricted access to every secret defined at the repo or org level — there is no GitHub Environment gate (`environment: production`) that would require deployment-protection rules, required reviewers, or branch restrictions before the secret is materialized in the runner.
2. **Vector:** a malicious PR (or compromised collaborator, or compromised dependency surfaced via `actions/checkout` — see unpinned-uses above) running on a non-`main` branch can still reach these secrets, because no environment-scoped protection rules apply.
3. **Sink:** the secret is written into `env:` at job-step level, where it is exfiltrable via any process the workflow spawns. Several secrets here (`AEON_PRIVATE_PAT`, `GH_GLOBAL`) carry **cross-repo** write privileges.
4. **Reachable scope:** `AEON_PRIVATE_PAT` writes to the private mirror (`aeon-private`). `GH_GLOBAL` is a fine-grained PAT covering this repo and its sibling repos. `CLAUDE_CODE_OAUTH_TOKEN` is a paying API token — exfiltration = direct billing impact.
5. **Blast radius:** in the absence of environment protections, a single supply-chain compromise or attacker-influenced workflow path discloses all five sensitive PATs. Adding `environment:` declarations is the canonical mitigation — it gates secret materialization on required reviewers, wait timers, and branch protection.

**Fix:** declare GitHub Environments in repo settings (e.g. `aeon-prod`) with required reviewer + branch restrictions, then add `environment: aeon-prod` to each job that uses these secrets. This is a repo-admin operation, not a workflow edit.

**Status:** Manual required — requires repo-settings change (create Environment, attach secrets, configure protection rules). The skill explicitly skips auto-fixing this class."""
    attack_chains.append(chain)

# Build the medium/low compact table

def render_table(rows, label):
    if not rows:
        return ''
    counter = Counter((f['short_rule'], f['file']) for f in rows)
    out = [f'\n## {label} ({len(rows)} findings — compact table)\n',
           '| Severity | Rule | File | Count | Sample line |',
           '|---|---|---|---|---|']
    for (rule, fname), n in counter.most_common():
        sample = next(f['line'] for f in rows if f['short_rule'] == rule and f['file'] == fname)
        sev = next(f['severity'] for f in rows if f['short_rule'] == rule and f['file'] == fname)
        out.append(f'| {sev} | `{rule}` | `{fname}` | {n} | {sample} |')
    return '\n'.join(out)

medium_table = render_table(medium, 'Medium-severity findings')
low_table = render_table(low, 'Low / Informational findings')

# Fingerprint trailer
trailer_lines = ['<!--', 'workflow-security-audit-fingerprints']
for f in findings:
    status = 'manual' if f.get('fix_status','').startswith('manual') else \
             ('auto-fixed' if f.get('fix_status') == 'auto-fixed' else 'open')
    trailer_lines.append(
        f"{f['fingerprint']} severity={f['severity']} status={status} "
        f"rule={f['short_rule']} file={f['file']} step={(f['step'] or '').replace(' ','_')[:60]}"
    )
trailer_lines.append('-->')
trailer = '\n'.join(trailer_lines)

repo_name = 'swarm-ai-research/aeon'
repo_url = 'https://github.com/swarm-ai-research/aeon'

report = f"""# Workflow Security Audit — {today}

**Verdict:** `{verdict}`
**Repo:** [{repo_name}]({repo_url})
**Files audited:** {file_count} ({workflow_count} workflows, {action_count} composite actions)
**Findings this run:** {s['total']} ({s['crit']} critical, {s['high']} high, {s['med']} medium, {s['low']} low)
**Delta vs (no prior audit):** {s['new']} new, {s['reintroduced']} reintroduced, {s['unchanged']} unchanged, {s['resolved']} resolved
**Auto-fixed:** {s['fixed_count']}
**Manual review required:** {s['manual_count']}

> **First-run note.** No prior `articles/workflow-security-audit-*.md` exists in the repo or its git history. Every finding is labeled `NEW` by construction. The next run will deltas against this report.

## Regressions (previously-fixed findings now present again)

_None — no prior audit to regress against._

## New findings — High

The 60 high-severity findings collapse to two patterns. Each is presented as one attack chain rather than 60 near-identical entries.

{chr(10).join(attack_chains)}

{medium_table}

{low_table}

## Carried over (unchanged)

_None — first run._

## Resolved since prior audit

_None — first run._

## Hand-rolled supplemental checks

| Check | Result |
|---|---|
| `toJson(github.event.*)` piped to shell (April 11 pattern) | clean — `messages.yml:659` already uses `env: _CLIENT_PAYLOAD_MESSAGE` → `printf '%s' "$_CLIENT_PAYLOAD_MESSAGE"` |
| `persist-credentials: true` on PR-ref checkout | clean — no `persist-credentials: true` present; no `pull_request_target`/`workflow_run` triggers |
| `GITHUB_ENV` write with `${{{{ github.event.* }}}}` interpolation | clean — only static literals (`CHAIN_STATUS=failed`) written |
| Fleet `inputs.*` flowing into `gh workflow run` / `gh api` / `run:` shell | clean — `chain-runner.yml` and `fleet-runner.yml` use `env:` indirection for all `inputs.*` references |
| Mutable ref on third-party action | clean — every `uses:` is first-party `actions/*` |

## Source status

- zizmor: `ok` (v1.25.2, persona=auditor) — 130 findings across 7 workflows
- actionlint: `ok` — 20 shellcheck findings (all style; none touch `${{{{ github.* }}}}` interpolations)
- hand-rolled: `ok` — 5 checks, 0 findings
- **Filename reconciliation:** the SARIF scan ran against `sync-aeon-public.yml`; that file has since been renamed to `sync-aeon-public-results.yml` (same content, same patterns). Findings retagged to the current filename. The bash sandbox blocked rerunning zizmor with `--output` in this session; the existing scan artifacts from earlier in the same session were used.

{trailer}
"""

with open('articles/workflow-security-audit-2026-06-20.md', 'w') as fh:
    fh.write(report)

print('report written: articles/workflow-security-audit-2026-06-20.md (' + str(len(report)) + ' bytes)')
print()
print('--- HEAD ---')
print(report[:1200])
