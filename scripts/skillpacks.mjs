#!/usr/bin/env node
/**
 * skillpacks — cluster the skills/ directory into coherent bundles.
 *
 * Builds a weighted graph over every skills/*\/SKILL.md, runs label
 * propagation, and emits three artifacts:
 *
 *   skillpacks.json                      — clusters with members + cohesion
 *   docs/skillpacks.md                   — readable digest (humans)
 *   docs/skillpacks.html                 — Cytoscape view (clusters as colors)
 *   skillpacks/<slug>.json               — per-pack install manifest
 *   docs/skillpacks-chains.md            — suggested aeon.yml chains
 *
 * Edge weights (additive across types between the same pair)
 *   depends_on                                        3.0   (rare but strongest)
 *   consume (chain-style references in skill body)    2.5
 *   shared frontmatter tag (capped: skip tags on >25 skills)  1.0
 *   shared file reference (memory/topics/*, scripts/*, etc.)  1.5
 *   TF-IDF cosine ≥ 0.18, top-5 per node              score × 4 (≤ ~2.0)
 *
 * Clustering: label propagation, deterministic (sorted iteration), capped at
 * 30 passes. Stable for 100–500 nodes.
 *
 * Cluster naming: pick top 2–3 IDF-weighted terms from member descriptions
 * (NOT bodies — descriptions are curated and yield legible names).
 *
 * Usage:
 *   node scripts/skillpacks.mjs           # writes all artifacts
 *   node scripts/skillpacks.mjs --json    # print skillpacks.json only
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, unlinkSync } from "node:fs";
import { resolve, relative, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const SKILLS_DIR = "skills";
const OUT_JSON = resolve(ROOT, "skillpacks.json");
const OUT_MD = resolve(ROOT, "docs/skillpacks.md");
const OUT_HTML = resolve(ROOT, "docs/skillpacks.html");
const OUT_CHAINS = resolve(ROOT, "docs/skillpacks-chains.md");
const OUT_PACKS_DIR = resolve(ROOT, "skillpacks");

// ── safe inline-JSON escape (XSS prevention for embedded graph data) ──────
// Skill names, descriptions, and tags are operator-authored, but a fork or
// imported skill could carry hostile content. Standard 5-replacement
// escape so `</script>`, U+2028/U+2029, and friends can't break out of
// the inline <script> in the Cytoscape view.
function safeJsonForScript(value) {
  return JSON.stringify(value)
    .replace(/</g, "\\u003c")
    .replace(/>/g, "\\u003e")
    .replace(/&/g, "\\u0026")
    .replace(/[\u2028\u2029]/g, (c) => c === "\u2028" ? "\\u2028" : "\\u2029");
}


// ── collect tracked SKILL.md files ─────────────────────────────────────────
function collectSkills() {
  let out;
  try {
    out = execFileSync(
      "git",
      ["ls-files", "--", `${SKILLS_DIR}/*/SKILL.md`],
      { cwd: ROOT, encoding: "utf8", maxBuffer: 32 * 1024 * 1024 },
    ).split("\n").filter(Boolean);
  } catch (err) {
    throw new Error(`skillpacks: git ls-files failed (${err.message})`);
  }
  return out
    .filter((p) => existsSync(resolve(ROOT, p)))
    .map((p) => resolve(ROOT, p))
    .sort();
}

// ── parse frontmatter + body ───────────────────────────────────────────────
const RE_FRONTMATTER = /^---\n([\s\S]*?)\n---/;
const RE_TAGS_INLINE = /^tags:\s*\[([^\]]*)\]/m;
const RE_DEPENDS = /^depends_on:\s*\[([^\]]*)\]/m;

function parseSkill(absPath) {
  const rel = relative(ROOT, absPath);
  const slug = rel.split("/")[1]; // skills/<slug>/SKILL.md
  const raw = readFileSync(absPath, "utf8");
  let body = raw;
  let frontmatter = "";
  const fm = raw.match(RE_FRONTMATTER);
  if (fm) { frontmatter = fm[1]; body = raw.slice(fm[0].length); }

  const nameM = frontmatter.match(/^name:\s*(.+)$/m);
  const descM = frontmatter.match(/^description:\s*(.+)$/m);
  const tagsM = frontmatter.match(RE_TAGS_INLINE);
  const depM = frontmatter.match(RE_DEPENDS);

  const tags = tagsM
    ? tagsM[1].split(",").map((s) => s.trim().replace(/^["']|["']$/g, "")).filter(Boolean)
    : [];
  const depends = depM
    ? depM[1].split(",").map((s) => s.trim().replace(/^["']|["']$/g, "")).filter(Boolean)
    : [];

  // File references the skill touches — strong signal of operational kinship.
  // Pull memory/topics/*, memory/state/*, scripts/*, docs/*, and other skill slugs.
  const refs = new Set();
  for (const m of body.matchAll(/\bmemory\/(topics|state)\/[a-zA-Z0-9_./-]+/g)) refs.add(m[0]);
  for (const m of body.matchAll(/\bscripts\/[a-zA-Z0-9_./-]+\.(sh|mjs|js|py)\b/g)) refs.add(m[0]);
  for (const m of body.matchAll(/\.outputs\/[a-zA-Z0-9_./-]+/g)) refs.add(m[0]);

  // Cross-skill mentions (consume edges live in skill prose, not frontmatter)
  const skillMentions = new Set();
  for (const m of body.matchAll(/\b(?:skill|consume|depends?(?:_on)?|requires?):\s*\[?([a-z0-9-]+)/gi)) {
    skillMentions.add(m[1]);
  }

  return {
    slug,
    name: nameM ? nameM[1].trim() : slug,
    description: descM ? descM[1].trim() : "",
    tags,
    depends,
    refs: [...refs],
    skillMentions: [...skillMentions],
    body,
  };
}

// ── TF-IDF over skill bodies ───────────────────────────────────────────────
const STOPWORDS = new Set((
  "a an and are as at be but by for from has have he her his how if in into is it its " +
  "of on or that the their they this to was we were what when where which who will with " +
  "you your i me my our us am do does did been being would could should may might can " +
  "not no nor so than then there here also any all each some such only just very more " +
  "most other than them these those one two three set use used using uses run runs " +
  "running ran via per eg ie etc skill skills today var today\\u2019s steps step phase output " +
  // Cadence words are not themes — drop from label terms.
  "weekly daily hourly minutely monthly yearly nightly cron schedule scheduled"
).split(" "));

function tokenize(text) {
  const out = [];
  for (const raw of text.toLowerCase().split(/[^a-z0-9]+/)) {
    if (raw.length < 3 || raw.length > 30) continue;
    if (/^[0-9]+$/.test(raw)) continue;
    if (STOPWORDS.has(raw)) continue;
    out.push(raw);
  }
  return out;
}

function stripBody(body) {
  return body
    .replace(/```[\s\S]*?```/g, "")
    .replace(/`[^`\n]+`/g, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\{%[\s\S]*?%\}/g, " ")
    .replace(/\{\{[\s\S]*?\}\}/g, " ");
}

