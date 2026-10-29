// tests/measure-ronde29.cjs
// FASE 1 Ronde 29: ukur kondisi hero/strip/booking/keunggulan TANPA mengubah kode.
// Output: playwright_review/sebelum_ronde29/{screenshot}.png + laporan_ukur.md + ukur.json
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:5000/';
const OUT = path.join(__dirname, '..', 'playwright_review', 'sebelum_ronde29');
const VIEWPORTS = [
    { name: '360x740', w: 360, h: 740, mobile: true },
    { name: '375x812', w: 375, h: 812, mobile: true },
    { name: '390x844', w: 390, h: 844, mobile: true },
    { name: '414x896', w: 414, h: 896, mobile: true },
    { name: '768x1024', w: 768, h: 1024, mobile: false },
    { name: '1366x600', w: 1366, h: 600, mobile: false },
    { name: '1440x900', w: 1440, h: 900, mobile: false },
    { name: '1920x1080', w: 1920, h: 1080, mobile: false },
];

const css = fs.readFileSync(path.join(__dirname, '..', 'assets', 'css', 'mt-custom.css'), 'utf8');

// --- statistik CSS: total !important + jumlah kemunculan selektor lingkup ---
const scopeTokens = [
    '.stitch-topbar', '.topbar-', '.hero-authority', '.hero-title', '.hero-brand-highlight',
    '.hero-lead', '.hero-btns-row', '.btn-hero-', '.hero-brands', '.brand-chip', '.brand-label',
    '.hero-visual-card-wrap', '.hero-truck-img', '.hero-telematics', '.telematics-',
    '.hero-stats-inner', '.stat-col', '.stat-item', '.stat-text-col', '.stat-icon', '.stat-number',
];
const cssNoComments = css.replace(/\/\*[\s\S]*?\*\//g, '');
const totalImportant = (css.match(/!important/g) || []).length;
const selectorCounts = {};
for (const t of scopeTokens) {
    selectorCounts[t] = (cssNoComments.split(t).length - 1);
}
// !important di dalam rule yang selektornya mengandung token lingkup
let scopeImportant = 0;
const scopeRules = [];
const ruleRe = /([^{}]+)\{([^{}]*)\}/g;
let m;
while ((m = ruleRe.exec(cssNoComments))) {
    const sel = m[1].trim();
    const body = m[2];
    if (!scopeTokens.some((t) => sel.includes(t))) continue;
    scopeRules.push(sel);
    if (/!important/.test(body)) scopeImportant += (body.match(/!important/g) || []).length;
}

const rgb = (s) => (s || '').replace(/\s/g, '');

async function measureViewport(browser, vp) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
    const page = await ctx.newPage();
    await page.goto(BASE, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(700);

    const data = await page.evaluate(() => {
        const rect = (el) => { const r = el.getBoundingClientRect(); return { l: +r.left.toFixed(1), t: +r.top.toFixed(1), r: +r.right.toFixed(1), b: +r.bottom.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1) }; };
        const lineCount = (el) => {
            const range = document.createRange();
            range.selectNodeContents(el);
            const rects = [...range.getClientRects()].filter((x) => x.height > 0 && x.height <= 40);
            return new Set(rects.map((x) => Math.round(x.top))).size;
        };
        const statCols = [...document.querySelectorAll('.hero-stats-inner .stat-col')].map((col, i) => {
            const item = col.querySelector('.stat-item');
            const textCol = col.querySelector('.stat-text-col');
            const num = col.querySelector('.elementor-counter-number-wrapper');
            const title = col.querySelector('.elementor-counter-title');
            const card = document.querySelector('.hero-stats-inner');
            return {
                i,
                col: rect(col),
                textCol: textCol ? rect(textCol) : null,
                num: num ? rect(num) : null,
                numText: num ? num.innerText.trim().replace(/\s+/g, ' ') : '',
                label: title ? title.innerText.trim() : '',
                labelLines: title ? lineCount(title) : null,
                scroll: {
                    col: { sw: col.scrollWidth, cw: col.clientWidth },
                    item: item ? { sw: item.scrollWidth, cw: item.clientWidth } : null,
                    textCol: textCol ? { sw: textCol.scrollWidth, cw: textCol.clientWidth } : null,
                    num: num ? { sw: num.scrollWidth, cw: num.clientWidth } : null,
                },
                overflowCol: num ? +(rect(num).r - rect(col).r).toFixed(1) : null,
                overflowCard: num ? +(rect(num).r - rect(card).r).toFixed(1) : null,
                overflowViewport: num ? +(rect(num).r - window.innerWidth).toFixed(1) : null,
                card: rect(card),
                cardCS: { pad: getComputedStyle(card).padding, marginTop: getComputedStyle(card).marginTop, radius: getComputedStyle(card).borderRadius },
            };
        });

        const secs = [...document.querySelectorAll('[class*="stitch-sec-"]')].filter((e) => /(^|\s)stitch-sec-/.test(e.className)).map((e) => {
            const cls = e.className.split(' ').find((c) => c.startsWith('stitch-sec-'));
            const cs = getComputedStyle(e);
            return { cls, id: e.id || null, rect: rect(e), padTop: cs.paddingTop, padBottom: cs.paddingBottom };
        });
        const gapsSec = [];
        for (let i = 0; i < secs.length - 1; i++) {
            gapsSec.push({ from: secs[i].cls, to: secs[i + 1].cls, gap: +(secs[i + 1].rect.t - secs[i].rect.b).toFixed(1) });
        }

        const card = document.querySelector('.hero-stats-inner');
        const bookingTitle = [...document.querySelectorAll('h1,h2,h3,h4')].find((h) => /Pesan Jadwal Servis Anda/.test(h.textContent));
        const gapStatsBooking = (card && bookingTitle) ? +(bookingTitle.getBoundingClientRect().top - card.getBoundingClientRect().bottom).toFixed(1) : null;

        const featCols = [...document.querySelectorAll('.feat-bento-col')].map((c) => {
            const cs = getComputedStyle(c);
            const parent = c.parentElement;
            return {
                w: rect(c).w, h: rect(c).h,
                width: cs.width, flexBasis: cs.flexBasis,
                parentFlexDir: getComputedStyle(parent).flexDirection,
                parentFlexWrap: getComputedStyle(parent).flexWrap,
                parentW: rect(parent).w,
                stacked: rect(c).w > rect(parent).w * 0.9,
            };
        });

        const bcard = document.querySelector('.booking-card');
        const bcs = bcard ? getComputedStyle(bcard) : null;
        const selects = [...document.querySelectorAll('#mt-booking-form select')].map((s) => {
            const cs = getComputedStyle(s);
            return {
                id: s.id, rect: rect(s), height: cs.height, fontSize: cs.fontSize,
                scrollW: s.scrollWidth, clientW: s.clientWidth,
                selectedText: s.options[s.selectedIndex] ? s.options[s.selectedIndex].text : '',
                textOverflow: cs.textOverflow, hasInlineStyle: s.hasAttribute('style'),
            };
        });
        const wa = document.querySelector('#mt-booking-wa');
        const taps = [...document.querySelectorAll('#mt-booking-form a, #mt-booking-form button, #mt-booking-form select, #mt-booking-form input')]
            .filter((e) => e.getBoundingClientRect().width > 0)
            .map((e) => ({ tag: e.tagName, id: e.id, w: +e.getBoundingClientRect().width.toFixed(1), h: +e.getBoundingClientRect().height.toFixed(1) }))
            .filter((x) => x.w < 44 || x.h < 44);

        const overflowEls = [];
        for (const el of document.querySelectorAll('body *')) {
            const r = el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) continue;
            if (r.right > window.innerWidth + 1 || r.left < -1) {
                const cs = getComputedStyle(el);
                if (cs.position === 'fixed') continue;
                overflowEls.push({
                    tag: el.tagName, cls: String(el.className).slice(0, 70),
                    l: +r.left.toFixed(1), r: +r.right.toFixed(1), w: +r.width.toFixed(1),
                    parentCls: String(el.parentElement && el.parentElement.className).slice(0, 60),
                });
                if (overflowEls.length >= 12) break;
            }
        }

        return {
            doc: { scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth },
            statCols, secs, gapsSec, gapStatsBooking,
            featCols,
            booking: bcard ? { rect: rect(bcard), padding: bcs.padding, height: bcs.height, selects, wa: wa ? { rect: rect(wa), boxShadow: getComputedStyle(wa).boxShadow, hasInlineStyle: wa.hasAttribute('style') } : null, taps, inlineStyled: document.querySelectorAll('#mt-booking-form [style]').length } : null,
            overflowEls,
            h1: (() => { const h = document.querySelector('.hero-title .elementor-heading-title'); if (!h) return null; const hl = h.querySelector('.hero-brand-highlight'); return { textDecoration: getComputedStyle(h).textDecorationLine, highlight: hl ? { position: getComputedStyle(hl).position, isolation: getComputedStyle(hl).isolation, afterZ: getComputedStyle(hl, '::after').zIndex, afterH: getComputedStyle(hl, '::after').height, afterBottom: getComputedStyle(hl, '::after').bottom, afterBg: getComputedStyle(hl, '::after').backgroundColor, afterContent: getComputedStyle(hl, '::after').content } : null }; })(),
            photo: (() => { const p = document.querySelector('.hero-truck-img'); const img = p && p.querySelector('img'); const badge = document.querySelector('.hero-authority-badge'); const chips = [...document.querySelectorAll('.brand-chip')]; const last = chips[chips.length - 1]; const wrap = document.querySelector('.hero-visual-card-wrap'); const cardEl = document.querySelector('.hero-telematics-card'); const vr = document.querySelector('.hero-visual-col'); return p ? { rect: rect(p), imgPos: img ? getComputedStyle(img).objectPosition : null, topDiff: badge ? +(rect(p).t - rect(badge).t).toFixed(1) : null, bottomVsChip: last ? +(rect(p).b - rect(last).b).toFixed(1) : null, wrap: wrap ? rect(wrap) : null, card: cardEl ? rect(cardEl) : null, cardRatio: cardEl ? +(rect(cardEl).w / rect(p).w * 100).toFixed(1) : null, visualCol: vr ? rect(vr) : null, before: wrap ? (() => { const c = getComputedStyle(wrap, '::before'); return { bg: c.backgroundColor, radius: c.borderRadius, w: c.width, h: c.height, transform: c.transform, inset: `${c.top} ${c.right} ${c.bottom} ${c.left}`, right: +(rect(wrap).r + 16).toFixed(1) }; })() : null } : null; })(),
        };
    });

    for (const [suffix, full] of [['view', false], ['full', true]]) {
        await page.screenshot({ path: path.join(OUT, `ronde29-${vp.name}-${suffix}.png`), fullPage: full });
    }
    await ctx.close();
    return data;
}

