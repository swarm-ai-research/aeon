#!/usr/bin/env node
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const ROOT = '/home/runner/work/aeon/aeon';
const h = createHash('sha1');

function sha1(p) {
  const d = createHash('sha1');
  d.update(readFileSync(p));
  return d.digest('hex');
}

const lines = [];
lines.push(sha1(join(ROOT, 'aeon.yml')) + '  aeon.yml');
lines.push(sha1(join(ROOT, 'skills.json')) + '  skills.json');

const skillsDir = join(ROOT, 'skills');
const skills = readdirSync(skillsDir, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => d.name)
  .sort();

const inputH = createHash('sha1');
for (const slug of skills) {
  const skillPath = join(skillsDir, slug, 'SKILL.md');
  if (!existsSync(skillPath)) continue;
  const raw = readFileSync(skillPath, 'utf8');
  // frontmatter between first and second ---
  const parts = raw.split(/^---$/m);
  if (parts.length >= 3) {
    const fm = parts[1];
    for (const line of fm.split('\n')) {
      inputH.update(`${skillPath}: ${line}\n`);
    }
  }
  // dependency-related lines
  for (const line of raw.split('\n')) {
    if (/^depends_on:|^- skill:|consume:|parallel:|trigger:/.test(line)) {
      inputH.update(line + '\n');
    }
  }
  // memory refs
  const refs = new Set();
  for (const m of raw.matchAll(/memory\/(topics|state)\/[a-zA-Z0-9_.-]+/g)) {
    refs.add(m[0]);
  }
  [...refs].sort().forEach(r => inputH.update(r + '\n'));
}
const inputDigest = inputH.digest('hex');
const combined = createHash('sha1');
for (const l of lines) combined.update(l + '\n');
combined.update(inputDigest + '  -\n');

const out = lines.join('\n') + '\n' + inputDigest + '  -\n';
writeFileSync(join(ROOT, '.skill-graph-tmp/fingerprint.txt'), out);
console.log(out);
console.log('final-fp:', combined.digest('hex'));
console.log('skills-count:', skills.length);
