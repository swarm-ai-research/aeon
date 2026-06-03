#!/usr/bin/env node
/**
 * unified-graph — merge the notes graph (notegraph.json) and the skills
 * clustering (skillpacks.json) into a single navigable view, with the new
 * cross-type edges that connect a skill to every note it reads from or
 * writes to.
 *
 * Two node kinds:
 *   note   — every node in notegraph.json
 *   skill  — every skill that survives clustering in skillpacks.json
 *
 * Three edge kinds:
 *   note→note          — inherited verbatim from notegraph (hard + soft)
 *   skill→note         — derived here by scanning each SKILL.md for
 *                        memory/**, docs/**, .outputs/** path references
 *                        that match a note in the corpus
 *   skill→skill (pack) — same-pack membership from skillpacks.json, useful
 *                        as a faint "these skills cluster" cue (low weight)
 *
 * Output:
 *   unified-graph.json      — machine-readable combined graph
 *   docs/unified-graph.html — Cytoscape view, notes circles, skills squares,
 *                             pack-colored skills, hover for in/out neighbors
 *
 * Usage:
 *   node scripts/unified-graph.mjs           # writes both artifacts
 *   node scripts/unified-graph.mjs --json    # print combined JSON only
 *
 * Depends on existing notegraph.json + skillpacks.json being present (both
 * are committed and refreshed by their respective daily/weekly skills).
 * If either is missing, run their generators first.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { resolve, relative, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const NOTEGRAPH_PATH = resolve(ROOT, "notegraph.json");
const SKILLPACKS_PATH = resolve(ROOT, "skillpacks.json");
const OUT_JSON = resolve(ROOT, "unified-graph.json");
const OUT_HTML = resolve(ROOT, "docs/unified-graph.html");

// ── safe inline-JSON escape (XSS prevention for embedded graph data) ──
// Cross-corpus graph mixes note titles, skill names, and tags — any of
// which could carry `</script>` from externally-derived content. Same
// 5-replacement pattern as notegraph.mjs / skillpacks.mjs / atlas.mjs.
function safeJsonForScript(value) {
  return JSON.stringify(value)
    .replace(/</g, "\\u003c")
    .replace(/>/g, "\\u003e")
    .replace(/&/g, "\\u0026")
    .replace(/[\u2028\u2029]/g, (c) => c === "\u2028" ? "\\u2028" : "\\u2029");
}

function lsSkillFiles() {
  return execFileSync("git", ["ls-files", "--", "skills/*/SKILL.md"], { cwd: ROOT, encoding: "utf8", maxBuffer: 32 * 1024 * 1024 })
    .split("\n").filter(Boolean)
    .filter((p) => existsSync(resolve(ROOT, p)));
}

function parseSkillRefs(relPath, noteIds) {
  // Pull every plausible note-path reference out of the SKILL.md body, then
  // intersect with the set of notes the notegraph actually knows about.
  // Catches: memory/topics/X.md, docs/X.md, memory/X.md, .outputs/X (which
  // we DO map to its source note if any). We intentionally do not match
  // skills/ paths here — those are skill→skill, handled separately.
  const raw = readFileSync(resolve(ROOT, relPath), "utf8");
  const slug = relPath.split("/")[1];
  const refs = new Set();
  // 1. exact note-id matches
  for (const id of noteIds) {
    if (raw.includes(id)) refs.add(id);
  }
  // 2. catch bare references like memory/topics/X (no .md) and add .md
  for (const m of raw.matchAll(/\b(memory|docs)\/[a-zA-Z0-9_./-]+/g)) {
    const candidate = m[0].endsWith(".md") ? m[0] : `${m[0]}.md`;
    if (noteIds.has(candidate)) refs.add(candidate);
  }
  return { slug, refs: [...refs] };
}

