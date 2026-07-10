import { readFileSync, readdirSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

function walk(dir) {
  const results = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) {
      if (p === 'memory/logs' || p.includes('node_modules') || p.includes('/.git')) continue;
      results.push(...walk(p));
    } else if (name.endsWith('.md')) {
      results.push(p);
    }
  }
  return results;
}

function sha1(buf) {
  return createHash('sha1').update(buf).digest('hex');
}

const files = [...walk('memory'), ...walk('docs')].sort();
const parts = [];
for (const f of files) {
  parts.push(`${sha1(readFileSync(f))}  ${f}`);
}
parts.push(`${sha1(readFileSync('scripts/notegraph.mjs'))}  scripts/notegraph.mjs`);

const combined = parts.join('\n') + '\n';
process.stdout.write(sha1(combined) + '\n');
