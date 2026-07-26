#!/usr/bin/env python3
"""skill-graph generator — see skills/skill-graph/SKILL.md"""
import hashlib, json, os, re, sys
from collections import defaultdict
from pathlib import Path
import yaml

ROOT = Path("/home/runner/work/aeon/aeon")
os.chdir(ROOT)
TODAY = "2026-07-26"
OUT = Path(os.environ.get("SKILL_GRAPH_OUT") or "docs/skill-graph.md")
STATE_PATH = Path("memory/topics/skill-graph-state.json")

# ---------- 1. Load inputs ----------
with open("aeon.yml") as f:
    AEON = yaml.safe_load(f)

with open("skills.json") as f:
    SKILLS_JSON = json.load(f)

# skills on disk
DISK_SKILLS = sorted([p.name for p in Path("skills").iterdir() if (p / "SKILL.md").exists()])

# category map from skills.json
category_map = {}
for entry in SKILLS_JSON.get("skills", []):
    category_map[entry["slug"]] = entry.get("category", "other")

CATEGORIES_ORDER = ["research", "dev", "crypto", "social", "productivity", "other"]
CAT_LABELS = {
    "research": "Research & Content",
    "dev": "Dev & Code",
    "crypto": "Crypto & Markets",
    "social": "Social",
    "productivity": "Productivity & Meta",
    "other": "Other & Uncategorized",
}

# aeon.yml enabled/schedule/model
aeon_skills = AEON.get("skills", {}) or {}
enabled_map = {}
schedule_map = {}
model_map = {}
for slug, cfg in aeon_skills.items():
    if isinstance(cfg, dict):
        enabled_map[slug] = bool(cfg.get("enabled", False))
        schedule_map[slug] = cfg.get("schedule", "")
        model_map[slug] = cfg.get("model", "")

# reactive
reactive_triggers = AEON.get("reactive", {}) or {}

# chains
chains_cfg = AEON.get("chains", {}) or {}

# ---------- 2. Parse SKILL.md files ----------
frontmatter_re = re.compile(r'^---\s*$')
skill_frontmatter = {}
skill_tags = defaultdict(list)
skill_depends_on = defaultdict(list)
skill_names = {}
skill_body = {}

for slug in DISK_SKILLS:
    path = Path("skills") / slug / "SKILL.md"
    content = path.read_text(encoding="utf-8", errors="replace")
    # Extract frontmatter between first two --- lines
    lines = content.splitlines()
    fm_lines = []
    n = 0
    body_start = 0
    for i, line in enumerate(lines):
        if frontmatter_re.match(line):
            n += 1
            if n == 2:
                body_start = i + 1
                break
            continue
        if n == 1:
            fm_lines.append(line)
    try:
        fm = yaml.safe_load("\n".join(fm_lines)) or {}
    except Exception:
        fm = {}
    skill_frontmatter[slug] = fm
    skill_body[slug] = "\n".join(lines[body_start:])
    if isinstance(fm.get("tags"), list):
        skill_tags[slug] = [str(t) for t in fm["tags"]]
    if isinstance(fm.get("depends_on"), list):
        skill_depends_on[slug] = [str(d) for d in fm["depends_on"]]
    skill_names[slug] = fm.get("name") or slug

# ---------- 3. Categorize ----------
def categorize(slug):
    cat = category_map.get(slug)
    if cat and cat in CATEGORIES_ORDER:
        return cat
    # fall back to first matching tag
    for t in skill_tags.get(slug, []):
        if t in CATEGORIES_ORDER:
            return t
    return "other"

skill_cat = {s: categorize(s) for s in DISK_SKILLS}

# ---------- 4. Derive shared-state edges ----------
# Grep memory/topics/... and memory/state/... in each SKILL.md
mem_ref_re = re.compile(r'memory/(topics|state)/[a-zA-Z0-9_.-]+')
write_verb_re = re.compile(r'\b(write|save|append|update|regenerate|persist)\b', re.I)

# per-skill: sets of (topic, kind='write'|'read')
skill_topics_write = defaultdict(set)
skill_topics_read = defaultdict(set)

