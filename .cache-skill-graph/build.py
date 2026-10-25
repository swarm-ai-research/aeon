#!/usr/bin/env python3
"""Build skill-graph: parse inputs, derive edges, emit docs/skill-graph.md + state."""
import glob
import hashlib
import json
import os
import re
import sys
from collections import defaultdict, Counter

ROOT = "/home/runner/work/aeon/aeon"
os.chdir(ROOT)

TODAY = "2026-10-25"
MODE_HINT = sys.argv[1] if len(sys.argv) > 1 else "SKILL_GRAPH_NEW"
INPUT_FP = sys.argv[2] if len(sys.argv) > 2 else "UNKNOWN"

# ------------- Load skills.json -----------------
with open("skills.json", "r", encoding="utf-8") as f:
    skills_json = json.load(f)
CATEGORIES = skills_json.get("categories", {})
CATEGORIES.setdefault("other", "Other & Uncategorized")
CATEGORY_ORDER = ["research", "dev", "crypto", "social", "productivity", "other"]
json_cat = {s["slug"]: s["category"] for s in skills_json["skills"]}

# ------------- Parse aeon.yml -----------------
with open("aeon.yml", "r", encoding="utf-8") as f:
    aeon_text = f.read()

# Find the skills: section (top-level) and parse per-skill blocks
# Flat form: `  slug: { enabled: ..., schedule: "..." }`
# Nested form:
#   slug:
#     enabled: true
#     schedule: "..."
# We'll scan line-by-line within the top-level `skills:` block.
enabled_map = {}
schedule_map = {}
model_map = {}

lines = aeon_text.split("\n")
in_skills = False
in_reactive = False
in_chains = False
current_skill = None
current_skill_indent = -1
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.lstrip(" ")
    indent = len(line) - len(stripped)

    if re.match(r"^skills:\s*$", line):
        in_skills = True; in_reactive = False; in_chains = False
        i += 1; continue
    if re.match(r"^reactive:\s*$", line):
        in_skills = False; in_reactive = True; in_chains = False
        i += 1; continue
    if re.match(r"^chains:\s*$", line):
        in_skills = False; in_reactive = False; in_chains = True
        i += 1; continue
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*:\s*$", line) and indent == 0 and in_skills:
        in_skills = False
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*:\s*", line) and indent == 0 and not re.match(r"^(skills|reactive|chains):", line):
        in_skills = False; in_reactive = False; in_chains = False

    if in_skills:
        # 1) Flat form on one line: `  slug: { enabled: true, schedule: "..." }`
        m = re.match(r"^\s{2}([a-zA-Z0-9_-]+):\s*\{(.*)", line)
        if m and indent == 2:
            slug = m.group(1)
            # Collect the content between opening '{' and the matching '}',
            # respecting quoted strings so a '}' inside quotes doesn't close.
            buf = m.group(2)
            def find_close(s, depth):
                in_q = None
                for idx, ch in enumerate(s):
                    if in_q:
                        if ch == in_q:
                            in_q = None
                    elif ch in ("'", '"'):
                        in_q = ch
                    elif ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            return idx, depth
                return -1, depth
            idx, depth = find_close(buf, 1)
            j = i
            if idx >= 0:
                buf = buf[:idx]
            else:
                while depth > 0 and j + 1 < len(lines):
                    j += 1
                    extra = " " + lines[j].strip()
                    idx2, depth = find_close(extra, depth)
                    if idx2 >= 0:
                        buf += extra[:idx2]
                        break
                    buf += extra
            kv = {}
            # Simple parsing: split by comma but respect quotes
            tokens = []
            cur = ""
            in_q = None
            for ch in buf:
                if in_q:
                    cur += ch
                    if ch == in_q:
                        in_q = None
                elif ch in ("'", '"'):
                    in_q = ch
                    cur += ch
                elif ch == ",":
                    tokens.append(cur.strip()); cur = ""
                else:
                    cur += ch
            if cur.strip():
                tokens.append(cur.strip())
            for t in tokens:
                if ":" in t:
                    k, v = t.split(":", 1)
                    kv[k.strip()] = v.strip().strip("'\"")
            enabled_map[slug] = (kv.get("enabled", "false") == "true")
            if "schedule" in kv:
                schedule_map[slug] = kv["schedule"]
            if "model" in kv:
                model_map[slug] = kv["model"]
            i = j + 1
            continue

        # 2) Nested form: `  slug:` on its own line, followed by indented keys
        m = re.match(r"^\s{2}([a-zA-Z0-9_-]+):\s*$", line)
        if m and indent == 2:
            slug = m.group(1)
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                nxt_strip = nxt.lstrip(" ")
                nxt_indent = len(nxt) - len(nxt_strip)
                if nxt.strip() == "" or nxt_indent > 2:
                    # continuation of this nested block
                    m2 = re.match(r"^\s+(enabled|schedule|model|var):\s*(.*)$", nxt)
                    if m2:
                        k = m2.group(1); raw = m2.group(2)
                        # Strip a trailing inline comment ` # ...` but respect quoted values
                        qm = re.match(r'^\s*"([^"]*)"', raw)
                        if qm:
                            v = qm.group(1)
                        else:
                            v = re.split(r"\s+#", raw, 1)[0].strip().strip("'\"").strip(",")
                        if k == "enabled":
                            enabled_map[slug] = (v == "true")
                        elif k == "schedule":
                            schedule_map[slug] = v
                        elif k == "model":
                            model_map[slug] = v
                    j += 1
                    continue
                break
            if slug not in enabled_map:
                enabled_map[slug] = False
            i = j
            continue
    i += 1

