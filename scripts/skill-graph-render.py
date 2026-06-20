#!/usr/bin/env python3
"""skill-graph: render docs/skill-graph.md from /tmp/skill-graph-model.json.

Also lints the Mermaid output, persists memory/topics/skill-graph-state.json
on success, and emits a structured summary block to stdout that the caller
shell can consume to drive notify / PR text.

Output to stdout:

```
MODE=<SKILL_GRAPH_*>
VERDICT=<one-line verdict>
SKILLS_TOTAL=<n>
ENABLED=<n>
EDGES_DEPENDS_ON=<n>
EDGES_CONSUME=<n>
EDGES_REACTIVE=<n>
EDGES_SHARED_STATE=<n>
WHAT_CHANGED=<short pipe-delim summary or ->
```
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "memory" / "topics" / "skill-graph-state.json"

CANONICAL_CATEGORIES = [
    ("research", "Research & Content"),
    ("dev", "Dev & Code"),
    ("crypto", "Crypto & Markets"),
    ("social", "Social"),
    ("productivity", "Productivity & Meta"),
]

# Map non-canonical categories from tag fallback into the 5 canonical buckets.
# Reviewed against actual skill list — keeps the overview comprehensible.
CATEGORY_REMAP = {
    "ai": "dev",
    "meta": "productivity",
    "data": "research",
    "content": "research",
    "security": "dev",
    "eval": "productivity",
    "creative": "research",
    "compute": "crypto",
    "other": "productivity",
}

# Collapsed shared state files — drawn in legend instead of N edges.
COLLAPSED_STATES = {"cron-state.json", "memory/cron-state.json"}


def canonicalize_category(cat: str) -> str:
    if cat in dict(CANONICAL_CATEGORIES):
        return cat
    return CATEGORY_REMAP.get(cat, "productivity")


def slug_id(slug: str) -> str:
    # Mermaid IDs must avoid characters that look like reserved tokens; the
    # skill spec asks for hyphenated slugs verbatim. Hyphens, digits, and
    # lowercase letters are all valid Mermaid IDs.
    return slug


def derive_edges(model: dict):
    """Return dict with depends_on, consume, reactive, shared_state edges."""
    edges = {
        "depends_on": [],
        "consume": [],
        "reactive": [],
        "shared_state": [],
    }

    skills = model["skills"]
    slug_set = set(skills.keys())

    # depends_on from frontmatter
    for slug, info in skills.items():
        deps = info.get("frontmatter", {}).get("depends_on", []) or []
        for d in deps:
            d_clean = d.strip().strip("\"'")
            if d_clean and d_clean in slug_set and d_clean != slug:
                edges["depends_on"].append((slug, d_clean))

    # consume from chains
    for cname, chain in (model.get("chains") or {}).items():
        for step in chain.get("steps", []):
            if "skill" in step and "consume" in step:
                for src in step["consume"]:
                    src_c = src.strip()
                    if src_c in slug_set and src_c != step["skill"]:
                        edges["consume"].append((src_c, step["skill"]))

    # reactive triggers — fan from "any failing skill" to the reactive target.
    # We only register the reactive target so it shows on the self-healing
    # callout; for the per-category diagrams a reactive skill is rendered as
    # its own node, not as N edges from every other skill.
    for rname, rconf in (model.get("reactive") or {}).items():
        for trg in rconf.get("triggers", []):
            edges["reactive"].append(("*", rname, trg.get("when", "")))

    # shared-state edges: writer -> reader for the same memory path,
    # excluding the cron-state ledger.
    writers_by_path: dict[str, list[str]] = defaultdict(list)
    readers_by_path: dict[str, list[str]] = defaultdict(list)
    for slug, info in skills.items():
        for w in info.get("writes", []):
            if any(c in w for c in COLLAPSED_STATES):
                continue
            writers_by_path[w].append(slug)
        for r in info.get("reads", []):
            if any(c in r for c in COLLAPSED_STATES):
                continue
            readers_by_path[r].append(slug)
    seen_pair: set[tuple[str, str]] = set()
    for path, writers in writers_by_path.items():
        for w in writers:
            for r in readers_by_path.get(path, []):
                if w == r:
                    continue
                pair = (w, r)
                if pair in seen_pair:
                    continue
                seen_pair.add(pair)
                edges["shared_state"].append((w, r, path))

    return edges


def schedule_label(sched: str | None) -> str:
    if not sched:
        return ""
    if sched in ("reactive", "workflow_dispatch"):
        return sched
    return sched


def render_node(slug: str, info: dict) -> str:
    aeon = info.get("aeon") or {}
    sched = schedule_label(aeon.get("schedule", "")) if aeon.get("enabled") else ""
    if sched:
        return f'    {slug_id(slug)}["{slug}<br/><i>{sched}</i>"]'
    return f'    {slug_id(slug)}["{slug}"]'


def render_external(slug: str, owner_cat: str) -> str:
    return f'    {slug_id(slug)}["{slug}<br/><i>{owner_cat}</i>"]'


def render_doc(model: dict, today: str, prior_doc: str | None) -> tuple[str, dict]:
    skills = model["skills"]
    edges = derive_edges(model)

    # Bucket skills by canonical category
    by_cat: dict[str, list[str]] = defaultdict(list)
    canonical_cat_of: dict[str, str] = {}
    for slug, info in skills.items():
        cc = canonicalize_category(info["category"])
        canonical_cat_of[slug] = cc
        by_cat[cc].append(slug)
    for cc in by_cat:
        by_cat[cc].sort()

    enabled_count = sum(1 for s in skills.values() if (s.get("aeon") or {}).get("enabled"))
    total = len(skills)

    # Verdict (NEW path — no prior structural state)
    verdict_one = ""
    what_changed_lines: list[str] = []
    prior_state = model.get("prior_state") or {}
    if model["mode"] == "SKILL_GRAPH_NEW":
        verdict_one = f"SKILL_GRAPH_NEW — {total} skills mapped across 5 categories, {enabled_count} enabled"
    else:
        # Compute deltas against prior_state if present
        prior_skills = set(prior_state.get("node_list", []))
        cur_skills = set(skills.keys())
        added = sorted(cur_skills - prior_skills)
        removed = sorted(prior_skills - cur_skills)
        prior_enabled = set(prior_state.get("enabled_list", []))
        cur_enabled = {s for s, info in skills.items() if (info.get("aeon") or {}).get("enabled")}
        flips_on = sorted(cur_enabled - prior_enabled)
        flips_off = sorted(prior_enabled - cur_enabled)
        parts = []
        if added:
            parts.append(f"NEW_SKILLS: {', '.join(added)}")
        if removed:
            parts.append(f"RETIRED_SKILLS: {', '.join(removed)}")
        if flips_on:
            parts.append(f"NEW_ENABLED: {', '.join(flips_on)}")
        if flips_off:
            parts.append(f"DISABLED: {', '.join(flips_off)}")
        if not parts:
            verdict_one = "ARCHITECTURE_OK"
        else:
            verdict_one = " · ".join(parts)
        if added:
            what_changed_lines.append(f"- **Added skills ({len(added)}):** " + ", ".join(f"`{s}`" for s in added))
        if removed:
            what_changed_lines.append(f"- **Retired skills ({len(removed)}):** " + ", ".join(f"`{s}`" for s in removed))
        if flips_on:
            what_changed_lines.append(f"- **Newly enabled ({len(flips_on)}):** " + ", ".join(f"`{s}`" for s in flips_on))
        if flips_off:
            what_changed_lines.append(f"- **Newly disabled ({len(flips_off)}):** " + ", ".join(f"`{s}`" for s in flips_off))

    # Build markdown
    out: list[str] = []
    out.append("# Skill Dependency Graph")
    out.append("")
    out.append(f"> Auto-generated by `skill-graph` on {today}. Mode: `{model['mode']}`.")
    out.append("")
    out.append(f"**Verdict:** {verdict_one}")
    out.append("")

    # 3. What changed since last run (skip on NEW)
    if model["mode"] != "SKILL_GRAPH_NEW":
        out.append("## What changed since last run")
        out.append("")
        if what_changed_lines:
            out.extend(what_changed_lines)
        else:
            out.append("- No structural changes since the previous run; fingerprints differ only in incidental fields.")
        out.append("")

    # 4. Overview
    out.append("## Overview")
    out.append("")
    out.append("Category boxes show **enabled / total** skill counts. Cross-category edges carry their count.")
    out.append("")
    out.append("```mermaid")
    out.append("flowchart LR")

    for key, label in CANONICAL_CATEGORIES:
        total_c = len(by_cat.get(key, []))
        en_c = sum(1 for s in by_cat.get(key, []) if (skills[s].get("aeon") or {}).get("enabled"))
        out.append(f'    subgraph {key}["{label} ({en_c} / {total_c})"]')
        out.append(f"        {key}_anchor( )")
        out.append("    end")

    # Cross-category edges: count all derived edges where src and dst are in
    # different canonical categories.
    cross_counts: dict[tuple[str, str], int] = defaultdict(int)
    for kind in ("depends_on", "consume"):
        for e in edges[kind]:
            src, dst = e[0], e[1]
            cs = canonical_cat_of.get(src)
            cd = canonical_cat_of.get(dst)
            if cs and cd and cs != cd:
                cross_counts[(cs, cd)] += 1
    for e in edges["shared_state"]:
        src, dst = e[0], e[1]
        cs = canonical_cat_of.get(src)
        cd = canonical_cat_of.get(dst)
        if cs and cd and cs != cd:
            cross_counts[(cs, cd)] += 1
    for (cs, cd), cnt in sorted(cross_counts.items()):
        out.append(f'    {cs}_anchor -->|"{cnt}"| {cd}_anchor')

    for key, _ in CANONICAL_CATEGORIES:
        out.append(f"    style {key}_anchor fill:transparent,stroke:transparent")
    out.append("```")
    out.append("")
    out.append("_Every skill also writes `memory/cron-state.json`, which is read by `heartbeat`, `skill-health`, `skill-repair`, and `skill-evals`. Collapsed here to keep the map readable — see Self-healing loop below._")
    out.append("")

    # 5. Self-healing loop callout
    out.append("## Self-healing loop")
    out.append("")
    out.append("Reactive trigger: `skill-repair` fires on `consecutive_failures >= 3` for any skill; `planner` fires on `>= 2` to re-plan the day around the regressing area.")
    out.append("")
    out.append("```mermaid")
    out.append("flowchart LR")
    sh_nodes = ["heartbeat", "skill-health", "skill-evals", "skill-repair", "self-improve"]
    for n in sh_nodes:
        if n in skills:
            out.append(f'    {n}[{n}]')
        else:
            out.append(f'    {n}[{n}]')
    out.append('    cron[("memory/cron-state.json")]')
    out.append("    heartbeat --> skill-health")
    out.append("    skill-health --> skill-evals")
    out.append("    skill-evals --> skill-repair")
    out.append("    skill-repair --> self-improve")
    out.append('    self-improve -.->|"updates aeon.yml"| heartbeat')
    out.append("    heartbeat -.-> cron")
    out.append("    skill-health -.-> cron")
    out.append("    skill-evals -.-> cron")
    out.append("    skill-repair -.-> cron")
    # planner reactive arrow
    if "planner" in skills:
        out.append('    planner[planner]')
        out.append('    skill-health -.->|"failures &gt;=2"| planner')
        out.append('    click planner "../skills/planner/SKILL.md"')
    for n in sh_nodes:
        if n in skills:
            out.append(f'    click {n} "../skills/{n}/SKILL.md"')
    out.append("```")
    out.append("")

    # 6. Per-category mini-diagrams
    out.append("## Per-category breakdown")
    out.append("")

    for key, label in CANONICAL_CATEGORIES:
        members = by_cat.get(key, [])
        en_c = sum(1 for s in members if (skills[s].get("aeon") or {}).get("enabled"))
        out.append(f"### {label} ({en_c} / {len(members)})")
        out.append("")
        out.append("```mermaid")
        out.append("flowchart LR")
        out.append("    classDef enabled fill:#fff,stroke:#000,stroke-width:2px,color:#000")
        out.append("    classDef disabled fill:#f5f5f5,stroke:#bbb,color:#888")
        out.append("    classDef external fill:none,stroke:#bbb,stroke-dasharray:3 3,color:#888")

        member_set = set(members)

        # Native nodes
        for slug in members:
            out.append(render_node(slug, skills[slug]))

        # Native edges + cross-category targets/sources
        edge_lines: list[str] = []
        external_nodes: set[str] = set()
        for src, dst in edges["depends_on"]:
            if src in member_set and dst in member_set:
                edge_lines.append(f"    {slug_id(src)} --> {slug_id(dst)}")
            elif src in member_set and dst not in member_set and dst in skills:
                external_nodes.add(dst)
                edge_lines.append(f"    {slug_id(src)} --> {slug_id(dst)}")
            elif dst in member_set and src not in member_set and src in skills:
                external_nodes.add(src)
                edge_lines.append(f"    {slug_id(src)} --> {slug_id(dst)}")
        for src, dst in edges["consume"]:
            if src in member_set and dst in member_set:
                edge_lines.append(f"    {slug_id(src)} -.-> {slug_id(dst)}")
            elif src in member_set and dst in skills:
                external_nodes.add(dst)
                edge_lines.append(f"    {slug_id(src)} -.-> {slug_id(dst)}")
            elif dst in member_set and src in skills:
                external_nodes.add(src)
                edge_lines.append(f"    {slug_id(src)} -.-> {slug_id(dst)}")
        for src, dst, _path in edges["shared_state"]:
            if src in member_set and dst in member_set:
                edge_lines.append(f"    {slug_id(src)} -..-> {slug_id(dst)}")
            elif src in member_set and dst in skills:
                external_nodes.add(dst)
                edge_lines.append(f"    {slug_id(src)} -..-> {slug_id(dst)}")
            elif dst in member_set and src in skills:
                external_nodes.add(src)
                edge_lines.append(f"    {slug_id(src)} -..-> {slug_id(dst)}")

        # Render external ghost nodes before edges
        external_nodes -= member_set
        for ext in sorted(external_nodes):
            owner = canonical_cat_of.get(ext, "other")
            out.append(render_external(ext, owner))

        # De-dup edges and append
        for line in dict.fromkeys(edge_lines).keys():
            out.append(line)

        # Click directives — once per declared node (member + external)
        seen_clicks: set[str] = set()
        for slug in members + sorted(external_nodes):
            if slug in seen_clicks:
                continue
            seen_clicks.add(slug)
            if skills.get(slug, {}).get("path"):
                out.append(f'    click {slug_id(slug)} "../skills/{slug}/SKILL.md"')

        # Enabled / disabled / external classes
        enabled_members = [s for s in members if (skills[s].get("aeon") or {}).get("enabled")]
        disabled_members = [s for s in members if not (skills[s].get("aeon") or {}).get("enabled")]
        if enabled_members:
            out.append("    class " + ",".join(enabled_members) + " enabled")
        if disabled_members:
            out.append("    class " + ",".join(disabled_members) + " disabled")
        if external_nodes:
            out.append("    class " + ",".join(sorted(external_nodes)) + " external")
        out.append("```")
        out.append("")

    # 9. Legend
    out.append("## Legend")
    out.append("")
    out.append("| Edge | Meaning |")
    out.append("|------|---------|")
    out.append("| `-->` solid | `depends_on` — declared in frontmatter |")
    out.append("| `-.->` dashed | `consume` — chain step receives prior output |")
    out.append("| `-..->` dotted | shared-state — one skill writes a memory file another reads |")
    out.append("")
    out.append("| Node style | Meaning |")
    out.append("|------------|---------|")
    out.append("| **Bold border** | Enabled in `aeon.yml` (schedule shown beneath) |")
    out.append("| Faded grey | Disabled / not scheduled |")
    out.append("| Dashed border | External skill referenced from another category |")
    out.append("")
    out.append("Click any node on github.com to open its `SKILL.md`. Reactive triggers and the shared `memory/cron-state.json` ledger are documented in the **Self-healing loop** section, not duplicated as edges in the per-category diagrams.")
    out.append("")

    # 10. Summary
    out.append("## Summary")
    out.append("")
    out.append("| Category | Total | Enabled |")
    out.append("|----------|-------|---------|")
    for key, label in CANONICAL_CATEGORIES:
        t_c = len(by_cat.get(key, []))
        e_c = sum(1 for s in by_cat.get(key, []) if (skills[s].get("aeon") or {}).get("enabled"))
        out.append(f"| {label} | {t_c} | {e_c} |")
    out.append(f"| **Total** | **{total}** | **{enabled_count}** |")
    out.append("")
    out.append("| Edge type | Count |")
    out.append("|-----------|-------|")
    out.append(f"| `depends_on` | {len(edges['depends_on'])} |")
    out.append(f"| `consume` (chains) | {len(edges['consume'])} |")
    out.append(f"| `reactive` | {len(edges['reactive'])} |")
    out.append(f"| `shared_state` (derived) | {len(edges['shared_state'])} |")
    out.append("")

    # 11. Footer
    out.append("---")
    out.append("")
    out.append(
        f"_skills parsed: {total} · depends_on: {len(edges['depends_on'])} · "
        f"consume: {len(edges['consume'])} · reactive: {len(edges['reactive'])} · "
        f"shared-state derived: {len(edges['shared_state'])} · "
        f"enabled: {enabled_count}/{total} · mode: {model['mode']}_"
    )
    out.append("")

    summary = {
        "skills_total": total,
        "enabled_count": enabled_count,
        "edges": {
            "depends_on": len(edges["depends_on"]),
            "consume": len(edges["consume"]),
            "reactive": len(edges["reactive"]),
            "shared_state": len(edges["shared_state"]),
        },
        "verdict": verdict_one,
        "node_list": sorted(skills.keys()),
        "enabled_list": sorted([s for s, info in skills.items() if (info.get("aeon") or {}).get("enabled")]),
    }
    return "\n".join(out), summary


# ---------- Lint ----------
def lint_mermaid(text: str, out_path: Path) -> tuple[bool, str]:
    """Sanity check Mermaid blocks. Returns (ok, error_msg)."""
    blocks: list[tuple[int, str]] = []
    in_block = False
    cur: list[str] = []
    start_line = 0
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```mermaid"):
            in_block = True
            cur = []
            start_line = i
            continue
        if in_block and line.strip().startswith("```"):
            in_block = False
            blocks.append((start_line, "\n".join(cur)))
            continue
        if in_block:
            cur.append(line)

    for start, block in blocks:
        # subgraph / end balance
        subs = sum(1 for ln in block.splitlines() if ln.strip().startswith("subgraph "))
        ends = sum(1 for ln in block.splitlines() if ln.strip() == "end")
        if subs != ends:
            return False, f"subgraph/end mismatch in block at line {start} ({subs} vs {ends})"
        # Bracket balance per line for [label] declarations
        for j, ln in enumerate(block.splitlines(), start + 1):
            opens = ln.count("[")
            closes = ln.count("]")
            if opens != closes:
                return False, f"bracket mismatch at line {j}: {ln.rstrip()!r}"
        # click directives reference existing paths
        for j, ln in enumerate(block.splitlines(), start + 1):
            m = re.match(r'\s*click\s+(\S+)\s+"([^"]+)"\s*$', ln)
            if not m:
                continue
            _node, path = m.group(1), m.group(2)
            rel = path
            if rel.startswith("../"):
                target = (out_path.parent / rel).resolve()
            else:
                target = (out_path.parent / rel).resolve()
            if not target.exists():
                return False, f"click target missing at line {j}: {path}"
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", required=True)
    ap.add_argument("--out", default="docs/skill-graph.md")
    args = ap.parse_args()

    model = json.loads(Path("/tmp/skill-graph-model.json").read_text())
    out_path = (ROOT / args.out).resolve()
    prior_doc = out_path.read_text(encoding="utf-8") if out_path.exists() else None
    doc, summary = render_doc(model, args.today, prior_doc)

    # Lint before writing
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp_path.write_text(doc, encoding="utf-8")
    ok, err = lint_mermaid(doc, out_path)
    if not ok:
        tmp_path.unlink(missing_ok=True)
        print(f"LINT_FAIL: {err}", file=sys.stderr)
        print("MODE=SKILL_GRAPH_ERROR")
        print(f"VERDICT=lint:{err}")
        return 2
    tmp_path.replace(out_path)

    state = {
        "generated_at": args.today,
        "input_fingerprint": model["fingerprint"],
        "skills_total": summary["skills_total"],
        "enabled_count": summary["enabled_count"],
        "edges": summary["edges"],
        "node_list_sha": hashlib.sha1("\n".join(summary["node_list"]).encode()).hexdigest(),
        "edge_list_sha": hashlib.sha1(json.dumps(summary["edges"], sort_keys=True).encode()).hexdigest(),
        "node_list": summary["node_list"],
        "enabled_list": summary["enabled_list"],
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

    print(f"MODE={model['mode']}")
    print(f"VERDICT={summary['verdict']}")
    print(f"SKILLS_TOTAL={summary['skills_total']}")
    print(f"ENABLED={summary['enabled_count']}")
    print(f"EDGES_DEPENDS_ON={summary['edges']['depends_on']}")
    print(f"EDGES_CONSUME={summary['edges']['consume']}")
    print(f"EDGES_REACTIVE={summary['edges']['reactive']}")
    print(f"EDGES_SHARED_STATE={summary['edges']['shared_state']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
