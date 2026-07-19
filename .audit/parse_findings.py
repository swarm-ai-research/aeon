#!/usr/bin/env python3
"""Parse zizmor SARIF + actionlint JSON into a canonical findings list."""
import json, hashlib, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent

def sev_from_zizmor(level, confidence):
    if level == "error" and confidence == "high":
        return "Critical"
    if level == "error":
        return "High"
    if level == "warning" and confidence == "high":
        return "High"
    if level == "warning":
        return "Medium"
    return "Low"

def fp(rule, file, ctx):
    return hashlib.sha256(f"{rule}|{file}|{ctx}".encode()).hexdigest()[:16]

def route_key(result):
    """Stable-ish logical route from zizmor codeFlows (job.step index)."""
    cfs = result.get("codeFlows") or []
    if not cfs:
        return ""
    tfs = cfs[0].get("threadFlows") or []
    if not tfs:
        return ""
    locs = tfs[0].get("locations") or []
    if not locs:
        return ""
    logs = locs[0].get("location", {}).get("logicalLocations") or []
    if not logs:
        return ""
    sym = logs[0].get("properties", {}).get("symbolic", {})
    route = sym.get("route", {}).get("route") or []
    parts = []
    for r in route:
        if "Key" in r:
            parts.append(str(r["Key"]))
        elif "Index" in r:
            parts.append(f"[{r['Index']}]")
    return ".".join(parts)

findings = []

# --- zizmor SARIF ---
with open(ROOT / "zizmor.sarif") as f:
    sarif = json.load(f)

for run in sarif.get("runs", []):
    for r in run.get("results", []):
        rule = r.get("ruleId", "unknown")
        level = r.get("level", "warning")
        props = r.get("properties", {}) or {}
        conf = (props.get("problem.severity") or props.get("security-severity")
                or props.get("zizmor/confidence") or "").lower()
        # zizmor puts confidence in properties differently across versions;
        # fall back to parsing the message.
        msg = (r.get("message", {}) or {}).get("text", "")
        loc = (r.get("locations") or [{}])[0]
        pl = (loc.get("physicalLocation") or {})
        art = (pl.get("artifactLocation") or {}).get("uri", "")
        if art and not art.startswith(".github/"):
            art = ".github/workflows/" + art
        region = pl.get("region") or {}
        line = region.get("startLine")
        snippet = ""
        try:
            snippet = (region.get("snippet") or {}).get("text") or ""
        except Exception:
            pass
        # confidence often lives in props like "problem.severity" (low/medium/high) or
        # "security-severity" (numeric 0-10). Fall back to numeric threshold.
        if not conf:
            try:
                num = float(props.get("security-severity", "0"))
                if num >= 8:
                    conf = "high"
                elif num >= 4:
                    conf = "medium"
                else:
                    conf = "low"
            except Exception:
                conf = "medium"
        sev = sev_from_zizmor(level, conf)
        # Prefer the step's `name:` line from the snippet as stable context;
        # fall back to snippet head plus line number.
        step_ctx = ""
        if snippet:
            for sl in snippet.splitlines():
                s = sl.strip()
                if s.startswith("name:"):
                    step_ctx = s[:80]
                    break
            if not step_ctx:
                step_ctx = snippet.strip().splitlines()[0][:80]
        step_ctx = step_ctx or f"line-{line}"
        # Use zizmor's logical route (`jobs.<job>.steps.[N]`) as a stable
        # tiebreaker so two `actions/checkout@v5` blocks at different step
        # indices don't collapse to one fingerprint. Route is line-drift-safe.
        route = route_key(r)
        f_id = fp(rule, art, f"{step_ctx}|{route}")
        findings.append({
            "fingerprint": f_id,
            "severity": sev,
            "rule_id": rule,
            "file": art,
            "line": line,
            "step": step_ctx,
            "pattern": (snippet.strip()[:120] if snippet else msg[:120]),
            "message": msg,
            "source": "zizmor",
            "confidence": conf,
            "level": level,
        })

# --- actionlint JSON ---
with open(ROOT / "actionlint.json") as f:
    txt = f.read().strip()
    al = json.loads(txt) if txt else []

for item in al:
    kind = item.get("kind", "")
    file = item.get("filepath", "")
    line = item.get("line")
    msg = item.get("message", "")
    snippet_head = (item.get("snippet") or "").splitlines()[0][:60]
    # security-relevant kinds
    sev = "Medium"
    if kind == "expression":
        sev = "High"
    if kind == "shellcheck" and any(sc in msg for sc in ("SC2086", "SC2046")) and "${{ github." in msg:
        sev = "High"
    f_id = fp(f"actionlint-{kind}", file, snippet_head or f"line-{line}")
    findings.append({
        "fingerprint": f_id,
        "severity": sev,
        "rule_id": f"actionlint-{kind}",
        "file": file,
        "line": line,
        "step": snippet_head,
        "pattern": msg[:120],
        "message": msg,
        "source": "actionlint",
    })