function buildUnified() {
  if (!existsSync(NOTEGRAPH_PATH)) throw new Error(`unified-graph: missing ${relative(ROOT, NOTEGRAPH_PATH)} — run scripts/notegraph.mjs first`);
  if (!existsSync(SKILLPACKS_PATH)) throw new Error(`unified-graph: missing ${relative(ROOT, SKILLPACKS_PATH)} — run scripts/skillpacks.mjs first`);
  const notegraph = JSON.parse(readFileSync(NOTEGRAPH_PATH, "utf8"));
  const skillpacks = JSON.parse(readFileSync(SKILLPACKS_PATH, "utf8"));

  const noteIds = new Set(notegraph.nodes.map((n) => n.id));
  const skillFiles = lsSkillFiles();
  const skillRefs = skillFiles.map((p) => parseSkillRefs(p, noteIds));

  // Pack lookup: slug → { label, packIdx, packLabel }
  const packBySlug = new Map();
  skillpacks.packs.forEach((p, i) => {
    for (const m of p.members) packBySlug.set(m, { packIdx: i, packLabel: p.label, packSlug: p.slug });
  });

  // Build nodes
  const nodes = [];
  for (const n of notegraph.nodes) {
    nodes.push({
      id: `note:${n.id}`,
      kind: "note",
      label: n.title,
      path: n.id,
      dir: n.dir,
      inDegree: n.inDegree,
      outDegree: n.outDegree,
      tags: n.tags || [],
    });
  }
  for (const sr of skillRefs) {
    const meta = packBySlug.get(sr.slug);
    nodes.push({
      id: `skill:${sr.slug}`,
      kind: "skill",
      label: sr.slug,
      slug: sr.slug,
      packIdx: meta?.packIdx ?? -1,
      packLabel: meta?.packLabel ?? "—",
      refCount: sr.refs.length,
    });
  }

  // Build edges
  const edges = [];
  // 1) note → note (preserve from notegraph)
  for (const e of notegraph.edges) {
    edges.push({
      source: `note:${e.source}`,
      target: `note:${e.target}`,
      kind: "note-note",
      type: e.type,
      hardness: e.hardness,
    });
  }
  // 2) skill → note (new cross-type edges)
  for (const sr of skillRefs) {
    for (const noteId of sr.refs) {
      edges.push({
        source: `skill:${sr.slug}`,
        target: `note:${noteId}`,
        kind: "skill-note",
        type: "touches",
      });
    }
  }
  // 3) skill → skill (same pack, low-weight membership cue)
  for (const p of skillpacks.packs) {
    if (p.members.length < 2 || p.members.length > 25) continue; // pack-clique noise grows quadratically
    for (let i = 0; i < p.members.length; i++) for (let j = i + 1; j < p.members.length; j++) {
      edges.push({
        source: `skill:${p.members[i]}`,
        target: `skill:${p.members[j]}`,
        kind: "skill-skill",
        type: `pack:${p.slug}`,
      });
    }
  }

  // Stats
  const stats = {
    notes: notegraph.nodes.length,
    skills: skillFiles.length,
    nodes: nodes.length,
    edges: edges.length,
    noteNoteEdges: edges.filter((e) => e.kind === "note-note").length,
    skillNoteEdges: edges.filter((e) => e.kind === "skill-note").length,
    skillSkillEdges: edges.filter((e) => e.kind === "skill-skill").length,
    skillsWithNoteRefs: skillRefs.filter((s) => s.refs.length > 0).length,
    topTouchedNotes: topByIncoming(edges, "skill-note", "target", 8),
    topTouchingSkills: topByIncoming(edges, "skill-note", "source", 8),
  };

  return {
    generatedAt: new Date().toISOString(),
    stats,
    nodes,
    edges,
  };
}

function topByIncoming(edges, kind, side, k) {
  const counts = new Map();
  for (const e of edges) if (e.kind === kind) counts.set(e[side], (counts.get(e[side]) || 0) + 1);
  return [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, k).map(([id, n]) => ({ id, count: n }));
}