function computeSimilarities(skills, topK = 5, minScore = 0.18) {
  const tfs = skills.map((s) => {
    const tokens = tokenize(stripBody(s.body) + " " + s.description + " " + s.name);
    const tf = new Map();
    for (const t of tokens) tf.set(t, (tf.get(t) || 0) + 1);
    return tf;
  });
  const df = new Map();
  for (const tf of tfs) for (const term of tf.keys()) df.set(term, (df.get(term) || 0) + 1);
  const N = skills.length;
  const useful = new Set();
  for (const [t, f] of df) if (f >= 2 && f <= N * 0.4) useful.add(t);

  const vectors = tfs.map((tf) => {
    const v = new Map();
    let normSq = 0;
    for (const [term, count] of tf) {
      if (!useful.has(term)) continue;
      const idf = Math.log(N / df.get(term));
      const w = (1 + Math.log(count)) * idf;
      v.set(term, w);
      normSq += w * w;
    }
    return { v, norm: Math.sqrt(normSq) };
  });

  const sims = [];
  for (let i = 0; i < skills.length; i++) {
    const { v: vi, norm: ni } = vectors[i];
    if (ni === 0) continue;
    const scored = [];
    for (let j = 0; j < skills.length; j++) {
      if (i === j) continue;
      const { v: vj, norm: nj } = vectors[j];
      if (nj === 0) continue;
      const [small, large] = vi.size < vj.size ? [vi, vj] : [vj, vi];
      let dot = 0;
      const shared = [];
      for (const [term, w] of small) {
        const w2 = large.get(term);
        if (w2 !== undefined) { dot += w * w2; shared.push([term, w * w2]); }
      }
      const score = dot / (ni * nj);
      if (score < minScore) continue;
      shared.sort((a, b) => b[1] - a[1]);
      scored.push({
        source: skills[i].slug,
        target: skills[j].slug,
        score: Math.round(score * 1000) / 1000,
        shared: shared.slice(0, 5).map(([t]) => t),
      });
    }
    scored.sort((a, b) => b.score - a.score);
    for (const s of scored.slice(0, topK)) sims.push(s);
  }
  return { sims, vectors, df, N };
}

