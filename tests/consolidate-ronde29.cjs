// tests/consolidate-ronde29.cjs
// FASE 2: hapus seluruh rule lama untuk lingkup topbar/hero/strip, lalu
// tambahkan blok "HERO v1" yang sudah dikonsolidasi.
// Rule non-lingkup dan selector campuran dipertahankan apa adanya.
const fs = require('fs');
const path = require('path');

const cssPath = path.join(__dirname, '..', 'assets', 'css', 'mt-custom.css');
const blockPath = path.join(__dirname, '..', 'tools', 'hero-v1.css');
const src = fs.readFileSync(cssPath, 'utf8');

const TOKENS = [
    '.stitch-topbar', '.topbar-', '.hero-authority', '.hero-title', '.hero-brand-highlight',
    '.hero-lead', '.hero-btns-row', '.btn-hero-', '.hero-brands', '.brand-chip', '.brand-label',
    '.hero-visual-card-wrap', '.hero-truck-img', '.hero-telematics', '.telematics-',
    '.hero-stats-inner', '.stat-col', '.stat-item', '.stat-text-col', '.stat-icon', '.stat-number',
    '.hero-text-col', '.hero-visual-col', '.hero-main-row', '.hero-', '.stitch-sec-hero',
];
const inScope = (sel) => TOKENS.some((t) => sel.includes(t));

function splitSelectors(sel) {
    const parts = [];
    let depth = 0, start = 0, quote = null;
    for (let i = 0; i < sel.length; i++) {
        const c = sel[i];
        if (quote) { if (c === '\\') i++; else if (c === quote) quote = null; continue; }
        if (c === '"' || c === "'") { quote = c; continue; }
        if (c === '(' || c === '[') depth++;
        else if (c === ')' || c === ']') depth--;
        else if (c === ',' && depth === 0) { parts.push(sel.slice(start, i).trim()); start = i + 1; }
    }
    parts.push(sel.slice(start).trim());
    return parts.filter(Boolean);
}

function findClose(s, open, end) {
    let p = open + 1, depth = 1, quote = null;
    while (p < end) {
        const c = s[p];
        if (quote) {
            if (c === '\\') { p += 2; continue; }
            if (c === quote) quote = null;
            p++; continue;
        }
        if (c === '/' && s[p + 1] === '*') { const e = s.indexOf('*/', p + 2); p = e < 0 ? end : e + 2; continue; }
        if (c === '"' || c === "'") { quote = c; p++; continue; }
        if (c === '{') depth++;
        else if (c === '}') { depth--; if (depth === 0) return p + 1; }
        p++;
    }
    return end;
}

function parseRange(s, start, end) {
    const nodes = [];
    let p = start;
    while (p < end) {
        let q = p;
        while (q < end && /\s/.test(s[q])) q++;
        if (q >= end) break;
        if (s.startsWith('/*', q)) {
            const e = s.indexOf('*/', q + 2);
            const stop = e < 0 ? end : e + 2;
            nodes.push({ type: 'comment', gap: s.slice(p, q), raw: s.slice(q, stop) });
            p = stop; continue;
        }
        const open = s.indexOf('{', q);
        if (open < 0 || open >= end) {
            nodes.push({ type: 'raw', gap: s.slice(p, q), raw: s.slice(q, end) });
            p = end; break;
        }
        const prelude = s.slice(q, open).trim();
        const close = findClose(s, open, end);
        if (prelude.startsWith('@media')) {
            nodes.push({
                type: 'media', gap: s.slice(p, q), prelude,
                children: parseRange(s, open + 1, close - 1),
                raw: s.slice(q, close),
            });
        } else if (prelude.startsWith('@')) {
            nodes.push({ type: 'at', gap: s.slice(p, q), raw: s.slice(q, close) });
        } else {
            nodes.push({
                type: 'rule', gap: s.slice(p, q), selector: prelude,
                raw: s.slice(q, close),
                bodyRaw: s.slice(open + 1, close - 1),
            });
        }
        p = close;
    }
    return nodes;
}

let removedRules = 0, rewrittenRules = 0, removedMedia = 0;

function serialize(nodes) {
    let out = '';
    for (const n of nodes) {
        if (n.type === 'comment' || n.type === 'raw' || n.type === 'at') { out += n.gap + n.raw; continue; }
        if (n.type === 'media') {
            const kids = serialize(n.children);
            if (!kids.trim()) { removedMedia++; out += n.gap; continue; }
            out += n.gap + n.prelude + ' {' + kids + '}';
            continue;
        }
        const parts = splitSelectors(n.selector);
        const keep = parts.filter((s) => !inScope(s));
        if (keep.length === 0) { removedRules++; out += n.gap; continue; }
        if (keep.length === parts.length) { out += n.gap + n.raw; continue; }
        rewrittenRules++;
        out += n.gap + keep.join(', ') + ' {' + n.bodyRaw + '}';
    }
    return out;
}

const tree = parseRange(src, 0, src.length);
let next = serialize(tree);

const marker = 'HERO v1 (konsolidasi Ronde 29)';
if (next.includes(marker)) {
    console.log('Blok HERO v1 sudah ada, tidak menambahkan lagi.');
} else {
    const block = fs.readFileSync(blockPath, 'utf8').trim();
    next = next.replace(/\s*$/, '\n\n') + block + '\n';
}

// Rapikan hanya bagian lama (di atas blok HERO v1): buang komentar yang
// menjelaskan rule lingkup yang sudah dihapus, lalu ringkas banner panjang.
const markerPos = next.indexOf(marker);
if (markerPos > 0) {
    const headEnd = next.lastIndexOf('/*', markerPos);
    let head = next.slice(0, headEnd);
    const tail = next.slice(headEnd);
    const commentRe = /\/\*[\s\S]*?\*\//g;
    head = head.replace(commentRe, (m) => (
        /hero|topbar|top bar|statistik|\bstat\b|bento|oranye/i.test(m) ? '' : m
    ));
    const condense = (m) => {
        const lines = m.slice(2, -2).split('\n')
            .map((l) => l.trim().replace(/^[=\-*]+\s*/, '').replace(/\s*[=\-*]+$/, ''))
            .filter(Boolean);
        return `/* ${lines.join(' ').replace(/\s+/g, ' ')} */`;
    };
    head = head.replace(commentRe, (m) => {
        const n = m.split('\n').length;
        const banner = /^\/\*\s*[=\-]/.test(m);
        return n >= 4 || (n >= 3 && banner) ? condense(m) : m;
    });
    head = head.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n');
    next = head + tail;
}

fs.writeFileSync(cssPath, next, 'utf8');
console.log(JSON.stringify({
    removedRules, rewrittenRules, removedMedia,
    linesBefore: src.split('\n').length,
    linesAfter: next.split('\n').length,
    importantBefore: (src.match(/!important/g) || []).length,
    importantAfter: (next.match(/!important/g) || []).length,
}, null, 2));
