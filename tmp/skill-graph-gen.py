#!/usr/bin/env python3
"""Generate skill-graph output for aeon."""
import json
import os
import re
import sys
import hashlib
import subprocess
from pathlib import Path

REPO = Path("/home/runner/work/aeon/aeon")
TODAY = os.environ.get("TODAY", "2026-09-27")
OUTPUT = Path(os.environ.get("OUTPUT_PATH", REPO / "docs" / "skill-graph.md"))
STATE_FILE = REPO / "memory" / "topics" / "skill-graph-state.json"
LOG_FILE = REPO / "memory" / "logs" / f"{TODAY}.md"

# Parse aeon.yml (simple regex-based since it uses inline objects that PyYAML handles fine)
import yaml
aeon_yml = yaml.safe_load((REPO / "aeon.yml").read_text())
skills_yml = aeon_yml.get("skills", {}) or {}
reactive = aeon_yml.get("reactive", {}) or {}
chains = aeon_yml.get("chains", {}) or {}

# skills.json
skills_json = json.loads((REPO / "skills.json").read_text())
category_map = {s["slug"]: s.get("category", "productivity") for s in skills_json.get("skills", [])}
categories_meta = skills_json.get("categories", {})

# Collect all skills (from disk + aeon.yml)
skill_dirs = sorted([p.name for p in (REPO / "skills").iterdir() if p.is_dir()])
skill_yml_names = list(skills_yml.keys())
all_skills = sorted(set(skill_dirs) | set(skill_yml_names))

# Read frontmatter from each skill
def parse_frontmatter(path):
    if not path.exists():
        return {}, ""
    text = path.read_text()
    m = re.match(r"^---\s*\n(.*?\n)---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception:
        fm = {}
    return fm, m.group(2)

skill_meta = {}
for s in all_skills:
    p = REPO / "skills" / s / "SKILL.md"
    fm, body = parse_frontmatter(p)
    skill_meta[s] = {"frontmatter": fm, "body": body, "exists": p.exists()}

# Categorize using skills.json first, then frontmatter tags, else productivity
VALID_CATS = ["research", "dev", "crypto", "social", "productivity"]
CATEGORY_KEYWORDS = {
    "research": ["research", "article", "paper", "content", "note", "memory", "digest", "brief", "explainer"],
    "dev": ["dev", "code", "repo", "workflow", "ci", "pr", "review", "issue", "build", "release", "vuln", "security", "fork", "skill", "meta"],
    "crypto": ["crypto", "chain", "defi", "token", "polymarket", "kalshi", "runpod", "compute", "rwa", "market", "trading", "x402", "wallet"],
    "social": ["social", "tweet", "farcaster", "telegram", "channel", "reddit", "hacker", "discord", "engage", "reply", "remix"],
    "productivity": ["productivity", "meta", "plan", "goal", "reflect", "recap", "review", "self", "flow", "note", "milestone", "idea", "tool", "onboard", "cost", "gallery", "campaign", "deploy", "spawn", "ads", "launch"],
}

def categorize(slug):
    cat = category_map.get(slug)
    if cat and cat in VALID_CATS:
        return cat
    fm = skill_meta.get(slug, {}).get("frontmatter", {})
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    for tag in tags:
        if tag in VALID_CATS:
            return tag
    for tag in tags:
        for cat, kws in CATEGORY_KEYWORDS.items():
            if any(k in tag.lower() for k in kws):
                return cat
    # keyword fallback on slug
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in slug.lower() for k in kws):
            return cat
    return "productivity"

skill_category = {s: categorize(s) for s in all_skills}

# Explicit edges: depends_on from frontmatter
depends_on = []  # (a, b) means a --> b (a depends on b)
for s in all_skills:
    fm = skill_meta[s]["frontmatter"]
    deps = fm.get("depends_on") or []
    if isinstance(deps, str):
        deps = [deps]
    for d in deps:
        if d in all_skills:
            depends_on.append((s, d))

# chains: parse consume: injections
consume_edges = []  # (target, source) — target consumes source
for chain_name, chain in (chains or {}).items():
    steps = (chain or {}).get("steps") or []
    for step in steps:
        if not isinstance(step, dict):
            continue
        if "skill" in step:
            target = step["skill"]
            for src in step.get("consume", []) or []:
                if src in all_skills and target in all_skills:
                    consume_edges.append((target, src))

