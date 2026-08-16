import fs from 'node:fs';
process.chdir('/home/runner/work/aeon/aeon');

// Extract grep-based ground truth
const text = fs.readFileSync('aeon.yml', 'utf8');
const lines = text.split('\n');
const enabledFromGrep = new Set();
let curSkill = null;
for (let i = 0; i < lines.length; i++) {
  const l = lines[i];
  // detect skill headers at indent 2
  const inline = l.match(/^ {2}([a-z0-9_-]+):\s*\{([^}]*(?:\}[^}]*)?)?/);
  const blockHeader = l.match(/^ {2}([a-z0-9_-]+):\s*(#.*)?$/);
  if (blockHeader) curSkill = blockHeader[1];
  if (inline) {
    curSkill = inline[1];
    // Check if enabled: true appears in this whole inline block
    // could span lines if multi-line
    let block = l;
    if (!/\}/.test(l)) {
      for (let j = i+1; j < lines.length; j++) {
        block += ' ' + lines[j];
        if (/\}/.test(lines[j])) break;
      }
    }
    if (/enabled:\s*true/.test(block)) enabledFromGrep.add(curSkill);
    continue;
  }
  if (/^\s+enabled:\s*true/.test(l) && curSkill && !/^\s*#/.test(l)) {
    enabledFromGrep.add(curSkill);
  }
}
console.log('enabled from grep count:', enabledFromGrep.size);
console.log([...enabledFromGrep].sort().join('\n'));
