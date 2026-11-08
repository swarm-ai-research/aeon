#!/usr/bin/env node
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const ROOT = '/home/runner/work/aeon/aeon';

// --- Parse aeon.yml (not strict yaml — just the structure present) ---
const yml = readFileSync(join(ROOT, 'aeon.yml'), 'utf8');
const ymlLines = yml.split('\n');

const aeon = { skills: {}, reactive: {}, chainsActive: false };

// Simple scan — each top-level `skillname: {` or `skillname:` entry inside `skills:` block
let section = null;
let currentKey = null;
let currentBuf = '';
let braceDepth = 0;
for (let i = 0; i < ymlLines.length; i++) {
  const raw = ymlLines[i];
  const line = raw.replace(/\r$/, '');
  if (/^skills:\s*$/.test(line)) { section = 'skills'; continue; }
  if (/^reactive:\s*$/.test(line)) { section = 'reactive'; continue; }
  if (/^chains:\s*$/.test(line)) { section = 'chains'; continue; }
  if (/^[a-z_-]+:\s*$/.test(line) && !/^\s/.test(line)) {
    if (!['skills', 'reactive', 'chains'].includes(line.replace(':', '').trim())) {
      section = 'other';
      continue;
    }
  }
  if (section === 'skills') {
    // A skill entry line starts with 2-space indent and `name: ...`
    const m = line.match(/^  ([a-zA-Z0-9_-]+):(\s*)(.*)$/);
    if (m && braceDepth === 0) {
      currentKey = m[1];
      const rest = m[3];
      // handle `{` opening a block
      if (rest.startsWith('{')) {
        braceDepth = (rest.match(/\{/g) || []).length - (rest.match(/\}/g) || []).length;
        currentBuf = rest;
        if (braceDepth === 0) {
          parseSkillInline(currentKey, currentBuf);
          currentKey = null;
          currentBuf = '';
        }
      } else if (rest === '' || rest.startsWith('#')) {
        // multi-line form
        currentBuf = '';
        braceDepth = 0;
        // read following indented lines
        let j = i + 1;
        const propLines = [];
        while (j < ymlLines.length) {
          const l2 = ymlLines[j];
          if (/^    [a-zA-Z_-]+:/.test(l2) || /^      /.test(l2) || /^    [|>]/.test(l2) || /^    \S/.test(l2)) {
            propLines.push(l2);
            j++;
          } else {
            break;
          }
        }
        parseSkillMultiline(currentKey, propLines);
        i = j - 1;
        currentKey = null;
      }
    } else if (braceDepth > 0) {
      currentBuf += '\n' + line;
      braceDepth += (line.match(/\{/g) || []).length - (line.match(/\}/g) || []).length;
      if (braceDepth === 0) {
        parseSkillInline(currentKey, currentBuf);
        currentKey = null;
        currentBuf = '';
      }
    }
  } else if (section === 'reactive') {
    const m = line.match(/^  ([a-zA-Z0-9_-]+):\s*$/);
    if (m) {
      currentKey = m[1];
      aeon.reactive[currentKey] = [];
    } else {
      const tm = line.match(/when:\s*"([^"]+)"/);
      const om = line.match(/on:\s*"([^"]+)"/);
      if (tm || om) {
        const entry = aeon.reactive[currentKey] && aeon.reactive[currentKey][aeon.reactive[currentKey].length - 1];
        if (entry && (tm || om)) {
          // finalize if already full
        }
      }
      if (/trigger:/.test(line)) continue;
      const bm = line.match(/\{\s*on:\s*"([^"]+)",\s*when:\s*"([^"]+)"\s*\}/);
      if (bm && currentKey) {
        aeon.reactive[currentKey].push({ on: bm[1], when: bm[2] });
      }
    }
  }
}