// ── build weighted graph ───────────────────────────────────────────────────
function buildEdges(skills, sims) {
  // adjacency keyed by sorted-pair string → { weight, reasons[] }
  const adj = new Map();
  const slugSet = new Set(skills.map((s) => s.slug));
  const add = (a, b, w, reason) => {
    if (a === b) return;
    if (!slugSet.has(a) || !slugSet.has(b)) return;
    const key = a < b ? `${a}|${b}` : `${b}|${a}`;
    const cur = adj.get(key) || { weight: 0, reasons: [] };
    cur.weight += w;
    cur.reasons.push(reason);
    adj.set(key, cur);
  };

  // depends_on
  for (const s of skills) for (const d of s.depends) add(s.slug, d, 3.0, `depends_on`);

  // cross-skill mentions in body (best-effort consume)
  for (const s of skills) for (const m of s.skillMentions) {
    if (m !== s.slug && slugSet.has(m)) add(s.slug, m, 1.0, `mentions:${m}`);
  }

  // Shared tags — keep the 25-member cap for raw per-tag edges (too many
  // small edges from common tags collectively dominate label propagation).
  // Common tags (meta, dev) reach the long tail via the tag-set Jaccard
  // edge below instead.
  const byTag = new Map();
  for (const s of skills) for (const t of s.tags) {
    if (!byTag.has(t)) byTag.set(t, []);
    byTag.get(t).push(s.slug);
  }
  for (const [tag, slugs] of byTag) {
    if (slugs.length < 2 || slugs.length > 25) continue;
    for (let i = 0; i < slugs.length; i++) for (let j = i + 1; j < slugs.length; j++) {
      add(slugs[i], slugs[j], 1.0, `tag:${tag}`);
    }
  }

  // Tag-set Jaccard — sharing an unusual *combination* of tags is stronger
  // signal than sharing one common tag, and the constraint scales naturally:
  // [dev, meta] only matches other skills with exactly [dev, meta], not the
  // entire dev or meta universe. This is what gives the [dev, meta] solo
  // tail something to connect to without flooding the graph.
  for (let i = 0; i < skills.length; i++) {
    const a = new Set(skills[i].tags);
    if (a.size === 0) continue;
    for (let j = i + 1; j < skills.length; j++) {
      const b = new Set(skills[j].tags);
      if (b.size === 0) continue;
      let inter = 0;
      for (const t of a) if (b.has(t)) inter++;
      if (inter === 0) continue;
      const union = a.size + b.size - inter;
      const jaccard = inter / union;
      if (jaccard < 0.6) continue; // strong tag-set overlap only
      add(skills[i].slug, skills[j].slug, jaccard * 1.2, `tagset:${[...a].sort().join(",")}`);
    }
  }

  // shared file references (memory/topics/*, scripts/*, .outputs/*)
  const byRef = new Map();
  for (const s of skills) for (const r of s.refs) {
    if (!byRef.has(r)) byRef.set(r, []);
    byRef.get(r).push(s.slug);
  }
  for (const [ref, slugs] of byRef) {
    if (slugs.length < 2 || slugs.length > 15) continue;
    for (let i = 0; i < slugs.length; i++) for (let j = i + 1; j < slugs.length; j++) {
      add(slugs[i], slugs[j], 1.5, `ref:${ref.replace(/^.*\//, "")}`);
    }
  }

  // similarity edges (already capped top-K)
  for (const s of sims) add(s.source, s.target, s.score * 4, `sim:${s.shared.slice(0, 3).join(",")}`);

  // emit edge list
  const edges = [];
  for (const [key, { weight, reasons }] of adj) {
    const [a, b] = key.split("|");
    edges.push({ a, b, weight: Math.round(weight * 100) / 100, reasons });
  }
  return edges;
}

