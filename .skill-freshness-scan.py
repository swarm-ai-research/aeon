import re, os, sys

skills_enabled = [
    "planner","batch-health","memory-flush","memory-structural-dedupe","stale-content-pr-sweeper",
    "issue-triage","pr-triage","pr-review","pr-tracker","github-monitor",
    "code-health","surplus-pulse","compute-futures-eda","goal-tracker","skill-health",
    "reflect","fleet-control","gitlawb-fleet-metrics","notegraph","suggest-edges",
    "skill-freshness","run-frequency-guard","heartbeat",
    "janitor","repo-revive","compute-pulse","compute-macro-correlate","changelog",
    "vuln-scanner","agi-tracker","milestone-tracker","config-validator","skill-analytics",
    "self-review","cost-report","ai-framework-watch","skill-evals","swarm-safety-eval",
    "skill-update-check","weekly-shiplog","workflow-security-audit","skill-graph","skillpacks",
    "skill-repair"
]

base = "/home/runner/work/aeon/aeon"

ref_patterns = [
    r'articles/[a-zA-Z0-9_-]+(?:-\$\{today\}|-[0-9]{4}-[0-9]{2}-[0-9]{2}|-\*)?\.md',
    r'\.outputs/[a-zA-Z0-9_-]+\.md',
    r'memory/topics/[a-zA-Z0-9_.-]+\.md',
    r'memory/state/[a-zA-Z0-9_.-]+\.json',
]

for skill in skills_enabled:
    path = os.path.join(base, "skills", skill, "SKILL.md")
    if not os.path.exists(path):
        continue
    try:
        with open(path) as f:
            content = f.read()
        content_no_fences = re.sub(r'```[^`]*?```', '', content, flags=re.DOTALL)
        lines = content_no_fences.split('\n')
        cleaned = []
        skip_next = False
        for line in lines:
            if '<!-- skill-freshness:ignore -->' in line:
                skip_next = True
                continue
            if skip_next:
                skip_next = False
                continue
            cleaned.append(line)
        text = '\n'.join(cleaned)

        found = set()
        for p in ref_patterns:
            for m in re.finditer(p, text):
                ref = m.group()
                parts = ref.split('/')
                if len(parts) >= 2:
                    name_part = parts[1]
                    prefix = re.sub(r'(-\$\{today\}|-[0-9]{4}-[0-9]{2}-[0-9]{2}|-\*)\.md$', '', name_part)
                    prefix = re.sub(r'\.md$', '', prefix)
                    if prefix == skill:
                        continue
                found.add(ref)

        for r in sorted(found):
            print(skill + '\t' + r)
    except Exception as e:
        print(f"ERROR {skill}: {e}", file=sys.stderr)