# reactive: trigger blocks
reactive_edges = []  # (skill, "*", "condition")
for sk, block in (reactive or {}).items():
    triggers = (block or {}).get("trigger") or []
    for t in triggers:
        if not isinstance(t, dict):
            continue
        on = t.get("on", "*")
        when = t.get("when", "")
        reactive_edges.append((sk, on, when))

# Derived shared-state edges: writers -> readers over memory/topics or memory/state
# For each skill, list writes and reads to memory/(topics|state)/X
writes = {}  # skill -> set of paths
reads = {}   # skill -> set of paths
articles_writers = set()
for s in all_skills:
    body = skill_meta[s]["body"]
    if not body:
        continue
    lines = body.split("\n")
    for i, line in enumerate(lines):
        for m in re.finditer(r"memory/(topics|state)/[a-zA-Z0-9_./-]+", line):
            path = m.group(0).rstrip(".,;:)")
            ctx = " ".join(lines[max(0, i-1):i+2]).lower()
            is_write = bool(re.search(r"\b(write|save|append|update|writes?|writing|commit|persist)\b.*(topics|state)/", ctx)) or "> " + path in ctx
            if is_write:
                writes.setdefault(s, set()).add(path)
            else:
                reads.setdefault(s, set()).add(path)
    # articles/ writer detection — require explicit write verb near articles/
    if re.search(r"\b(write|save|append|commit|create|generate|persist|publish)\b[^\n]{0,80}articles/", body, re.IGNORECASE):
        articles_writers.add(s)

# Build shared-state edges: writer W of P -> reader R of P where W != R
shared_state_edges = set()
for w, wpaths in writes.items():
    for r, rpaths in reads.items():
        if w == r:
            continue
        common = wpaths & rpaths
        if common:
            shared_state_edges.add((w, r, sorted(common)[0]))

# content-pipeline edges: writers of articles/ -> distributors
content_targets = ["syndicate-article", "rss-feed", "update-gallery"]
content_edges = []
for w in articles_writers:
    if w in content_targets:
        continue  # skip self-loops
    for tgt in content_targets:
        if tgt in all_skills and tgt != w:
            content_edges.append((w, tgt))

# Enabled state
enabled = {s: bool((skills_yml.get(s) or {}).get("enabled")) for s in all_skills}
schedule = {s: (skills_yml.get(s) or {}).get("schedule", "") for s in all_skills}

# Fingerprint
def compute_fingerprint():
    h = hashlib.sha1()
    for f in ["aeon.yml", "skills.json"]:
        h.update(hashlib.sha1((REPO / f).read_bytes()).hexdigest().encode())
    frontmatter_lines = []
    for s in sorted(all_skills):
        fm = skill_meta[s]["frontmatter"]
        frontmatter_lines.append(f"{s}: {json.dumps(fm, sort_keys=True, default=str)}")
        body = skill_meta[s]["body"]
        for line in (body or "").split("\n"):
            if re.match(r"^(depends_on:|- skill:|consume:|parallel:|trigger:)", line):
                frontmatter_lines.append(f"{s}: {line}")
        refs = sorted(set(re.findall(r"memory/(?:topics|state)/[a-zA-Z0-9_.-]+", body or "")))
        for ref in refs:
            frontmatter_lines.append(f"{s}: {ref}")
    combined = "\n".join(frontmatter_lines).encode()
    h.update(hashlib.sha1(combined).hexdigest().encode())
    return h.hexdigest()

fingerprint = compute_fingerprint()

# Check state file
mode = "SKILL_GRAPH_NEW"
prior_fingerprint = None
if STATE_FILE.exists():
    try:
        prior = json.loads(STATE_FILE.read_text())
        prior_fingerprint = prior.get("input_fingerprint")
        if prior_fingerprint == fingerprint:
            mode = "SKILL_GRAPH_NO_CHANGE"
        else:
            mode = "SKILL_GRAPH_OK"
    except Exception:
        mode = "SKILL_GRAPH_OK"

