import json, yaml, re, hashlib, datetime, subprocess, sys

NOW = datetime.datetime(2026, 6, 20, 6, 10, 0, tzinfo=datetime.timezone.utc)

# Enabled skills from aeon.yml
text = open('aeon.yml').read()
doc = yaml.safe_load(text)
skills_section = doc.get('skills', {})
enabled = {k: v for k, v in skills_section.items()
           if isinstance(v, dict) and v.get('enabled') is True}

# cron-state
try:
    cron = json.load(open('memory/cron-state.json'))
except Exception:
    cron = {}

# skill-runs (7d)
try:
    sr_raw = subprocess.run(['./scripts/skill-runs', '--hours', '168', '--failures', '--json'],
                            capture_output=True, text=True, timeout=120)
    sr = json.loads(sr_raw.stdout) if sr_raw.returncode == 0 else {}
except Exception:
    sr = {}
sr_by_skill = {s['skill']: s for s in sr.get('skills', [])}


def parse_iso(s):
    if not s:
        return None
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))


def classify(name, st):
    if not st:
        # No entry in cron-state
        in_sr = sr_by_skill.get(name)
        if in_sr and in_sr.get('total', 0) > 0:
            # Has workflow runs but no cron-state entry — partial
            fail = in_sr.get('failure', 0)
            succ = in_sr.get('success', 0)
            if succ == 0 and fail >= 3:
                return 'CRITICAL'
            return 'WARNING'
        return 'NO DATA'

    cf = st.get('consecutive_failures', 0)
    sr_rate = st.get('success_rate', 1)
    last_status = st.get('last_status', 'unknown')
    last_failed = parse_iso(st.get('last_failed'))
    last_dispatch = parse_iso(st.get('last_dispatch'))
    # Days since last success — proxy: if 0 successes ever, use days since first dispatch (or today as floor)
    if st.get('total_successes', 0) == 0:
        # No success ever — use days since now-cron-state's earliest activity
        # Approx: total_runs / runs_per_day. They run multiple times per day usually.
        # Use last_dispatch if available, otherwise assume long-running.
        days_since_last_success = 7  # conservative bucket
    else:
        days_since_last_success = 0

    if cf >= 3 or (last_status == 'failed' and days_since_last_success >= 3):
        return 'CRITICAL'
    # DEGRADED, FLAPPING, WARNING, HEALTHY checks omitted — won't apply when cf>=3
    if sr_rate < 0.6:
        return 'DEGRADED'
    if sr_rate < 0.8 or cf >= 1:
        return 'WARNING'
    return 'HEALTHY'


classification = {'critical': [], 'degraded': [], 'flapping': [],
                  'warning': [], 'healthy': [], 'no_data': []}

for name in sorted(enabled):
    st = cron.get(name, {})
    status = classify(name, st)
    cf = st.get('consecutive_failures', 0)
    last_err = st.get('last_error', '')
    sev = cf * (1 + 7 / 7)  # proxy ratio
    entry = {
        'name': name,
        'consecutive_failures': cf,
        'last_error_tail': last_err[:60] if last_err else '',
        'success_rate': st.get('success_rate', None),
        'total_runs': st.get('total_runs', 0),
        'severity': sev,
    }
    bucket = {
        'CRITICAL': 'critical',
        'DEGRADED': 'degraded',
        'FLAPPING': 'flapping',
        'WARNING': 'warning',
        'HEALTHY': 'healthy',
        'NO DATA': 'no_data',
    }[status]
    classification[bucket].append(entry)


# Sort critical by severity (consecutive_failures desc)
classification['critical'].sort(key=lambda e: -e['consecutive_failures'])

# Systemic pattern detection: all errors look like truncated JSON ending with "total_cost_usd":0,"usage":{"input_tokens":0
systemic_pattern = re.compile(r'total_cost_usd":0,"usage":\{"input_tokens":0')
matching_systemic = [e for e in classification['critical']
                     if systemic_pattern.search(cron.get(e['name'], {}).get('last_error', '') or '')]
systemic_note = None
if len(matching_systemic) >= 2:
    systemic_note = f'SYSTEMIC: {len(matching_systemic)} skills failing with zero-token result_json (Claude Code producing no output on cron runs)'

# Compute hash from sorted critical/degraded/flapping names + systemic
sig_parts = []
for bucket in ('critical', 'degraded', 'flapping'):
    sig_parts.extend(sorted(e['name'] for e in classification[bucket]))
if systemic_note:
    sig_parts.append(systemic_note)
sig = '|'.join(sig_parts)
current_hash = hashlib.sha256(sig.encode()).hexdigest()[:16]

summary = {
    'critical_n': len(classification['critical']),
    'degraded_n': len(classification['degraded']),
    'flapping_n': len(classification['flapping']),
    'warning_n': len(classification['warning']),
    'healthy_n': len(classification['healthy']),
    'no_data_n': len(classification['no_data']),
    'hash': current_hash,
    'systemic': systemic_note,
}

print(json.dumps({'summary': summary,
                  'critical': classification['critical'],
                  'no_data': [e['name'] for e in classification['no_data']],
                  'warning': [e['name'] for e in classification['warning']],
                  'healthy': [e['name'] for e in classification['healthy']]}, indent=2))