// ── HTML view ──────────────────────────────────────────────────────────────
function renderHtml(graph) {
  const json = safeJsonForScript(graph);
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Unified Graph — notes ↔ skills</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{color-scheme:dark}
html,body{margin:0;height:100%;font:14px/1.4 system-ui,sans-serif;background:#0e0f12;color:#e6e6e6}
#toolbar{position:fixed;top:8px;left:8px;right:8px;z-index:10;display:flex;gap:8px;align-items:center;padding:8px 12px;background:rgba(20,22,28,0.92);border:1px solid #2a2d35;border-radius:8px}
#toolbar input[type=search]{flex:1;padding:6px 10px;background:#1a1c22;border:1px solid #2a2d35;border-radius:6px;color:#e6e6e6}
#toolbar label{display:flex;align-items:center;gap:4px;user-select:none;font-size:12px}
#stats{color:#888;font-size:12px}
#cy{width:100vw;height:100vh}
#panel{position:fixed;right:8px;top:56px;width:340px;max-height:calc(100vh - 80px);overflow:auto;padding:12px 14px;background:rgba(20,22,28,0.95);border:1px solid #2a2d35;border-radius:8px;display:none}
#panel h3{margin:0 0 6px;font-size:14px}
#panel .meta{color:#888;font-size:12px;margin-bottom:8px}
#panel ul{margin:4px 0 8px;padding-left:18px}
#panel a{color:#7cc1ff;text-decoration:none;cursor:pointer}
.legend{display:flex;gap:10px;align-items:center;font-size:12px;color:#aaa}
.swatch{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:4px;vertical-align:middle}
.sq{border-radius:2px}
</style></head><body>
<div id="toolbar">
  <strong>Unified Graph</strong>
  <input id="search" type="search" placeholder="Search…">
  <label><input id="noteToggle" type="checkbox" checked> notes</label>
  <label><input id="skillToggle" type="checkbox" checked> skills</label>
  <label><input id="skillSkillToggle" type="checkbox"> pack ties</label>
  <span class="legend">
    <span><span class="swatch" style="background:#7cc1ff"></span>memory</span>
    <span><span class="swatch" style="background:#f7a072"></span>docs</span>
    <span><span class="swatch sq" style="background:#a78bfa"></span>skill</span>
  </span>
  <span id="stats"></span>
</div>
<div id="cy"></div><div id="panel"></div>
<script src="https://unpkg.com/cytoscape@3.30.2/dist/cytoscape.min.js"></script>
<script>
const G = ${json};
const noteColor = (dir) => dir === "memory" ? "#7cc1ff" : dir === "docs" ? "#f7a072" : "#bbb";
const els = [
  ...G.nodes.map(n => ({
    data: { id: n.id, label: n.label, kind: n.kind, dir: n.dir, packLabel: n.packLabel },
    classes: n.kind,
  })),
  ...G.edges.map((e, i) => ({
    data: { id: 'e' + i, source: e.source, target: e.target, kind: e.kind, type: e.type, hardness: e.hardness || '' },
    classes: e.kind + (e.hardness ? ' ' + e.hardness : ''),
  })),
];

const cy = cytoscape({
  container: document.getElementById('cy'),
  elements: els,
  style: [
    { selector: 'node.note', style: {
      'background-color': (n) => noteColor(n.data('dir')),
      'shape': 'ellipse',
      'label': 'data(label)', 'color': '#e6e6e6', 'font-size': 9,
      'text-valign': 'center', 'text-halign': 'center',
      'text-outline-color': '#0e0f12', 'text-outline-width': 1.5,
      'width': 18, 'height': 18,
    }},
    { selector: 'node.skill', style: {
      'background-color': '#a78bfa',
      'shape': 'round-rectangle',
      'label': 'data(label)', 'color': '#e6e6e6', 'font-size': 9,
      'text-valign': 'center', 'text-halign': 'center',
      'text-outline-color': '#0e0f12', 'text-outline-width': 1.5,
      'width': 22, 'height': 14,
    }},
    { selector: 'edge', style: {
      'width': 0.6, 'curve-style': 'bezier',
      'line-color': '#3a3d45', 'target-arrow-color': '#3a3d45',
      'target-arrow-shape': 'triangle', 'arrow-scale': 0.7,
      'opacity': 0.4,
    }},
    { selector: 'edge.soft', style: { 'line-style': 'dashed', 'opacity': 0.25 }},
    { selector: 'edge.skill-note', style: { 'line-color': '#a78bfa', 'target-arrow-color': '#a78bfa', 'width': 1.0, 'opacity': 0.6 }},
    { selector: 'edge.skill-skill', style: { 'line-color': '#444', 'opacity': 0.15, 'display': 'none' }},
    { selector: 'node.faded, edge.faded', style: { 'opacity': 0.08 }},
    { selector: 'node.hit', style: { 'border-width': 2, 'border-color': '#fff' }},
  ],
  layout: { name: 'cose', animate: false, idealEdgeLength: 90, nodeRepulsion: 5500, gravity: 0.4 },
});

document.getElementById('stats').textContent =
  G.stats.nodes + ' nodes · ' + G.stats.edges + ' edges · ' + G.stats.skillNoteEdges + ' cross';

const setKindVis = (kind, on) => cy.nodes('.' + kind).style('display', on ? 'element' : 'none');
document.getElementById('noteToggle').addEventListener('change', (e) => setKindVis('note', e.target.checked));
document.getElementById('skillToggle').addEventListener('change', (e) => setKindVis('skill', e.target.checked));
document.getElementById('skillSkillToggle').addEventListener('change', (e) => {
  cy.edges('.skill-skill').style('display', e.target.checked ? 'element' : 'none');
});

const el = (t,o={}) => { const n=document.createElement(t); if(o.text!==undefined)n.textContent=o.text; if(o.className)n.className=o.className; if(o.attrs)for(const[k,v]of Object.entries(o.attrs))n.setAttribute(k,v); if(o.children)for(const c of o.children)n.appendChild(c); return n; };
const panel = document.getElementById('panel');

cy.on('tap', 'node', (evt) => {
  const n = evt.target;
  panel.replaceChildren();
  panel.style.display = 'block';
  panel.appendChild(el('h3', { text: n.data('label') }));
  panel.appendChild(el('div', { className: 'meta', text: n.id() + (n.data('packLabel') && n.data('packLabel') !== '—' ? ' · pack: ' + n.data('packLabel') : '') }));
  const out = n.outgoers('edge').map(e => ({ to: e.target().data('label'), id: e.target().id(), kind: e.data('kind'), type: e.data('type') }));
  const inn = n.incomers('edge').map(e => ({ from: e.source().data('label'), id: e.source().id(), kind: e.data('kind'), type: e.data('type') }));
  const goto = (id) => { const t = cy.getElementById(id); cy.animate({ center: { eles: t }, zoom: 1.4 }, { duration: 300 }); t.trigger('tap'); };
  const makeList = (rows, key) => {
    const ul = el('ul');
    for (const r of rows.slice(0, 25)) {
      const a = el('a', { text: r[key], attrs: { href: '#' } });
      a.addEventListener('click', (ev) => { ev.preventDefault(); goto(r.id); });
      const meta = el('span', { className: 'meta', text: ' · ' + r.kind + (r.type ? ' (' + r.type + ')' : '') });
      ul.appendChild(el('li', { children: [a, meta] }));
    }
    return ul;
  };
  panel.appendChild(el('strong', { text: 'Outgoing (' + out.length + ')' }));
  panel.appendChild(makeList(out, 'to'));
  panel.appendChild(el('strong', { text: 'Incoming (' + inn.length + ')' }));
  panel.appendChild(makeList(inn, 'from'));
});
cy.on('tap', (evt) => { if (evt.target === cy) panel.style.display = 'none'; });

document.getElementById('search').addEventListener('input', (e) => {
  const q = e.target.value.trim().toLowerCase();
  cy.elements().removeClass('faded hit');
  if (!q) return;
  const matches = cy.nodes().filter(n => n.data('label').toLowerCase().includes(q) || n.id().toLowerCase().includes(q));
  if (matches.length === 0) return;
  cy.elements().not(matches.union(matches.neighborhood())).addClass('faded');
  matches.addClass('hit');
});
</script></body></html>
`;
}

// ── main ───────────────────────────────────────────────────────────────────
function main() {
  const argv = process.argv.slice(2);
  const graph = buildUnified();

  if (argv.includes("--json")) {
    process.stdout.write(JSON.stringify(graph, null, 2));
    return;
  }

  mkdirSync(dirname(OUT_HTML), { recursive: true });
  writeFileSync(OUT_JSON, JSON.stringify(graph, null, 2));
  writeFileSync(OUT_HTML, renderHtml(graph));

  const s = graph.stats;
  console.log(`unified-graph: ${s.notes} notes + ${s.skills} skills · ${s.skillNoteEdges} cross-type edges (${s.skillsWithNoteRefs} skills touch notes)`);
  console.log(`  top touched notes:`);
  for (const t of s.topTouchedNotes.slice(0, 5)) console.log(`    ${t.count}  ${t.id}`);
  console.log(`  top touching skills:`);
  for (const t of s.topTouchingSkills.slice(0, 5)) console.log(`    ${t.count}  ${t.id}`);
  console.log(`  wrote ${relative(ROOT, OUT_JSON)}`);
  console.log(`  wrote ${relative(ROOT, OUT_HTML)}`);
}

main();