function parseSkillInline(key, buf) {
  const flat = buf.replace(/\n/g, ' ').replace(/\s+/g, ' ');
  const enabledM = flat.match(/enabled:\s*(true|false)/);
  const schedM = flat.match(/schedule:\s*"([^"]*)"/);
  const varM = flat.match(/var:\s*"([^"]*)"/);
  const modelM = flat.match(/model:\s*"([^"]*)"/);
  aeon.skills[key] = {
    enabled: enabledM ? enabledM[1] === 'true' : false,
    schedule: schedM ? schedM[1] : '',
    var: varM ? varM[1] : '',
    model: modelM ? modelM[1] : '',
  };
}
function parseSkillMultiline(key, lines) {
  const obj = { enabled: false, schedule: '', var: '', model: '' };
  for (const l of lines) {
    const e = l.match(/\s*enabled:\s*(true|false)/);
    const s = l.match(/\s*schedule:\s*"([^"]*)"/);
    const v = l.match(/\s*var:\s*"([^"]*)"/);
    const m = l.match(/\s*model:\s*"([^"]*)"/);
    if (e) obj.enabled = e[1] === 'true';
    if (s) obj.schedule = s[1];
    if (v) obj.var = v[1];
    if (m) obj.model = m[1];
  }
  aeon.skills[key] = obj;
}

// --- Parse skills.json for category map ---
const skillsJson = JSON.parse(readFileSync(join(ROOT, 'skills.json'), 'utf8'));
const catMap = {};
for (const s of skillsJson.skills || []) {
  catMap[s.slug] = s.category;
}
const categoryLabels = { ...(skillsJson.categories || {}), other: 'Other & Uncategorized' };

// --- Parse each SKILL.md frontmatter + body ---
const skillsDir = join(ROOT, 'skills');
const slugs = readdirSync(skillsDir, { withFileTypes: true })
  .filter(d => d.isDirectory() && existsSync(join(skillsDir, d.name, 'SKILL.md')))
  .map(d => d.name)
  .sort();