if mode == "SKILL_GRAPH_NO_CHANGE":
    log_entry = f"\n## skill-graph\nSKILL_GRAPH_NO_CHANGE — {len(all_skills)} skills, identical fingerprint\n"
    if LOG_FILE.exists():
        LOG_FILE.write_text(LOG_FILE.read_text() + log_entry)
    else:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOG_FILE.write_text(f"# Log for {TODAY}\n{log_entry}")
    print("MODE=SKILL_GRAPH_NO_CHANGE")
    sys.exit(0)

# Diff vs prior docs/skill-graph.md
prior_nodes = set()
prior_edges = set()
if OUTPUT.exists():
    prior_text = OUTPUT.read_text()
    prior_nodes = set(re.findall(r"click ([a-z0-9_-]+) \"", prior_text))
    for m in re.finditer(r"([a-z0-9_-]+)\s*(-->|-\.->|-\.\.->)\s*([a-z0-9_-]+)", prior_text):
        prior_edges.add((m.group(1), m.group(2), m.group(3)))

# Current node/edge sets for diff
current_nodes = set(all_skills)
current_edges = set()
for (a, b) in depends_on:
    current_edges.add((a, "-->", b))
for (a, b) in consume_edges:
    current_edges.add((a, "-.->", b))
# reactive edges are metadata (skill-level trigger), not graph edges — recorded separately
for (w, r, p) in shared_state_edges:
    current_edges.add((w, "-..->", r))
for (w, tgt) in content_edges:
    current_edges.add((w, "-->", tgt))

added_nodes = current_nodes - prior_nodes
removed_nodes = prior_nodes - current_nodes
added_edges = current_edges - prior_edges
removed_edges = prior_edges - current_edges

# Determine verdict
if not OUTPUT.exists() or mode == "SKILL_GRAPH_NEW":
    verdict = f"SKILL_GRAPH_NEW — {len(all_skills)} skills mapped across 5 categories"
elif added_nodes:
    verdict = f"NEW_SKILLS: {', '.join(sorted(added_nodes)[:5])}"
elif removed_nodes:
    verdict = f"RETIRED_SKILLS: {', '.join(sorted(removed_nodes)[:5])}"
elif added_edges:
    sample = list(sorted(added_edges))[:3]
    verdict = "NEW_DEPS: " + ", ".join(f"{a}→{b}" for (a, _, b) in sample)
else:
    verdict = "ARCHITECTURE_OK"

# Lint: build set of nodes we'll declare, then check edges/clicks
# We'll declare every skill in the appropriate subgraph.
declared_nodes = set(all_skills)

# Group by category
by_category = {c: [] for c in VALID_CATS}
for s in all_skills:
    by_category.setdefault(skill_category[s], []).append(s)
for c in by_category:
    by_category[c].sort()

# Cross-category edges (for overview)
cross_edges = []  # (src_cat, tgt_cat, count)
cross_count = {}
# also intra-category edges for per-category diagrams
intra_edges = {c: [] for c in VALID_CATS}
all_edge_records = []  # (a, kind, b) — kind is one of '-->' '-.->' '-..->'
for (a, b) in depends_on:
    all_edge_records.append((a, "-->", b, "depends_on"))
for (a, b) in consume_edges:
    all_edge_records.append((a, "-.->", b, "consume"))
for (w, r, p) in shared_state_edges:
    all_edge_records.append((w, "-..->", r, "shared_state"))
for (w, tgt) in content_edges:
    all_edge_records.append((w, "-->", tgt, "depends_on"))
# reactive: emit as -.-> from trigger skill to "any-skill" abstract? Use a state node.

# Classify each edge as intra or cross
for (a, kind, b, etype) in all_edge_records:
    ca = skill_category.get(a, "productivity")
    cb = skill_category.get(b, "productivity")
    if ca == cb:
        intra_edges[ca].append((a, kind, b, etype))
    else:
        cross_count[(ca, cb, kind)] = cross_count.get((ca, cb, kind), 0) + 1

# Counters for the summary
depends_count = len(depends_on) + len(content_edges)
consume_count = len(consume_edges)
reactive_count = len(reactive_edges)
shared_state_count = len(shared_state_edges)
enabled_count = sum(1 for s in all_skills if enabled[s])
total = len(all_skills)

