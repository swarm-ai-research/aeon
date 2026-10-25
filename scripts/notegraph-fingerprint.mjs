#!/usr/bin/env node
// Pure-node replacement for the shell fingerprint pipeline in skills/notegraph/SKILL.md.
// Produces byte-identical output to:
//   { find memory docs -name '*.md' ... | sort | xargs sha1sum; sha1sum scripts/notegraph.mjs; } | sha1sum | awk '{print $1}'
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, relative } from 'node:path';

const root = new URL('..', import.meta.url).pathname.replace(/\/$/, '');

function walk(dir, out) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (name === 'node_modules' || name === '.git') continue;
    let st;
    try { st = statSync(full); } catch { continue; }
    if (st.isDirectory()) walk(full, out);
    else if (name.endsWith('.md')) out.push(full);
  }
}

const files = [];
walk(join(root, 'memory'), files);
walk(join(root, 'docs'), files);

const kept = files
  .map(f => relative(root, f))
  .filter(rel => !rel.startsWith('memory/logs/'))
  .sort();

const outer = createHash('sha1');
for (const rel of kept) {
  const h = createHash('sha1').update(readFileSync(join(root, rel))).digest('hex');
  outer.update(`${h}  ${rel}\n`);
}
const extractorHash = createHash('sha1')
  .update(readFileSync(join(root, 'scripts/notegraph.mjs')))
  .digest('hex');
outer.update(`${extractorHash}  scripts/notegraph.mjs\n`);

process.stdout.write(outer.digest('hex') + '\n');
