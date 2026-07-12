#!/usr/bin/env python3
"""Parse zizmor SARIF + actionlint JSON + hand-rolled checks into a unified findings list."""
import json, hashlib, re, pathlib, glob

SARIF = ".audit/zizmor.sarif"
AL = ".audit/actionlint.json"
OUT = ".audit/parsed.json"

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def resolve_uri(uri):
    # zizmor emits paths relative to its target arg; workflows targeted from
    # .github/workflows/ come back bare (e.g. "aeon.yml") — always prefer the
    # .github/ prefix even when a same-named file exists at repo root.
    for pref in (".github/workflows/", ".github/actions/"):
        p = pref + uri
        if pathlib.Path(p).exists():
            return p
    if pathlib.Path(uri).exists():
        return uri
    return uri

_step_cache = {}
def step_name_for(path, line):
    if not pathlib.Path(path).exists():
        return None
    if path not in _step_cache:
        _step_cache[path] = pathlib.Path(path).read_text().splitlines()
    lines = _step_cache[path]
    for i in range(min(line, len(lines)) - 1, -1, -1):
        m = re.match(r'^(\s*)-\s+name:\s+(.+?)\s*$', lines[i])
        if m:
            return m.group(2).strip().strip('"\'').strip()
    return None

def line_snippet(path, line):
    if not pathlib.Path(path).exists():
        return ""
    try:
        lines = pathlib.Path(path).read_text().splitlines()
        if 1 <= line <= len(lines):
            return lines[line-1].strip()[:120]
    except Exception:
        pass
    return ""

# --- zizmor SARIF ---
zdata = json.load(open(SARIF))
zresults = zdata.get("runs", [{}])[0].get("results", [])
findings = []

for r in zresults:
    rule = r.get("ruleId","unknown")
    level = r.get("level","warning")
    msg = r.get("message",{}).get("text","")
    loc = r.get("locations",[{}])[0].get("physicalLocation",{})
    uri = resolve_uri(loc.get("artifactLocation",{}).get("uri","?"))
    line = loc.get("region",{}).get("startLine", 0)
    props = r.get("properties", {})
    zsev = str(props.get("zizmor/severity","Unknown")).lower()
    zconf = str(props.get("zizmor/confidence","Unknown")).lower()

    # Map severity per SKILL.md (level+confidence-based; zizmor's own severity as guardrail)
    if level == "error" and zconf == "high":
        sev = "Critical"
    elif level == "error":
        sev = "High"
    elif level == "warning" and zconf == "high":
        sev = "High"
    elif level == "warning":
        sev = "Medium"
    else:
        sev = "Low"

    # But override for pedantic-persona findings: they map to Low per zizmor's own tier
    if props.get("zizmor/persona","") == "Pedantic":
        sev = "Low"

    step = step_name_for(uri, line)
    step_key = step or f"L{line}"
    rule_short = rule.replace("zizmor/","")
    fp = sha(f"{rule_short}|{uri}|{step_key}")
    findings.append({
        "fingerprint": fp,
        "severity": sev,
        "rule_id": rule_short,
        "file": uri,
        "line": line,
        "step": step,
        "pattern": line_snippet(uri, line),
        "source": "zizmor",
        "message": msg[:240],
        "zsev": zsev,
        "zconf": zconf,
    })

# --- actionlint ---
try:
    al = json.load(open(AL))
except Exception:
    al = []

for entry in al:
    rule = entry.get("kind","actionlint")
    msg = entry.get("message","")
    file = entry.get("filepath","?")
    line = entry.get("line",0)
    step = step_name_for(file, line)
    step_key = step or f"L{line}"
    sev = "Medium"
    if rule == "expression":
        sev = "High"
    if rule == "shellcheck":
        codes = re.findall(r'SC\d{4}', msg)
        if any(c in ("SC2086","SC2046") for c in codes):
            try:
                lines_ = pathlib.Path(file).read_text().splitlines()
                window = "\n".join(lines_[max(0,line-40):line+5])
                if re.search(r'\$\{\{\s*(github|inputs|env|steps|matrix)\.', window):
                    sev = "High"
            except Exception:
                pass
    fp = sha(f"actionlint/{rule}|{file}|{step_key}|{msg[:60]}")
    findings.append({
        "fingerprint": fp,
        "severity": sev,
        "rule_id": f"actionlint/{rule}",
        "file": file,
        "line": line,
        "step": step,
        "pattern": line_snippet(file, line),
        "source": "actionlint",
        "message": msg[:240],
    })

# --- hand-rolled checks ---
target_files = sorted(set(
    glob.glob(".github/workflows/*.yml") +
    glob.glob(".github/workflows/*.yaml") +
    glob.glob(".github/actions/**/action.yml") +
    glob.glob(".github/actions/**/action.yaml")
))

def scan_lines(path):
    return pathlib.Path(path).read_text().splitlines()

