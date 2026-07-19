// Compute skillpacks input fingerprint matching:
//   { git ls-files -- 'skills/*/SKILL.md' | sort | xargs sha1sum; sha1sum scripts/skillpacks.mjs; } | sha1sum
import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

const files = execSync("git ls-files -- 'skills/*/SKILL.md'", { encoding: 'utf8' })
  .trim()
  .split('\n')
  .filter(Boolean)
  .sort();

const h = createHash('sha1');
for (const f of files) {
  const fileHash = createHash('sha1').update(readFileSync(f)).digest('hex');
  h.update(`${fileHash}  ${f}\n`);
}
const scriptHash = createHash('sha1').update(readFileSync('scripts/skillpacks.mjs')).digest('hex');
h.update(`${scriptHash}  scripts/skillpacks.mjs\n`);
console.log(h.digest('hex'));