# ------------- Parse SKILL.md frontmatter -----------------
skills_meta = {}
all_slugs = []
for p in sorted(glob.glob("skills/*/SKILL.md")):
    slug = p.split("/")[1]
    all_slugs.append(slug)
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    # Extract frontmatter
    fm = {}
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if m:
        fm_text = m.group(1)
        # parse simple key: value pairs
        for ln in fm_text.split("\n"):
            if ":" in ln and not ln.startswith(" "):
                k, v = ln.split(":", 1)
                fm[k.strip()] = v.strip()
    # Explicit depends_on in the body or frontmatter: look for a line like `depends_on: [a, b]`
    depends = []
    dm = re.search(r"^depends_on:\s*\[(.*?)\]\s*$", text, re.MULTILINE)
    if dm:
        depends = [x.strip() for x in dm.group(1).split(",") if x.strip()]
    tags = []
    tm = re.match(r"\[(.*)\]", fm.get("tags", ""))
    if tm:
        tags = [t.strip() for t in tm.group(1).split(",") if t.strip()]
    skills_meta[slug] = {
        "name": fm.get("name", slug),
        "tags": tags,
        "depends_on": depends,
        "path": p,
        "body": text,
    }

# ------------- Categorize -----------------
category_of = {}
for slug in all_slugs:
    if slug in json_cat:
        category_of[slug] = json_cat[slug]
    else:
        # fall back to first matching tag
        tags = skills_meta[slug]["tags"]
        cat = None
        for t in tags:
            if t in CATEGORIES:
                cat = t; break
        if not cat:
            # heuristic tag mapping (dev > research > crypto > social > productivity priority)
            tagmap = {
                "dev": "dev", "build": "dev", "security": "dev", "github": "dev",
                "research": "research", "content": "research", "news": "research",
                "creative": "research", "docs": "research",
                "crypto": "crypto",
                "social": "social", "community": "social", "growth": "social", "ads": "social",
                "meta": "productivity", "productivity": "productivity",
                "ops": "productivity", "reliability": "productivity", "memory": "productivity",
                "projects": "productivity",
            }
            # priority order: scan all tags in a preferred order
            priority = ["dev", "research", "crypto", "social", "productivity"]
            for p in priority:
                for t in tags:
                    if tagmap.get(t) == p:
                        cat = p; break
                if cat: break
        category_of[slug] = cat or "other"

# ------------- Explicit edges -----------------
depends_edges = []  # (src, tgt)
for slug in all_slugs:
    for dep in skills_meta[slug]["depends_on"]:
        if dep in skills_meta:
            depends_edges.append((slug, dep))

