#!/usr/bin/env python3
"""skill-graph: collect parsed model + fingerprint for the skill-graph skill.

Writes intermediate JSON to /tmp/skill-graph-model.json and a fingerprint to
/tmp/skill-graph.fingerprint.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
AEON_YML = ROOT / "aeon.yml"
SKILLS_JSON = ROOT / "skills.json"
STATE_FILE = ROOT / "memory" / "topics" / "skill-graph-state.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
TOPIC_RE = re.compile(r"memory/(?:topics|state)/[A-Za-z0-9_./-]+")
WRITE_VERB_RE = re.compile(r"\b(write|writes|save|saves|append|appends|update|updates|persist|persists)\b", re.IGNORECASE)
WRITE_REDIRECT_RE = re.compile(r"(>>|>)\s*memory/(?:topics|state)/")


def parse_skill_frontmatter(md: str) -> dict:
    m = FRONTMATTER_RE.match(md)
    fm: dict = {}
    if not m:
        return fm
    block = m.group(1)
    cur_key = None
    for line in block.splitlines():
        if not line.strip():
            cur_key = None
            continue
        if line.startswith("  - ") and cur_key in ("tags", "depends_on"):
            fm.setdefault(cur_key, []).append(line[4:].strip().strip("\"'"))
            continue
        if line[0:1] != " " and ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                fm[k] = [x.strip().strip("\"'") for x in inner.split(",") if x.strip()]
                cur_key = None
            elif v == "":
                fm[k] = []
                cur_key = k
            else:
                fm[k] = v.strip().strip("\"'")
                cur_key = None
    return fm


def classify_refs(body: str):
    """Return (writes, reads) sets of topic/state references in body.

    Heuristic per skill spec: a reference is classified as a *write* when any
    of the surrounding 3 lines contain a write-verb or a redirection.
    """
    lines = body.splitlines()
    writes: set[str] = set()
    reads: set[str] = set()
    # Pre-compute write-eligibility per line index
    write_flag = [bool(WRITE_VERB_RE.search(ln) or WRITE_REDIRECT_RE.search(ln)) for ln in lines]
    for i, line in enumerate(lines):
        refs = TOPIC_RE.findall(line)
        if not refs:
            continue
        window_write = any(write_flag[max(0, i - 1): min(len(lines), i + 2)])
        for ref in refs:
            ref = ref.rstrip(".,:;\"')")
            if window_write:
                writes.add(ref)
            else:
                reads.add(ref)
    return sorted(writes), sorted(reads - writes)


def parse_all_skills() -> dict:
    out: dict[str, dict] = {}
    for sk_dir in sorted(SKILLS_DIR.iterdir()):
        if not sk_dir.is_dir():
            continue
        skill_md = sk_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        body = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = parse_skill_frontmatter(body)
        writes, reads = classify_refs(body)
        out[sk_dir.name] = {
            "slug": sk_dir.name,
            "frontmatter": fm,
            "writes": writes,
            "reads": reads,
            "path": str(skill_md.relative_to(ROOT)),
        }
    return out


# ---------- aeon.yml parsing ----------
def parse_aeon_yml(text: str) -> dict:
    skills: dict[str, dict] = {}
    chains: dict[str, dict] = {}
    reactive: dict[str, dict] = {}

    cleaned: list[str] = []
    for raw in text.splitlines():
        s = raw.rstrip()
        if s.lstrip().startswith("#"):
            continue
        # Strip trailing inline comments. Walk char-by-char so '#' inside
        # quotes is preserved (e.g. schedules don't contain '#', but values
        # might in the future).
        in_quote: str | None = None
        out_chars: list[str] = []
        for ch in s:
            if in_quote:
                if ch == in_quote:
                    in_quote = None
                out_chars.append(ch)
            else:
                if ch in ("\"", "'"):
                    in_quote = ch
                    out_chars.append(ch)
                elif ch == "#":
                    break
                else:
                    out_chars.append(ch)
        cleaned.append("".join(out_chars).rstrip())
    text2 = "\n".join(cleaned)

    # Restrict to the top-level `skills:` block so we don't mis-treat
    # `channels.jsonrender` or other namespaces as skills.
    skills_block_lines: list[str] = []
    in_skills = False
    for ln in text2.splitlines():
        if ln.rstrip() == "skills:":
            in_skills = True
            continue
        if in_skills and ln and not ln.startswith(" ") and ln.rstrip().endswith(":"):
            in_skills = False
            continue
        if in_skills:
            skills_block_lines.append(ln)
    skills_block = "\n".join(skills_block_lines)

    # Inline form on a single line
    inline_re = re.compile(
        r"^  ([a-z0-9][a-z0-9-]*)\s*:\s*\{\s*([^}]+)\s*\}\s*$",
        re.MULTILINE,
    )
    field_re = re.compile(r"([a-z_]+)\s*:\s*\"?([^,\"]+?)\"?\s*(?:,|$)")

    def fields_from(body: str) -> dict:
        fields: dict = {}
        for fm_ in field_re.finditer(body):
            k = fm_.group(1).strip()
            v = fm_.group(2).strip()
            if v in ("true", "false"):
                fields[k] = v == "true"
            else:
                fields[k] = v
        return fields

    for m in inline_re.finditer(skills_block):
        slug = m.group(1)
        fields = fields_from(m.group(2))
        skills[slug] = {
            "enabled": bool(fields.get("enabled", False)),
            "schedule": str(fields.get("schedule", "")),
            "var": str(fields.get("var", "")),
            "model": str(fields.get("model", "")),
        }

    # Multi-line section form (still within the skills: block only)
    section_re = re.compile(r"^  ([a-z0-9][a-z0-9-]*)\s*:\s*$", re.MULTILINE)
    lines = skills_block.splitlines()
    for i, line in enumerate(lines):
        if not section_re.match(line):
            continue
        slug = section_re.match(line).group(1)
        # Collect block until indent drops to <= 2 on a non-blank line
        j = i + 1
        block: list[str] = []
        while j < len(lines):
            ln = lines[j]
            if ln.strip() == "":
                block.append(ln)
                j += 1
                continue
            cur_indent = len(ln) - len(ln.lstrip())
            if cur_indent <= 2:
                break
            block.append(ln)
            j += 1
        block_text = "\n".join(block)
        if not block_text.strip():
            continue
        fields: dict = {}
        brace = re.search(r"\{([^}]*)\}", block_text, re.DOTALL)
        if brace:
            fields.update(fields_from(brace.group(1).replace("\n", " ")))
        else:
            for fm_ in re.finditer(r"^\s+([a-z_]+):\s*(.+?)\s*$", block_text, re.MULTILINE):
                k_ = fm_.group(1).strip()
                v_ = fm_.group(2).strip().rstrip(",").strip().strip("\"'")
                if v_.startswith("|") or v_ == "":
                    continue
                if v_ in ("true", "false"):
                    fields[k_] = v_ == "true"
                else:
                    fields[k_] = v_
        if not fields:
            continue
        existing = skills.get(slug, {})
        skills[slug] = {
            "enabled": bool(existing.get("enabled", False) or fields.get("enabled", False)),
            "schedule": existing.get("schedule") or str(fields.get("schedule", "")),
            "var": existing.get("var", "") or str(fields.get("var", "")),
            "model": existing.get("model") or str(fields.get("model", "")),
        }

    def slice_top_block(name: str) -> str:
        out_lines: list[str] = []
        in_block = False
        for ln in text2.splitlines():
            if not in_block:
                if ln.rstrip() == f"{name}:":
                    in_block = True
                continue
            # End the block when we hit another top-level key
            if ln and not ln.startswith(" ") and ln.rstrip().endswith(":"):
                break
            out_lines.append(ln)
        return "\n".join(out_lines)

    chains_block = slice_top_block("chains")
    reactive_block = slice_top_block("reactive")

    # Walk the chains block manually (same shape as reactive).
    chain_bodies: dict[str, str] = {}
    cur_chain: str | None = None
    cur_body: list[str] = []
    def flush_chain():
        if cur_chain is not None:
            chain_bodies[cur_chain] = "\n".join(cur_body)
    for ln in chains_block.splitlines():
        m = re.match(r"^  ([a-z][a-z0-9-]*):\s*$", ln)
        if m:
            flush_chain()
            cur_chain = m.group(1)
            cur_body = []
        elif cur_chain is not None:
            cur_body.append(ln)
    flush_chain()

    for cname, body in chain_bodies.items():
        sched = re.search(r"schedule:\s*\"?([^\"\n]+)\"?", body)
        steps: list[dict] = []
        for sm in re.finditer(r"-\s*parallel:\s*\[([^\]]+)\]", body):
            steps.append({"parallel": [s.strip() for s in sm.group(1).split(",")]})
        for sm in re.finditer(r"-\s*skill:\s*([a-z0-9-]+)(?:[^\n]*consume:\s*\[([^\]]+)\])?", body):
            step = {"skill": sm.group(1)}
            if sm.group(2):
                step["consume"] = [s.strip() for s in sm.group(2).split(",")]
            steps.append(step)
        chains[cname] = {"schedule": sched.group(1) if sched else "", "steps": steps}

    # Walk the reactive block manually to capture per-skill triggers.
    cur_skill: str | None = None
    skill_body: list[str] = []
    def flush():
        if cur_skill is None:
            return
        body = "\n".join(skill_body)
        triggers = []
        for tm in re.finditer(r"\{\s*on:\s*\"([^\"]+)\"\s*,\s*when:\s*\"([^\"]+)\"\s*\}", body):
            triggers.append({"on": tm.group(1), "when": tm.group(2)})
        reactive[cur_skill] = {"triggers": triggers}
    for ln in reactive_block.splitlines():
        m = re.match(r"^  ([a-z][a-z0-9-]*):\s*$", ln)
        if m:
            flush()
            cur_skill = m.group(1)
            skill_body = []
        elif cur_skill is not None:
            skill_body.append(ln)
    flush()

    return {"skills": skills, "chains": chains, "reactive": reactive}


def parse_skills_json(text: str) -> dict:
    data = json.loads(text)
    cat = {s["slug"]: s.get("category", "other") for s in data.get("skills", [])}
    return {"categories": cat, "category_labels": data.get("categories", {})}


def compute_fingerprint() -> str:
    h = hashlib.sha1()
    h.update(AEON_YML.read_bytes())
    h.update(SKILLS_JSON.read_bytes())
    for p in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        md = p.read_text(encoding="utf-8", errors="replace")
        fm_match = FRONTMATTER_RE.match(md)
        if fm_match:
            h.update(f"{p.name}:".encode())
            h.update(fm_match.group(1).encode())
        for line in md.splitlines():
            if line.startswith("depends_on:") or line.startswith("- skill:") \
               or "consume:" in line or "parallel:" in line or "trigger:" in line:
                h.update(line.encode())
        refs = sorted(set(TOPIC_RE.findall(md)))
        for r in refs:
            h.update(r.encode())
    return h.hexdigest()


def main() -> int:
    import time
    _t0 = time.time()
    def _step(label):
        print(f"  {label}: {time.time()-_t0:.2f}s", flush=True)
    fp = compute_fingerprint()
    _step("fingerprint")
    Path("/tmp/skill-graph.fingerprint").write_text(fp + "\n")

    state: dict = {}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
        except Exception:
            state = {}

    mode = "SKILL_GRAPH_NEW"
    prior_fp = state.get("input_fingerprint")
    if prior_fp == fp:
        mode = "SKILL_GRAPH_NO_CHANGE"
    elif prior_fp:
        mode = "SKILL_GRAPH_OK"

    aeon = parse_aeon_yml(AEON_YML.read_text(encoding="utf-8"))
    _step("parse_aeon_yml")
    sj = parse_skills_json(SKILLS_JSON.read_text(encoding="utf-8"))
    _step("parse_skills_json")
    skills = parse_all_skills()
    _step("parse_all_skills")

    cat_map = sj["categories"]
    for slug, info in skills.items():
        cat = cat_map.get(slug)
        if not cat or cat == "other":
            tags = info["frontmatter"].get("tags") or []
            if tags:
                cat = tags[0]
            else:
                cat = "other"
        info["category"] = cat

    for slug, conf in aeon["skills"].items():
        if slug in skills:
            skills[slug]["aeon"] = conf
        else:
            skills[slug] = {
                "slug": slug,
                "frontmatter": {},
                "writes": [],
                "reads": [],
                "path": None,
                "category": cat_map.get(slug, "other") or "other",
                "aeon": conf,
            }

    out = {
        "fingerprint": fp,
        "mode": mode,
        "prior_state": state,
        "skills": skills,
        "chains": aeon["chains"],
        "reactive": aeon["reactive"],
        "category_labels": sj["category_labels"],
    }
    Path("/tmp/skill-graph-model.json").write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"mode={mode} fingerprint={fp} skills={len(skills)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