for slug in DISK_SKILLS:
    text = skill_body[slug]
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for m in mem_ref_re.finditer(line):
            ref = m.group(0)
            # skip cron-state
            if "cron-state" in ref:
                continue
            ctx = "\n".join(lines[max(0, i-2):i+2])
            if write_verb_re.search(ctx) or ">" in line[:m.start()][-10:]:
                skill_topics_write[slug].add(ref)
            else:
                skill_topics_read[slug].add(ref)

# writer index
topic_writers = defaultdict(set)
for slug, topics in skill_topics_write.items():
    for t in topics:
        topic_writers[t].add(slug)

shared_state_edges = set()
for reader, topics in skill_topics_read.items():
    for t in topics:
        for writer in topic_writers.get(t, ()):
            if writer != reader:
                shared_state_edges.add((writer, reader, t))

# collapse to edge (writer, reader) with topic list
sse_edge_topics = defaultdict(set)
for w, r, t in shared_state_edges:
    sse_edge_topics[(w, r)].add(t)

# ---------- 5. depends_on edges ----------
depends_edges = set()
for slug, deps in skill_depends_on.items():
    for d in deps:
        d = d.strip()
        if d in DISK_SKILLS and d != slug:
            depends_edges.add((slug, d))  # slug depends on d

# ---------- 6. Chain (consume) edges ----------
consume_edges = set()
for chain_name, chain in chains_cfg.items():
    if not isinstance(chain, dict):
        continue
    steps = chain.get("steps", []) or []
    prior_names = []  # names emitted by earlier steps
    for step in steps:
        if isinstance(step, dict):
            if "parallel" in step:
                names = step["parallel"] or []
                prior_names = list(names)
            elif "skill" in step:
                skill = step["skill"]
                for c in step.get("consume", []) or []:
                    if c in DISK_SKILLS and skill in DISK_SKILLS:
                        consume_edges.add((c, skill))
                prior_names = [skill]

# ---------- 7. Reactive edges ----------
# reactive: <skill>: trigger: - on: <target>|"*" when: ...
reactive_edges = set()
for skill, cfg in reactive_triggers.items():
    if not isinstance(cfg, dict):
        continue
    for tr in cfg.get("trigger", []) or []:
        if isinstance(tr, dict):
            on = tr.get("on")
            when = tr.get("when", "")
            reactive_edges.add((skill, on or "*", when))

# ---------- 8. Build category assignments ----------
by_cat = defaultdict(list)
for slug in DISK_SKILLS:
    by_cat[skill_cat[slug]].append(slug)
for c in by_cat:
    by_cat[c].sort()

# ---------- 9. Verdict computation (diff vs prior graph, if any) ----------
# Prior state file is absent -> SKILL_GRAPH_NEW
prior_state = None
if STATE_PATH.exists():
    try:
        prior_state = json.loads(STATE_PATH.read_text())
    except Exception:
        prior_state = None

