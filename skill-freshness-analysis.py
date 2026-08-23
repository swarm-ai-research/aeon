import os, re, hashlib, json

ENABLED = [
    'planner','batch-health','memory-flush','memory-structural-dedupe','janitor',
    'stale-content-pr-sweeper','issue-triage','pr-triage','pr-review','pr-tracker',
    'github-monitor','repo-revive','code-health','surplus-pulse','compute-pulse',
    'compute-macro-correlate','compute-futures-eda','changelog','vuln-scanner',
    'goal-tracker','agi-tracker','milestone-tracker','skill-health','config-validator',
    'skill-analytics','reflect','self-review','skill-repair','cost-report',
    'ai-framework-watch','skill-evals','swarm-safety-eval','skill-update-check',
    'fleet-control','gitlawb-fleet-metrics','weekly-shiplog','workflow-security-audit',
    'skill-graph','notegraph','skillpacks','suggest-edges','skill-freshness',
    'run-frequency-guard','heartbeat'
]

DEP_PATTERNS = [
    r'memory/topics/[a-zA-Z0-9_.-]+\.md',
    r'memory/topics/[a-zA-Z0-9_.-]+\.json',
    r'memory/state/[a-zA-Z0-9_.-]+\.json',
    r'\.outputs/[a-zA-Z0-9_-]+\.md',
]

now = 1787472249
checkout_mtime = 1787472052

THRESHOLDS = {
    'topics': 168,
    'state': 720,
    'outputs': 4,
    'articles_daily': 28,
    'articles_weekly': 192,
}

cross_deps = []
self_deps = []
missing_deps = []
implicit_count = 0

for skill in ENABLED:
    path = 'skills/' + skill + '/SKILL.md'
    if not os.path.exists(path):
        continue
    with open(path) as f:
        content = f.read()

    found_paths = set()
    for pattern in DEP_PATTERNS:
        for match in re.findall(pattern, content):
            if match in found_paths:
                continue
            found_paths.add(match)
            implicit_count += 1

            base = os.path.basename(match).replace('.md','').replace('.json','')
            base_clean = re.sub(r'-state(-.*)?$', '', base)
            is_self = (base == skill or base_clean == skill)

            if not os.path.exists(match):
                missing_deps.append((skill, match))
                continue

            mtime = os.stat(match).st_mtime
            age_h = (now - mtime) / 3600

            if 'memory/topics' in match:
                threshold = THRESHOLDS['topics']
                cls = 'topics'
            elif 'memory/state' in match:
                threshold = THRESHOLDS['state']
                cls = 'state'
            elif '.outputs' in match:
                threshold = THRESHOLDS['outputs']
                cls = 'outputs'
            else:
                threshold = THRESHOLDS['articles_daily']
                cls = 'articles'

            if age_h <= threshold:
                sev = 'OK'
            elif age_h <= 2 * threshold:
                sev = 'WARN'
            else:
                sev = 'STALE'

            if is_self:
                self_deps.append((skill, match, age_h, threshold, cls, sev))
            else:
                cross_deps.append((skill, match, age_h, threshold, cls, sev))

print("=== CROSS-CONSUMER DEPS ===")
for s, d, age, thr, cls, sev in cross_deps:
    print("  " + s + " -> " + d + "  age=" + str(round(age,3)) + "h  threshold=" + str(thr) + "h  sev=" + sev)

print("\n=== SELF-STATE READS (filtered) ===")
for s, d, age, thr, cls, sev in self_deps:
    print("  " + s + " -> " + d + "  age=" + str(round(age,3)) + "h")

print("\n=== MISSING IMPLICIT DEPS (not flagged) ===")
for s, d in missing_deps:
    print("  " + s + " -> " + d)

flagged = [(s,d,age,thr,cls,sev) for s,d,age,thr,cls,sev in cross_deps if sev != 'OK']

print("\n=== SUMMARY ===")
print("Enabled skills: " + str(len(ENABLED)))
print("Implicit refs discovered: " + str(implicit_count))
print("Cross-consumer deps (scored): " + str(len(cross_deps)))
print("Self-state deps (filtered): " + str(len(self_deps)))
print("Missing implicit deps (not flagged): " + str(len(missing_deps)))
print("Flagged: " + str(len(flagged)))

if not flagged:
    verdict = "FRESHNESS_OK"
    fingerprint = hashlib.sha1(b"").hexdigest()
else:
    verdict = "FRESHNESS_STALE" if any(s in ['STALE','MISSING'] for _,_,_,_,_,s in flagged) else "FRESHNESS_WARN"
    rows = sorted(c + ":" + d + ":" + sev for c,d,_,_,_,sev in flagged)
    fingerprint = hashlib.sha1("\n".join(rows).encode()).hexdigest()

print("Fleet verdict: " + verdict)
print("Fingerprint: " + fingerprint)

prev_state_path = "memory/topics/skill-freshness-state.json"
with open(prev_state_path) as f:
    prev = json.load(f)

print("Prev verdict: " + prev.get("last_verdict",""))
print("Prev fingerprint: " + prev.get("last_flagged_fingerprint",""))
same = (fingerprint == prev.get("last_flagged_fingerprint","") and verdict == prev.get("last_verdict",""))
print("Same as prev: " + str(same))
if same:
    print("Status: FRESHNESS_NO_CHANGE -> no notification")
