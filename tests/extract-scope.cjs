// Ekstrak rule CSS lingkup hero/strip/topbar + konteks @media yang benar.
const fs = require('fs');
const path = require('path');
const file = path.join(__dirname, '..', 'assets', 'css', 'mt-custom.css');
const src = fs.readFileSync(file, 'utf8');

const TOKENS = [
    '.stitch-topbar', '.topbar-', '.hero-authority', '.hero-title', '.hero-brand-highlight',
    '.hero-lead', '.hero-btns-row', '.btn-hero-', '.hero-brands', '.brand-chip', '.brand-label',
    '.hero-visual-card-wrap', '.hero-truck-img', '.hero-telematics', '.telematics-',
    '.hero-stats-inner', '.stat-col', '.stat-item', '.stat-text-col', '.stat-icon', '.stat-number',
    '.hero-text-col', '.hero-visual-col', '.hero-main-row',
];
const inScope = (sel) => TOKENS.some((t) => sel.includes(t));
const lineOf = (idx) => src.slice(0, idx).split('\n').length;
const clean = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '').trim().replace(/\s+/g, ' ');

const out = [];
let pos = 0;
const n = src.length;

function skipWsComments(p) {
    while (p < n) {
        if (/\s/.test(src[p])) { p++; continue; }
        if (src[p] === '/' && src[p + 1] === '*') {
            const e = src.indexOf('*/', p + 2);
            p = e < 0 ? n : e + 2;
            continue;
        }
        break;
    }
    return p;
}

function findBlockEnd(open) { // open = index '{'
    let p = open + 1, depth = 1;
    while (p < n && depth > 0) {
        const c = src[p];
        if (c === '/' && src[p + 1] === '*') { const e = src.indexOf('*/', p + 2); p = e < 0 ? n : e + 2; continue; }
        if (c === '"' || c === "'") { const q = c; p++; while (p < n && src[p] !== q) { if (src[p] === '\\') p++; p++; } p++; continue; }
        if (c === '{') depth++;
        else if (c === '}') depth--;
        p++;
    }
    return p; // setelah '}'
}

function walk(p, end, media, base) {
    p = skipWsComments(p);
    while (p < end) {
        // @media
        if (src[p] === '@') {
            const open = src.indexOf('{', p);
            if (open < 0 || open >= end) break;
            const prelude = clean(src.slice(p, open));
            const close = findBlockEnd(open);
            if (/^@media/.test(prelude)) {
                walk(open + 1, close - 1, prelude, base);
            }
            p = skipWsComments(close);
            continue;
        }
        const open = src.indexOf('{', p);
        if (open < 0 || open >= end) break;
        const sel = clean(src.slice(p, open));
        const close = findBlockEnd(open);
        const body = clean(src.slice(open + 1, close - 1));
        if (sel && inScope(sel)) {
            out.push({ media, selector: sel, body, line: lineOf(p) });
        }
        p = skipWsComments(close);
    }
}

walk(0, n, '(base)', 0);
fs.writeFileSync(path.join(__dirname, '..', 'playwright_review', 'sebelum_ronde29', 'scope-rules.json'), JSON.stringify(out, null, 2), 'utf8');
const byMedia = {};
for (const r of out) byMedia[r.media] = (byMedia[r.media] || 0) + 1;
console.log('total rule lingkup:', out.length);
console.log(byMedia);
