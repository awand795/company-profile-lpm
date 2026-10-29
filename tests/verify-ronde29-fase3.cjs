// tests/verify-ronde29-fase3.cjs
// Verifikasi 3A-3H Ronde 29 pada halaman live (localhost:5000).
const { chromium } = require('playwright');

const results = [];
function ck(code, name, ok, detail) {
    results.push({ code, name, ok: !!ok, detail });
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${code} ${name}  ${detail ?? ''}`);
}

(async () => {
    const browser = await chromium.launch({ headless: true });

    // 3A, 3B, 3C, 3D @1440x900
    let page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto('http://localhost:5000/', { waitUntil: 'load' });
    await page.waitForTimeout(400);
    const d1440 = await page.evaluate(() => {
        const q = (s) => document.querySelector(s);
        const r = (e) => { const x = e.getBoundingClientRect(); return { l: x.left, t: x.top, w: x.width, h: x.height, r: x.right, b: x.bottom }; };
        const cs = (e, p) => getComputedStyle(e, p);
        const photo = q('.hero-truck-img');
        const card = q('.hero-telematics-card');
        const wrap = q('.hero-visual-card-wrap');
        const col = q('.hero-visual-col');
        const marker = q('.hero-brand-highlight');
        const tint = cs(wrap, '::before');
        const overlay = cs(photo, '::after');
        const chips = [...document.querySelectorAll('.hero-brands-block .brand-chip')].map((e) => Math.round(r(e).t));
        const rows = {};
        chips.forEach((y) => { rows[y] = (rows[y] || 0) + 1; });
        return {
            markerBg: cs(marker).backgroundImage,
            markerAfter: cs(marker, '::after').content,
            photo: r(photo), ratio: r(photo).w / r(photo).h,
            cardW: r(card).w, cardPct: r(card).w / r(photo).w,
            overlay: overlay.backgroundImage,
            wrapPad: [cs(wrap).paddingTop, cs(wrap).paddingRight, cs(wrap).paddingBottom, cs(wrap).paddingLeft],
            tint: { top: tint.top, right: tint.right, bottom: tint.bottom, left: tint.left, transform: tint.transform },
            wrap: r(wrap), col: r(col),
            photoB: r(photo).b,
            chipB: Math.max(...[...document.querySelectorAll('.hero-brands-block .brand-chip')].map((e) => r(e).b)),
            chipRows: Object.values(rows), chipCount: chips.length,
        };
    });
    ck('3A', 'H1 memakai marker highlight, bukan garis bawah', /linear-gradient/.test(d1440.markerBg) && d1440.markerAfter === 'none', d1440.markerBg.slice(0, 80));
    ck('3B', 'Foto >= 640px @1440', d1440.photo.w >= 640, `${d1440.photo.w}x${d1440.photo.h}`);
    // Ronde 30 E1 menggantikan target rasio 1,55: tinggi foto kini mengikuti
    // kolom teks agar dasar foto sejajar dasar chip merek terakhir.
    ck('3B', 'Dasar foto = dasar chip terakhir (<= 4px)', Math.abs(d1440.photoB - d1440.chipB) <= 4, `${d1440.photoB.toFixed(1)}/${d1440.chipB.toFixed(1)}`);
    ck('3B', 'Overlay foto 0.30', /0\.3\b|0\.30\b/.test(d1440.overlay), d1440.overlay);
    ck('3B', 'Kartu telematika <= 62% lebar foto', d1440.cardPct <= 0.62, d1440.cardPct.toFixed(3));
    // Ronde 30 E1: padding-bawah 16px dihapus; tint menggantung 16px ke bawah.
    ck('3C', 'Tint di dalam grid, padding 16px kanan, bawah 0, tint -16px', d1440.wrapPad[1] === '16px' && d1440.wrapPad[2] === '0px' && d1440.tint.transform === 'none' && d1440.tint.bottom === '-16px', `${JSON.stringify(d1440.wrapPad)} ${d1440.tint.bottom}`);
    ck('3C', 'Tepi tint tidak keluar kolom', parseFloat(d1440.tint.right) <= d1440.wrap.w + 0.5 && parseFloat(d1440.tint.bottom) <= d1440.wrap.b + 0.5 && d1440.wrap.r <= d1440.col.r + 0.5, `tint ${d1440.tint.right}/${d1440.tint.bottom}`);
    ck('3D', 'Enam chip merek = 2 baris x 3', d1440.chipCount === 6 && d1440.chipRows.length === 2 && d1440.chipRows.every((n) => n === 3), d1440.chipRows.join(','));
    await page.close();

    // 3D CTA @1366x600
    page = await browser.newPage({ viewport: { width: 1366, height: 600 } });
    await page.goto('http://localhost:5000/', { waitUntil: 'load' });
    await page.waitForTimeout(300);
    const ctaBottom = await page.evaluate(() => {
        const rows = [...document.querySelectorAll('.hero-btns-row .elementor-button')];
        return Math.max(...rows.map((e) => e.getBoundingClientRect().bottom));
    });
    ck('3D', 'Bawah CTA <= 460px @1366x600', ctaBottom <= 460, ctaBottom.toFixed(1));
    await page.close();

    // 3E/3F/3G/3H @390x844
    page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await page.goto('http://localhost:5000/', { waitUntil: 'load' });
    await page.waitForTimeout(400);
    const m = await page.evaluate(() => {
        const q = (s) => document.querySelector(s);
        const r = (e) => { const x = e.getBoundingClientRect(); return { l: x.left, t: x.top, w: x.width, h: x.height, r: x.right, b: x.bottom }; };
        const cs = (e, p) => getComputedStyle(e, p);
        const stats = q('.hero-stats-inner');
        const book = q('.stitch-sec-booking');
        const title = q('.stat-number .elementor-counter-title');
        const line = cs(title, '::before');
        const formEls = [...document.querySelectorAll('#mt-booking-form label, #mt-booking-form select, .booking-info, #mt-booking-wa')];
        const feat = q('.features-grid-row');
        const featCol = q('.feat-bento-col');
        return {
            statsDisplay: cs(stats).display,
            statsDir: cs(stats).flexDirection,
            colW: r(q('.stat-col')).w, statsW: r(stats).w,
            icon: r(q('.stat-icon .elementor-icon')),
            numFs: parseFloat(cs(q('.stat-number .elementor-counter-number-wrapper')).fontSize),
            lineW: line.width, lineH: line.height,
            titleLines: r(title).h / parseFloat(cs(title).lineHeight),
            gap: r(book).t - r(stats).b,
            heroInnerPb: cs(q('.stitch-sec-hero > .e-con-inner')).paddingBottom,
            bookPad: cs(book.querySelector('.e-con-inner')).paddingTop,
            eyebrowAlign: cs(q('.stitch-sec-booking p.elementor-heading-title')).textAlign,
            h2Align: cs(q('.stitch-sec-booking h2')).textAlign,
            leadAlign: cs(q('.stitch-sec-booking .elementor-widget-text-editor')).textAlign,
            inline: formEls.map((e) => e.getAttribute('style')),
            selectH: cs(q('#mt-booking-unit')).height,
            selectFs: cs(q('#mt-booking-unit')).fontSize,
            waMinH: cs(q('#mt-booking-wa')).minHeight, waH: r(q('#mt-booking-wa')).h,
            featDir: cs(feat).flexDirection, featColW: r(featCol).w, featRowW: r(feat).w,
            overflow: document.documentElement.scrollWidth - window.innerWidth,
        };
    });
    ck('3E', 'Strip mobile satu kolom vertikal', m.statsDisplay === 'flex' && m.statsDir === 'column', `${m.statsDisplay}/${m.statsDir}`);
    ck('3E', 'Sel penuh, ikon 36px', Math.abs(m.colW - (m.statsW - 32)) < 3 && m.icon.w === 36 && m.icon.h === 36, `${m.colW}/${m.icon.w}`);
    ck('3E', 'Angka clamp dan garis 24x3', m.numFs >= 24 && m.numFs <= 30 && m.lineW === '24px' && m.lineH === '3px', `${m.numFs}px ${m.lineW}x${m.lineH}`);
    ck('3E', 'Label maksimal 3 baris', m.titleLines <= 3.05, m.titleLines.toFixed(2));
    // Ronde 30 E4: padding bawah hero mobile 0 (jarak total ke eyebrow 56-64px).
    ck('3F', 'Hero padding-bottom 0px mobile', m.heroInnerPb === '0px', m.heroInnerPb);
    ck('3F', 'Section booking padding 44px mobile', m.bookPad === '44px', m.bookPad);
    ck('3F', 'Jarak strip -> section booking <= 72px', m.gap <= 72, m.gap.toFixed(1));
    ck('3F', 'Eyebrow/H2/lead booking rata kiri', [m.eyebrowAlign, m.h2Align, m.leadAlign].every((x) => x === 'start' || x === 'left'), `${m.eyebrowAlign}/${m.h2Align}/${m.leadAlign}`);
    ck('3G', 'Form booking tanpa inline style', m.inline.every((x) => !x), m.inline.filter(Boolean).length + ' inline');
    ck('3G', 'Select 48px / 16px', m.selectH === '48px' && m.selectFs === '16px', `${m.selectH}/${m.selectFs}`);
    ck('3G', 'Tombol WA >= 52px', m.waMinH === '52px' && m.waH >= 52, `${m.waMinH}/${m.waH.toFixed(1)}`);
    ck('3H', 'Keunggulan 1 kolom mobile (native)', m.featDir === 'column' && Math.abs(m.featColW - m.featRowW) < 2, `${m.featDir} ${m.featColW}/${m.featRowW}`);
    ck('LAYOUT', 'Tanpa overflow horizontal @390', m.overflow <= 0, `${m.overflow}px`);
    await page.close();

    await browser.close();
    const fail = results.filter((x) => !x.ok);
    console.log(`\nTOTAL ${results.length - fail.length} PASS / ${fail.length} FAIL`);
    process.exit(fail.length ? 1 : 0);
})();
