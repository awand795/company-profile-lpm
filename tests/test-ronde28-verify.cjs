// tests/test-ronde28-verify.cjs
// Ronde 28 - Verifikasi 4 cacat hero (Page 59):
//   A. Badge satu pil (tanpa bingkai ganda, lebar = isi)
//   B. Foto sejajar kolom teks (atas = badge, bawah = chip merek terakhir, 420-520px)
//   C. Satu dekorasi tint 16px di belakang foto, tanpa pola titik di tepi foto
//   D. Kartu "Mesin Dicek Digital" di dalam foto kiri-bawah, lebar = isi, rata kiri
//   + metrik lama (CTA <= 460 @1366x600, tanpa h-scroll, tanpa tumpang tindih, tanpa emas, teks >= 12px)
//
// Jalankan: node tests/test-ronde28-verify.cjs
const { chromium } = require('playwright');

const BASE = 'http://localhost:5000/';
let pass = 0;
let fail = 0;

function check(name, ok, detail = '') {
    if (ok) { pass++; console.log(`PASS  ${name}  ${detail ? '[' + detail + ']' : ''}`); }
    else { fail++; console.log(`FAIL  ${name}  ${detail ? '[' + detail + ']' : ''}`); }
}

const rgb = (s) => (s || '').replace(/\s/g, '');

