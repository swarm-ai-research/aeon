import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

const files = execSync("git ls-files -- 'skills/*/SKILL.md'", { encoding: 'utf8' })
  .split('\n')
  .filter(Boolean)
  .sort();

const parts = [];
for (const f of files) {
  const h = createHash('sha1').update(readFileSync(f)).digest('hex');
  parts.push(`${h}  ${f}`);
}
const extHash = createHash('sha1').update(readFileSync('scripts/skillpacks.mjs')).digest('hex');
parts.push(`${extHash}  scripts/skillpacks.mjs`);

const combined = parts.map(p => p + '\n').join('');
const fp = createHash('sha1').update(combined).digest('hex');
console.log(fp);
