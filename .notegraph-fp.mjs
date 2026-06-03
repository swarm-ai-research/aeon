import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === 'node_modules' || name === '.git') continue;
    const p = join(dir, name);
    let s;
    try { s = statSync(p); } catch { continue; }
    if (s.isDirectory()) {
      if (p === 'memory/logs') continue;
      walk(p, out);
    } else if (name.endsWith('.md')) {
      out.push(p);
    }
  }
  return out;
}

const files = [...walk('memory'), ...walk('docs')].sort();
const sums = files.map(f => `${createHash('sha1').update(readFileSync(f)).digest('hex')}  ${f}`);
sums.push(`${createHash('sha1').update(readFileSync('scripts/notegraph.mjs')).digest('hex')}  scripts/notegraph.mjs`);
const blob = sums.join('\n') + '\n';
const fp = createHash('sha1').update(blob).digest('hex');
console.log(fp);