const skills = {};
for (const slug of slugs) {
  const raw = readFileSync(join(skillsDir, slug, 'SKILL.md'), 'utf8');
  const parts = raw.split(/^---$/m);
  let fm = '';
  let body = raw;
  if (parts.length >= 3) {
    fm = parts[1];
    body = parts.slice(2).join('---');
  }
  const nameM = fm.match(/^name:\s*(.+)$/m);
  const tagsM = fm.match(/^tags:\s*\[([^\]]+)\]/m);
  const dependsOn = [];
  // depends_on may be yaml list form
  const dM = fm.match(/^depends_on:\s*(.*)$/m);
  if (dM) {
    const rest = dM[1].trim();
    if (rest.startsWith('[')) {
      const inner = rest.replace(/^\[|\]$/g, '');
      inner.split(',').map(s => s.trim()).filter(Boolean).forEach(s => dependsOn.push(s.replace(/["']/g, '')));
    } else if (rest) {
      dependsOn.push(rest.replace(/["']/g, ''));
    }
    // multi-line
    const lines = fm.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].startsWith('depends_on:')) {
        let j = i + 1;
        while (j < lines.length && /^\s*-\s+/.test(lines[j])) {
          const tok = lines[j].replace(/^\s*-\s+/, '').trim().replace(/["']/g, '');
          if (tok) dependsOn.push(tok);
          j++;
        }
        break;
      }
    }
  }
  const tags = tagsM ? tagsM[1].split(',').map(s => s.trim().replace(/["']/g, '')).filter(Boolean) : [];
  const name = nameM ? nameM[1].trim() : slug;

  // body-level analysis
  const refs = new Map();  // path -> {read, write}
  const lines = body.split('\n');
  const refRe = /memory\/(topics|state)\/[a-zA-Z0-9_.-]+/g;
  for (let i = 0; i < lines.length; i++) {
    const ln = lines[i];
    for (const m of ln.matchAll(refRe)) {
      const p = m[0];
      if (!refs.has(p)) refs.set(p, { read: false, write: false });
      // look at surrounding 3 lines
      const window = lines.slice(Math.max(0, i - 1), Math.min(lines.length, i + 2)).join(' ');
      if (/(write|save|append|>|update)\b[^\n]*(topics|state)\//i.test(window)) {
        refs.get(p).write = true;
      } else {
        refs.get(p).read = true;
      }
    }
  }

  // articles/*.md writes — heuristic
  const writesArticles =
    tags.includes('research') &&
    /articles\/[^\s`]*\.md/.test(body) &&
    /(write|generate|produce|publish|append|save).*article/i.test(body);

  skills[slug] = {
    slug,
    name,
    tags,
    dependsOn: [...new Set(dependsOn)],
    refs: Object.fromEntries(refs),
    writesArticles,
    enabled: aeon.skills[slug] ? aeon.skills[slug].enabled : false,
    schedule: aeon.skills[slug] ? aeon.skills[slug].schedule : '',
    var: aeon.skills[slug] ? aeon.skills[slug].var : '',
    model: aeon.skills[slug] ? aeon.skills[slug].model : '',
    category: catMap[slug] || (tags[0] || 'other'),
  };
}

// --- Derived edges ---
// 1. shared-state: write by A, read by B on same topic/state
const sharedEdges = new Set();
const topicWriters = new Map();  // topic → [slugs]
const topicReaders = new Map();
for (const slug of Object.keys(skills)) {
  for (const [path, mode] of Object.entries(skills[slug].refs)) {
    if (mode.write) {
      if (!topicWriters.has(path)) topicWriters.set(path, []);
      topicWriters.get(path).push(slug);
    }
    if (mode.read) {
      if (!topicReaders.has(path)) topicReaders.set(path, []);
      topicReaders.get(path).push(slug);
    }
  }
}
// Skip cron-state (collapsed per SKILL instructions, but it's memory/cron-state.json not memory/state/*)
for (const [path, writers] of topicWriters) {
  const readers = topicReaders.get(path) || [];
  for (const w of writers) {
    for (const r of readers) {
      if (w !== r) sharedEdges.add(JSON.stringify([w, r, path]));
    }
  }
}

// 2. content pipeline: research-tagged skills writing articles → syndicate-article, rss-feed, update-gallery
const contentSinks = ['syndicate-article', 'rss-feed', 'update-gallery'].filter(s => skills[s]);
const contentPipelineEdges = [];
for (const slug of Object.keys(skills)) {
  if (skills[slug].writesArticles) {
    for (const sink of contentSinks) {
      if (sink !== slug) contentPipelineEdges.push([slug, sink]);
    }
  }
}

// 3. depends_on
const dependsEdges = [];
for (const slug of Object.keys(skills)) {
  for (const dep of skills[slug].dependsOn) {
    if (skills[dep]) dependsEdges.push([slug, dep]);
  }
}

// 4. reactive edges: reactive triggers mean a skill fires when ANY skill meets a condition
// We model these as "reactive hubs": a reactive skill sits outside the main dep graph;
// its trigger is captured in a legend note. For the "self-healing loop" diagram we draw
// it explicitly.
const reactiveTriggers = aeon.reactive;

// 5. consume edges (chains) — all chains commented out, so none active
const consumeEdges = [];

// Write parsed structure
const out = {
  skills,
  categoryLabels,
  dependsEdges: dependsEdges.map(e => ({ from: e[0], to: e[1] })),
  consumeEdges,
  reactiveTriggers,
  sharedEdges: [...sharedEdges].map(j => {
    const [w, r, p] = JSON.parse(j);
    return { from: w, to: r, path: p };
  }),
  contentPipelineEdges: contentPipelineEdges.map(e => ({ from: e[0], to: e[1] })),
  counts: {
    total: slugs.length,
    enabled: Object.values(skills).filter(s => s.enabled).length,
  },
};

writeFileSync(join(ROOT, '.skill-graph-tmp/parsed.json'), JSON.stringify(out, null, 2));
console.log('parsed:', slugs.length, 'skills,',
  'enabled:', out.counts.enabled,
  'depends_on:', dependsEdges.length,
  'shared_state:', out.sharedEdges.length,
  'content_pipeline:', out.contentPipelineEdges.length,
  'reactive:', Object.keys(reactiveTriggers).length);