consume_edges = []     # (src, tgt)  from chains
reactive_edges = []    # (trigger_skill, source_skill or "*")
# aeon.yml chains block is all comments on this fingerprint; parse anyway for completeness
# ---- reactive: block ----
# We parsed its presence manually earlier; extract specifically:
m = re.search(r"^reactive:\n(.*?)(^[a-zA-Z_][a-zA-Z0-9_-]*:|\Z)", aeon_text, re.DOTALL | re.MULTILINE)
if m:
    rblock = m.group(1)
    cur_sk = None
    for ln in rblock.split("\n"):
        mm = re.match(r"^\s{2}([a-zA-Z0-9_-]+):\s*$", ln)
        if mm:
            cur_sk = mm.group(1); continue
        mm = re.match(r"^\s+-\s*\{\s*on:\s*\"?([^,\"]+)\"?\s*,\s*when:.*\}", ln)
        if mm and cur_sk:
            reactive_edges.append((cur_sk, mm.group(1)))

# ------------- Derived shared-state edges -----------------
# For each skill, scan body for memory/(topics|state)/X refs,
# classify as write (nearby write-keyword) or read.
topic_writers = defaultdict(set)
topic_readers = defaultdict(set)
WRITE_RE = re.compile(r"(write|save|append|update|writing|persist|regenerate)[^\n]{0,80}memory/(topics|state)/([a-zA-Z0-9_.-]+)", re.IGNORECASE)
REF_RE = re.compile(r"memory/(topics|state)/([a-zA-Z0-9_.-]+)")
for slug, meta in skills_meta.items():
    body = meta["body"]
    all_refs = set(f"memory/{m.group(1)}/{m.group(2)}" for m in REF_RE.finditer(body))
    # Writes: find write-keyword within 3 lines of a ref
    writes = set()
    body_lines = body.split("\n")
    for idx, ln in enumerate(body_lines):
        if re.search(r"\b(write|save|append|update|regenerate|persist|writing)\b", ln, re.IGNORECASE):
            window = "\n".join(body_lines[max(0, idx-1):idx+3])
            for m2 in REF_RE.finditer(window):
                writes.add(f"memory/{m2.group(1)}/{m2.group(2)}")
    # Also catch inline forms like `> memory/topics/x` (redirect)
    for ln in body_lines:
        if ">" in ln or "**write" in ln.lower() or "writes to" in ln.lower():
            for m2 in REF_RE.finditer(ln):
                writes.add(f"memory/{m2.group(1)}/{m2.group(2)}")
    reads = all_refs - writes
    for r in writes:
        topic_writers[r].add(slug)
    for r in reads:
        topic_readers[r].add(slug)

# Build shared-state edges: writer -> reader for same topic
shared_edges = set()
# cron-state is written by every skill - collapse into legend note, skip
CRON_STATE_KEYS = {"memory/state/cron-state", "memory/cron-state.json", "memory/state/cron-state.json"}
for topic, writers in topic_writers.items():
    if "cron-state" in topic:
        continue
    readers = topic_readers.get(topic, set())
    for w in writers:
        for r in readers:
            if w != r:
                shared_edges.add((w, r, topic))
shared_edges = sorted(shared_edges)

# ------------- Article pipeline edges (research → syndicate-article etc) -----------------
article_pipeline_targets = {"syndicate-article", "rss-feed", "update-gallery"}
article_pipeline_edges = []
for slug, meta in skills_meta.items():
    tags = meta["tags"]
    body = meta["body"]
    if "research" in tags or re.search(r"\barticles/\b", body):
        for tgt in article_pipeline_targets:
            if tgt in skills_meta and slug != tgt:
                # only include if the skill writes to articles/
                if re.search(r"(write|save|append).{0,40}articles/", body, re.IGNORECASE) or re.search(r"articles/\$\{", body) or re.search(r"articles/[a-z-]+\.md", body):
                    article_pipeline_edges.append((slug, tgt))
article_pipeline_edges = sorted(set(article_pipeline_edges))