# Category totals
cat_counts = {c: len(by_category.get(c, [])) for c in VALID_CATS}
enabled_by_cat = {c: sum(1 for s in by_category.get(c, []) if enabled[s]) for c in VALID_CATS}

# Category labels
CAT_LABEL = {
    "research": "Research & Content",
    "dev": "Dev & Code",
    "crypto": "Crypto & Markets",
    "social": "Social",
    "productivity": "Productivity & Meta",
}

def node_label(s):
    sched = schedule.get(s, "")
    if enabled[s] and sched:
        return f"{s}<br/>{sched}" if sched != "reactive" else f"{s}<br/>reactive"
    return s

def escape_label(s):
    return s.replace('"', "'")

# Lint pass
lint_errors = []
# Every node used in an edge must be declared
for (a, kind, b, etype) in all_edge_records:
    if a not in declared_nodes:
        lint_errors.append(f"undeclared node in edge: {a}")
    if b not in declared_nodes:
        lint_errors.append(f"undeclared node in edge: {b}")
# Every click path must exist on disk
for s in all_skills:
    if not (REPO / "skills" / s / "SKILL.md").exists():
        # ok — we'll only emit clicks for skills that exist
        pass

if lint_errors:
    mode = "SKILL_GRAPH_ERROR"
    for err in lint_errors[:10]:
        print("LINT_ERR:", err, file=sys.stderr)

# Generate the document
lines = []
lines.append("# Skill Dependency Graph")
lines.append("")
lines.append(f"_Auto-generated by skill-graph on {TODAY}_")
lines.append("")
lines.append(f"**Mode:** `{mode}` · **Verdict:** {verdict}")
lines.append("")

# What changed
if mode != "SKILL_GRAPH_NEW":
    lines.append("## What changed since last run")
    lines.append("")
    if not added_nodes and not removed_nodes and not added_edges and not removed_edges:
        lines.append("_No structural change (edges + nodes stable). Enabled-state and schedule annotations may still be refreshed._")
    else:
        if added_nodes:
            lines.append(f"- **Added skills** ({len(added_nodes)}): {', '.join(sorted(added_nodes))}")
        if removed_nodes:
            lines.append(f"- **Removed skills** ({len(removed_nodes)}): {', '.join(sorted(removed_nodes))}")
        if added_edges:
            lines.append(f"- **Added edges** ({len(added_edges)}):")
            for (a, k, b) in sorted(added_edges):
                lines.append(f"  - `{a} {k} {b}`")
        if removed_edges:
            lines.append(f"- **Removed edges** ({len(removed_edges)}):")
            for (a, k, b) in sorted(removed_edges):
                lines.append(f"  - `{a} {k} {b}`")
    lines.append("")

# Overview diagram
lines.append("## Overview")
lines.append("")
lines.append("Cross-category dependency map. Each category is a subgraph box; edge labels are the count of dependencies crossing that boundary.")
lines.append("")
lines.append("```mermaid")
lines.append("flowchart LR")
for c in VALID_CATS:
    lines.append(f"  subgraph {c}[\"{CAT_LABEL[c]} ({cat_counts[c]})\"]")
    lines.append(f"    {c}_hub[\"{cat_counts[c]} skills<br/>{enabled_by_cat[c]} enabled\"]")
    lines.append("  end")
# Cross-category edges with counts
for ((ca, cb, kind), n) in sorted(cross_count.items()):
    lines.append(f"  {ca}_hub {kind}|{n}| {cb}_hub")
lines.append("```")
lines.append("")

