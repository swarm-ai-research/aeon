import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';

function stripGeneratedAt(s) {
  // Remove any generatedAt ISO timestamp variants
  return s
    .replace(/"generatedAt"\s*:\s*"[^"]*"/g, '"generatedAt":"<STRIPPED>"')
    .replace(/regenerated on \d{4}-\d{2}-\d{2}/g, 'regenerated on <STRIPPED>')
    .replace(/Regenerated on \d{4}-\d{2}-\d{2}/g, 'Regenerated on <STRIPPED>');
}
function hash(s) {
  return createHash('sha1').update(s).digest('hex');
}

const files = [
  'notegraph.json',
  'docs/notegraph.md',
  'docs/notegraph.html',
  'docs/notegraph-speedrun.html',
];

for (const f of files) {
  const cur = readFileSync(f, 'utf8');
  let prev;
  try {
    prev = execSync(`git show HEAD:${f}`, { encoding: 'utf8' });
  } catch (e) {
    console.log(`${f}: NEW FILE (not in HEAD)`);
    continue;
  }
  const curStripped = stripGeneratedAt(cur);
  const prevStripped = stripGeneratedAt(prev);
  const curH = hash(curStripped);
  const prevH = hash(prevStripped);
  const rawIdentical = cur === prev;
  const topoIdentical = curStripped === prevStripped;
  console.log(`${f}: raw_identical=${rawIdentical} topo_identical=${topoIdentical} prev=${prevH.slice(0,10)} cur=${curH.slice(0,10)}`);
}
