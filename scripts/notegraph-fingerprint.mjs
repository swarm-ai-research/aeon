#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const ROOTS = ['memory', 'docs'];
const EXCLUDES = ['memory/logs', 'node_modules', '.git'];

function walk(dir, out) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (EXCLUDES.some(e => p === e || p.startsWith(e + '/') || p.includes('/' + e + '/'))) continue;
    const st = statSync(p);
    if (st.isDirectory()) walk(p, out);
    else if (st.isFile() && p.endsWith('.md')) out.push(p);
  }
}

const files = [];
for (const r of ROOTS) walk(r, files);
files.sort();

const lines = [];
for (const f of files) {
  const h = createHash('sha1').update(readFileSync(f)).digest('hex');
  lines.push(`${h}  ${f}`);
}
const extractor = 'scripts/notegraph.mjs';
const h = createHash('sha1').update(readFileSync(extractor)).digest('hex');
lines.push(`${h}  ${extractor}`);

const combined = lines.join('\n') + '\n';
process.stdout.write(createHash('sha1').update(combined).digest('hex') + '\n');