# ------------- Dump metadata used in render -----------------
state = {
    "generated_at": TODAY,
    "input_fingerprint": INPUT_FP,
    "skills_total": len(all_slugs),
    "enabled_count": sum(1 for s in all_slugs if enabled_map.get(s)),
    "edges": {
        "depends_on": len(depends_edges),
        "consume": len(consume_edges),
        "reactive": len(reactive_edges),
        "shared_state": len(shared_edges),
    },
    "node_list_sha": hashlib.sha1("\n".join(sorted(all_slugs)).encode()).hexdigest(),
    "edge_list_sha": hashlib.sha1(
        "\n".join(sorted(
            [f"d:{a}->{b}" for a, b in depends_edges]
            + [f"c:{a}->{b}" for a, b in consume_edges]
            + [f"r:{a}<-{b}" for a, b in reactive_edges]
            + [f"s:{a}->{b}:{t}" for a, b, t in shared_edges]
        )).encode()
    ).hexdigest(),
}

# ================= RENDER =================
out = []
out.append("# Skill Dependency Graph\n")
out.append(f"> Auto-generated by `skill-graph` on {TODAY}. Mode: `{MODE_HINT}`.\n")

# Verdict line
if MODE_HINT == "SKILL_GRAPH_NEW":
    verdict = f"SKILL_GRAPH_NEW — {len(all_slugs)} skills mapped across {len([c for c in CATEGORY_ORDER if any(category_of[s]==c for s in all_slugs)])} categories, {state['enabled_count']} enabled"
else:
    verdict = f"ARCHITECTURE_OK — {len(all_slugs)} skills, {state['enabled_count']} enabled"
out.append(f"**Verdict:** {verdict}\n")

# Count per category and enabled per category
cat_total = Counter(category_of[s] for s in all_slugs)
cat_enabled = Counter(category_of[s] for s in all_slugs if enabled_map.get(s))

# Cross-category edge counts (depends_on + shared_state collapsed by category pair)
cross_cat = Counter()
for a, b in depends_edges:
    ca, cb = category_of.get(a, "other"), category_of.get(b, "other")
    if ca != cb:
        cross_cat[(ca, cb)] += 1
for a, b, _t in shared_edges:
    ca, cb = category_of.get(a, "other"), category_of.get(b, "other")
    if ca != cb:
        cross_cat[(ca, cb)] += 1

# -------- Overview diagram --------
out.append("## Overview\n")
out.append("Category boxes show **enabled / total** skill counts. Cross-category edges carry their count.\n")
out.append("```mermaid")
out.append("flowchart LR")
for cat in CATEGORY_ORDER:
    if cat_total.get(cat, 0) == 0:
        continue
    label = CATEGORIES[cat]
    out.append(f'    subgraph {cat}["{label} ({cat_enabled.get(cat,0)} / {cat_total.get(cat,0)})"]')
    out.append(f'        {cat}_anchor( )')
    out.append(f'    end')
for (ca, cb), n in sorted(cross_cat.items(), key=lambda kv: (-kv[1], kv[0])):
    out.append(f'    {ca}_anchor -- "{n}" --> {cb}_anchor')
out.append("    classDef cat fill:#fafafa,stroke:#333,color:#000")
out.append("```\n")

# -------- Self-healing loop callout --------
out.append("## Self-healing loop\n")
out.append("`cron-state.json` is the shared state node every scheduled skill writes to after each run; the health/repair cluster reads it.\n")
out.append("```mermaid")
out.append("flowchart LR")
# only include if these skills exist
healing_chain = ["heartbeat", "skill-health", "skill-evals", "skill-repair", "self-improve"]
present = [s for s in healing_chain if s in skills_meta]
cron_node = 'cron-state["memory/cron-state.json<br/>(written by every scheduled skill)"]'
out.append(f"    {cron_node}")
for s in present:
    out.append(f"    {s}[{s}]")
for i in range(len(present) - 1):
    out.append(f"    {present[i]} --> {present[i+1]}")
out.append(f"    cron-state -.-> skill-health" if "skill-health" in present else "")
out.append(f"    cron-state -.-> heartbeat" if "heartbeat" in present else "")
# planner reactive edge from fleet to self-healing
if "planner" in skills_meta:
    out.append(f"    planner[planner]")
    out.append(f"    cron-state -.-> planner")
    out.append(f'    planner -. "reactive cf>=2" .-> skill-repair' if "skill-repair" in present else "")
out.append(f'    classDef health fill:#fff,stroke:#000,stroke-width:2px,color:#000')
for s in present + (["planner"] if "planner" in skills_meta else []):
    out.append(f"    click {s} \"../skills/{s}/SKILL.md\"")
out.append("```\n")