# Self-healing loop
lines.append("## Self-healing loop")
lines.append("")
lines.append("Every skill writes to `memory/cron-state.json`; the health/repair pipeline reads it. This shared-state node stands in for ~N edges the graph would otherwise carry to `heartbeat`, `skill-health`, and `skill-repair`.")
lines.append("")
lines.append("```mermaid")
lines.append("flowchart LR")
lines.append("  cron_state[(memory/cron-state.json)]")
lines.append("  heartbeat --> skill-health")
lines.append("  skill-health --> skill-evals")
lines.append("  skill-evals --> skill-repair")
lines.append("  skill-repair --> self-improve")
lines.append("  cron_state -.-> heartbeat")
lines.append("  cron_state -.-> skill-health")
lines.append("  cron_state -.-> skill-repair")
loop_nodes = ["heartbeat", "skill-health", "skill-evals", "skill-repair", "self-improve"]
for n in loop_nodes:
    if (REPO / "skills" / n / "SKILL.md").exists():
        lines.append(f"  click {n} \"../skills/{n}/SKILL.md\"")
    cls = "enabled" if enabled.get(n) else "disabled"
    lines.append(f"  class {n} {cls}")
lines.append("  classDef enabled fill:#fff,stroke:#000,stroke-width:2px,color:#000")
lines.append("  classDef disabled fill:#f5f5f5,stroke:#bbb,color:#888")
lines.append("```")
lines.append("")

# Per-category diagrams
lines.append("## Per-category detail")
lines.append("")
for c in VALID_CATS:
    skills_in_cat = by_category.get(c, [])
    if not skills_in_cat:
        continue
    lines.append(f"### {CAT_LABEL[c]}")
    lines.append("")
    lines.append(f"_{cat_counts[c]} skills · {enabled_by_cat[c]} enabled_")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    # Declare nodes
    for s in skills_in_cat:
        label = escape_label(node_label(s))
        lines.append(f"  {s}[\"{label}\"]")
    # intra-category edges
    for (a, kind, b, etype) in intra_edges[c]:
        lines.append(f"  {a} {kind} {b}")
    # Cross-category (as ghost nodes)
    ghost_targets = {}
    for (a, kind, b, etype) in all_edge_records:
        if a in skills_in_cat and skill_category.get(b) != c:
            ghost_targets.setdefault(b, []).append((a, kind, etype))
        if b in skills_in_cat and skill_category.get(a) != c:
            ghost_targets.setdefault(a, []).append((None, kind, etype))
    if ghost_targets:
        lines.append(f"  subgraph external[\"external\"]")
        for ext in sorted(ghost_targets.keys()):
            lines.append(f"    ext_{ext}[\"{ext}\"]:::external")
        lines.append("  end")
        for ext, refs in sorted(ghost_targets.items()):
            for (a, kind, etype) in refs:
                if a is None:
                    # incoming: external -> nothing rendered (avoid double)
                    continue
                lines.append(f"  {a} {kind} ext_{ext}")
    # Clicks + classes
    for s in skills_in_cat:
        if (REPO / "skills" / s / "SKILL.md").exists():
            lines.append(f"  click {s} \"../skills/{s}/SKILL.md\"")
        cls = "enabled" if enabled[s] else "disabled"
        lines.append(f"  class {s} {cls}")
    lines.append("  classDef enabled fill:#fff,stroke:#000,stroke-width:2px,color:#000")
    lines.append("  classDef disabled fill:#f5f5f5,stroke:#bbb,color:#888")
    lines.append("  classDef external fill:none,stroke:#bbb,stroke-dasharray:3 3,color:#888")
    lines.append("```")
    lines.append("")

# Legend
lines.append("## Legend")
lines.append("")
lines.append("- `A --> B` — A depends on B (explicit `depends_on:` or content pipeline)")
lines.append("- `A -.-> B` — A consumes B (chain injection) or reactive trigger")
lines.append("- `A -..-> B` — A and B share state (writer→reader over `memory/topics/*` or `memory/state/*`)")
lines.append("- **Bold border** — skill is `enabled: true` in `aeon.yml`; schedule shown in node label")
lines.append("- **Faded grey** — skill is disabled (present but not scheduled)")
lines.append("- **Dashed border** — external ghost node (skill lives in another category)")
lines.append("- Click any node to open its `SKILL.md`")
lines.append("")
lines.append("**Collapsed edge:** every enabled skill writes `memory/cron-state.json` on completion. Rather than drawing ~90 edges into `skill-health`/`skill-repair`/`heartbeat`, the self-healing loop diagram represents it as a single shared-state node.")
lines.append("")