# --- Hand-rolled checks ---
def scan(pattern_desc, matcher, severity):
    for path in sorted(pathlib.Path(".github/workflows").glob("*.y*ml")):
        text = path.read_text()
        for idx, line in enumerate(text.splitlines(), 1):
            if matcher(line, text, idx):
                f_id = fp(pattern_desc, str(path), line.strip()[:60])
                findings.append({
                    "fingerprint": f_id,
                    "severity": severity,
                    "rule_id": pattern_desc,
                    "file": str(path),
                    "line": idx,
                    "step": line.strip()[:60],
                    "pattern": line.strip()[:120],
                    "message": pattern_desc,
                    "source": "hand-rolled",
                })

import re
# 1. toJson-into-shell injection
scan("toJson-into-shell",
     lambda l, t, i: bool(re.search(r"\$\(.*toJson\(github\.event", l))
                     or bool(re.search(r"echo\s+'?\"?\$\{\{\s*toJson\(github", l)),
     "Critical")

# 2. persist-credentials: true on checkout when using PR head SHA
# scan for `persist-credentials: true` block; then check nearby ref: github.event.pull_request
def persist_head_matcher(_l, text, _i):
    return False  # handled in file-level pass below

# file-level attack-chain checks
for path in sorted(pathlib.Path(".github/workflows").glob("*.y*ml")):
    text = path.read_text()
    lines = text.splitlines()
    triggers = re.findall(r"^on:\s*$|pull_request_target|workflow_run|issue_comment|workflow_dispatch|repository_dispatch", text, re.M)
    has_pr_target = "pull_request_target" in text
    has_workflow_run = "workflow_run" in text
    for i, ln in enumerate(lines, 1):
        if "persist-credentials: true" in ln:
            surround = "\n".join(lines[max(0, i - 15):min(len(lines), i + 15)])
            if "pull_request.head.sha" in surround or "pull_request.head.ref" in surround:
                sev = "Critical" if has_pr_target else ("High" if has_workflow_run else "Medium")
                f_id = fp("persist-creds-pr-head", str(path), ln.strip()[:60])
                findings.append({
                    "fingerprint": f_id,
                    "severity": sev,
                    "rule_id": "persist-creds-pr-head",
                    "file": str(path),
                    "line": i,
                    "step": ln.strip()[:60],
                    "pattern": ln.strip()[:120],
                    "message": "persist-credentials: true near PR head checkout on privileged trigger",
                    "source": "hand-rolled",
                })

# 3. GITHUB_ENV / GITHUB_OUTPUT writes with user-controlled data
scan("github-env-injection",
     lambda l, t, i: bool(re.search(r'echo\s+"[^"]*\$\{\{\s*github\.event\.[^}]+\}\}[^"]*"\s*>>\s*"?\$GITHUB_(ENV|OUTPUT)"?', l)),
     "High")

# 4. Fleet-specific: inputs.* passed to gh workflow run / gh api dispatches / shell
scan("inputs-to-gh-dispatch",
     lambda l, t, i: bool(re.search(r'(gh workflow run|gh api.*dispatches).*\$\{\{\s*inputs\.', l)),
     "High")

# 5. Mutable ref on third-party action
def third_party_mutable(l, _t, _i):
    m = re.search(r'uses:\s*([^/@\s]+)/([^@\s]+)@([^\s]+)', l)
    if not m:
        return False
    owner = m.group(1)
    ref = m.group(3)
    trusted = {"actions", "github", "docker", "aws-actions", "./"}
    if owner in trusted or owner.startswith("./"):
        return False
    # SHA is 40 hex chars
    if re.fullmatch(r"[0-9a-f]{40}", ref):
        return False
    return True

scan("mutable-third-party-ref", third_party_mutable, "Medium")

# Dedup findings by fingerprint
seen = {}
for x in findings:
    key = x["fingerprint"]
    if key in seen:
        # merge — keep highest severity
        order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        if order[x["severity"]] > order[seen[key]["severity"]]:
            seen[key] = x
    else:
        seen[key] = x

out = list(seen.values())
out.sort(key=lambda x: ({"Critical": 0, "High": 1, "Medium": 2, "Low": 3}[x["severity"]], x["file"], x["line"] or 0))

with open(ROOT / "findings.json", "w") as f:
    json.dump(out, f, indent=2)

# summary counts
counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
by_source = {"zizmor": 0, "actionlint": 0, "hand-rolled": 0}
for x in out:
    counts[x["severity"]] += 1
    by_source[x["source"]] += 1

print(f"total={len(out)} crit={counts['Critical']} high={counts['High']} med={counts['Medium']} low={counts['Low']}")
print(f"by_source: zizmor={by_source['zizmor']} actionlint={by_source['actionlint']} hand-rolled={by_source['hand-rolled']}")