// ── label propagation (deterministic) ──────────────────────────────────────
function labelPropagate(skills, edges, maxIter = 30) {
  const slugs = skills.map((s) => s.slug).sort();
  const adj = new Map();
  for (const s of slugs) adj.set(s, []);
  for (const e of edges) {
    adj.get(e.a).push([e.b, e.weight]);
    adj.get(e.b).push([e.a, e.weight]);
  }
  // initial labels: each node is its own community
  const label = new Map(slugs.map((s) => [s, s]));

  for (let iter = 0; iter < maxIter; iter++) {
    let changed = 0;
    for (const slug of slugs) { // sorted iteration → deterministic
      const counts = new Map();
      for (const [nbr, w] of adj.get(slug)) {
        const l = label.get(nbr);
        counts.set(l, (counts.get(l) || 0) + w);
      }
      if (counts.size === 0) continue;
      // pick max weight, tie-break alphabetically for determinism
      let best = null, bestW = -Infinity;
      for (const [l, w] of [...counts.entries()].sort((a, b) => a[0] < b[0] ? -1 : 1)) {
        if (w > bestW) { bestW = w; best = l; }
      }
      if (best !== label.get(slug)) { label.set(slug, best); changed++; }
    }
    if (changed === 0) break;
  }

  // group by label
  const clusters = new Map();
  for (const [slug, l] of label) {
    if (!clusters.has(l)) clusters.set(l, []);
    clusters.get(l).push(slug);
  }
  return [...clusters.values()].sort((a, b) => b.length - a.length);
}

// ── name each cluster from member descriptions ─────────────────────────────
// Picks terms that recur across the cluster, not corpus-unique terms that
// happen to live in one outlier member's description. Previously the corpus-
// IDF dominated, so a 20-skill cluster could be labeled by a term appearing
// in 1 member (e.g. "smithery" labeling a self-improvement cluster).
function nameCluster(members, skills, df, N, allUsedNames) {
  const bySlug = new Map(skills.map((s) => [s.slug, s]));
  // Per-cluster *document* frequency: how many members mention the term in
  // their description/name (not raw term frequency, which one verbose
  // description can dominate).
  const clusterDf = new Map();
  for (const slug of members) {
    const s = bySlug.get(slug);
    if (!s) continue;
    const seen = new Set(tokenize(s.description + " " + s.name));
    for (const t of seen) clusterDf.set(t, (clusterDf.get(t) || 0) + 1);
  }
  // Require the term to recur in at least 2 members (a single outlier
  // description shouldn't get to label the whole cluster). Beyond that,
  // let the coverage-weighted score do the ranking.
  const scored = [];
  for (const [term, cdf] of clusterDf) {
    if (cdf < 2) continue;
    const dfTerm = df.get(term) || 1;
    if (dfTerm > N * 0.4) continue; // too generic across corpus
    // Score = how much of the cluster mentions this × how unusual it is in the corpus.
    // (cdf / members.length) is the "coverage"; log(N/df) is the IDF.
    const coverage = cdf / members.length;
    scored.push([term, coverage * Math.log(N / dfTerm)]);
  }
  scored.sort((a, b) => b[1] - a[1]);
  const top = scored.slice(0, 4).map(([t]) => t);
  let label = top.slice(0, 2).join(" · ") || `cluster-${members.length}`;
  let i = 2;
  while (allUsedNames.has(label) && i < top.length) {
    label = top.slice(0, ++i).join(" · ");
  }
  if (allUsedNames.has(label)) label += ` (${members.length})`;
  allUsedNames.add(label);
  return { label, topTerms: top };
}

// ── cohesion: avg edge weight inside the cluster ───────────────────────────
function cohesion(members, edges) {
  const memberSet = new Set(members);
  let sum = 0, count = 0;
  for (const e of edges) {
    if (memberSet.has(e.a) && memberSet.has(e.b)) { sum += e.weight; count++; }
  }
  if (count === 0) return 0;
  return Math.round((sum / count) * 100) / 100;
}

// ── load existing categories from skills.json for comparison ───────────────
function loadExistingCategories() {
  const path = resolve(ROOT, "skills.json");
  if (!existsSync(path)) return new Map();
  try {
    const j = JSON.parse(readFileSync(path, "utf8"));
    const out = new Map();
    for (const s of j.skills || []) out.set(s.slug, s.category);
    return out;
  } catch { return new Map(); }
}

// ── renderers ──────────────────────────────────────────────────────────────
function slugify(label) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40);
}

