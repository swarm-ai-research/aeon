#!/usr/bin/env node
// Skill-graph generator. Reads inputs, computes fingerprint, generates the
// multi-diagram doc, persists state, and prints result JSON on the last line.

import fs from 'node:fs';
import crypto from 'node:crypto';

const REPO = '/home/runner/work/aeon/aeon';
process.chdir(REPO);

const TODAY = process.env.TODAY || '2026-08-16';
const OUT = process.env.OUT_PATH || 'docs/skill-graph.md';
const STATE_PATH = 'memory/topics/skill-graph-state.json';
const LOG_PATH = `memory/logs/${TODAY}.md`;

const sha1 = (b) => crypto.createHash('sha1').update(b).digest('hex');

// -------- Step 1: fingerprint --------
function computeFingerprint() {
  const parts = [];
  parts.push(sha1(fs.readFileSync('aeon.yml')) + '  aeon.yml');
  parts.push(sha1(fs.readFileSync('skills.json')) + '  skills.json');
  const slugs = fs.readdirSync('skills').filter(d => fs.existsSync(`skills/${d}/SKILL.md`)).sort();
  const acc = [];
  for (const slug of slugs) {
    const file = `skills/${slug}/SKILL.md`;
    const text = fs.readFileSync(file, 'utf8');
    let inFm = false, done = false;
    for (const line of text.split('\n')) {
      if (line === '---') {
        if (!inFm) { inFm = true; continue; }
        else { done = true; break; }
      }
      if (inFm && !done) acc.push(`${file}: ${line}`);
    }
    for (const line of text.split('\n')) {
      if (/^depends_on:|^- skill:|consume:|parallel:|trigger:/.test(line)) acc.push(line);
    }
    const refs = new Set();
    const re = /memory\/(topics|state)\/[a-zA-Z0-9_.-]+/g;
    let m; while ((m = re.exec(text)) !== null) refs.add(m[0]);
    for (const r of [...refs].sort()) acc.push(r);
  }
  const inner = sha1(acc.join('\n') + '\n');
  const fp = sha1(parts.join('\n') + '\n' + inner + '  -');
  return fp;
}