# -------- What-changed section --------
# Mode SKILL_GRAPH_NEW: skip
# For completeness here we skip it.

# -------- Per-category mini-diagrams --------
out.append("## Per-category diagrams\n")
# Build intra-category depends and shared edges maps
intra = defaultdict(list)  # cat -> list of (edge_type, a, b, meta)
cross_in = defaultdict(list)  # cat -> list of (ext_slug, local_slug, type) incoming
cross_out = defaultdict(list) # cat -> list of (local_slug, ext_slug, type) outgoing
for a, b in depends_edges:
    ca, cb = category_of[a], category_of[b]
    if ca == cb:
        intra[ca].append(("depends", a, b, ""))
    else:
        cross_out[ca].append((a, b, "depends"))
        cross_in[cb].append((a, b, "depends"))
for a, b, t in shared_edges:
    ca, cb = category_of[a], category_of[b]
    if ca == cb:
        intra[ca].append(("shared", a, b, t))
    else:
        cross_out[ca].append((a, b, "shared"))
        cross_in[cb].append((a, b, "shared"))

MAX_EXTERNAL = 20

def node_id(s):
    return s  # hyphenated slug as-is (Mermaid tolerates hyphens in flowchart IDs)

for cat in CATEGORY_ORDER:
    slugs_in = sorted([s for s in all_slugs if category_of[s] == cat])
    if not slugs_in:
        continue
    label = CATEGORIES[cat]
    out.append(f"### {label}  _({cat_enabled.get(cat,0)} enabled / {cat_total.get(cat,0)})_\n")
    out.append("```mermaid")
    out.append("flowchart LR")
    # declare each node with enabled/disabled hint in label (schedule for enabled)
    for s in slugs_in:
        annot = ""
        if enabled_map.get(s) and schedule_map.get(s):
            sch = schedule_map[s].replace('"', '').strip()
            annot = f"<br/><span style='font-size:0.8em'>{sch}</span>"
        name = skills_meta[s]["name"].replace('"', "'")
        out.append(f'    {node_id(s)}["{s}{annot}"]')
    # intra-category edges
    for et, a, b, m in intra[cat]:
        if et == "depends":
            out.append(f'    {node_id(a)} --> {node_id(b)}')
        elif et == "shared":
            out.append(f'    {node_id(a)} -..-> {node_id(b)}')
    # ghost cluster of cross-category deps (dedup edges by (direction, a, b, t))
    externals = []
    seen_edges = set()
    for a, b, t in cross_out[cat]:
        key = ("out", a, b, t)
        if key in seen_edges: continue
        seen_edges.add(key)
        externals.append(key)
    for a, b, t in cross_in[cat]:
        key = ("in", a, b, t)
        if key in seen_edges: continue
        seen_edges.add(key)
        externals.append(key)
    if externals:
        out.append(f'    subgraph {cat}_ext["cross-category"]')
        seen = set()
        for direction, a, b, t in externals[:MAX_EXTERNAL]:
            ext = b if direction == "out" else a
            if ext in seen:
                continue
            seen.add(ext)
            out.append(f'        {node_id(ext)}:::external["{ext}"]')
        if len(externals) > MAX_EXTERNAL:
            out.append(f'        more_{cat}["… +{len(externals)-MAX_EXTERNAL} more"]:::external')
        out.append(f'    end')
        for direction, a, b, t in externals[:MAX_EXTERNAL]:
            arrow = "-->" if t == "depends" else "-..->"
            if direction == "out":
                out.append(f'    {node_id(a)} {arrow} {node_id(b)}')
            else:
                out.append(f'    {node_id(a)} {arrow} {node_id(b)}')
    # classDefs + classes
    out.append("    classDef enabled fill:#fff,stroke:#000,stroke-width:2px,color:#000")
    out.append("    classDef disabled fill:#f5f5f5,stroke:#bbb,color:#888")
    out.append("    classDef external fill:none,stroke:#bbb,stroke-dasharray:3 3,color:#888")
    for s in slugs_in:
        cls = "enabled" if enabled_map.get(s) else "disabled"
        out.append(f"    class {node_id(s)} {cls}")
    # click-throughs
    for s in slugs_in:
        out.append(f'    click {node_id(s)} "../skills/{s}/SKILL.md"')
    # click-throughs for externals (if any)
    seen_click = set()
    for direction, a, b, t in externals[:MAX_EXTERNAL]:
        ext = b if direction == "out" else a
        if ext in seen_click:
            continue
        seen_click.add(ext)
        out.append(f'    click {node_id(ext)} "../skills/{ext}/SKILL.md"')
    out.append("```\n")

