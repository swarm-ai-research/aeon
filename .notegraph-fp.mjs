#!/usr/bin/env node
import { readFileSync, writeFileSync, statSync } from 'node:fs';
import { readdirSync } from 'node:fs';
import { join, relative } from 'node:path';
import { createHash } from 'node:crypto';

const roots = ['memory', 'docs'];
const files = [];

function walk(dir) {
  for (const ent of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, ent.name);
    if (ent.isDirectory()) {
      if (p.startsWith('memory/logs')) continue;
      if (p.includes('node_modules')) continue;
      if (p.includes('.git')) continue;
      walk(p);
    } else if (ent.isFile() && ent.name.endsWith('.md')) {
      files.push(p);
    }
  }
}

for (const r of roots) walk(r);
files.sort();

let allHashLines = '';
for (const f of files) {
  const h = createHash('sha1').update(readFileSync(f)).digest('hex');
  allHashLines += `${h}  ${f}\n`;
}
const extractorHash = createHash('sha1').update(readFileSync('scripts/notegraph.mjs')).digest('hex');
allHashLines += `${extractorHash}  scripts/notegraph.mjs\n`;

const finalFingerprint = createHash('sha1').update(allHashLines).digest('hex');
console.log(finalFingerprint);
writeFileSync('/tmp/notegraph.fingerprint', finalFingerprint + '\n');