// -------- Parse aeon.yml --------
function parseAeon() {
  const text = fs.readFileSync('aeon.yml', 'utf8');
  const lines = text.split('\n');
  const skills = {};
  const reactive = {};
  const chains = {};
  let section = null; // 'skills' | 'reactive' | 'chains' | null
  let cur = null; // current skill/reactive/chain name
  let curChainStep = null;
  let inSteps = false;
  let mlKey = null; // multi-line "|" key
  let mlInd = 0;
  let mlBuf = [];
  const commitMl = () => {
    if (!mlKey) return;
    if (skills[cur]) skills[cur][mlKey] = mlBuf.join('\n');
    mlKey = null; mlBuf = [];
  };
  const indentOf = (l) => (l.match(/^ */) || [''])[0].length;

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const ind = indentOf(raw);
    // Multi-line block
    if (mlKey) {
      if (raw.trim() === '' || ind >= mlInd) { mlBuf.push(raw.slice(mlInd)); continue; }
      commitMl();
    }
    if (/^\s*#/.test(raw)) continue;
    if (raw.trim() === '') continue;
    if (ind === 0) {
      commitMl();
      cur = null; curChainStep = null; inSteps = false;
      if (/^skills:\s*$/.test(raw)) { section = 'skills'; continue; }
      if (/^reactive:\s*$/.test(raw)) { section = 'reactive'; continue; }
      if (/^chains:\s*$/.test(raw)) { section = 'chains'; continue; }
      section = null;
      continue;
    }
    if (section === 'skills') {
      // Match `  slug: { ... }` or `  slug:`
      const inlineSkill = raw.match(/^ {2}([a-z0-9_-]+):\s*\{(.*)\}(\s*(#.*)?)?$/);
      const blockSkill = raw.match(/^ {2}([a-z0-9_-]+):\s*(#.*)?$/);
      if (inlineSkill) {
        cur = inlineSkill[1];
        skills[cur] = skills[cur] || {};
        parseInlineMap(inlineSkill[2], skills[cur]);
        continue;
      } else if (blockSkill) {
        cur = blockSkill[1];
        skills[cur] = skills[cur] || {};
        // Handle multi-line brace form: next non-comment line may start with `{`
        let j = i + 1;
        while (j < lines.length && (/^\s*#/.test(lines[j]) || lines[j].trim() === '')) j++;
        if (j < lines.length && /^\s*\{/.test(lines[j])) {
          // collect through matching `}`
          const buf = [];
          let depth = 0, started = false;
          for (; j < lines.length; j++) {
            const l = lines[j];
            for (const ch of l) {
              if (ch === '{') { depth++; started = true; }
              else if (ch === '}') depth--;
            }
            buf.push(l);
            if (started && depth === 0) { i = j; break; }
          }
          const joined = buf.join(' ');
          const inner = joined.slice(joined.indexOf('{')+1, joined.lastIndexOf('}'));
          parseInlineMap(inner, skills[cur]);
        }
        continue;
      }
      if (cur && ind >= 4) {
        // multi-line var: |
        const ml = raw.match(/^ {4}([a-z_]+):\s*\|\s*$/);
        if (ml) { mlKey = ml[1]; mlBuf = []; mlInd = 6; continue; }
        // handle `{` continuing over multiple lines? Skip — inline works because our aeon.yml uses single-line {...}
        const kv = raw.match(/^ {4}([a-z_]+):\s*(.*)$/);
        if (kv) setSkillKV(skills[cur], kv[1], kv[2].trim());
      }
    } else if (section === 'reactive') {
      const m2 = raw.match(/^ {2}([a-z0-9_-]+):\s*$/);
      if (m2) { cur = m2[1]; reactive[cur] = { trigger: [] }; continue; }
      if (cur && /^ {4}trigger:\s*$/.test(raw)) continue;
      const trg = raw.match(/^ {6}-\s*\{(.*)\}\s*$/);
      if (trg && cur) {
        const t = {};
        parseInlineMap(trg[1], t);
        reactive[cur].trigger.push(t);
      }
    } else if (section === 'chains') {
      const m2 = raw.match(/^ {2}([a-z0-9_-]+):\s*$/);
      if (m2) { cur = m2[1]; chains[cur] = { steps: [] }; inSteps = false; curChainStep = null; continue; }
      if (cur && /^ {4}steps:\s*$/.test(raw)) { inSteps = true; continue; }
      if (cur && /^ {4}schedule:\s*(.*)$/.test(raw)) {
        chains[cur].schedule = raw.match(/^ {4}schedule:\s*(.*)$/)[1].trim().replace(/^["']|["']$/g,'');
        continue;
      }
      if (inSteps) {
        const stepStart = raw.match(/^ {6}-\s*(.*)$/);
        if (stepStart) {
          curChainStep = { skill: null, consume: [], parallel: [] };
          chains[cur].steps.push(curChainStep);
          const rest = stepStart[1].trim();
          const kvm = rest.match(/^(skill|parallel|consume):\s*(.*)$/);
          if (kvm) applyChainKV(curChainStep, kvm[1], kvm[2].trim());
        } else {
          const kvm = raw.match(/^ {8}(skill|parallel|consume):\s*(.*)$/);
          if (kvm && curChainStep) applyChainKV(curChainStep, kvm[1], kvm[2].trim());
        }
      }
    }
  }
  commitMl();
  return { skills, reactive, chains };
}
function applyChainKV(step, k, v) {
  if (k === 'skill') step.skill = v.replace(/^["']|["']$/g,'');
  else step[k] = v.replace(/^\[|\]$/g,'').split(',').map(s => s.trim().replace(/^["']|["']$/g,'')).filter(Boolean);
}
function setSkillKV(dst, key, val) {
  // Strip trailing inline comment when the value is quoted or a bareword
  const qm = val.match(/^"([^"]*)"/);
  if (qm) val = qm[1];
  else {
    const bm = val.match(/^([^#\s"]+)/);
    if (bm) val = bm[1];
    val = val.replace(/^["']|["']$/g,'');
  }
  if (key === 'enabled') dst.enabled = (val === 'true');
  else if (key === 'schedule') dst.schedule = val;
  else if (key === 'model') dst.model = val;
  else if (key === 'var') dst.var = val;
}
function parseInlineMap(body, dst) {
  // split on commas not inside quotes
  const parts = [];
  let depth = 0, cur = '', inStr = null;
  for (const ch of body) {
    if (inStr) { cur += ch; if (ch === inStr) inStr = null; continue; }
    if (ch === '"' || ch === "'") { inStr = ch; cur += ch; continue; }
    if (ch === '[' || ch === '{') { depth++; cur += ch; continue; }
    if (ch === ']' || ch === '}') { depth--; cur += ch; continue; }
    if (ch === ',' && depth === 0) { parts.push(cur.trim()); cur = ''; continue; }
    cur += ch;
  }
  if (cur.trim()) parts.push(cur.trim());
  for (const p of parts) {
    const m = p.match(/^([a-z_]+):\s*(.*)$/);
    if (m) setSkillKV(dst, m[1], m[2].trim());
  }
}

// -------- Parse skills.json --------
function parseSkillsJson() {
  const raw = fs.readFileSync('skills.json', 'utf8');
  return JSON.parse(raw);
}

// -------- Parse SKILL.md frontmatter --------
function parseSkillFm(slug) {
  const file = `skills/${slug}/SKILL.md`;
  if (!fs.existsSync(file)) return null;
  const text = fs.readFileSync(file, 'utf8');
  const lines = text.split('\n');
  let inFm = false, done = false;
  const fmLines = [];
  for (const line of lines) {
    if (line === '---') {
      if (!inFm) { inFm = true; continue; }
      else { done = true; break; }
    }
    if (inFm && !done) fmLines.push(line);
  }
  const fm = { name: slug, tags: [], depends_on: [] };
  for (const line of fmLines) {
    const m = line.match(/^([a-zA-Z0-9_]+):\s*(.*)$/);
    if (!m) continue;
    const key = m[1];
    let val = m[2].trim();
    if (val.startsWith('[') && val.endsWith(']')) {
      fm[key] = val.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g,'')).filter(Boolean);
    } else {
      fm[key] = val.replace(/^["']|["']$/g,'');
    }
  }
  fm.text = text;
  return fm;
}

// -------- Derived shared-state edges --------
function deriveSharedState(slugs, fms) {
  const writers = new Map();
  const readers = new Map();
  const WRITE = /(write|save|append|update|persist|regenerate|rewrite|writes?\s|create|patch)\b/i;
  for (const slug of slugs) {
    const fm = fms[slug]; if (!fm) continue;
    const lines = fm.text.split('\n');
    const localFound = new Map(); // resource -> 'W'|'R'
    for (let i = 0; i < lines.length; i++) {
      const re = /memory\/(topics|state)\/[a-zA-Z0-9_.-]+/g;
      let m; while ((m = re.exec(lines[i])) !== null) {
        const resource = m[0];
        const window = lines.slice(Math.max(0, i-3), Math.min(lines.length, i+4)).join(' ');
        const isW = WRITE.test(window) || />\s*['"`]?memory\//.test(window);
        const prev = localFound.get(resource);
        if (prev === 'W' || isW) localFound.set(resource, 'W');
        else if (!prev) localFound.set(resource, 'R');
      }
    }
    for (const [resource, kind] of localFound) {
      const map = kind === 'W' ? writers : readers;
      if (!map.has(resource)) map.set(resource, new Set());
      map.get(resource).add(slug);
    }
  }
  const edges = new Map();
  for (const [resource, wset] of writers) {
    if (/cron-state\.json/.test(resource)) continue;
    const rset = readers.get(resource) || new Set();
    // also count any other writer as a reader (writers still see the file)
    for (const w of wset) {
      for (const r of new Set([...(rset), ...wset])) {
        if (w === r) continue;
        const key = `${w}->${r}`;
        if (!edges.has(key)) edges.set(key, new Set());
        edges.get(key).add(resource);
      }
    }
  }
  return [...edges.entries()].map(([k, resources]) => {
    const [from, to] = k.split('->'); return { from, to, resources: [...resources] };
  });
}

// -------- Categorize --------
function categorize(slugs, fms, skillsJson) {
  const catBySlug = {};
  const jsonBySlug = new Map();
  for (const s of skillsJson.skills) jsonBySlug.set(s.slug, s);
  const validCats = new Set(Object.keys(skillsJson.categories));
  for (const slug of slugs) {
    const j = jsonBySlug.get(slug);
    if (j && validCats.has(j.category)) { catBySlug[slug] = j.category; continue; }
    // Fall back to first matching tag
    const fm = fms[slug];
    if (fm && Array.isArray(fm.tags)) {
      let placed = false;
      for (const tag of fm.tags) {
        if (validCats.has(tag)) { catBySlug[slug] = tag; placed = true; break; }
        // Map common aliases
        const aliasMap = {
          content: 'research',
          data: 'research',
          eval: 'dev',
          meta: 'productivity',
          security: 'dev',
          ai: 'research',
          creative: 'research',
          growth: 'social',
          community: 'social',
          docs: 'productivity',
          memory: 'productivity',
          ops: 'productivity',
          github: 'dev',
          build: 'dev',
          dx: 'dev',
          protocol: 'dev',
          ecosystem: 'dev',
          infra: 'dev',
          compute: 'crypto',
          depin: 'crypto',
          markets: 'crypto',
          gpu: 'crypto',
          pricing: 'crypto',
          x402: 'crypto',
          'compute-futures': 'crypto',
          'compute-markets': 'crypto',
          'prediction-markets': 'crypto',
          macro: 'crypto',
          capability: 'research',
          ideas: 'productivity',
          research: 'research',
          crypto: 'crypto',
          dev: 'dev',
          social: 'social',
          productivity: 'productivity',
          analysis: 'research',
          ads: 'social',
        };
        if (aliasMap[tag]) { catBySlug[slug] = aliasMap[tag]; placed = true; break; }
      }
      if (!placed) catBySlug[slug] = 'productivity';
    } else {
      catBySlug[slug] = 'productivity';
    }
  }
  return catBySlug;
}

// -------- Build edges --------
function buildEdges(slugs, fms, aeon, sharedState) {
  const edges = { depends_on: [], consume: [], reactive: [], shared_state: sharedState };
  const setOfSlugs = new Set(slugs);
  for (const slug of slugs) {
    const fm = fms[slug]; if (!fm) continue;
    if (Array.isArray(fm.depends_on)) {
      for (const dep of fm.depends_on) {
        if (setOfSlugs.has(dep)) edges.depends_on.push({ from: dep, to: slug });
      }
    }
  }
  for (const [name, cfg] of Object.entries(aeon.chains || {})) {
    let prev = null;
    for (const step of cfg.steps || []) {
      const currents = step.parallel && step.parallel.length ? step.parallel : (step.skill ? [step.skill] : []);
      for (const c of currents) {
        for (const src of (step.consume || [])) {
          if (setOfSlugs.has(src) && setOfSlugs.has(c)) edges.consume.push({ from: src, to: c, chain: name });
        }
      }
    }
  }
  for (const [target, cfg] of Object.entries(aeon.reactive || {})) {
    for (const trg of cfg.trigger || []) {
      const on = trg.on || '*';
      edges.reactive.push({ from: on, to: target, when: trg.when || '' });
    }
  }
  return edges;
}

// -------- Mermaid rendering --------
const CAT_ORDER = ['research', 'dev', 'crypto', 'social', 'productivity'];
const CAT_TITLES = { research: 'Research & Content', dev: 'Dev & Code', crypto: 'Crypto & Markets', social: 'Social', productivity: 'Productivity & Meta' };

function mermaidNode(slug, aeon) {
  const s = aeon.skills[slug] || {};
  const schedLabel = s.enabled ? (s.schedule ? ` (${s.schedule})` : '') : '';
  const label = schedLabel ? `${slug}<br/>${escapeMermaid(s.schedule || '')}` : slug;
  return `  ${slug}["${label}"]:::${s.enabled ? 'enabled' : 'disabled'}`;
}
function escapeMermaid(s) {
  return String(s).replace(/"/g, '\'').replace(/[\[\]]/g, '');
}

function renderOverview(catBySlug, edges) {
  const catCounts = Object.fromEntries(CAT_ORDER.map(c => [c, 0]));
  for (const c of Object.values(catBySlug)) if (catCounts[c] != null) catCounts[c]++;

  // Count cross-category edges
  const crossCounts = new Map(); // "a->b" -> count
  const bump = (a, b) => {
    if (a === b) return;
    const k = `${a}->${b}`;
    crossCounts.set(k, (crossCounts.get(k) || 0) + 1);
  };
  for (const e of edges.depends_on) if (catBySlug[e.from] && catBySlug[e.to]) bump(catBySlug[e.from], catBySlug[e.to]);
  for (const e of edges.consume) if (catBySlug[e.from] && catBySlug[e.to]) bump(catBySlug[e.from], catBySlug[e.to]);
  for (const e of edges.shared_state) if (catBySlug[e.from] && catBySlug[e.to]) bump(catBySlug[e.from], catBySlug[e.to]);

  const lines = [];
  lines.push('```mermaid');
  lines.push('flowchart LR');
  for (const c of CAT_ORDER) {
    lines.push(`  ${c}["${CAT_TITLES[c]}<br/><small>${catCounts[c]} skills</small>"]`);
  }
  for (const [k, n] of crossCounts) {
    const [a, b] = k.split('->');
    lines.push(`  ${a} -- "${n}" --> ${b}`);
  }
  lines.push('  classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px');
  lines.push('```');
  return lines.join('\n');
}

function renderSelfHealing(aeon) {
  const chain = ['heartbeat', 'skill-health', 'skill-evals', 'skill-repair', 'self-improve'];
  const lines = [];
  lines.push('```mermaid');
  lines.push('flowchart LR');
  for (const s of chain) {
    const enabled = aeon.skills[s]?.enabled ? 'enabled' : 'disabled';
    lines.push(`  ${s}[${s}]:::${enabled}`);
  }
  lines.push('  cron_state[("memory/cron-state.json")]:::external');
  for (let i = 0; i < chain.length - 1; i++) lines.push(`  ${chain[i]} --> ${chain[i+1]}`);
  for (const s of chain) lines.push(`  ${s} -..-> cron_state`);
  lines.push('  classDef enabled fill:#fff,stroke:#000,stroke-width:2px,color:#000');
  lines.push('  classDef disabled fill:#f5f5f5,stroke:#bbb,color:#888');
  lines.push('  classDef external fill:none,stroke:#bbb,stroke-dasharray:3 3,color:#888');
  for (const s of chain) lines.push(`  click ${s} "../skills/${s}/SKILL.md"`);
  lines.push('```');
  return lines.join('\n');
}

function renderCategory(cat, slugs, catBySlug, edges, aeon) {
  const local = slugs.filter(s => catBySlug[s] === cat).sort();
  const localSet = new Set(local);
  const lines = [];
  lines.push('```mermaid');
  lines.push('flowchart LR');
  lines.push(`  subgraph ${cat}["${CAT_TITLES[cat]} (${local.length})"]`);
  for (const s of local) {
    const cfg = aeon.skills[s] || {};
    const enabledCls = cfg.enabled ? 'enabled' : 'disabled';
    const schedFrag = cfg.enabled && cfg.schedule ? `<br/><small>${escapeMermaid(cfg.schedule)}</small>` : '';
    lines.push(`    ${s}["${s}${schedFrag}"]:::${enabledCls}`);
  }
  lines.push('  end');

  // External ghost nodes for cross-category refs
  const externals = new Set();
  const externalEdges = [];
  const intraEdges = [];
  const pushEdge = (from, to, style) => {
    const fromLocal = localSet.has(from), toLocal = localSet.has(to);
    if (fromLocal && toLocal) intraEdges.push({ from, to, style });
    else if (fromLocal || toLocal) {
      const ext = fromLocal ? to : from;
      externals.add(ext);
      externalEdges.push({ from, to, style });
    }
  };
  for (const e of edges.depends_on) pushEdge(e.from, e.to, '-->');
  for (const e of edges.consume) pushEdge(e.from, e.to, '-.->');
  for (const e of edges.shared_state) pushEdge(e.from, e.to, '-..->');

  if (externals.size) {
    lines.push('  subgraph ext[" "]');
    lines.push('    direction TB');
    for (const s of externals) lines.push(`    ${s}[${s}]:::external`);
    lines.push('  end');
    lines.push('  style ext fill:none,stroke:#ddd,stroke-dasharray:3 3');
  }

  for (const e of intraEdges) lines.push(`  ${e.from} ${e.style} ${e.to}`);
  for (const e of externalEdges) lines.push(`  ${e.from} ${e.style} ${e.to}`);

  lines.push('  classDef enabled fill:#fff,stroke:#000,stroke-width:2px,color:#000');
  lines.push('  classDef disabled fill:#f5f5f5,stroke:#bbb,color:#888');
  lines.push('  classDef external fill:none,stroke:#bbb,stroke-dasharray:3 3,color:#888');

  for (const s of [...local, ...externals]) {
    lines.push(`  click ${s} "../skills/${s}/SKILL.md"`);
  }
  lines.push('```');
  return lines.join('\n');
}

// -------- Mermaid lint --------
function lintMermaid(md) {
  const errors = [];
  const blocks = md.match(/```mermaid\n[\s\S]*?```/g) || [];
  for (const block of blocks) {
    const body = block.replace(/^```mermaid\n/, '').replace(/```$/, '');
    const lines = body.split('\n');
    // subgraph/end balance
    let sgDepth = 0;
    for (const line of lines) {
      if (/^\s*subgraph\b/.test(line)) sgDepth++;
      if (/^\s*end\s*$/.test(line)) sgDepth--;
      if (sgDepth < 0) { errors.push(`unbalanced subgraph/end: ${line}`); break; }
    }
    if (sgDepth !== 0) errors.push(`unclosed subgraph blocks: depth=${sgDepth}`);
    // Bracket balance in node declarations
    for (const line of lines) {
      const m = line.match(/^\s*[a-zA-Z0-9_-]+(\[|\(|\{).*$/);
      if (!m) continue;
      const open = (line.match(/\[/g) || []).length;
      const close = (line.match(/\]/g) || []).length;
      if (open !== close) { errors.push(`bracket mismatch: ${line}`); }
    }
    // click paths exist
    const clickRe = /^\s*click\s+([a-zA-Z0-9_-]+)\s+"([^"]+)"/gm;
    let cm;
    while ((cm = clickRe.exec(body)) !== null) {
      const rel = cm[2];
      // Skip URLs
      if (/^https?:/.test(rel)) continue;
      const resolved = rel.startsWith('../') ? rel.slice(3) : rel;
      if (!fs.existsSync(resolved)) errors.push(`click path missing: ${rel}`);
    }
  }
  return errors;
}

// -------- Diff vs prior doc --------
function extractNodesFromDoc(text) {
  const nodes = new Set();
  const re = /^\s*([a-z0-9-]+)\[[^\]]*\]/gm;
  let m; while ((m = re.exec(text)) !== null) nodes.add(m[1]);
  return nodes;
}
function extractEdgesFromDoc(text) {
  const edges = new Set();
  const re = /^\s*([a-z0-9-]+)\s+(-->|-\.->|-\.\.->|--\s*"[^"]*"\s*-->)\s+([a-z0-9-]+)/gm;
  let m; while ((m = re.exec(text)) !== null) edges.add(`${m[1]} ${m[2]} ${m[3]}`);
  return edges;
}

// -------- Main --------
function main() {
  const fingerprint = computeFingerprint();
  const priorState = fs.existsSync(STATE_PATH) ? JSON.parse(fs.readFileSync(STATE_PATH, 'utf8')) : null;
  let mode;
  if (!priorState) mode = 'SKILL_GRAPH_NEW';
  else if (priorState.input_fingerprint === fingerprint) mode = 'SKILL_GRAPH_NO_CHANGE';
  else mode = 'SKILL_GRAPH_OK';

  const slugs = fs.readdirSync('skills').filter(d => fs.existsSync(`skills/${d}/SKILL.md`)).sort();
  const fms = {};
  for (const s of slugs) fms[s] = parseSkillFm(s);
  const aeon = parseAeon();
  const skillsJson = parseSkillsJson();
  const catBySlug = categorize(slugs, fms, skillsJson);
  const sharedState = deriveSharedState(slugs, fms);
  const edges = buildEdges(slugs, fms, aeon, sharedState);

  // Enabled counts
  const enabledCount = slugs.filter(s => aeon.skills[s]?.enabled).length;
  const catCounts = {};
  for (const c of CAT_ORDER) catCounts[c] = 0;
  for (const s of slugs) if (catCounts[catBySlug[s]] != null) catCounts[catBySlug[s]]++;

  const priorDocText = fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8') : '';
  const priorNodes = extractNodesFromDoc(priorDocText);
  const priorEdges = extractEdgesFromDoc(priorDocText);

  // Verdict
  const newNodes = slugs.filter(s => !priorNodes.has(s));
  const removedNodes = [...priorNodes].filter(n => !slugs.includes(n));
  const currentEdgeSet = new Set();
  for (const e of edges.depends_on) currentEdgeSet.add(`${e.from} --> ${e.to}`);
  for (const e of edges.consume) currentEdgeSet.add(`${e.from} -.-> ${e.to}`);
  for (const e of edges.shared_state) currentEdgeSet.add(`${e.from} -..-> ${e.to}`);
  const newEdges = [...currentEdgeSet].filter(e => !priorEdges.has(e));
  const removedEdges = [...priorEdges].filter(e => !currentEdgeSet.has(e));

  let verdictOneLine;
  if (mode === 'SKILL_GRAPH_NEW') verdictOneLine = `INITIALIZED: ${slugs.length} skills`;
  else if (newNodes.length) verdictOneLine = `NEW_SKILLS: ${newNodes.slice(0,5).join(', ')}${newNodes.length>5?'…':''}`;
  else if (removedNodes.length) verdictOneLine = `RETIRED_SKILLS: ${removedNodes.slice(0,5).join(', ')}${removedNodes.length>5?'…':''}`;
  else if (newEdges.length) verdictOneLine = `NEW_DEPS: ${newEdges.slice(0,3).join(', ')}${newEdges.length>3?'…':''}`;
  else verdictOneLine = 'ARCHITECTURE_OK';

  // Build the multi-diagram doc
  const md = [];
  md.push(`# Skill Dependency Graph`);
  md.push('');
  md.push(`Auto-generated by \`skill-graph\` on ${TODAY}. Mode: \`${mode}\`.`);
  md.push('');
  md.push(`**Verdict:** ${verdictOneLine}`);
  md.push('');

  if (mode !== 'SKILL_GRAPH_NEW') {
    md.push(`## What changed since last run`);
    md.push('');
    if (!newNodes.length && !removedNodes.length && !newEdges.length && !removedEdges.length) {
      md.push('_No structural changes._');
    } else {
      if (newNodes.length) md.push(`- **Added skills** (${newNodes.length}): ${newNodes.join(', ')}`);
      if (removedNodes.length) md.push(`- **Removed skills** (${removedNodes.length}): ${removedNodes.join(', ')}`);
      if (newEdges.length) md.push(`- **New edges** (${newEdges.length}): ${newEdges.slice(0,10).join('; ')}${newEdges.length>10?'…':''}`);
      if (removedEdges.length) md.push(`- **Removed edges** (${removedEdges.length}): ${removedEdges.slice(0,10).join('; ')}${removedEdges.length>10?'…':''}`);
    }
    md.push('');
  }

  md.push(`## Overview`);
  md.push('');
  md.push(renderOverview(catBySlug, edges));
  md.push('');

  md.push(`## Self-healing loop`);
  md.push('');
  md.push(renderSelfHealing(aeon));
  md.push('');

  md.push(`## Per-category detail`);
  md.push('');
  for (const cat of CAT_ORDER) {
    md.push(`### ${CAT_TITLES[cat]} (${catCounts[cat]} skills)`);
    md.push('');
    md.push(renderCategory(cat, slugs, catBySlug, edges, aeon));
    md.push('');
  }

  md.push(`## Legend`);
  md.push('');
  md.push(`- \`-->\` **depends_on** — declared in SKILL.md frontmatter`);
  md.push(`- \`-.->\` **consume** — chain step in \`aeon.yml\` consumes prior step's output`);
  md.push(`- \`-..->\` **reactive / shared-state** — one skill writes memory that another reads`);
  md.push(`- **Bold, white** = \`enabled: true\` in \`aeon.yml\` (schedule shown under node)`);
  md.push(`- **Grey, faded** = disabled`);
  md.push(`- **Dashed border, ghost node** = external cross-category reference in per-category diagrams`);
  md.push(`- Every node is a hyperlink to its \`SKILL.md\``);
  md.push('');
  md.push(`> Note: every skill also writes \`memory/cron-state.json\` (consumed by \`heartbeat\` / \`skill-health\` / \`skill-repair\`) — collapsed to the self-healing loop diagram above.`);
  md.push('');

  md.push(`## Summary`);
  md.push('');
  md.push(`| Metric | Count |`);
  md.push(`|---|---|`);
  md.push(`| Total skills | ${slugs.length} |`);
  md.push(`| Enabled | ${enabledCount} |`);
  md.push(`| Disabled | ${slugs.length - enabledCount} |`);
  for (const c of CAT_ORDER) md.push(`| Category: ${CAT_TITLES[c]} | ${catCounts[c]} |`);
  md.push(`| Edges: depends_on | ${edges.depends_on.length} |`);
  md.push(`| Edges: consume | ${edges.consume.length} |`);
  md.push(`| Edges: reactive | ${edges.reactive.length} |`);
  md.push(`| Edges: shared-state (derived) | ${edges.shared_state.length} |`);
  md.push('');

  md.push(`---`);
  md.push('');
  md.push(`_skills parsed: ${slugs.length} · depends_on: ${edges.depends_on.length} · consume: ${edges.consume.length} · reactive: ${edges.reactive.length} · shared-state derived: ${edges.shared_state.length} · enabled: ${enabledCount}/${slugs.length} · mode: ${mode}_`);
  md.push('');

  const doc = md.join('\n');
  const lintErrors = lintMermaid(doc);
  return {
    fingerprint, mode, verdictOneLine, doc, lintErrors,
    slugs, catBySlug, edges, enabledCount, catCounts,
    newNodes, removedNodes, newEdges, removedEdges,
  };
}

const result = main();
// Emit doc + summary
const OUT_JSON = 'tmp-skill-graph/result.json';
const OUT_DOC = 'tmp-skill-graph/skill-graph.md';
fs.writeFileSync(OUT_DOC, result.doc);
const state = {
  generated_at: TODAY,
  input_fingerprint: result.fingerprint,
  skills_total: result.slugs.length,
  enabled_count: result.enabledCount,
  edges: {
    depends_on: result.edges.depends_on.length,
    consume: result.edges.consume.length,
    reactive: result.edges.reactive.length,
    shared_state: result.edges.shared_state.length,
  },
  node_list_sha: sha1(result.slugs.sort().join('\n')),
  edge_list_sha: sha1([...result.edges.depends_on, ...result.edges.consume, ...result.edges.shared_state]
    .map(e => `${e.from}->${e.to}`).sort().join('\n')),
};
const summary = {
  mode: result.mode, verdict: result.verdictOneLine,
  slugs_total: result.slugs.length, enabled: result.enabledCount,
  edges: state.edges,
  newNodes: result.newNodes, removedNodes: result.removedNodes,
  newEdges: result.newEdges, removedEdges: result.removedEdges,
  lintErrors: result.lintErrors,
  state,
};
fs.writeFileSync(OUT_JSON, JSON.stringify(summary, null, 2));
console.log(JSON.stringify(summary));