(async () => {
    fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ headless: true });
    const results = {};
    for (const vp of VIEWPORTS) {
        results[vp.name] = await measureViewport(browser, vp);
        console.log('OK', vp.name);
    }
    await browser.close();

    // ---------- laporan markdown ----------
    const mobiles = ['360x740', '375x812', '390x844', '414x896'];
    const L = [];
    L.push('# Laporan Ukur Ronde 29 — Kondisi Sebelum Perbaikan');
    L.push('');
    L.push(`Tanggal: 2026-10-29 · URL: ${BASE} · CSS: ${css.split('\n').length} baris, ${totalImportant} \`!important\`, ${scopeImportant} \`!important\` pada lingkup hero/strip.`);
    L.push('');
    L.push('## Ringkasan CSS');
    L.push('');
    L.push('| Metrik | Nilai |');
    L.push('| --- | --- |');
    L.push(`| Total baris mt-custom.css | ${css.split('\n').length} |`);
    L.push(`| Total \`!important\` | ${totalImportant} |`);
    L.push(`| \`!important\` pada rule lingkup hero/strip/topbar | ${scopeImportant} |`);
    L.push(`| Rule lingkup terdeteksi | ${scopeRules.length} |`);
    L.push('');
    L.push('| Selektor | Kemunculan di CSS |');
    L.push('| --- | --- |');
    for (const [k, v] of Object.entries(selectorCounts).sort((a, b) => b[1] - a[1])) L.push(`| \`${k}\` | ${v} |`);
    L.push('');
    L.push('## Scroll Horizontal (8 viewport)');
    L.push('');
    L.push('| Viewport | scrollWidth | innerWidth | Selisih | Penyebab (elemen) |');
    L.push('| --- | --- | --- | --- | --- |');
    for (const vp of VIEWPORTS) {
        const d = results[vp.name];
        const culprits = d.overflowEls.slice(0, 4).map((e) => `${e.tag}.${e.cls.split(' ')[0]} (${e.l}..${e.r})`).join('; ') || '—';
        L.push(`| ${vp.name} | ${d.doc.scrollW} | ${d.doc.innerW} | ${d.doc.scrollW - d.doc.innerW} | ${culprits} |`);
    }
    L.push('');
    L.push('## A. Strip Statistik Mobile (4 ukuran)');
    for (const vp of mobiles) {
        const d = results[vp];
        L.push('');
        L.push(`### ${vp}`);
        L.push('');
        L.push('| # | Lebar kolom | Area teks | scrollW/cw kolom | scrollW/cw teks | Angka | Baris label | Overflow angka vs kolom | vs kartu | vs viewport |');
        L.push('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |');
        for (const s of d.statCols) {
            L.push(`| ${s.i + 1} | ${s.col.w}px | ${s.textCol ? s.textCol.w : '—'}px | ${s.scroll.col.sw}/${s.scroll.col.cw} | ${s.scroll.textCol ? s.scroll.textCol.sw + '/' + s.scroll.textCol.cw : '—'} | ${s.numText} | ${s.labelLines} | ${s.overflowCol}px | ${s.overflowCard}px | ${s.overflowViewport}px |`);
        }
        L.push('');
        L.push(`Kartu strip: padding ${d.statCols[0] ? d.statCols[0].cardCS.pad : '—'}, margin-top ${d.statCols[0] ? d.statCols[0].cardCS.marginTop : '—'}, radius ${d.statCols[0] ? d.statCols[0].cardCS.radius : '—'}.`);
    }
    L.push('');
    L.push('## B. Jarak Vertikal');
    L.push('');
    L.push('| Viewport | Bawah kartu strip → judul booking |');
    L.push('| --- | --- |');
    for (const vp of VIEWPORTS) L.push(`| ${vp.name} | ${results[vp.name].gapStatsBooking}px |`);
    L.push('');
    L.push('### Jarak antar-section (bawah section → atas section berikutnya)');
    L.push('');
    L.push('| Viewport | Section | Jarak ke berikutnya |');
    L.push('| --- | --- | --- |');
    for (const vp of VIEWPORTS) for (const g of results[vp.name].gapsSec) L.push(`| ${vp.name} | ${g.from} → ${g.to} | ${g.gap}px |`);
    L.push('');
    L.push('## C. Kartu Keunggulan (.feat-bento-col)');
    L.push('');
    L.push('| Viewport | # | Lebar | Tinggi | flex-basis | Flex-direction induk | Menumpuk 1 kolom? |');
    L.push('| --- | --- | --- | --- | --- | --- | --- |');
    for (const vp of VIEWPORTS) results[vp.name].featCols.forEach((f, i) => L.push(`| ${vp.name} | ${i + 1} | ${f.w}px | ${f.h}px | ${f.flexBasis} | ${f.parentFlexDir} | ${f.stacked ? 'ya' : 'tidak'} |`));
    L.push('');
    L.push('## D. Form Booking (mobile 390, desktop 1440)');
    for (const vp of ['390x844', '1440x900']) {
        const b = results[vp].booking;
        L.push('');
        L.push(`### ${vp}`);
        L.push('');
        if (!b) { L.push('Tidak ditemukan.'); continue; }
        L.push(`- Tinggi kartu: **${b.rect.h}px**, padding **${b.padding}**, elemen ber-style inline: **${b.inlineStyled}**`);
        L.push(`- Tombol WA: **${b.wa.rect.w}×${b.wa.rect.h}px**, shadow \`${b.wa.boxShadow}\`, inline style: **${b.wa.hasInlineStyle}**`);
        L.push(`- Tap target < 44px di form: **${b.taps.length}** ${b.taps.length ? JSON.stringify(b.taps) : ''}`);
        L.push('');
        L.push('| Select | Tinggi | Font | scrollW/cw | Teks terpilih | text-overflow | Inline style |');
        L.push('| --- | --- | --- | --- | --- | --- | --- |');
        for (const s of b.selects) L.push(`| ${s.id} | ${s.height} | ${s.fontSize} | ${s.scrollW}/${s.clientW} | ${s.selectedText} | ${s.textOverflow} | ${s.hasInlineStyle ? 'ya' : 'tidak'} |`);
    }
    L.push('');
    L.push('## E. H1 & Foto (kondisi awal)');
    L.push('');
    L.push('| Viewport | text-decoration H1 | sorotan ::after | Lebar foto | Tinggi foto | Δ atas foto-badge | Δ bawah foto-chip | Kartu/foto | Tint |');
    L.push('| --- | --- | --- | --- | --- | --- | --- | --- | --- |');
    for (const vp of VIEWPORTS) {
        const d = results[vp.name]; const p = d.photo;
        L.push(`| ${vp.name} | ${d.h1 ? d.h1.textDecoration : '—'} | ${d.h1 && d.h1.highlight ? d.h1.highlight.afterContent + ' h=' + d.h1.highlight.afterH + ' bg=' + d.h1.highlight.afterBg : '—'} | ${p ? p.rect.w : '—'} | ${p ? p.rect.h : '—'} | ${p ? p.topDiff : '—'} | ${p ? p.bottomVsChip : '—'} | ${p ? p.cardRatio + '%' : '—'} | ${p && p.before ? p.before.transform : '—'} |`);
    }
    L.push('');
    L.push('## Screenshot');
    L.push('');
    for (const vp of VIEWPORTS) L.push(`- \`ronde29-${vp.name}-view.png\`, \`ronde29-${vp.name}-full.png\``);
    fs.writeFileSync(path.join(OUT, 'laporan_ukur.md'), L.join('\n') + '\n', 'utf8');
    fs.writeFileSync(path.join(OUT, 'ukur.json'), JSON.stringify({ meta: { totalImportant, scopeImportant, scopeRules: scopeRules.length, selectorCounts, lines: css.split('\n').length }, results }, null, 2), 'utf8');
    console.log('Laporan:', path.join(OUT, 'laporan_ukur.md'));
})();
