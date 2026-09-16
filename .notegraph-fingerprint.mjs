#!/usr/bin/env node
import { createHash } from 'crypto';
import { readFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) {
      if (p === 'memory/logs' || p.endsWith('/node_modules') || p.endsWith('/.git')) continue;
      walk(p, out);
    } else if (name.endsWith('.md')) {
      out.push(p);
    }
  }
  return out;
}

const files = [...walk('memory'), ...walk('docs')].sort();
const lines = [];
for (const f of files) {
  const h = createHash('sha1').update(readFileSync(f)).digest('hex');
  lines.push(`${h}  ${f}`);
}
const extractorHash = createHash('sha1').update(readFileSync('scripts/notegraph.mjs')).digest('hex');
lines.push(`${extractorHash}  scripts/notegraph.mjs`);
const finger = createHash('sha1').update(lines.join('\n') + '\n').digest('hex');
console.log(finger);
