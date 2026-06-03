#!/usr/bin/env node
/**
 * notegraph — extract a navigable graph from the repo's notes.
 *
 * Scans memory/** and docs/** for markdown files and emits:
 *   - notegraph.json  (nodes + edges, machine-readable)
 *   - docs/notegraph.md   (Mermaid, committable, mirrors docs/skill-graph.md)
 *   - docs/notegraph.html (Cytoscape.js, interactive, served from GitHub Pages)
 *
 * Edge types
 *   hard   — explicit: [[wikilinks]], markdown [text](path.md), bare path mentions
 *   soft   — implicit: shared tags, shared H2/H3 headings, filename-mentioned-in-body
 *
 * Soft edges are tagged so the HTML view can toggle them off.
 *
 * Usage:
 *   node scripts/notegraph.mjs            # writes all three artifacts
 *   node scripts/notegraph.mjs --json     # only print JSON to stdout
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { resolve, relative, join, basename, extname, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const SCAN_DIRS = ["memory", "docs"];
// Paths skipped even when tracked: logs are dated daily files that would
// dominate the graph without informing it; the notegraph outputs below are
// themselves part of the scanned corpus and would otherwise re-ingest their
// own generated labels as bare name-mentions on the next run (Codex PR #106).
const SKIP_PATH_RE = /(^|\/)(node_modules|_site|memory\/logs)(\/|$)/;
const SKIP_FILE_RE = /^docs\/notegraph(-speedrun)?\.(md|html)$/;
const OUT_JSON = resolve(ROOT, "notegraph.json");
const OUT_MERMAID = resolve(ROOT, "docs/notegraph.md");
const OUT_HTML = resolve(ROOT, "docs/notegraph.html");
const OUT_SPEEDRUN = resolve(ROOT, "docs/notegraph-speedrun.html");

// ── safe inline-JSON escape ───────────────────────────────────────────────
// Standard pattern for embedding JSON inside a <script> tag — a note title,
// tag, or any user-influenced string containing `</script>` would otherwise
// terminate the inline script and let attacker JS execute on the published
// page. U+2028 / U+2029 are valid JSON whitespace but illegal in JS string
// literals; `>` and `&` are belt-and-suspenders against attribute / comment
// contexts even though our embed is plain script-content. Matches what
// Webpack, lodash, and most server-render libs do.
function safeJsonForScript(value) {
  return JSON.stringify(value)
    .replace(/</g, "\\u003c")
    .replace(/>/g, "\\u003e")
    .replace(/&/g, "\\u0026")
    .replace(/[\u2028\u2029]/g, (c) => c === "\u2028" ? "\\u2028" : "\\u2029");
}


// ── scan ───────────────────────────────────────────────────────────────────
// Only scan files tracked by git. Untracked drafts in the working tree would
// otherwise leak into the committed graph as dangling references that
// disappear on the next CI run, churning the graph every day.
function collectFiles() {
  let out;
  try {
    const stdout = execFileSync(
      "git",
      ["ls-files", "--", ...SCAN_DIRS.map((d) => `${d}/*.md`)],
      { cwd: ROOT, encoding: "utf8", maxBuffer: 32 * 1024 * 1024 },
    );
    out = stdout.split("\n").filter(Boolean);
  } catch (err) {
    // Not a git repo or git unavailable — surface the failure, don't silently
    // fall back to a filesystem walk that would reintroduce the dangling-refs bug.
    throw new Error(`notegraph: git ls-files failed (${err.message}). Run inside a git checkout.`);
  }
  return out
    .filter((p) => extname(p) === ".md")
    .filter((p) => !SKIP_PATH_RE.test(p))
    .filter((p) => !SKIP_FILE_RE.test(p))
    .filter((p) => existsSync(resolve(ROOT, p))) // skip tracked-but-deleted-locally
    .map((p) => resolve(ROOT, p))
    .sort();
}

// ── parse ──────────────────────────────────────────────────────────────────
const RE_WIKILINK = /\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]/g;
const RE_MDLINK = /\[([^\]]+)\]\(([^)]+)\)/g;
const RE_TAG = /(?:^|\s)#([a-z][a-z0-9_-]{1,30})\b/gi;
const RE_HEADING = /^(#{2,3})\s+(.+?)\s*$/gm;
const RE_FRONTMATTER = /^---\n([\s\S]*?)\n---/;

function parseFile(absPath) {
  const rel = relative(ROOT, absPath);
  const id = rel;
  const raw = readFileSync(absPath, "utf8");
  let body = raw;
  let title = basename(rel, ".md");
  let tags = new Set();

  const fm = raw.match(RE_FRONTMATTER);
  if (fm) {
    body = raw.slice(fm[0].length);
    const t = fm[1].match(/^title:\s*(.+)$/m);
    if (t) title = t[1].trim().replace(/^["']|["']$/g, "");
    const tg = fm[1].match(/^tags:\s*\[(.+)\]/m);
    if (tg) tg[1].split(",").forEach((x) => tags.add(x.trim().replace(/^["']|["']$/g, "")));
  } else {
    // first H1 wins as title
    const h1 = body.match(/^#\s+(.+)$/m);
    if (h1) title = h1[1].trim();
  }

  // Strip fenced + inline code before tag/heading extraction — code blocks
  // pollute the graph with CSS hex colors, shell flags, etc.
  const stripped = body
    .replace(/```[\s\S]*?```/g, "")
    .replace(/`[^`\n]+`/g, "");

  // inline #tags — require at least one non-hex letter to avoid #fafafa-style false positives
  for (const m of stripped.matchAll(RE_TAG)) {
    const t = m[1].toLowerCase();
    if (/^[0-9a-f]{6}$/.test(t)) continue;
    tags.add(t);
  }

  // H2/H3 headings (lowercased, for soft co-heading edges) — from stripped body
  const headings = new Set();
  for (const m of stripped.matchAll(RE_HEADING)) {
    const h = m[2].toLowerCase().replace(/[^\w\s-]/g, "").trim();
    if (h && h.length > 3) headings.add(h);
  }

  // wikilinks
  const wikilinks = [];
  for (const m of body.matchAll(RE_WIKILINK)) wikilinks.push(m[1].trim());

  // markdown links — keep only intra-repo .md links
  const mdlinks = [];
  for (const m of body.matchAll(RE_MDLINK)) {
    const href = m[2].split("#")[0].split("?")[0];
    if (!href || /^https?:/i.test(href) || href.startsWith("mailto:")) continue;
    if (!href.endsWith(".md")) continue;
    mdlinks.push(href);
  }

  return { id, rel, abs: absPath, title, tags, headings, wikilinks, mdlinks, body };
}

// ── resolve edges ──────────────────────────────────────────────────────────
function buildIndex(notes) {
  const byId = new Map();
  const byBasename = new Map(); // basename without .md → [ids]
  const byTitle = new Map();    // lowercased title → [ids]
  for (const n of notes) {
    byId.set(n.id, n);
    const b = basename(n.rel, ".md").toLowerCase();
    if (!byBasename.has(b)) byBasename.set(b, []);
    byBasename.get(b).push(n.id);
    const t = n.title.toLowerCase();
    if (!byTitle.has(t)) byTitle.set(t, []);
    byTitle.get(t).push(n.id);
  }
  return { byId, byBasename, byTitle };
}

function resolveTarget(note, target, idx) {
  // 1) treat as path relative to note's dir
  const tryPath = (p) => {
    const candidate = relative(ROOT, resolve(dirname(note.abs), p));
    if (idx.byId.has(candidate)) return candidate;
    return null;
  };
  if (target.endsWith(".md")) {
    const p = tryPath(target);
    if (p) return p;
    // try repo-root relative
    if (idx.byId.has(target)) return target;
  }
  // 2) wikilink / bare name → basename or title match
  const key = target.toLowerCase().replace(/\.md$/, "");
  const byB = idx.byBasename.get(key);
  if (byB && byB.length === 1) return byB[0];
  const byT = idx.byTitle.get(key);
  if (byT && byT.length === 1) return byT[0];
  // ambiguous or missing
  return null;
}

function buildEdges(notes) {
  const idx = buildIndex(notes);
  const edges = [];
  const seen = new Set();
  const push = (source, target, type, weight, meta) => {
    if (source === target) return;
    const key = `${source}|${target}|${type}`;
    if (seen.has(key)) return;
    seen.add(key);
    const edge = { source, target, type, weight };
    if (meta) Object.assign(edge, meta);
    edges.push(edge);
  };

  // ── hard edges ───────────────────────────────────────────────────────────
  for (const n of notes) {
    for (const w of n.wikilinks) {
      const t = resolveTarget(n, w, idx);
      if (t) push(n.id, t, "wikilink", 1.0);
    }
    for (const m of n.mdlinks) {
      const t = resolveTarget(n, m, idx);
      if (t) push(n.id, t, "mdlink", 1.0);
    }
    // bare path mentions: scan body for `memory/...md` or `docs/...md` substrings
    const body = n.body;
    for (const other of notes) {
      if (other.id === n.id) continue;
      // Look for exact relpath OR for basename surrounded by non-word chars
      if (body.includes(other.id)) {
        push(n.id, other.id, "path-mention", 0.8);
        continue;
      }
      const b = basename(other.rel, ".md");
      if (b.length < 5) continue; // avoid noise from short names
      const re = new RegExp(`(?:^|[^\\w/-])${b.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\$&")}(?=[^\\w]|$)`);
      if (re.test(body)) push(n.id, other.id, "name-mention", 0.5);
    }
  }

  // ── soft edges: shared tags & shared headings (undirected, emitted both ways) ──
  // group notes by tag, emit clique edges (capped to avoid explosion)
  const byTag = new Map();
  for (const n of notes) for (const t of n.tags) {
    if (!byTag.has(t)) byTag.set(t, []);
    byTag.get(t).push(n.id);
  }
  for (const [tag, ids] of byTag) {
    if (ids.length < 2 || ids.length > 12) continue; // skip universal tags
    for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) {
      push(ids[i], ids[j], `tag:${tag}`, 0.4);
      push(ids[j], ids[i], `tag:${tag}`, 0.4);
    }
  }

  const byHeading = new Map();
  for (const n of notes) for (const h of n.headings) {
    if (!byHeading.has(h)) byHeading.set(h, []);
    byHeading.get(h).push(n.id);
  }
  for (const [h, ids] of byHeading) {
    if (ids.length < 2 || ids.length > 6) continue;
    for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) {
      push(ids[i], ids[j], "co-heading", 0.3);
      push(ids[j], ids[i], "co-heading", 0.3);
    }
  }

  // ── soft edges: TF-IDF cosine similarity, top-3 per node ≥ 0.25 ─────────
  // Lexical overlap only — no embeddings, no API calls, deterministic.
  // Stripped code is used so fenced examples don't dominate term frequency.
  const SIM_TOP_K = 3;
  const SIM_MIN = 0.25;
  const similarities = computeSimilarities(notes, SIM_TOP_K, SIM_MIN);
  for (const { source, target, score, shared } of similarities) {
    // Emit both directions; the score is symmetric and per-direction top-K
    // selection can pick asymmetric neighbors.
    push(source, target, "similar", score, { shared });
  }

  return edges;
}

// ── tf-idf cosine similarity ──────────────────────────────────────────────
const STOPWORDS = new Set((
  "a an and are as at be but by for from has have he her his how if in into is it its " +
  "of on or that the their they this to was we were what when where which who will with " +
  "you your i me my our us am do does did been being would could should may might can " +
  "not no nor so than then there here also any all each some such only just very more " +
  "most other than them these those one two three new set use used using uses run runs " +
  "running ran via per eg ie etc"
).split(" "));

function tokenize(text) {
  // Lowercase, split on non-alphanumeric, drop short/stopword/all-digit tokens.
  const out = [];
  for (const raw of text.toLowerCase().split(/[^a-z0-9]+/)) {
    if (raw.length < 3 || raw.length > 30) continue;
    if (/^[0-9]+$/.test(raw)) continue;
    if (STOPWORDS.has(raw)) continue;
    out.push(raw);
  }
  return out;
}

function computeSimilarities(notes, topK, minScore) {
  // Build per-note term-frequency maps from the same stripped body the
  // tag/heading extractor sees, so code blocks don't skew vectors.
  const tfs = notes.map((n) => {
    // Strip code fences, inline code, raw HTML tags, and CSS-style inline
    // attributes. Jekyll templates in docs/ carry HTML that would otherwise
    // make every layout-heavy file falsely similar to every other one.
    const stripped = n.body
      .replace(/```[\s\S]*?```/g, "")
      .replace(/`[^`\n]+`/g, "")
      .replace(/<style[\s\S]*?<\/style>/gi, "")
      .replace(/<script[\s\S]*?<\/script>/gi, "")
      .replace(/<[^>]+>/g, " ")
      .replace(/style="[^"]*"/g, " ")
      // Jekyll Liquid template syntax — {% if … %}, {% endfor %}, {{ var | filter }}
      .replace(/\{%[\s\S]*?%\}/g, " ")
      .replace(/\{\{[\s\S]*?\}\}/g, " ");
    const tokens = tokenize(stripped + " " + n.title);
    const tf = new Map();
    for (const t of tokens) tf.set(t, (tf.get(t) || 0) + 1);
    return tf;
  });

  // Document frequency for IDF.
  const df = new Map();
  for (const tf of tfs) for (const term of tf.keys()) df.set(term, (df.get(term) || 0) + 1);

  const N = notes.length;
  // Drop terms that appear in >50% of docs (too generic to discriminate) or only 1 doc (no overlap possible).
  const usefulTerms = new Set();
  for (const [term, freq] of df) if (freq >= 2 && freq <= N * 0.5) usefulTerms.add(term);

  // Build sparse TF-IDF vectors keyed by term.
  const vectors = tfs.map((tf) => {
    const v = new Map();
    let normSq = 0;
    for (const [term, count] of tf) {
      if (!usefulTerms.has(term)) continue;
      const idf = Math.log(N / df.get(term));
      const w = (1 + Math.log(count)) * idf;
      v.set(term, w);
      normSq += w * w;
    }
    return { v, norm: Math.sqrt(normSq) };
  });

  // Compute pairwise cosine; keep top-K per source above threshold.
  const out = [];
  for (let i = 0; i < notes.length; i++) {
    const { v: vi, norm: ni } = vectors[i];
    if (ni === 0) continue;
    const scored = [];
    for (let j = 0; j < notes.length; j++) {
      if (i === j) continue;
      const { v: vj, norm: nj } = vectors[j];
      if (nj === 0) continue;
      // Iterate the smaller vector.
      const [small, large] = vi.size < vj.size ? [vi, vj] : [vj, vi];
      let dot = 0;
      const sharedTerms = [];
      for (const [term, w] of small) {
        const w2 = large.get(term);
        if (w2 !== undefined) { dot += w * w2; sharedTerms.push([term, w * w2]); }
      }
      const score = dot / (ni * nj);
      if (score < minScore) continue;
      sharedTerms.sort((a, b) => b[1] - a[1]);
      scored.push({
        source: notes[i].id,
        target: notes[j].id,
        score: Math.round(score * 1000) / 1000,
        shared: sharedTerms.slice(0, 5).map(([t]) => t),
      });
    }
    scored.sort((a, b) => b.score - a.score);
    for (const e of scored.slice(0, topK)) out.push(e);
  }
  return out;
}

function classifyHardness(type) {
  if (type === "wikilink" || type === "mdlink" || type === "path-mention" || type === "name-mention") return "hard";
  return "soft";
}

function buildGraph() {
  const files = collectFiles();
  const notes = files.map(parseFile);
  const edges = buildEdges(notes);

  // degree stats
  const inDeg = new Map(), outDeg = new Map();
  for (const e of edges) {
    outDeg.set(e.source, (outDeg.get(e.source) || 0) + 1);
    inDeg.set(e.target, (inDeg.get(e.target) || 0) + 1);
  }

  const nodes = notes.map((n) => ({
    id: n.id,
    title: n.title,
    dir: n.rel.split("/")[0],
    tags: [...n.tags],
    inDegree: inDeg.get(n.id) || 0,
    outDegree: outDeg.get(n.id) || 0,
  }));

  const annotatedEdges = edges.map((e) => ({ ...e, hardness: classifyHardness(e.type) }));

  return {
    generatedAt: new Date().toISOString(),
    stats: {
      nodes: nodes.length,
      edges: annotatedEdges.length,
      hard: annotatedEdges.filter((e) => e.hardness === "hard").length,
      soft: annotatedEdges.filter((e) => e.hardness === "soft").length,
      orphans: nodes.filter((n) => n.inDegree === 0 && n.outDegree === 0).length,
    },
    nodes,
    edges: annotatedEdges,
  };
}

// ── renderers ──────────────────────────────────────────────────────────────
function sanitizeMermaidId(id) {
  return id.replace(/[^a-zA-Z0-9]/g, "_");
}

function renderMermaid(graph) {
  // Mermaid chokes on huge graphs — limit to hard edges + top-degree nodes.
  const hardEdges = graph.edges.filter((e) => e.hardness === "hard");
  const keep = new Set();
  for (const e of hardEdges) { keep.add(e.source); keep.add(e.target); }
  const nodes = graph.nodes.filter((n) => keep.has(n.id));

  const byDir = new Map();
  for (const n of nodes) {
    if (!byDir.has(n.dir)) byDir.set(n.dir, []);
    byDir.get(n.dir).push(n);
  }

  let out = `# Note Graph\n\n`;
  out += `> Auto-generated by \`scripts/notegraph.mjs\` on ${graph.generatedAt.slice(0, 10)}.\n`;
  out += `> Re-run with \`node scripts/notegraph.mjs\` to update.\n\n`;
  out += `**${graph.stats.nodes} notes**, ${graph.stats.hard} hard edges, ${graph.stats.soft} soft edges, ${graph.stats.orphans} orphans.\n\n`;
  out += `Hard edges only are shown below. For the full interactive graph (soft edges + zoom + search), open [\`notegraph.html\`](./notegraph.html).\n\n`;
  out += "```mermaid\nflowchart LR\n";
  for (const [dir, ns] of byDir) {
    out += `  subgraph ${sanitizeMermaidId(dir)}["${dir}/ (${ns.length})"]\n`;
    for (const n of ns) {
      const label = n.title.replace(/"/g, "'").slice(0, 40);
      out += `    ${sanitizeMermaidId(n.id)}["${label}"]\n`;
    }
    out += "  end\n";
  }
  for (const e of hardEdges) {
    const arrow = e.type === "wikilink" || e.type === "mdlink" ? "-->" : "-.->";
    out += `  ${sanitizeMermaidId(e.source)} ${arrow} ${sanitizeMermaidId(e.target)}\n`;
  }
  out += "```\n\n";
  out += "## Edge legend\n\n";
  out += "| Style | Meaning |\n|---|---|\n";
  out += "| `-->` solid | explicit `[[wikilink]]` or markdown link |\n";
  out += "| `-.->` dotted | path or filename mention in body text |\n\n";
  out += "Soft edges (shared tags, co-headings) are omitted here to keep the diagram legible — they live in `notegraph.json` and the HTML view.\n";
  return out;
}

function renderHtml(graph) {
  const json = safeJsonForScript(graph);
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Note Graph</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  html, body { margin: 0; height: 100%; font: 14px/1.4 system-ui, sans-serif; background: #0e0f12; color: #e6e6e6; }
  #toolbar { position: fixed; top: 8px; left: 8px; right: 8px; z-index: 10; display: flex; gap: 8px; align-items: center; padding: 8px 12px; background: rgba(20,22,28,0.92); border: 1px solid #2a2d35; border-radius: 8px; backdrop-filter: blur(6px); }
  #toolbar input[type=search] { flex: 1; padding: 6px 10px; background: #1a1c22; border: 1px solid #2a2d35; border-radius: 6px; color: #e6e6e6; }
  #toolbar label { display: flex; align-items: center; gap: 4px; user-select: none; }
  #stats { color: #888; font-size: 12px; }
  #cy { width: 100vw; height: 100vh; }
  #panel { position: fixed; right: 8px; top: 56px; width: 320px; max-height: calc(100vh - 80px); overflow: auto; padding: 12px 14px; background: rgba(20,22,28,0.95); border: 1px solid #2a2d35; border-radius: 8px; display: none; }
  #panel h3 { margin: 0 0 6px; font-size: 14px; }
  #panel .meta { color: #888; font-size: 12px; margin-bottom: 8px; }
  #panel ul { margin: 4px 0 8px; padding-left: 18px; }
  #panel a { color: #7cc1ff; text-decoration: none; }
</style>
</head>
<body>
<div id="toolbar">
  <strong>Note Graph</strong>
  <input id="search" type="search" placeholder="Search title or path…">
  <label><input id="softToggle" type="checkbox" checked> soft edges</label>
  <span id="stats"></span>
</div>
<div id="cy"></div>
<div id="panel"></div>
<script src="https://unpkg.com/cytoscape@3.30.2/dist/cytoscape.min.js"></script>
<script>
  const GRAPH = ${json};
  const colorFor = (dir) => dir === "memory" ? "#7cc1ff" : dir === "docs" ? "#f7a072" : "#bbb";

  const elements = [
    ...GRAPH.nodes.map(n => ({
      data: { id: n.id, label: n.title, dir: n.dir, tags: n.tags, inDeg: n.inDegree, outDeg: n.outDegree },
      classes: n.dir,
    })),
    ...GRAPH.edges.map((e, i) => ({
      data: { id: 'e' + i, source: e.source, target: e.target, type: e.type, hardness: e.hardness, score: e.weight, shared: e.shared || [] },
      classes: e.hardness + (e.type === 'similar' ? ' similar' : ''),
    })),
  ];

  const cy = cytoscape({
    container: document.getElementById('cy'),
    elements,
    style: [
      { selector: 'node', style: {
        'background-color': (n) => colorFor(n.data('dir')),
        'label': 'data(label)',
        'color': '#e6e6e6', 'font-size': 10,
        'text-valign': 'center', 'text-halign': 'center',
        'text-outline-color': '#0e0f12', 'text-outline-width': 2,
        'width': (n) => 12 + Math.min(40, (n.data('inDeg') + n.data('outDeg')) * 2),
        'height': (n) => 12 + Math.min(40, (n.data('inDeg') + n.data('outDeg')) * 2),
      }},
      { selector: 'edge', style: {
        'width': 1, 'curve-style': 'bezier',
        'line-color': '#3a3d45', 'target-arrow-color': '#3a3d45',
        'target-arrow-shape': 'triangle', 'arrow-scale': 0.8,
        'opacity': 0.7,
      }},
      { selector: 'edge.soft', style: { 'line-style': 'dashed', 'opacity': 0.35 }},
      { selector: 'edge.similar', style: { 'line-color': '#a78bfa', 'target-arrow-color': '#a78bfa' }},
      { selector: 'node.faded, edge.faded', style: { 'opacity': 0.08 }},
      { selector: 'node.hit', style: { 'border-width': 2, 'border-color': '#fff' }},
    ],
    layout: { name: 'cose', animate: false, idealEdgeLength: 90, nodeRepulsion: 4500 },
  });

  document.getElementById('stats').textContent =
    GRAPH.stats.nodes + ' nodes · ' + GRAPH.stats.hard + ' hard · ' + GRAPH.stats.soft + ' soft · ' + GRAPH.stats.orphans + ' orphans';

  document.getElementById('softToggle').addEventListener('change', (e) => {
    cy.edges('.soft').style('display', e.target.checked ? 'element' : 'none');
  });

  // Build the panel with DOM nodes (never innerHTML) so a note title or
  // tag containing HTML tags displays as text rather than executing. The
  // graph ingests memory/** which can include externally-derived content.
  const panel = document.getElementById('panel');
  const el = (tag, opts = {}) => {
    const e = document.createElement(tag);
    if (opts.text !== undefined) e.textContent = opts.text;
    if (opts.className) e.className = opts.className;
    if (opts.attrs) for (const [k, v] of Object.entries(opts.attrs)) e.setAttribute(k, v);
    if (opts.children) for (const c of opts.children) e.appendChild(c);
    return e;
  };
  const neighborItem = (label, id, type, onClick, extra) => {
    const a = el('a', { text: label, attrs: { href: '#' } });
    a.addEventListener('click', (ev) => { ev.preventDefault(); onClick(id); });
    const meta = el('span', { className: 'meta', text: ' ' + type + (extra ? ' · ' + extra : '') });
    return el('li', { children: [a, meta] });
  };
  const edgeExtra = (e) => {
    if (e.data('type') === 'similar') {
      const shared = e.data('shared') || [];
      const score = e.data('score');
      return (score ? score.toFixed(2) : '') + (shared.length ? ' [' + shared.join(', ') + ']' : '');
    }
    return '';
  };
  cy.on('tap', 'node', (evt) => {
    const n = evt.target;
    const outgoing = n.outgoers('edge').map(e => ({ to: e.target().data('label'), id: e.target().id(), type: e.data('type'), extra: edgeExtra(e) }));
    const incoming = n.incomers('edge').map(e => ({ from: e.source().data('label'), id: e.source().id(), type: e.data('type'), extra: edgeExtra(e) }));
    const gotoNode = (id) => {
      const target = cy.getElementById(id);
      cy.animate({ center: { eles: target }, zoom: 1.4 }, { duration: 300 });
      target.trigger('tap');
    };
    panel.replaceChildren();
    panel.style.display = 'block';
    panel.appendChild(el('h3', { text: n.data('label') }));
    panel.appendChild(el('div', { className: 'meta', text: n.id() }));
    if (n.data('tags').length) {
      panel.appendChild(el('div', { className: 'meta', text: 'tags: ' + n.data('tags').join(', ') }));
    }
    panel.appendChild(el('strong', { text: 'Outgoing (' + outgoing.length + ')' }));
    panel.appendChild(el('ul', { children: outgoing.map(o => neighborItem(o.to, o.id, o.type, gotoNode, o.extra)) }));
    panel.appendChild(el('strong', { text: 'Incoming (' + incoming.length + ')' }));
    panel.appendChild(el('ul', { children: incoming.map(o => neighborItem(o.from, o.id, o.type, gotoNode, o.extra)) }));
  });
  cy.on('tap', (evt) => { if (evt.target === cy) panel.style.display = 'none'; });

  const search = document.getElementById('search');
  search.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    cy.elements().removeClass('faded hit');
    if (!q) return;
    const matches = cy.nodes().filter(n => n.data('label').toLowerCase().includes(q) || n.id().toLowerCase().includes(q));
    if (matches.length === 0) return;
    const keep = matches.union(matches.neighborhood());
    cy.elements().not(keep).addClass('faded');
    matches.addClass('hit');
  });
</script>
</body>
</html>
`;
}

// ── speedrun game ──────────────────────────────────────────────────────────
// Wikispeedruns-style: pick a random start + target, navigate via links only,
// score by clicks + time. Self-contained HTML with graph inlined so it works
// from a plain file:// open (no static server needed).
function renderSpeedrunHtml(graph) {
  const json = safeJsonForScript(graph);
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Note Graph Speedrun</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{color-scheme:dark}
html,body{margin:0;padding:0;height:100%;font:15px/1.5 system-ui,-apple-system,sans-serif;background:#0e0f12;color:#e6e6e6}
body{display:flex;flex-direction:column}
header{padding:14px 20px;border-bottom:1px solid #2a2d35;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
header h1{margin:0;font-size:16px;font-weight:600}
.stat{color:#888;font-size:13px}
.stat strong{color:#e6e6e6}
header button{background:#1a1c22;color:#e6e6e6;border:1px solid #2a2d35;border-radius:6px;padding:6px 12px;cursor:pointer;font:inherit}
header button:hover{background:#2a2d35}
main{flex:1;display:grid;grid-template-columns:280px 1fr 320px;min-height:0}
main>section{overflow:auto;padding:16px 20px}
#target{border-right:1px solid #2a2d35}
#current{border-right:1px solid #2a2d35}
#history{background:#11141a}
h2{margin:0 0 8px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:#888}
.note-title{margin:0 0 6px;font-size:18px;font-weight:600}
.note-path{color:#888;font-size:12px;font-family:ui-monospace,monospace;margin-bottom:16px;word-break:break-all}
.note-tags{color:#a78bfa;font-size:12px;margin-bottom:12px}
ul.links{list-style:none;padding:0;margin:0}
ul.links li{margin:0 0 6px}
ul.links a{color:#7cc1ff;text-decoration:none;display:block;padding:6px 8px;border-radius:4px}
ul.links a:hover{background:#1a1c22}
ul.links a .edge-type{color:#555;font-size:11px;margin-left:6px}
.group-label{color:#666;font-size:11px;text-transform:uppercase;letter-spacing:.05em;padding:10px 8px 4px}
#history ol{padding-left:20px;margin:0}
#history li{margin:4px 0;font-size:13px;color:#aaa}
#history li.current{color:#e6e6e6;font-weight:600}
#banner{padding:12px 20px;text-align:center;font-weight:600}
#banner.win{background:#14532d;color:#bbf7d0}
#banner.giveup{background:#1f2937;color:#aaa}
#banner.hidden{display:none}
.hint{color:#888;font-size:12px;margin-top:12px}
.meta-row{color:#888;font-size:12px;display:flex;gap:14px;margin-bottom:12px;flex-wrap:wrap}
.meta-row strong{color:#e6e6e6}
</style></head><body>
<header>
  <h1>Note Graph Speedrun</h1>
  <span class="stat">clicks <strong id="stat-clicks">0</strong></span>
  <span class="stat">time <strong id="stat-time">0s</strong></span>
  <span class="stat">corpus <strong id="stat-corpus"></strong></span>
  <button id="btn-new">New run</button>
  <button id="btn-hard">Harder (3+ hops)</button>
  <button id="btn-soft">Allow soft edges</button>
  <button id="btn-giveup">Give up</button>
</header>
<div id="banner" class="hidden"></div>
<main>
  <section id="target"><h2>Target</h2><div id="target-card"></div></section>
  <section id="current"><h2>You are here</h2><div id="current-card"></div></section>
  <section id="history"><h2>Path</h2><ol id="history-list"></ol></section>
</main>
<script>
const GRAPH = ${json};
const byId = new Map(GRAPH.nodes.map(n => [n.id, n]));
const hardAdj = new Map();
const softAdj = new Map();
for (const n of GRAPH.nodes) { hardAdj.set(n.id, new Map()); softAdj.set(n.id, new Map()); }
for (const e of GRAPH.edges) {
  const m = e.hardness === 'hard' ? hardAdj : softAdj;
  if (!m.get(e.source).has(e.target)) m.get(e.source).set(e.target, e.type);
}
document.getElementById('stat-corpus').textContent = GRAPH.nodes.length + ' notes';

function shortestPath(from, to, includeSoft) {
  const prev = new Map([[from, null]]);
  const queue = [from];
  while (queue.length) {
    const node = queue.shift();
    if (node === to) break;
    for (const next of hardAdj.get(node).keys()) if (!prev.has(next)) { prev.set(next, node); queue.push(next); }
    if (includeSoft) for (const next of softAdj.get(node).keys()) if (!prev.has(next)) { prev.set(next, node); queue.push(next); }
  }
  if (!prev.has(to)) return null;
  const path = []; let cur = to;
  while (cur !== null) { path.unshift(cur); cur = prev.get(cur); }
  return path;
}

function pickPair(minHops, includeSoft) {
  const navigable = GRAPH.nodes.filter(n => hardAdj.get(n.id).size >= 1);
  for (let attempt = 0; attempt < 200; attempt++) {
    const start = navigable[Math.floor(Math.random() * navigable.length)];
    const target = GRAPH.nodes[Math.floor(Math.random() * GRAPH.nodes.length)];
    if (start.id === target.id) continue;
    const path = shortestPath(start.id, target.id, includeSoft);
    if (!path || path.length - 1 < minHops || path.length - 1 > 8) continue;
    return { start, target, optimalHops: path.length - 1, optimalPath: path };
  }
  return null;
}

let state = null;
let timerId = null;
let allowSoft = false;
let hardMode = false;

function startRun() {
  document.getElementById('banner').className = 'hidden';
  const pair = pickPair(hardMode ? 3 : 2, allowSoft);
  if (!pair) { alert('Could not find a suitable pair — try toggling difficulty.'); return; }
  state = { start: pair.start, target: pair.target, current: pair.start, history: [pair.start.id], clicks: 0, startedAt: null, optimalHops: pair.optimalHops, optimalPath: pair.optimalPath, finished: false };
  if (timerId) clearInterval(timerId); timerId = null;
  document.getElementById('stat-clicks').textContent = '0';
  document.getElementById('stat-time').textContent = '0s';
  renderAll();
}

function navigateTo(nodeId) {
  if (!state || state.finished) return;
  if (state.startedAt === null) {
    state.startedAt = Date.now();
    timerId = setInterval(() => {
      if (!state || state.finished) return;
      document.getElementById('stat-time').textContent = Math.floor((Date.now() - state.startedAt) / 1000) + 's';
    }, 1000);
  }
  state.clicks++;
  state.current = byId.get(nodeId);
  state.history.push(nodeId);
  document.getElementById('stat-clicks').textContent = state.clicks;
  if (nodeId === state.target.id) finish('win'); else renderAll();
}

function finish(mode) {
  state.finished = true;
  if (timerId) clearInterval(timerId);
  const banner = document.getElementById('banner');
  const elapsed = state.startedAt ? Math.floor((Date.now() - state.startedAt) / 1000) : 0;
  if (mode === 'win') {
    const par = state.clicks === state.optimalHops ? ' (optimal!)' : ' (par ' + state.optimalHops + ')';
    banner.className = 'win';
    banner.textContent = 'Reached target in ' + state.clicks + ' click' + (state.clicks === 1 ? '' : 's') + ', ' + elapsed + 's' + par;
  } else {
    banner.className = 'giveup';
    banner.textContent = 'Gave up. Shortest path was: ' + state.optimalPath.map(id => byId.get(id).title).join(' → ');
  }
  renderAll();
}

const el = (tag, opts = {}) => { const e = document.createElement(tag); if (opts.text !== undefined) e.textContent = opts.text; if (opts.className) e.className = opts.className; if (opts.attrs) for (const [k,v] of Object.entries(opts.attrs)) e.setAttribute(k,v); if (opts.children) for (const c of opts.children) e.appendChild(c); return e; };

function renderAll() { renderTarget(); renderCurrent(); renderHistory(); }
function renderTarget() {
  const c = document.getElementById('target-card'); c.replaceChildren();
  if (!state) return;
  const t = state.target;
  c.appendChild(el('div', { className: 'note-title', text: t.title }));
  c.appendChild(el('div', { className: 'note-path', text: t.id }));
  if (t.tags && t.tags.length) c.appendChild(el('div', { className: 'note-tags', text: '#' + t.tags.join(' #') }));
  c.appendChild(el('div', { className: 'meta-row', children: [
    el('span', { children: [document.createTextNode('par '), el('strong', { text: String(state.optimalHops) })] }),
    el('span', { children: [document.createTextNode('in-degree '), el('strong', { text: String(t.inDegree) })] }),
  ] }));
  c.appendChild(el('div', { className: 'hint', text: 'Navigate from "' + state.start.title + '" to this note via links only.' }));
}
function renderCurrent() {
  const c = document.getElementById('current-card'); c.replaceChildren();
  if (!state) return;
  const n = state.current;
  c.appendChild(el('div', { className: 'note-title', text: n.title }));
  c.appendChild(el('div', { className: 'note-path', text: n.id }));
  if (n.tags && n.tags.length) c.appendChild(el('div', { className: 'note-tags', text: '#' + n.tags.join(' #') }));
  const hard = [...hardAdj.get(n.id).entries()].map(([id, type]) => ({ id, type }));
  const soft = allowSoft ? [...softAdj.get(n.id).entries()].map(([id, type]) => ({ id, type })) : [];
  const ul = el('ul', { className: 'links' });
  if (hard.length === 0 && soft.length === 0) {
    ul.appendChild(el('li', { children: [el('div', { className: 'group-label', text: 'dead end — no outgoing links' })] }));
  } else {
    if (hard.length) {
      ul.appendChild(el('li', { children: [el('div', { className: 'group-label', text: 'wiki / markdown links (' + hard.length + ')' })] }));
      for (const { id, type } of hard.sort((a,b) => byId.get(a.id).title.localeCompare(byId.get(b.id).title))) {
        const t = byId.get(id); if (!t) continue;
        const a = el('a', { attrs: { href: '#' } });
        a.appendChild(document.createTextNode(t.title));
        a.appendChild(el('span', { className: 'edge-type', text: type }));
        a.addEventListener('click', (ev) => { ev.preventDefault(); navigateTo(id); });
        ul.appendChild(el('li', { children: [a] }));
      }
    }
    if (soft.length) {
      ul.appendChild(el('li', { children: [el('div', { className: 'group-label', text: 'soft edges (' + soft.length + ')' })] }));
      for (const { id, type } of soft.sort((a,b) => byId.get(a.id).title.localeCompare(byId.get(b.id).title))) {
        const t = byId.get(id); if (!t) continue;
        const a = el('a', { attrs: { href: '#' } });
        a.appendChild(document.createTextNode(t.title));
        a.appendChild(el('span', { className: 'edge-type', text: type }));
        a.addEventListener('click', (ev) => { ev.preventDefault(); navigateTo(id); });
        ul.appendChild(el('li', { children: [a] }));
      }
    }
  }
  c.appendChild(ul);
}
function renderHistory() {
  const ol = document.getElementById('history-list'); ol.replaceChildren();
  if (!state) return;
  state.history.forEach((id, i) => {
    const n = byId.get(id);
    const li = el('li', { text: n.title + (i === state.history.length - 1 ? ' ← here' : '') });
    if (i === state.history.length - 1) li.className = 'current';
    ol.appendChild(li);
  });
}

document.getElementById('btn-new').addEventListener('click', startRun);
document.getElementById('btn-giveup').addEventListener('click', () => { if (state && !state.finished && state.startedAt) finish('giveup'); });
document.getElementById('btn-hard').addEventListener('click', (ev) => { hardMode = !hardMode; ev.target.style.background = hardMode ? '#a78bfa33' : ''; startRun(); });
document.getElementById('btn-soft').addEventListener('click', (ev) => { allowSoft = !allowSoft; ev.target.style.background = allowSoft ? '#a78bfa33' : ''; if (state) renderCurrent(); });

startRun();
</script></body></html>
`;
}

// ── main ───────────────────────────────────────────────────────────────────
function main() {
  const argv = process.argv.slice(2);
  const graph = buildGraph();

  if (argv.includes("--json")) {
    process.stdout.write(JSON.stringify(graph, null, 2));
    return;
  }

  mkdirSync(dirname(OUT_MERMAID), { recursive: true });
  writeFileSync(OUT_JSON, JSON.stringify(graph, null, 2));
  writeFileSync(OUT_MERMAID, renderMermaid(graph));
  writeFileSync(OUT_HTML, renderHtml(graph));
  writeFileSync(OUT_SPEEDRUN, renderSpeedrunHtml(graph));

  const s = graph.stats;
  console.log(`notegraph: ${s.nodes} nodes · ${s.hard} hard · ${s.soft} soft · ${s.orphans} orphans`);
  console.log(`  wrote ${relative(ROOT, OUT_JSON)}`);
  console.log(`  wrote ${relative(ROOT, OUT_MERMAID)}`);
  console.log(`  wrote ${relative(ROOT, OUT_HTML)}`);
  console.log(`  wrote ${relative(ROOT, OUT_SPEEDRUN)}`);
}

main();
