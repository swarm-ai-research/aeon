#!/usr/bin/env node
import { createHash } from 'crypto';
import { readFileSync } from 'fs';
import { execSync } from 'child_process';

const files = execSync("find memory docs -name '*.md' -not -path 'memory/logs/*' -not -path '*/node_modules/*' -not -path '*/.git/*'", { encoding: 'utf8' })
  .split('\n')
  .filter(Boolean)
  .sort();

const h = createHash('sha1');
for (const f of files) {
  const fh = createHash('sha1').update(readFileSync(f)).digest('hex');
  h.update(`${fh}  ${f}\n`);
}
const sh = createHash('sha1').update(readFileSync('scripts/notegraph.mjs')).digest('hex');
h.update(`${sh}  scripts/notegraph.mjs\n`);
console.log(h.digest('hex'));