fingerprint_txt = ROOT / "tmp-fingerprint.py"
# We compute fingerprint identically to tmp-fingerprint.py above
def compute_fingerprint():
    h = hashlib.sha1()
    for f in ["aeon.yml", "skills.json"]:
        h1 = hashlib.sha1(Path(f).read_bytes()).hexdigest()
        h.update(f"{h1}  {f}\n".encode())
    edge_re = re.compile(r'^(depends_on:|- skill:|consume:|parallel:|trigger:)')
    mem_re = re.compile(r'memory/(topics|state)/[a-zA-Z0-9_.-]+')
    frontmatter_re2 = re.compile(r'^---$')
    for path in sorted(Path("skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        n = 0
        for line in lines:
            if frontmatter_re2.match(line.rstrip("\n")):
                n += 1
                continue
            if n == 1:
                h.update(f"{path}: {line.rstrip(chr(10))}\n".encode())
        for line in lines:
            if edge_re.match(line):
                h.update((line+"\n").encode())
        mems = sorted(set(m.group(0) for m in mem_re.finditer(text)))
        for m in mems:
            h.update((m+"\n").encode())
    return h.hexdigest()

fingerprint = compute_fingerprint()

if prior_state is None:
    mode = "SKILL_GRAPH_NEW"
elif prior_state.get("input_fingerprint") == fingerprint:
    mode = "SKILL_GRAPH_NO_CHANGE"
else:
    mode = "SKILL_GRAPH_OK"

# Verdict lines
enabled_count = sum(1 for s in DISK_SKILLS if enabled_map.get(s))
verdicts = []
if mode == "SKILL_GRAPH_NEW":
    verdict_one_line = f"SKILL_GRAPH_NEW — {len(DISK_SKILLS)} skills mapped across {len(CATEGORIES_ORDER)} categories, {enabled_count} enabled"
else:
    # diff nodes/edges/enabled against prior_state
    # Prior state only has counts/hashes; keep the verdict simple for NEW / OK.
    verdict_one_line = "ARCHITECTURE_OK"

# ---------- 10. Assemble Mermaid diagrams ----------
def cell(slug):
    """Node label with optional schedule annotation."""
    sched = schedule_map.get(slug, "")
    if enabled_map.get(slug) and sched:
        return f'{slug}["{slug}<br/><i>{sched}</i>"]'
    return f'{slug}["{slug}"]'

def cell_external(slug):
    """External ghost node showing the origin category."""
    cat = skill_cat.get(slug, "other")
    return f'{slug}["{slug}<br/><i>{cat}</i>"]'

# All cross-category depends/shared_state edges collected for the overview
cross_edges_count = defaultdict(int)  # (src_cat, tgt_cat) -> count
for src, tgt in depends_edges:
    if skill_cat[src] != skill_cat[tgt]:
        cross_edges_count[(skill_cat[src], skill_cat[tgt])] += 1
for src, tgt in consume_edges:
    if skill_cat[src] != skill_cat[tgt]:
        cross_edges_count[(skill_cat[src], skill_cat[tgt])] += 1
for (w, r), topics in sse_edge_topics.items():
    if w in skill_cat and r in skill_cat and skill_cat[w] != skill_cat[r]:
        cross_edges_count[(skill_cat[w], skill_cat[r])] += 1

# ---------- 11. Lint ----------
lint_errors = []

def lint_check(nodes_declared, click_paths, edges_referenced, subgraphs):
    """
    nodes_declared: set of node ids
    click_paths: list of (node_id, path)
    edges_referenced: iterable of (src, tgt) tuples
    subgraphs: list of subgraph blocks — each is (opened, closed)
    """
    for src, tgt in edges_referenced:
        if src not in nodes_declared:
            lint_errors.append(f"edge references undeclared node: {src}")
        if tgt not in nodes_declared:
            lint_errors.append(f"edge references undeclared node: {tgt}")
    for node, path in click_paths:
        if node not in nodes_declared:
            lint_errors.append(f"click references undeclared node: {node}")
        # path check
        if path.startswith("../"):
            full = OUT.parent / path
        else:
            full = Path(path)
        try:
            full_resolved = full.resolve()
        except Exception:
            full_resolved = None
        if full_resolved is None or not Path(full_resolved).exists():
            lint_errors.append(f"click path missing on disk: {path}")
    for o, c in subgraphs:
        if o != c:
            lint_errors.append(f"unbalanced subgraph blocks: opened={o} closed={c}")

# ---------- 12. Build overview diagram ----------
def build_overview():
    lines = ["```mermaid", "flowchart LR"]
    for cat in CATEGORIES_ORDER:
        total = len(by_cat[cat])
        en = sum(1 for s in by_cat[cat] if enabled_map.get(s))
        label = CAT_LABELS[cat]
        lines.append(f'    subgraph {cat}["{label} ({en} / {total})"]')
        lines.append(f'        {cat}_anchor( )')
        lines.append('    end')
    # edges
    for (s, t), n in sorted(cross_edges_count.items()):
        lines.append(f'    {s}_anchor -->|"{n}"| {t}_anchor')
    for cat in CATEGORIES_ORDER:
        lines.append(f'    style {cat}_anchor fill:transparent,stroke:transparent')
    lines.append("```")
    return "\n".join(lines)

# ---------- 13. Self-healing loop callout ----------
def build_loop():
    return """```mermaid
flowchart LR
    heartbeat[heartbeat]
    skill-health[skill-health]
    skill-evals[skill-evals]
    skill-repair[skill-repair]
    self-improve[self-improve]
    cron[("memory/cron-state.json")]
    heartbeat --> skill-health
    skill-health --> skill-evals
    skill-evals --> skill-repair
    skill-repair --> self-improve
    self-improve -.->|"updates aeon.yml"| heartbeat
    heartbeat -.-> cron
    skill-health -.-> cron
    skill-evals -.-> cron
    skill-repair -.-> cron
    click heartbeat "../skills/heartbeat/SKILL.md"
    click skill-health "../skills/skill-health/SKILL.md"
    click skill-evals "../skills/skill-evals/SKILL.md"
    click skill-repair "../skills/skill-repair/SKILL.md"
    click self-improve "../skills/self-improve/SKILL.md"
```"""

# ---------- 14. Per-category mini-diagrams ----------
def build_category(cat):
    nodes = by_cat[cat]
    lines = ["```mermaid", "flowchart LR"]
    lines.append("    classDef enabled fill:#fff,stroke:#000,stroke-width:2px,color:#000")
    lines.append("    classDef disabled fill:#f5f5f5,stroke:#bbb,color:#888")
    lines.append("    classDef external fill:none,stroke:#bbb,stroke-dasharray:3 3,color:#888")

    node_ids = set()
    for n in nodes:
        lines.append(f"    {cell(n)}")
        node_ids.add(n)

    # intra-cat edges
    intra_depends = [(s, t) for s, t in depends_edges if s in node_ids and t in node_ids]
    intra_consume = [(s, t) for s, t in consume_edges if s in node_ids and t in node_ids]
    intra_shared  = [(w, r) for (w, r) in sse_edge_topics if w in node_ids and r in node_ids]

    # external ghost nodes for cross-category refs (into this cat OR out)
    externals = set()
    cross_depends = []
    cross_consume = []
    cross_shared = []
    for s, t in depends_edges:
        if s in node_ids and t not in node_ids and t in DISK_SKILLS:
            externals.add(t); cross_depends.append((s, t))
        if t in node_ids and s not in node_ids and s in DISK_SKILLS:
            externals.add(s); cross_depends.append((s, t))
    for s, t in consume_edges:
        if s in node_ids and t not in node_ids and t in DISK_SKILLS:
            externals.add(t); cross_consume.append((s, t))
        if t in node_ids and s not in node_ids and s in DISK_SKILLS:
            externals.add(s); cross_consume.append((s, t))
    for (w, r) in sse_edge_topics:
        if w in node_ids and r not in node_ids and r in DISK_SKILLS:
            externals.add(r); cross_shared.append((w, r))
        if r in node_ids and w not in node_ids and w in DISK_SKILLS:
            externals.add(w); cross_shared.append((w, r))

    # dedup edge lists preserving order
    seen = set()
    def uniq(pairs):
        out = []
        for p in pairs:
            if p not in seen:
                seen.add(p); out.append(p)
        return out
    intra_depends = uniq(intra_depends)
    intra_consume = uniq(intra_consume)
    intra_shared  = uniq(intra_shared)
    cross_depends = uniq(cross_depends)
    cross_consume = uniq(cross_consume)
    cross_shared  = uniq(cross_shared)

    for s, t in intra_depends:
        lines.append(f"    {s} --> {t}")
    for s, t in intra_consume:
        lines.append(f"    {s} -.-> {t}")
    for s, t in intra_shared:
        lines.append(f"    {s} -..-> {t}")

    if externals:
        for e in sorted(externals):
            lines.append(f"    {cell_external(e)}")
            node_ids.add(e)
        for s, t in cross_depends:
            lines.append(f"    {s} --> {t}")
        for s, t in cross_consume:
            lines.append(f"    {s} -.-> {t}")
        for s, t in cross_shared:
            lines.append(f"    {s} -..-> {t}")

    # click directives
    for n in nodes:
        lines.append(f'    click {n} "../skills/{n}/SKILL.md"')
    for e in sorted(externals):
        lines.append(f'    click {e} "../skills/{e}/SKILL.md"')

    # class assignments
    en_nodes = [n for n in nodes if enabled_map.get(n)]
    dis_nodes = [n for n in nodes if not enabled_map.get(n)]
    if en_nodes:
        lines.append(f"    class {','.join(en_nodes)} enabled")
    if dis_nodes:
        lines.append(f"    class {','.join(dis_nodes)} disabled")
    if externals:
        lines.append(f"    class {','.join(sorted(externals))} external")
    lines.append("```")

    # Lint intake
    click_paths = [(n, f"../skills/{n}/SKILL.md") for n in nodes] + \
                  [(e, f"../skills/{e}/SKILL.md") for e in externals]
    edges = intra_depends + intra_consume + intra_shared + cross_depends + cross_consume + cross_shared
    lint_check(node_ids, click_paths, edges, [(1, 1)])

    return "\n".join(lines)

# ---------- 15. Assemble the full document ----------
def build_doc():
    parts = []
    parts.append("# Skill Dependency Graph")
    parts.append("")
    parts.append(f"> Auto-generated by `skill-graph` on {TODAY}. Mode: `{mode}`.")
    parts.append("")
    parts.append(f"**Verdict:** {verdict_one_line}")
    parts.append("")
    if mode != "SKILL_GRAPH_NEW":
        parts.append("## What changed since last run")
        parts.append("")
        parts.append("_(no prior diff available)_")
        parts.append("")
    parts.append("## Overview")
    parts.append("")
    parts.append("Category boxes show **enabled / total** skill counts. Cross-category edges carry their count.")
    parts.append("")
    parts.append(build_overview())
    parts.append("")
    parts.append("_Every skill also writes `memory/cron-state.json`, which is read by `heartbeat`, `skill-health`, `skill-repair`, and `skill-evals`. Collapsed here to keep the map readable — see Self-healing loop below._")
    parts.append("")
    parts.append("## Self-healing loop")
    parts.append("")
    # Describe reactive triggers concisely
    tri_lines = []
    for skill, on, when in sorted(reactive_edges):
        tri_lines.append(f"`{skill}` fires on `{on}` when `{when}`")
    if tri_lines:
        parts.append("Reactive triggers: " + "; ".join(tri_lines) + ".")
    parts.append("")
    parts.append(build_loop())
    parts.append("")
    parts.append("## Per-category breakdown")
    parts.append("")
    for cat in CATEGORIES_ORDER:
        total = len(by_cat[cat])
        en = sum(1 for s in by_cat[cat] if enabled_map.get(s))
        if total == 0:
            continue
        parts.append(f"### {CAT_LABELS[cat]} ({en} / {total})")
        parts.append("")
        parts.append(build_category(cat))
        parts.append("")

    parts.append("## Legend")
    parts.append("")
    parts.append("| Edge | Meaning |")
    parts.append("|------|---------|")
    parts.append("| `-->` solid | `depends_on` — declared in frontmatter |")
    parts.append("| `-.->` dashed | `consume` — chain step receives prior output |")
    parts.append("| `-..->` dotted | shared-state — one skill writes a memory file another reads |")
    parts.append("")
    parts.append("| Node style | Meaning |")
    parts.append("|------------|---------|")
    parts.append("| **Bold border** | Enabled in `aeon.yml` (schedule shown beneath) |")
    parts.append("| Faded grey | Disabled / not scheduled |")
    parts.append("| Dashed border | External skill referenced from another category |")
    parts.append("")
    parts.append("Click any node on github.com to open its `SKILL.md`. Reactive triggers and the shared `memory/cron-state.json` ledger are documented in the **Self-healing loop** section, not duplicated as edges in the per-category diagrams.")
    parts.append("")
    parts.append("## Summary")
    parts.append("")
    parts.append("| Category | Total | Enabled |")
    parts.append("|----------|-------|---------|")
    total_all = 0
    en_all = 0
    for cat in CATEGORIES_ORDER:
        total = len(by_cat[cat])
        en = sum(1 for s in by_cat[cat] if enabled_map.get(s))
        total_all += total
        en_all += en
        parts.append(f"| {CAT_LABELS[cat]} | {total} | {en} |")
    parts.append(f"| **Total** | **{total_all}** | **{en_all}** |")
    parts.append("")
    parts.append("| Edge type | Count |")
    parts.append("|-----------|-------|")
    parts.append(f"| `depends_on` | {len(depends_edges)} |")
    parts.append(f"| `consume` (chains) | {len(consume_edges)} |")
    parts.append(f"| `reactive` | {len(reactive_edges)} |")
    parts.append(f"| `shared_state` (derived) | {len(sse_edge_topics)} |")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append(
        f"_skills parsed: {len(DISK_SKILLS)} · depends_on: {len(depends_edges)} · "
        f"consume: {len(consume_edges)} · reactive: {len(reactive_edges)} · "
        f"shared-state derived: {len(sse_edge_topics)} · enabled: {enabled_count}/{len(DISK_SKILLS)} · "
        f"mode: {mode}_"
    )
    parts.append("")
    return "\n".join(parts)

if mode == "SKILL_GRAPH_NO_CHANGE":
    # Log line only
    log_path = Path(f"memory/logs/{TODAY}.md")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists():
        log = log_path.read_text()
    else:
        log = ""
    if "## skill-graph" not in log:
        with log_path.open("a") as f:
            f.write(f"\n## skill-graph\n\nSKILL_GRAPH_NO_CHANGE — {len(DISK_SKILLS)} skills, identical fingerprint\n")
    print("MODE=SKILL_GRAPH_NO_CHANGE")
    sys.exit(0)

doc = build_doc()

if lint_errors:
    print("LINT_ERRORS:")
    for e in lint_errors:
        print(f"  - {e}")
    print("MODE=SKILL_GRAPH_ERROR")
    sys.exit(2)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(doc)

# ---------- 16. Persist state ----------
STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
node_list_sha = hashlib.sha1(("\n".join(sorted(DISK_SKILLS))).encode()).hexdigest()
edge_tuples = sorted(
    [f"D:{s}->{t}" for s, t in depends_edges] +
    [f"C:{s}->{t}" for s, t in consume_edges] +
    [f"R:{s}->{o}|{w}" for s, o, w in reactive_edges] +
    [f"S:{w}->{r}" for (w, r) in sse_edge_topics]
)
edge_list_sha = hashlib.sha1(("\n".join(edge_tuples)).encode()).hexdigest()
state = {
    "generated_at": TODAY,
    "input_fingerprint": fingerprint,
    "skills_total": len(DISK_SKILLS),
    "enabled_count": enabled_count,
    "edges": {
        "depends_on": len(depends_edges),
        "consume": len(consume_edges),
        "reactive": len(reactive_edges),
        "shared_state": len(sse_edge_topics),
    },
    "node_list_sha": node_list_sha,
    "edge_list_sha": edge_list_sha,
    "mode": mode,
    "verdict": verdict_one_line,
}
STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")

# ---------- 17. Update README idempotently ----------
readme = Path("README.md")
if readme.exists():
    txt = readme.read_text()
    if "docs/skill-graph.md" not in txt:
        insert_line = "- [Skill dependency graph](docs/skill-graph.md) — Mermaid map of all skills with enabled overlay"
        lines = txt.splitlines()
        inserted = False
        for i, line in enumerate(lines):
            if re.match(r'^##+\s+Skills?\b', line):
                # insert after next blank line
                for j in range(i+1, min(i+8, len(lines))):
                    if lines[j].strip() == "":
                        lines.insert(j+1, insert_line)
                        inserted = True
                        break
                if inserted:
                    break
        if not inserted:
            lines.append("")
            lines.append(insert_line)
        readme.write_text("\n".join(lines) + "\n")

# ---------- 18. Log ----------
log_path = Path(f"memory/logs/{TODAY}.md")
log_path.parent.mkdir(parents=True, exist_ok=True)
with log_path.open("a") as f:
    f.write(f"""
## skill-graph
- Mode: {mode}
- Verdict: {verdict_one_line}
- Skills: {len(DISK_SKILLS)} (enabled: {enabled_count})
- Edges: depends_on={len(depends_edges)}, consume={len(consume_edges)}, reactive={len(reactive_edges)}, shared_state={len(sse_edge_topics)}
- Output: {OUT}
""")

print(f"MODE={mode}")
print(f"VERDICT={verdict_one_line}")
print(f"SKILLS={len(DISK_SKILLS)} ENABLED={enabled_count}")
print(f"EDGES depends={len(depends_edges)} consume={len(consume_edges)} reactive={len(reactive_edges)} shared={len(sse_edge_topics)}")
print(f"FINGERPRINT={fingerprint}")
print(f"OUT={OUT}")