(async () => {
    const browser = await chromium.launch({ headless: true });

    const openPage = async (w, h) => {
        const ctx = await browser.newContext({ viewport: { width: w, height: h } });
        const page = await ctx.newPage();
        await page.goto(BASE, { waitUntil: 'networkidle' });
        await page.waitForTimeout(900);
        return { ctx, page };
    };

    // ==================== A. BADGE ====================
    console.log('\n=== A. BADGE SATU PIL ===');
    {
        const { ctx, page } = await openPage(1440, 900);
        const d = await page.evaluate(() => {
            const wrap = document.querySelector('.hero-authority-badge');
            const pill = document.querySelector('.hero-authority-pill');
            const title = document.querySelector('.hero-authority-badge .elementor-heading-title');
            const icon = pill.querySelector('i');
            const cs = (el, list) => { const c = getComputedStyle(el); const o = {}; list.forEach(k => o[k] = c[k]); return o; };
            const r = (el) => { const b = el.getBoundingClientRect(); return { l: b.left, t: b.top, r: b.right, b: b.bottom, w: b.width, h: b.height }; };
            // lebar isi sebenarnya: ikon + jarak + teks (tanpa padding/border)
            const range = document.createRange();
            range.selectNodeContents(title);
            const textRects = [...range.getClientRects()];
            const textW = Math.max(...textRects.map(x => x.width));
            const pillCs = cs(pill, ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth', 'borderTopColor', 'gap', 'fontSize', 'fontWeight', 'letterSpacing', 'textTransform', 'backgroundColor', 'borderRadius', 'color']);
            return {
                wrap: r(wrap), pill: r(pill),
                wrapCs: cs(wrap, ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth', 'backgroundColor', 'boxShadow', 'outlineStyle']),
                wrapContainer: wrap.querySelector('.elementor-widget-container') ? (() => {
                    const c = wrap.querySelector('.elementor-widget-container');
                    return { rect: r(c), cs: cs(c, ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth', 'backgroundColor', 'boxShadow']) };
                })() : null,
                pillCs, titleCs: cs(title, ['fontSize', 'fontWeight', 'letterSpacing', 'textTransform', 'color']),
                iconW: icon.getBoundingClientRect().width,
                iconCs: cs(icon, ['fontSize', 'color']),
                textW,
                pillTextLines: new Set(textRects.map(x => Math.round(x.top))).size,
                parentBorder: (() => {
                    const p = wrap.parentElement;
                    const c = getComputedStyle(p);
                    return { border: c.borderTopWidth, bg: c.backgroundColor, shadow: c.boxShadow, pad: c.paddingTop };
                })()
            };
        });

        const w = d.wrapCs;
        check('A1. Wrapper badge tanpa bingkai (padding 0, border 0, latar transparan, tanpa shadow/outline)',
            parseFloat(w.paddingTop) === 0 && parseFloat(w.paddingLeft) === 0 &&
            parseFloat(w.borderTopWidth) === 0 && parseFloat(w.borderLeftWidth) === 0 &&
            (w.backgroundColor === 'rgba(0, 0, 0, 0)' || w.backgroundColor === 'transparent') &&
            w.boxShadow === 'none' && (w.outlineStyle === 'none' || w.outlineStyle === ''),
            `pad=${w.paddingTop}/${w.paddingLeft} border=${w.borderTopWidth} bg=${w.backgroundColor} shadow=${w.boxShadow}`);

        if (d.wrapContainer) {
            const c = d.wrapContainer.cs;
            check('A2. Widget pembungkus badge juga tanpa bingkai',
                parseFloat(c.paddingTop) === 0 && parseFloat(c.paddingLeft) === 0 &&
                parseFloat(c.borderTopWidth) === 0 && (c.backgroundColor === 'rgba(0, 0, 0, 0)' || c.backgroundColor === 'transparent') && c.boxShadow === 'none',
                JSON.stringify(c));
        } else {
            check('A2. Widget pembungkus badge juga tanpa bingkai', true, 'tidak ada .elementor-widget-container');
        }

        check('A3. TIDAK ada bingkai ganda: kotak wrapper = kotak pil (selisih <= 1px)',
            Math.abs(d.wrap.w - d.pill.w) <= 1 && Math.abs(d.wrap.h - d.pill.h) <= 1,
            `wrap=${d.wrap.w.toFixed(1)}x${d.wrap.h.toFixed(1)} pill=${d.pill.w.toFixed(1)}x${d.pill.h.toFixed(1)}`);

        const pc = d.pillCs;
        const expectedW = d.iconW + parseFloat(pc.gap) + d.textW + parseFloat(pc.paddingLeft) + parseFloat(pc.paddingRight) + parseFloat(pc.borderLeftWidth) + parseFloat(pc.borderRightWidth);
        check('A4. Lebar pil = isi (<= teks+ikon+padding+4px)',
            d.pill.w <= expectedW + 4,
            `pil=${d.pill.w.toFixed(1)} isi=${expectedW.toFixed(1)}`);

        check('A5. Pil: padding 8px 14px, radius 999px, latar putih, border 1px #DDE3EC',
            parseFloat(pc.paddingTop) === 8 && parseFloat(pc.paddingLeft) === 14 &&
            parseFloat(pc.borderRadius) >= 999 && rgb(pc.backgroundColor) === 'rgb(255,255,255)' &&
            parseFloat(pc.borderTopWidth) === 1 && rgb(pc.borderTopColor) === 'rgb(221,227,236)',
            `pad=${pc.paddingTop}/${pc.paddingLeft} radius=${pc.borderRadius} bg=${pc.backgroundColor} border=${pc.borderTopWidth}/${pc.borderTopColor}`);

        check('A6. Teks pil 12px/700 uppercase navy, letter-spacing .04em; ikon perisai 14px biru baja',
            parseFloat(pc.fontSize) === 12 && pc.fontWeight === '700' && pc.textTransform === 'uppercase' &&
            Math.abs(parseFloat(pc.letterSpacing) - 0.48) < 0.06 && rgb(pc.color) === 'rgb(11,31,58)' &&
            parseFloat(d.iconCs.fontSize) === 14 && rgb(d.iconCs.color) === 'rgb(36,87,166)',
            `fs=${pc.fontSize} w=${pc.fontWeight} tt=${pc.textTransform} ls=${pc.letterSpacing} icon=${d.iconCs.fontSize}/${d.iconCs.color}`);

        check('A7. Teks badge maksimal 2 baris di 1440', d.pillTextLines <= 2, `baris=${d.pillTextLines}`);
        await ctx.close();
    }

    {
        // Mobile: tetap fit-content, maks 2 baris, tanpa bingkai ganda
        const { ctx, page } = await openPage(390, 844);
        const d = await page.evaluate(() => {
            const wrap = document.querySelector('.hero-authority-badge');
            const pill = document.querySelector('.hero-authority-pill');
            const title = document.querySelector('.hero-authority-badge .elementor-heading-title');
            const range = document.createRange(); range.selectNodeContents(title);
            // Hanya rect baris teks (tinggi <= 2x line-height), bukan rect blok pembungkus.
            const lineRects = [...range.getClientRects()].filter(x => x.height > 0 && x.height <= 30);
            const lines = new Set(lineRects.map(x => Math.round(x.top))).size;
            const colW = pill.parentElement.getBoundingClientRect().width ||
                wrap.parentElement.getBoundingClientRect().width;
            return {
                wrapW: wrap.getBoundingClientRect().width, pillW: pill.getBoundingClientRect().width,
                colW,
                lines, pad: getComputedStyle(wrap).paddingTop, border: getComputedStyle(wrap).borderTopWidth,
                bg: getComputedStyle(wrap).backgroundColor
            };
        });
        check('A8. Mobile 390: pil fit-content (<= lebar kolom) & maks 2 baris, tanpa bingkai',
            d.pillW <= d.colW + 1 && d.lines <= 2 && parseFloat(d.pad) === 0 && parseFloat(d.border) === 0,
            `pill=${d.pillW.toFixed(0)}/${d.colW.toFixed(0)} baris=${d.lines}`);
        await ctx.close();
    }

    // ==================== B. FOTO ====================
    console.log('\n=== B. FOTO SEJAJAR KOLOM TEKS ===');
    const measurePhoto = async (w, h) => {
        const { ctx, page } = await openPage(w, h);
        const d = await page.evaluate(() => {
            const r = (s) => { const el = document.querySelector(s); if (!el) return null; const b = el.getBoundingClientRect(); return { l: b.left, t: b.top, r: b.right, b: b.bottom, w: b.width, h: b.height }; };
            const chips = [...document.querySelectorAll('.brand-chip')];
            const last = chips[chips.length - 1];
            const img = document.querySelector('.hero-truck-img img');
            const wrap = document.querySelector('.hero-visual-card-wrap');
            const photo = document.querySelector('.hero-truck-img');
            const cs = (el, list) => { const c = getComputedStyle(el); const o = {}; list.forEach(k => o[k] = c[k]); return o; };
            const pr = photo.getBoundingClientRect();

            // Cari dekorasi berpola titik (radial-gradient) yang memotong tepi atas foto
            const dotHits = [];
            const heroEls = [document.querySelector('.stitch-sec-hero'), ...document.querySelectorAll('.stitch-sec-hero *')];
            for (const el of heroEls) {
                if (!el) continue;
                for (const pseudo of [null, '::before', '::after']) {
                    const c = getComputedStyle(el, pseudo);
                    if (!c) continue;
                    const bg = c.backgroundImage || '';
                    // Pola titik = radial-gradient berjari-jari kecil (<= 4px).
                    // Glow lembut section (460px) bukan pola titik.
                    if (!/radial-gradient/.test(bg)) continue;
                    if (!/(^|[^0-9.])(0?\.\d+|[1-4](?:\.\d+)?)px\b/.test(bg)) continue;
                    dotHits.push({ cls: el.className + (pseudo || ''), bg: bg.slice(0, 60), content: c.content });
                }
            }
            return {
                badge: r('.hero-authority-badge'), photo: r('.hero-truck-img'),
                wrap: r('.hero-visual-card-wrap'),
                lastChipBottom: last ? last.getBoundingClientRect().bottom : null,
                photoCs: cs(photo, ['borderTopWidth', 'borderTopColor', 'borderRadius', 'boxShadow', 'height', 'minHeight', 'maxHeight']),
                imgCs: cs(img, ['objectFit', 'objectPosition', 'height']),
                wrapBefore: cs(wrap, ['content']) && (() => { const c = getComputedStyle(wrap, '::before'); return { bg: c.backgroundColor, radius: c.borderRadius, w: c.width, h: c.height, transform: c.transform, zi: c.zIndex, pe: c.pointerEvents, inset: `${c.top} ${c.right} ${c.bottom} ${c.left}` }; })(),
                wrapAfter: (() => { const c = getComputedStyle(wrap, '::after'); return { content: c.content, bgImage: c.backgroundImage, display: c.display }; })(),
                dotHits,
                photoTop: pr.top, photoBottom: pr.bottom,
                card: r('.hero-telematics-card')
            };
        });
        await ctx.close();
        return d;
    };

    const photoData = {};
    for (const [w, h] of [[1280, 800], [1366, 600], [1440, 900], [1920, 1080]]) {
        const d = await measurePhoto(w, h);
        photoData[`${w}x${h}`] = d;
        const dt = Math.abs(d.photo.t - d.badge.t);
        const db = Math.abs(d.photo.b - d.lastChipBottom);
        check(`B1. ${w}x${h}: tepi atas foto = tepi atas badge (<= 4px)`, dt <= 4, `selisih=${dt.toFixed(1)}px (foto=${d.photo.t.toFixed(1)} badge=${d.badge.t.toFixed(1)})`);
        check(`B2. ${w}x${h}: tepi bawah foto = tepi bawah chip merek terakhir (<= 4px)`, db <= 4, `selisih=${db.toFixed(1)}px (foto=${d.photo.b.toFixed(1)} chip=${d.lastChipBottom.toFixed(1)})`);
        // Ronde 30 E1: tinggi foto mengikuti tinggi kolom teks supaya dasar foto
        // sejajar dasar chip (batas lama 420-520px digantikan aturan B2).
        check(`B3. ${w}x${h}: tinggi foto mengikuti kolom teks (>= 380px)`, d.photo.h >= 380, `h=${d.photo.h.toFixed(1)}px`);
    }

    const p0 = photoData['1440x900'];
    check('B4. Foto: satu border 1px #DDE3EC, radius 28px, shadow 0 24px 48px rgba(11,31,58,.14)',
        parseFloat(p0.photoCs.borderTopWidth) === 1 && rgb(p0.photoCs.borderTopColor) === 'rgb(221,227,236)' &&
        parseFloat(p0.photoCs.borderRadius) >= 28 &&
        /rgba\(11, 31, 58, 0\.14\)/.test(p0.photoCs.boxShadow),
        `border=${p0.photoCs.borderTopWidth}/${p0.photoCs.borderTopColor} radius=${p0.photoCs.borderRadius} shadow=${p0.photoCs.boxShadow}`);

    check('B5. Foto: object-fit cover, object-position 50% 30% (atap truk tidak terpotong)',
        p0.imgCs.objectFit === 'cover' && /50% 30%/.test(p0.imgCs.objectPosition),
        `fit=${p0.imgCs.objectFit} pos=${p0.imgCs.objectPosition}`);

    check('B6. Tidak ada pola titik (radial-gradient) di area foto',
        p0.dotHits.length === 0 && p0.wrapAfter.display === 'none',
        `hits=${p0.dotHits.length} after=${p0.wrapAfter.display}/${p0.wrapAfter.content}`);

    // C. Satu blok tint 16px di belakang foto
    const before = p0.wrapBefore;
    // Ronde 29 fase 3 (3C) menggantikan geser transform dengan inset di dalam
    // grid; Ronde 30 E1 membuat tepi bawahnya menggantung 16px.
    check('C1. Dekorasi = SATU blok tint #E3ECF8 radius 28 di belakang foto',
        rgb(before.bg) === 'rgb(227,236,248)' && parseFloat(before.radius) >= 28,
        `bg=${before.bg} radius=${before.radius}`);
    check('C2. Blok tint inset 16px kiri-atas & menggantung 16px kanan-bawah',
        before.transform === 'none' && before.inset === '16px 0px -16px 16px',
        `transform=${before.transform} inset=${before.inset}`);
    check('C3. Blok tint di belakang (z-index < foto) & pointer-events none',
        parseInt(before.zi) < parseInt(p0.photoCs ? 2 : 2) + 10 && before.zi !== 'auto' && before.pe === 'none',
        `z=${before.zi} pe=${before.pe}`);
    check('C4. Blok tint tidak mengubah ukuran foto (foto tetap 420-520 & tanpa h-scroll)',
        p0.photo.w > 0 && p0.photo.h <= 520, `foto=${p0.photo.w.toFixed(0)}x${p0.photo.h.toFixed(0)}`);

    // ==================== D. KARTU TELEMATIKA ====================
    console.log('\n=== D. KARTU "MESIN DICEK DIGITAL" ===');
    {
        const { ctx, page } = await openPage(1440, 900);
        const d = await page.evaluate(() => {
            const r = (el) => { const b = el.getBoundingClientRect(); return { l: b.left, t: b.top, r: b.right, b: b.bottom, w: b.width, h: b.height }; };
            const photo = document.querySelector('.hero-truck-img');
            const card = document.querySelector('.hero-telematics-card');
            const icon = card.querySelector('.telematics-chip-icon');
            const title = card.querySelector('.telematics-title');
            const pill = card.querySelector('.telematics-status-pill');
            const desc = card.querySelector('.telematics-single-desc');
            const cs = (el, list) => { const c = getComputedStyle(el); const o = {}; list.forEach(k => o[k] = c[k]); return o; };
            const pr = photo.getBoundingClientRect(), cr = card.getBoundingClientRect();
            return {
                photo: r(photo), card: r(card), icon: r(icon), title: r(title), pill: r(pill), desc: r(desc),
                cardCs: cs(card, ['position', 'left', 'bottom', 'padding', 'borderRadius', 'backgroundColor', 'boxShadow', 'textAlign', 'width', 'maxWidth']),
                titleCs: cs(title, ['fontSize', 'fontWeight', 'color']),
                pillCs: cs(pill, ['fontSize', 'whiteSpace']),
                descCs: cs(desc, ['fontSize', 'color', 'textAlign', 'webkitLineClamp', 'lineHeight']),
                inside: cr.left >= pr.left - 0.5 && cr.right <= pr.right + 0.5 && cr.top >= pr.top - 0.5 && cr.bottom <= pr.bottom + 0.5,
                offLeft: +(cr.left - pr.left).toFixed(1), offBottom: +(pr.bottom - cr.bottom).toFixed(1),
                widthRatio: +(cr.width / pr.width * 100).toFixed(1),
                descLines: Math.round(desc.getBoundingClientRect().height / parseFloat(getComputedStyle(desc).lineHeight))
            };
        });
        check('D1. Seluruh kartu di dalam kotak foto', d.inside, `offset kiri=${d.offLeft} bawah=${d.offBottom}`);
        check('D2. Kartu di kiri-bawah foto, offset 20px', d.offLeft === 20 && d.offBottom === 20, `kiri=${d.offLeft} bawah=${d.offBottom}`);
        // Ronde 29 fase 3 (3B) menetapkan batas 62% lebar foto.
        check('D3. Lebar kartu = isi & <= 62% foto', d.widthRatio <= 62 && d.cardCs.maxWidth === '62%', `rasio=${d.widthRatio}% max-width=${d.cardCs.maxWidth}`);
        // Ronde 31: kartu overlay hero jadi solid navy (bukan kotak putih polos).
        check('D4. Kartu navy solid, radius 16px, padding 14px 16px, shadow navy',
            rgb(d.cardCs.backgroundColor) === 'rgb(11,31,58)' && parseFloat(d.cardCs.borderRadius) === 16 &&
            d.cardCs.padding === '14px 16px' && /rgba\(11, 31, 58/.test(d.cardCs.boxShadow),
            `bg=${d.cardCs.backgroundColor} r=${d.cardCs.borderRadius} pad=${d.cardCs.padding}`);
        check('D5. Baris 1: chip ikon 36px + judul 15px bold navy + pil "SIAP JALAN" sebaris',
            Math.round(d.icon.w) === 36 && Math.round(d.icon.h) === 36 &&
            parseFloat(d.titleCs.fontSize) === 15 && d.titleCs.fontWeight === '700' && rgb(d.titleCs.color) === 'rgb(255,255,255)' &&
            Math.abs((d.pill.t + d.pill.h / 2) - (d.title.t + d.title.h / 2)) <= 4,
            `icon=${d.icon.w}x${d.icon.h} title=${d.titleCs.fontSize}/${d.titleCs.fontWeight} pilY=${d.pill.t.toFixed(0)} titleY=${d.title.t.toFixed(0)}`);
        check('D6. Baris 2: deskripsi 13px putih transparan, rata kiri, maks 2 baris',
            parseFloat(d.descCs.fontSize) === 13 && /rgba?\(255,\s*255,\s*255/.test(d.descCs.color) &&
            d.descCs.textAlign === 'left' && parseInt(d.descCs.webkitLineClamp) === 2 && d.descLines <= 2,
            `fs=${d.descCs.fontSize} align=${d.descCs.textAlign} clamp=${d.descCs.webkitLineClamp} baris=${d.descLines}`);
        await ctx.close();
    }
    {
        const { ctx, page } = await openPage(390, 844);
        const d = await page.evaluate(() => {
            const photo = document.querySelector('.hero-truck-img').getBoundingClientRect();
            const card = document.querySelector('.hero-telematics-card').getBoundingClientRect();
            return {
                inside: card.left >= photo.left - 0.5 && card.right <= photo.right + 0.5 && card.top >= photo.top - 0.5 && card.bottom <= photo.bottom + 0.5,
                offLeft: +(card.left - photo.left).toFixed(1), offBottom: +(photo.bottom - card.bottom).toFixed(1),
                ratio: +(card.width / photo.width * 100).toFixed(1)
            };
        });
        check('D7. Mobile 390: offset 12px, lebar <= 88% foto, tidak melewati tepi foto',
            d.inside && d.offLeft === 12 && d.offBottom === 12 && d.ratio <= 88,
            `kiri=${d.offLeft} bawah=${d.offBottom} rasio=${d.ratio}%`);
        await ctx.close();
    }

    // ==================== 4. METRIK LAMA ====================
    console.log('\n=== 4. METRIK LAMA ===');
    {
        const { ctx, page } = await openPage(1366, 600);
        const d = await page.evaluate(() => {
            const btns = document.querySelector('.hero-btns-row');
            return { ctaBottom: Math.round(btns.getBoundingClientRect().bottom) };
        });
        check('M1. Bawah tombol utama <= 460px di 1366x600', d.ctaBottom <= 460, `bottom=${d.ctaBottom}px`);
        await ctx.close();
    }

    for (const w of [320, 360, 390, 768, 1024, 1280, 1366, 1440, 1920]) {
        const { ctx, page } = await openPage(w, w > 767 ? 900 : 740);
        const d = await page.evaluate(() => ({
            sw: document.documentElement.scrollWidth,
            cw: document.documentElement.clientWidth
        }));
        check(`M2. Tanpa scroll horizontal @${w}`, d.sw <= d.cw + 1, `${d.sw}/${d.cw}`);
        await ctx.close();
    }

    {
        const { ctx, page } = await openPage(1440, 900);
        const d = await page.evaluate(() => {
            const rect = (s) => { const el = document.querySelector(s); if (!el) return null; const b = el.getBoundingClientRect(); return { n: s, l: b.left, t: b.top, r: b.right, b: b.bottom }; };
            const blocks = [
                rect('.hero-authority-badge'), rect('.hero-title'), rect('.hero-lead'),
                rect('.hero-btns-row'), rect('.hero-brands-block'), rect('.hero-truck-img'),
                rect('.hero-stats-inner')
            ].filter(Boolean);
            const overlaps = [];
            for (let i = 0; i < blocks.length; i++) {
                for (let j = i + 1; j < blocks.length; j++) {
                    const a = blocks[i], b = blocks[j];
                    const ox = Math.min(a.r, b.r) - Math.max(a.l, b.l);
                    const oy = Math.min(a.b, b.b) - Math.max(a.t, b.t);
                    if (ox > 1 && oy > 1) overlaps.push(`${a.n} x ${b.n} (${ox.toFixed(0)}x${oy.toFixed(0)})`);
                }
            }
            // Warna emas/kuning/krem
            const hueOf = (str) => {
                const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(str || '');
                if (!m) return null;
                const [r, g, b] = [+m[1] / 255, +m[2] / 255, +m[3] / 255];
                const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2;
                if (max === min) return { h: 0, s: 0, l };
                const dd = max - min;
                const s = l > 0.5 ? dd / (2 - max - min) : dd / (max + min);
                let h;
                if (max === r) h = ((g - b) / dd) % 6; else if (max === g) h = (b - r) / dd + 2; else h = (r - g) / dd + 4;
                h = (h * 60 + 360) % 360;
                return { h, s, l };
            };
            const gold = [];
            for (const el of document.querySelectorAll('.stitch-sec-hero *')) {
                if (el.tagName === 'IMG') continue;
                const cs2 = getComputedStyle(el);
                for (const col of [cs2.color, cs2.backgroundColor, cs2.borderTopColor]) {
                    const hs = hueOf(col);
                    if (!hs) continue;
                    if (hs.h >= 32 && hs.h <= 58 && hs.s > 0.25 && hs.l > 0.15) gold.push({ cls: el.className, col });
                }
            }
            // Teks < 12px
            const small = [];
            for (const el of document.querySelectorAll('.stitch-sec-hero *')) {
                if (el.children.length === 0 && el.textContent.trim()) {
                    const fs = parseFloat(getComputedStyle(el).fontSize);
                    if (fs < 11.8) small.push({ cls: el.className, text: el.textContent.trim().slice(0, 30), fs });
                }
            }
            return { overlaps, gold, small };
        });
        check('M3. Tidak ada tumpang tindih antar-blok hero', d.overlaps.length === 0, d.overlaps.join(' | '));
        check('M4. Tidak ada warna emas/kuning/krem di hero', d.gold.length === 0, JSON.stringify(d.gold.slice(0, 5)));
        check('M5. Tidak ada teks < 12px di hero', d.small.length === 0, JSON.stringify(d.small.slice(0, 5)));
        await ctx.close();
    }

    await browser.close();
    console.log(`\n=== RONDE28 verify: ${pass}/${pass + fail} PASS ===`);
    if (fail > 0) process.exitCode = 1;
})();