function renderMarkdown(packs, skills, existing, generatedAt) {
  const bySlug = new Map(skills.map((s) => [s.slug, s]));
  let out = `# Skillpacks\n\n`;
  out += `> Auto-generated by \`scripts/skillpacks.mjs\` on ${generatedAt.slice(0, 10)}.\n`;
  out += `> Re-run with \`node scripts/skillpacks.mjs\` to update.\n\n`;
  out += `**${skills.length} skills** clustered into **${packs.length} packs** via label propagation over a weighted graph (frontmatter tags, shared file references, TF-IDF body similarity, declared deps).\n\n`;
  out += `Compare against the manual 5-category taxonomy in \`skills.json\` to see where the data agrees vs disagrees.\n\n`;
  out += `Interactive view: [\`skillpacks.html\`](./skillpacks.html). Suggested chains: [\`skillpacks-chains.md\`](./skillpacks-chains.md).\n\n`;
  out += `## Packs\n\n`;
  for (const p of packs) {
    out += `### ${p.label}  \`${p.slug}\`\n\n`;
    out += `**${p.members.length} skills** · cohesion **${p.cohesion}** · top terms: \`${p.topTerms.join(", ")}\`\n\n`;
    // category breakdown
    const catCount = new Map();
    for (const slug of p.members) {
      const c = existing.get(slug) || "unknown";
      catCount.set(c, (catCount.get(c) || 0) + 1);
    }
    const catStr = [...catCount.entries()].sort((a, b) => b[1] - a[1])
      .map(([c, n]) => `${c}:${n}`).join(" · ");
    out += `Existing categories in this pack: \`${catStr}\`\n\n`;
    out += `| slug | description |\n|---|---|\n`;
    for (const slug of p.members.sort()) {
      const s = bySlug.get(slug);
      if (!s) continue;
      const desc = (s.description || "").slice(0, 100).replace(/\|/g, "\\|");
      out += `| \`${slug}\` | ${desc} |\n`;
    }
    out += `\n`;
  }
  return out;
}