for f in target_files:
    lines = scan_lines(f)
    for i, l in enumerate(lines):
        line_num = i + 1
        # 1) toJson-into-shell
        if re.search(r"echo\s+['\"]\$\{\{\s*toJson\(", l) or re.search(r"echo\s+['\"]?\$\{\{\s*toJson\(github\.event", l):
            step = step_name_for(f, line_num)
            step_key = step or f"L{line_num}"
            fp = sha(f"handrolled/tojson-shell|{f}|{step_key}")
            findings.append({
                "fingerprint": fp,
                "severity": "Critical",
                "rule_id": "handrolled/tojson-shell-injection",
                "file": f,
                "line": line_num,
                "step": step,
                "pattern": l.strip()[:120],
                "source": "hand-rolled",
                "message": "toJson(github.event.*) piped through echo into shell — script injection risk",
            })
        # 2) GITHUB_ENV / GITHUB_OUTPUT write with user-controlled data
        if re.search(r'echo\s+["\']?[A-Z_][A-Z0-9_]*=\$\{\{\s*(github\.event\.|inputs\.|client_payload)', l) and (
            ">> \"$GITHUB_ENV\"" in l or ">> $GITHUB_ENV" in l
            or ">> \"$GITHUB_OUTPUT\"" in l or ">> $GITHUB_OUTPUT" in l
        ):
            step = step_name_for(f, line_num)
            step_key = step or f"L{line_num}"
            fp = sha(f"handrolled/env-write|{f}|{step_key}")
            findings.append({
                "fingerprint": fp,
                "severity": "High",
                "rule_id": "handrolled/github-env-write-user-data",
                "file": f,
                "line": line_num,
                "step": step,
                "pattern": l.strip()[:120],
                "source": "hand-rolled",
                "message": "GITHUB_ENV/OUTPUT write with untrusted context — newline injection bypasses masking",
            })
        # 3) inputs/github.event into gh workflow run / gh api dispatches shell
        if re.search(r'(gh\s+workflow\s+run|gh\s+api\s+repos/.*dispatches).*\$\{\{\s*(inputs|github\.event)\.', l):
            step = step_name_for(f, line_num)
            step_key = step or f"L{line_num}"
            fp = sha(f"handrolled/gh-dispatch-inject|{f}|{step_key}")
            findings.append({
                "fingerprint": fp,
                "severity": "High",
                "rule_id": "handrolled/gh-dispatch-injection",
                "file": f,
                "line": line_num,
                "step": step,
                "pattern": l.strip()[:120],
                "source": "hand-rolled",
                "message": "inputs.* / github.event.* interpolated into gh workflow run/dispatch shell",
            })

# 4) Mutable ref on third-party action
TRUSTED_OWNERS = {"actions","github","docker","aws-actions"}
for f in target_files:
    lines = scan_lines(f)
    for i, l in enumerate(lines):
        m = re.search(r'uses:\s*([^/@\s]+)/([^@\s]+)@(\S+)', l)
        if not m:
            continue
        owner, action, ref = m.groups()
        if owner in TRUSTED_OWNERS:
            continue
        if re.fullmatch(r'[0-9a-f]{40}', ref):
            continue
        line_num = i + 1
        step = step_name_for(f, line_num)
        step_key = step or f"L{line_num}"
        fp = sha(f"handrolled/mutable-ref|{f}|{step_key}|{owner}/{action}")
        findings.append({
            "fingerprint": fp,
            "severity": "Medium",
            "rule_id": "handrolled/mutable-third-party-ref",
            "file": f,
            "line": line_num,
            "step": step,
            "pattern": l.strip()[:120],
            "source": "hand-rolled",
            "message": f"Third-party action {owner}/{action} pinned to mutable ref {ref}",
        })

# 5) persist-credentials + PR head ref (poisoned pipeline)
for f in target_files:
    text = pathlib.Path(f).read_text()
    for m in re.finditer(r'uses:\s*actions/checkout@\S+', text):
        start = m.start()
        window = text[start:start+800]
        has_pr_ref = re.search(r'ref:\s*\$\{\{\s*github\.event\.pull_request\.head\.(sha|ref)', window)
        has_persist_true = re.search(r'persist-credentials:\s*true', window)
        has_persist_false = re.search(r'persist-credentials:\s*false', window)
        if has_pr_ref and (has_persist_true or not has_persist_false):
            line_num = text[:start].count("\n") + 1
            step = step_name_for(f, line_num)
            step_key = step or f"L{line_num}"
            has_pr_target = "pull_request_target" in text[:2000]
            has_wf_run = "workflow_run" in text[:2000]
            sev = "Critical" if has_pr_target else "High"
            fp = sha(f"handrolled/poisoned-pipeline|{f}|{step_key}")
            findings.append({
                "fingerprint": fp,
                "severity": sev,
                "rule_id": "handrolled/poisoned-pipeline",
                "file": f,
                "line": line_num,
                "step": step,
                "pattern": (text.splitlines()[line_num-1].strip()[:120] if line_num-1 < len(text.splitlines()) else ""),
                "source": "hand-rolled",
                "message": "checkout with PR head ref and default/persisted credentials — poisoned pipeline",
            })

# Dedup by fingerprint (keep the higher-severity if collision)
SEV_ORDER = {"Critical":4,"High":3,"Medium":2,"Low":1}
seen = {}
for x in findings:
    fp = x["fingerprint"]
    prev = seen.get(fp)
    if prev is None or SEV_ORDER.get(x["severity"],0) > SEV_ORDER.get(prev["severity"],0):
        seen[fp] = x
final = list(seen.values())
pathlib.Path(OUT).write_text(json.dumps(final, indent=2))
print(f"parsed {len(zresults)} zizmor + {len(al)} actionlint entries + {sum(1 for x in findings if x['source']=='hand-rolled')} hand-rolled → {len(final)} unique findings")
by_sev = {}
for x in final:
    by_sev[x["severity"]] = by_sev.get(x["severity"],0)+1
print("severity:", by_sev)
by_source = {}
for x in final:
    by_source[x["source"]] = by_source.get(x["source"],0)+1
print("source:", by_source)