# Summary table
lines.append("## Summary")
lines.append("")
lines.append("| Metric | Value |")
lines.append("| --- | --- |")
lines.append(f"| Total skills | {total} |")
lines.append(f"| Enabled | {enabled_count} |")
lines.append(f"| Disabled | {total - enabled_count} |")
for c in VALID_CATS:
    lines.append(f"| {CAT_LABEL[c]} | {cat_counts[c]} ({enabled_by_cat[c]} enabled) |")
lines.append(f"| Edges `-->` (depends_on) | {depends_count} |")
lines.append(f"| Edges `-.->` (consume) | {consume_count} |")
lines.append(f"| Reactive triggers | {reactive_count} |")
lines.append(f"| Shared-state edges | {shared_state_count} |")
lines.append("")

# Footer
footer = f"skills parsed: {total} · depends_on: {depends_count} · consume: {consume_count} · reactive: {reactive_count} · shared-state derived: {shared_state_count} · enabled: {enabled_count}/{total} · mode: {mode}"
lines.append(f"---")
lines.append(f"")
lines.append(f"_{footer}_")
lines.append("")

# Write output
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines))
print(f"WROTE: {OUTPUT}")

# Update README idempotently
readme = REPO / "README.md"
if readme.exists():
    readme_text = readme.read_text()
    if "docs/skill-graph.md" not in readme_text:
        # Try to insert under a "## Skills" header
        m = re.search(r"^(## Skills.*?)$", readme_text, re.MULTILINE)
        insert_line = "\n- [Skill dependency graph](docs/skill-graph.md) — auto-generated Mermaid map of all skills.\n"
        if m:
            idx = m.end()
            readme_text = readme_text[:idx] + insert_line + readme_text[idx:]
        else:
            readme_text = readme_text.rstrip() + "\n" + insert_line
        readme.write_text(readme_text)
        print("UPDATED README")
    else:
        print("README already references docs/skill-graph.md — skipped")

# Persist state
node_list_sha = hashlib.sha1("\n".join(sorted(all_skills)).encode()).hexdigest()
edge_tuples = sorted(f"{a}|{k}|{b}" for (a, k, b) in current_edges)
edge_list_sha = hashlib.sha1("\n".join(edge_tuples).encode()).hexdigest()
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
STATE_FILE.write_text(json.dumps({
    "generated_at": TODAY,
    "input_fingerprint": fingerprint,
    "skills_total": total,
    "enabled_count": enabled_count,
    "edges": {
        "depends_on": depends_count,
        "consume": consume_count,
        "reactive": reactive_count,
        "shared_state": shared_state_count,
    },
    "node_list_sha": node_list_sha,
    "edge_list_sha": edge_list_sha,
}, indent=2))
print(f"WROTE STATE: {STATE_FILE}")

# Log entry
log_entry_lines = [
    "",
    "### skill-graph",
    f"- Mode: {mode}",
    f"- Verdict: {verdict}",
    f"- Skills: {total} (enabled: {enabled_count})",
    f"- Edges: depends_on={depends_count}, consume={consume_count}, reactive={reactive_count}, shared_state={shared_state_count}",
    f"- PR: pending",
    f"- Source-status: {footer}",
]
log_entry = "\n".join(log_entry_lines) + "\n"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
if LOG_FILE.exists():
    LOG_FILE.write_text(LOG_FILE.read_text() + log_entry)
else:
    LOG_FILE.write_text(f"# Log for {TODAY}\n{log_entry}")
print(f"LOGGED: {LOG_FILE}")

# Persist metadata for downstream (verdict/mode)
(REPO / "tmp" / "skill-graph-meta.json").write_text(json.dumps({
    "mode": mode,
    "verdict_one_line": verdict,
    "total": total,
    "enabled": enabled_count,
    "depends_on": depends_count,
    "consume": consume_count,
    "reactive": reactive_count,
    "shared_state": shared_state_count,
    "footer": footer,
    "added_nodes": sorted(added_nodes),
    "removed_nodes": sorted(removed_nodes),
    "added_edges": [list(e) for e in sorted(added_edges)],
    "removed_edges": [list(e) for e in sorted(removed_edges)],
}, indent=2))
print("META WRITTEN")