function renderHtml(packs, skills, edges) {
  const slugToPack = new Map();
  packs.forEach((p, i) => p.members.forEach((m) => slugToPack.set(m, i)));
  // distinct palette — cycles after 16, fine for typical pack counts
  const palette = ["#7cc1ff", "#f7a072", "#a78bfa", "#86efac", "#fde68a", "#fca5a5", "#67e8f9", "#c4b5fd", "#fdba74", "#fcd34d", "#bef264", "#5eead4", "#f0abfc", "#fecaca", "#ddd6fe", "#bbf7d0"];
  const nodes = skills.map((s) => ({
    data: { id: s.slug, label: s.name, pack: slugToPack.get(s.slug) ?? -1, packLabel: packs[slugToPack.get(s.slug)]?.label ?? "—", desc: s.description },
  }));
  const els = [
    ...nodes,
    ...edges.map((e, i) => ({ data: { id: "e" + i, source: e.a, target: e.b, weight: e.weight, reasons: e.reasons.slice(0, 4) } })),
  ];
  const graphJson = safeJsonForScript({ elements: els, packs: packs.map((p) => ({ label: p.label, slug: p.slug, members: p.members.length })) });
  const paletteJson = safeJsonForScript(palette);
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Skillpacks</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  html,body{margin:0;height:100%;font:14px/1.4 system-ui,sans-serif;background:#0e0f12;color:#e6e6e6}
  #toolbar{position:fixed;top:8px;left:8px;right:8px;z-index:10;display:flex;gap:8px;align-items:center;padding:8px 12px;background:rgba(20,22,28,0.92);border:1px solid #2a2d35;border-radius:8px}
  #toolbar input[type=search]{flex:1;padding:6px 10px;background:#1a1c22;border:1px solid #2a2d35;border-radius:6px;color:#e6e6e6}
  #stats{color:#888;font-size:12px}
  #cy{width:100vw;height:100vh}
  #legend{position:fixed;left:8px;top:56px;max-height:calc(100vh - 80px);overflow:auto;padding:8px 12px;background:rgba(20,22,28,0.95);border:1px solid #2a2d35;border-radius:8px;width:240px}
  #legend h3{margin:0 0 6px;font-size:13px}
  .legend-item{display:flex;align-items:center;gap:6px;padding:2px 0;cursor:pointer;font-size:12px}
  .swatch{width:12px;height:12px;border-radius:3px;flex-shrink:0}
  #panel{position:fixed;right:8px;top:56px;width:320px;max-height:calc(100vh - 80px);overflow:auto;padding:12px 14px;background:rgba(20,22,28,0.95);border:1px solid #2a2d35;border-radius:8px;display:none}
  #panel h3{margin:0 0 6px;font-size:14px}
  #panel .meta{color:#888;font-size:12px;margin-bottom:8px}
</style></head><body>
<div id="toolbar"><strong>Skillpacks</strong><input id="search" type="search" placeholder="Search skill name or slug…"><span id="stats"></span></div>
<div id="legend"><h3>Packs</h3><div id="legend-items"></div></div>
<div id="cy"></div><div id="panel"></div>
<script src="https://unpkg.com/cytoscape@3.30.2/dist/cytoscape.min.js"></script>
<script>
const G = ${graphJson};
const PALETTE = ${paletteJson};
const colorFor = (i) => i < 0 ? "#666" : PALETTE[i % PALETTE.length];

const cy = cytoscape({
  container: document.getElementById('cy'),
  elements: G.elements,
  style: [
    { selector: 'node', style: {
      'background-color': (n) => colorFor(n.data('pack')),
      'label': 'data(label)', 'color': '#e6e6e6', 'font-size': 8,
      'text-valign': 'center', 'text-halign': 'center',
      'text-outline-color': '#0e0f12', 'text-outline-width': 1.5,
      'width': 18, 'height': 18,
    }},
    { selector: 'edge', style: {
      'width': (e) => Math.min(4, 0.4 + e.data('weight') * 0.3),
      'curve-style': 'bezier', 'line-color': '#3a3d45', 'opacity': 0.4,
    }},
    { selector: 'node.faded, edge.faded', style: { 'opacity': 0.08 }},
    { selector: 'node.hit', style: { 'border-width': 2, 'border-color': '#fff' }},
  ],
  layout: { name: 'cose', animate: false, idealEdgeLength: 80, nodeRepulsion: 6000, gravity: 0.5 },
});

document.getElementById('stats').textContent = G.elements.filter(e=>!e.data.source).length + ' skills · ' + G.packs.length + ' packs · ' + G.elements.filter(e=>e.data.source).length + ' edges';

const li = document.getElementById('legend-items');
const el = (t,o={}) => { const n=document.createElement(t); if(o.text!==undefined)n.textContent=o.text; if(o.className)n.className=o.className; if(o.attrs)for(const[k,v]of Object.entries(o.attrs))n.setAttribute(k,v); if(o.children)for(const c of o.children)n.appendChild(c); return n; };
G.packs.forEach((p, i) => {
  const sw = el('span',{className:'swatch'}); sw.style.background = colorFor(i);
  const item = el('div',{className:'legend-item',children:[sw, el('span',{text:p.label+' ('+p.members+')'})]});
  item.addEventListener('click', () => {
    cy.elements().removeClass('faded hit');
    const pNodes = cy.nodes().filter(n => n.data('pack') === i);
    if (pNodes.length === 0) return;
    const keep = pNodes.union(pNodes.connectedEdges());
    cy.elements().not(keep).addClass('faded');
  });
  li.appendChild(item);
});

const panel = document.getElementById('panel');
cy.on('tap', 'node', (evt) => {
  const n = evt.target;
  panel.replaceChildren();
  panel.style.display = 'block';
  panel.appendChild(el('h3', { text: n.data('label') }));
  panel.appendChild(el('div', { className: 'meta', text: n.id() }));
  panel.appendChild(el('div', { className: 'meta', text: 'pack: ' + n.data('packLabel') }));
  if (n.data('desc')) panel.appendChild(el('div', { text: n.data('desc') }));
  const neighbors = n.connectedEdges().map(e => {
    const other = e.source().id() === n.id() ? e.target() : e.source();
    return { id: other.id(), label: other.data('label'), weight: e.data('weight'), reasons: e.data('reasons') || [] };
  }).sort((a,b)=>b.weight-a.weight).slice(0, 12);
  panel.appendChild(el('strong', { text: 'Top neighbors (' + neighbors.length + ')' }));
  const ul = el('ul');
  for (const nb of neighbors) {
    const a = el('a', { text: nb.label, attrs: { href: '#' } });
    a.addEventListener('click', (ev) => { ev.preventDefault(); const t = cy.getElementById(nb.id); cy.animate({ center: { eles: t }, zoom: 1.4 }, { duration: 300 }); t.trigger('tap'); });
    const meta = el('span', { className: 'meta', text: ' · w=' + nb.weight + ' [' + nb.reasons.join(', ') + ']' });
    ul.appendChild(el('li', { children: [a, meta] }));
  }
  panel.appendChild(ul);
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

function renderChainSuggestions(packs, skills, generatedAt) {
  const bySlug = new Map(skills.map((s) => [s.slug, s]));
  let out = `# Suggested aeon.yml Chains\n\n`;
  out += `> Auto-generated by \`scripts/skillpacks.mjs\` on ${generatedAt.slice(0, 10)}.\n`;
  out += `> Advisory only — these are clustering-derived suggestions, **not** auto-applied to \`aeon.yml\`. Pick the ones that fit and paste them under \`chains:\`.\n\n`;
  out += `## How to read this\n\n`;
  out += `Each candidate chain bundles a cluster's skills. Skills within a pack share vocabulary, file references, or tags strongly enough that running them as a chain (parallel where independent, sequential where one consumes another's output) is a reasonable default.\n\n`;
  out += `The proposal does **not** guess sequencing — it just groups. Decide for yourself which steps should be \`parallel:\` vs sequential with \`consume:\`.\n\n`;
  let candidateCount = 0;
  for (const p of packs) {
    if (p.members.length < 3 || p.members.length > 10) continue; // chains larger than ~10 are unwieldy
    candidateCount++;
    out += `### \`${p.slug}\`-chain (${p.label})\n\n`;
    out += `\`\`\`yaml\nchains:\n  ${p.slug}:\n    schedule: "0 7 * * *"  # adjust\n    on_error: continue\n    steps:\n      - parallel:\n`;
    for (const slug of p.members.sort()) out += `          - ${slug}\n`;
    out += `\`\`\`\n\n`;
    out += `**Why these belong together:** ${p.topTerms.join(", ")}.\n\n`;
  }
  if (candidateCount === 0) out += `_No clusters in the 3–10 size range — try lowering the similarity threshold._\n`;
  return out;
}

function renderPackManifest(p, skills) {
  const bySlug = new Map(skills.map((s) => [s.slug, s]));
  return {
    pack: p.slug,
    label: p.label,
    cohesion: p.cohesion,
    topTerms: p.topTerms,
    members: p.members.sort().map((slug) => {
      const s = bySlug.get(slug);
      return {
        slug,
        name: s?.name || slug,
        description: s?.description || "",
        install: `./add-skill aaronjmars/aeon ${slug}`,
      };
    }),
    install_all: p.members.sort().map((slug) => `./add-skill aaronjmars/aeon ${slug}`),
  };
}

// ── main ───────────────────────────────────────────────────────────────────
function main() {
  const argv = process.argv.slice(2);
  const files = collectSkills();
  const skills = files.map(parseSkill);
  if (skills.length === 0) { console.error("skillpacks: no skills found"); process.exit(1); }

  const { sims, df, N } = computeSimilarities(skills);
  // Salvage pass: lower-threshold neighbors only for solo candidates, so a
  // skill with no above-threshold similarities still has something to attach
  // to. These are kept separate so the main edge set stays principled.
  const salvageSims = computeSimilarities(skills, 3, 0.10).sims;
  const edges = buildEdges(skills, sims);
  const rawClusters = labelPropagate(skills, edges);

  // Drop true singletons from the "pack" view — they're not packs, they're loners.
  // Then a second pass: try to attach each solo to whichever non-solo pack has
  // the strongest aggregate edge weight into it. A solo with no edges into any
  // multi-node cluster stays solo.
  let packs = [];
  let solos = [];
  for (const c of rawClusters) (c.length === 1 ? solos.push(c[0]) : packs.push(c));

  const edgesBySlug = new Map();
  for (const e of edges) {
    if (!edgesBySlug.has(e.a)) edgesBySlug.set(e.a, []);
    if (!edgesBySlug.has(e.b)) edgesBySlug.set(e.b, []);
    edgesBySlug.get(e.a).push([e.b, e.weight]);
    edgesBySlug.get(e.b).push([e.a, e.weight]);
  }
  // For solo attachment, augment the edge map with the salvage similarities
  // so a skill with no above-0.18 sim still gets to find its nearest pack.
  const salvageBySlug = new Map();
  for (const s of salvageSims) {
    if (!salvageBySlug.has(s.source)) salvageBySlug.set(s.source, []);
    salvageBySlug.get(s.source).push([s.target, s.score * 2]); // salvage weight is half of main
  }

  const stillSolo = [];
  for (const solo of solos) {
    const scoresByPack = new Map();
    const allEdges = [
      ...(edgesBySlug.get(solo) || []),
      ...(salvageBySlug.get(solo) || []),
    ];
    for (const [nbr, w] of allEdges) {
      for (let i = 0; i < packs.length; i++) {
        if (packs[i].includes(nbr)) {
          scoresByPack.set(i, (scoresByPack.get(i) || 0) + w);
        }
      }
    }
    if (scoresByPack.size === 0) { stillSolo.push(solo); continue; }
    let bestIdx = -1, bestW = -Infinity;
    for (const [i, w] of [...scoresByPack.entries()].sort((a, b) => a[0] - b[0])) {
      if (w > bestW) { bestW = w; bestIdx = i; }
    }
    packs[bestIdx] = [...packs[bestIdx], solo];
  }

  // Pair-up pass: any solos that are still solo after pack attachment, but
  // are each other's nearest salvage neighbor, form their own 2-skill pack
  // rather than sitting in the appendix forever.
  const trulySolo = [];
  const paired = new Set();
  for (const a of stillSolo) {
    if (paired.has(a)) continue;
    const nbrs = (salvageBySlug.get(a) || []).filter(([n]) => stillSolo.includes(n) && !paired.has(n));
    if (nbrs.length === 0) { trulySolo.push(a); continue; }
    nbrs.sort((x, y) => y[1] - x[1]);
    const [partner] = nbrs[0];
    // confirm mutual: a should be in partner's top salvage neighbors too
    const reverseNbrs = (salvageBySlug.get(partner) || []).filter(([n]) => stillSolo.includes(n) && !paired.has(n));
    reverseNbrs.sort((x, y) => y[1] - x[1]);
    if (reverseNbrs[0]?.[0] === a) {
      packs.push([a, partner]);
      paired.add(a); paired.add(partner);
    } else {
      trulySolo.push(a);
    }
  }
  solos = trulySolo;

  const usedNames = new Set();
  const packData = packs.map((members) => {
    const { label, topTerms } = nameCluster(members, skills, df, N, usedNames);
    return {
      slug: slugify(label) || `pack-${members.length}`,
      label,
      topTerms,
      members,
      cohesion: cohesion(members, edges),
    };
  });
  // dedupe slugs
  const slugSeen = new Map();
  for (const p of packData) {
    if (slugSeen.has(p.slug)) { p.slug = `${p.slug}-${slugSeen.get(p.slug) + 1}`; }
    slugSeen.set(p.slug, (slugSeen.get(p.slug) || 0) + 1);
  }
  if (solos.length > 0) {
    packData.push({
      slug: "solo",
      label: "Solo (unclustered)",
      topTerms: [],
      members: solos.flat(),
      cohesion: 0,
    });
  }

  const existing = loadExistingCategories();
  const generatedAt = new Date().toISOString();
  const summary = {
    generatedAt,
    stats: { skills: skills.length, edges: edges.length, packs: packData.length, solos: solos.length },
    packs: packData,
  };

  if (argv.includes("--json")) {
    process.stdout.write(JSON.stringify(summary, null, 2));
    return;
  }

  mkdirSync(dirname(OUT_MD), { recursive: true });
  mkdirSync(OUT_PACKS_DIR, { recursive: true });
  // Clean stale per-pack manifests from prior runs so the directory always
  // reflects the current cluster set (pack labels are not stable across runs).
  for (const name of readdirSync(OUT_PACKS_DIR)) {
    if (name.endsWith(".json")) unlinkSync(resolve(OUT_PACKS_DIR, name));
  }
  writeFileSync(OUT_JSON, JSON.stringify(summary, null, 2));
  writeFileSync(OUT_MD, renderMarkdown(packData, skills, existing, generatedAt));
  writeFileSync(OUT_HTML, renderHtml(packData, skills, edges));
  writeFileSync(OUT_CHAINS, renderChainSuggestions(packData, skills, generatedAt));
  for (const p of packData) {
    if (p.slug === "solo") continue;
    writeFileSync(resolve(OUT_PACKS_DIR, `${p.slug}.json`), JSON.stringify(renderPackManifest(p, skills), null, 2));
  }

  console.log(`skillpacks: ${skills.length} skills · ${packData.length - (solos.length > 0 ? 1 : 0)} packs · ${solos.length} solos · ${edges.length} edges`);
  for (const p of packData) console.log(`  [${p.members.length}]  ${p.slug}  —  ${p.label}`);
  console.log(`  wrote ${relative(ROOT, OUT_JSON)}`);
  console.log(`  wrote ${relative(ROOT, OUT_MD)}`);
  console.log(`  wrote ${relative(ROOT, OUT_HTML)}`);
  console.log(`  wrote ${relative(ROOT, OUT_CHAINS)}`);
  console.log(`  wrote ${relative(ROOT, OUT_PACKS_DIR)}/*.json`);
}

main();