# -------- Legend --------
out.append("## Legend\n")
out.append("- `-->` **explicit depends_on** (declared in SKILL.md frontmatter)")
out.append("- `-.->` **chain consume** (output passed between chained steps)")
out.append("- `-..->` **reactive / shared memory state** (one skill writes `memory/topics/*` or `memory/state/*`; another reads)")
out.append("- **Bold border** = `enabled: true` in `aeon.yml`; faded grey = disabled")
out.append("- **Dashed ghost nodes** in per-category panels = cross-category dependencies (duplicated for layout)")
out.append("- **Click any node** to open its `SKILL.md` on GitHub")
out.append("- `memory/cron-state.json` is written by *every* scheduled skill after each run — the self-healing cluster (`heartbeat` / `skill-health` / `skill-evals` / `skill-repair` / `self-improve`) reads it. Collapsed into the self-healing diagram to keep the per-category panels readable.\n")

# -------- Summary table --------
out.append("## Summary\n")
out.append("| Category | Enabled | Total |")
out.append("|---|---:|---:|")
for cat in CATEGORY_ORDER:
    if cat_total.get(cat, 0):
        out.append(f"| {CATEGORIES[cat]} | {cat_enabled.get(cat,0)} | {cat_total.get(cat,0)} |")
out.append(f"| **All** | **{state['enabled_count']}** | **{len(all_slugs)}** |\n")

out.append("| Edge type | Count |")
out.append("|---|---:|")
out.append(f"| explicit `depends_on` | {state['edges']['depends_on']} |")
out.append(f"| chain `consume` | {state['edges']['consume']} |")
out.append(f"| reactive triggers | {state['edges']['reactive']} |")
out.append(f"| derived shared-state (topics/state) | {state['edges']['shared_state']} |")
out.append("")

# -------- Source-status footer --------
out.append("---")
out.append(
    f"_skills parsed: {len(all_slugs)} · depends_on: {state['edges']['depends_on']} · "
    f"consume: {state['edges']['consume']} · reactive: {state['edges']['reactive']} · "
    f"shared-state derived: {state['edges']['shared_state']} · "
    f"enabled: {state['enabled_count']}/{len(all_slugs)} · mode: {MODE_HINT}_"
)

doc = "\n".join(out).rstrip() + "\n"

# -------- Lint (post-render, before write) --------
lint_errors = []
# Each click-through path must exist
for m in re.finditer(r'click\s+(\S+)\s+"([^"]+)"', doc):
    node, path = m.group(1), m.group(2)
    # path is relative from docs/skill-graph.md i.e. docs/, resolve: strip leading ../
    resolved = path
    if resolved.startswith("../"):
        resolved = resolved[3:]
    full = os.path.join(ROOT, resolved)
    if not os.path.exists(full):
        lint_errors.append(f"click target missing: {node} -> {path}")

# Every subgraph has matching end
# Count per Mermaid block
mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", doc, re.DOTALL)
for idx, blk in enumerate(mermaid_blocks):
    n_sub = len(re.findall(r"^\s*subgraph\s", blk, re.MULTILINE))
    n_end = len(re.findall(r"^\s*end\s*$", blk, re.MULTILINE))
    if n_sub != n_end:
        lint_errors.append(f"mermaid block #{idx+1}: {n_sub} subgraph vs {n_end} end")

if lint_errors:
    print("LINT_FAIL", file=sys.stderr)
    for e in lint_errors:
        print(" -", e, file=sys.stderr)
    sys.exit(2)

# -------- Write outputs --------
os.makedirs("docs", exist_ok=True)
with open("docs/skill-graph.md", "w", encoding="utf-8") as f:
    f.write(doc)

os.makedirs("memory/topics", exist_ok=True)
with open("memory/topics/skill-graph-state.json", "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)
    f.write("\n")

# One-line verdict for commit message
print(verdict)
