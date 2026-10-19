// Perbaiki karakter escape yang salah: hapus backslash yang menempel langsung
// sebelum karakter non-ASCII (mis. "\“" -> "“") pada file PHP.
const fs = require('fs');

const target = process.argv[2];
if (!target) {
    console.error('usage: node fix-escapes.cjs <file>');
    process.exit(1);
}
const src = fs.readFileSync(target, 'utf8');
const re = /\\([^\x00-\x7F])/g;
const matches = src.match(re) || [];
const out = src.replace(re, '$1');
if (out !== src) {
    fs.writeFileSync(target, out);
}
console.log(`${target}: removed ${matches.length} stray backslashes; sample: ${[...new Set(matches)].slice(0, 8).join(' ')}`);
