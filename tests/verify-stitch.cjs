/**
 * tests/verify-stitch.cjs — RONDE 21 (REVAMP13)
 * Verifikasi menyeluruh Beranda Stitch (Page 59):
 *   A. Ukuran header/topbar/hero ATF (batas yang tidak boleh rusak)
 *   B. Kebenaran data: 0 emoji, 0 string kota terlarang, semua tel: valid,
 *      0 host localhost selain situs, format angka Indonesia
 *   C. Struktur & aksesibilitas: 1 H1, semua <img> ber-alt, anchor ke tujuan nyata
 *   D. Fungsi: menu mobile (hamburger), booking membentuk URL WhatsApp benar
 *      (diuji tanpa mengirim), link Masuk/Daftar dari FLEET_URL
 *   E. Layout: 0 horizontal overflow 320–1920, mobile 390 rata tengah, tablet 1 kolom
 *   F. Editor Elementor Page 59 sehat
 * Jalankan: cd tests && node verify-stitch.cjs
 */
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Jumlah section hasil build terakhir (dibaca dari JSON export builder).
const BUILD_SECTIONS = JSON.parse(fs.readFileSync(
    path.join(__dirname, '..', 'elementor-exports', 'beranda-stitch-elementor.json'), 'utf-8')).length;

const BASE_URL = process.env.MT_URL || 'http://localhost:5000/';
const EMOJI_RE = /[\u{2000}-\u{2BFF}\u{1F000}-\u{1FAFF}\u{FE0F}\u{2764}\u{2714}\u{26A1}\u{2794}\u{27A4}]/u;
const FORBIDDEN = ['cikarang', 'tanjung priok', 'jabodetabek', 'karawang', 'trans-jawa', 'giic'];

let pass = 0, fail = 0;
function check(name, ok, detail) {
    if (ok) { pass++; console.log(`PASS  ${name}  [${detail}]`); }
    else { fail++; console.log(`FAIL  ${name}  [${detail}]`); }
}

(async () => {
    const browser = await chromium.launch({ headless: true });

    // ---------- A. ATF 1366x600 ----------
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 600 } });
        const page = await ctx.newPage();
        await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 60000 });
        await page.evaluate(() => document.fonts.ready);
        await page.waitForTimeout(1500);
        const m = await page.evaluate(() => {
            const box = (sel) => {
                const el = document.querySelector(sel);
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return { top: Math.round(r.top), bottom: Math.round(r.bottom), height: Math.round(r.height * 100) / 100 };
            };
            const btns = document.querySelector('.hero-btns-row');
            return {
                topbar: box('.stitch-topbar'),
                header: box('.stitch-navbar'),
                heroBtnsBottom: btns ? Math.round(btns.getBoundingClientRect().bottom) : null,
                headerFont: (() => {
                    const h1 = document.querySelector('h1.elementor-heading-title');
                    if (!h1) return null;
                    const cs = getComputedStyle(h1);
                    const loaded = Array.from(document.fonts)
                        .filter((f) => f.family.includes('Jakarta') && f.status === 'loaded')
                        .map((f) => f.weight);
                    const c = document.createElement('canvas').getContext('2d');
                    c.font = '800 48px "Plus Jakarta Sans"';
                    const wFont = c.measureText('Servis Truk Cepat,').width;
                    c.font = '800 48px sans-serif';
                    const wFallback = c.measureText('Servis Truk Cepat,').width;
                    return { family: cs.fontFamily, weight: cs.fontWeight, loaded,
                             berbedaDariFallback: Math.abs(wFont - wFallback) > 5 };
                })(),
                commaGap: (() => {
                    const h1 = document.querySelector('h1.elementor-heading-title');
                    if (!h1) return null;
                    const node = h1.firstChild;
                    const text = node.textContent;
                    const range = document.createRange();
                    const iCepat = text.indexOf('Cepat');
                    const iComma = text.indexOf(',');
                    if (iCepat < 0 || iComma < 0) return null;
                    range.setStart(node, iCepat); range.setEnd(node, iCepat + 5);
                    const a = range.getBoundingClientRect();
                    range.setStart(node, iComma); range.setEnd(node, iComma + 1);
                    const b = range.getBoundingClientRect();
                    return { gap: Math.round((b.left - a.right) * 10) / 10, ws: /Cepat\s+,/.test(text) };
                })(),
            };
        });
        check('ATF: topbar <= 40px', m.topbar && m.topbar.height <= 40.5, `height=${m.topbar && m.topbar.height}`);
        check('ATF: header <= 72px', m.header && m.header.height <= 72, `height=${m.header && m.header.height}`);
        check('ATF: bawah CTA hero <= 470px (1366x600)', m.heroBtnsBottom !== null && m.heroBtnsBottom <= 470, `bottom=${m.heroBtnsBottom}`);
        check('HERO: font heading memakai Plus Jakarta Sans (benar-benar termuat)',
            !!(m.headerFont && m.headerFont.loaded.includes('800') && m.headerFont.berbedaDariFallback),
            JSON.stringify(m.headerFont));
        check('HERO: koma "Cepat," tanpa spasi & tanpa jarak aneh',
            !!(m.commaGap && !m.commaGap.ws && Math.abs(m.commaGap.gap) < 3), JSON.stringify(m.commaGap));
        await ctx.close();
    }

    // ---------- Sticky header ----------
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 60000 });
        await page.evaluate(() => window.scrollTo(0, 600));
        await page.waitForTimeout(800);
        const sticky = await page.evaluate(() => {
            const el = document.querySelector('.stitch-navbar');
            const r = el.getBoundingClientRect();
            return { height: Math.round(r.height * 100) / 100, scrolled: el.classList.contains('sticky-scrolled') };
        });
        check('ATF: sticky header <= 60px', sticky.height <= 60.5, `height=${sticky.height} scrolled=${sticky.scrolled}`);
        await ctx.close();
    }

    // ---------- B/C/D. Konten & fungsi (1440 desktop) ----------
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        const errors = [];
        page.on('pageerror', (e) => errors.push(String(e)));
        page.on('console', (msg) => { if (msg.type() === 'error') errors.push(msg.text()); });
        await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 60000 });
        await page.waitForTimeout(1200);

        const data = await page.evaluate(() => {
            const html = document.documentElement.innerHTML;
            const text = document.body.innerText;
            const emoji = (html.match(/[\u{2000}-\u{2BFF}\u{1F000}-\u{1FAFF}\u{FE0F}]/gu) || [])
                .filter((c) => !'‐–—‘’“”…±×÷≤≥≈°'.includes(c));
            const tel = Array.from(document.querySelectorAll('a[href^="tel:"]')).map((a) => a.getAttribute('href'));
            const localhost = Array.from(html.matchAll(/https?:\/\/localhost(:\d+)?/g)).map((m) => m[0]);
            const siteHost = location.origin;
            const imgs = Array.from(document.images).map((img) => ({
                src: img.currentSrc || img.src,
                alt: img.getAttribute('alt'),
            }));
            const anchors = Array.from(document.querySelectorAll('a[href^="#"]'))
                .map((a) => a.getAttribute('href'))
                .filter((h) => h && h.length > 1);
            return {
                text,
                htmlHasEmoji: emoji.slice(0, 10),
                tel,
                localhost: Array.from(new Set(localhost)),
                siteHost,
                h1Count: document.querySelectorAll('h1').length,
                imgsNoAlt: imgs.filter((i) => !i.alt || !i.alt.trim()),
                imgCount: imgs.length,
                anchors: Array.from(new Set(anchors)),
                // textContent (bukan innerText): wrapper counter memakai flex, jadi
                // innerText menyisipkan baris baru antar-item ("5.200\n+") padahal
                // secara visual renggangannya 0px. Whitespace dibuang untuk pengecekan.
                stats: Array.from(document.querySelectorAll('.stat-number .elementor-counter-number'))
                    .map((el) => el.closest('.stat-col').textContent.replace(/\s+/g, '')),
            };
        });

        check('KONTEN: 0 emoji di halaman', data.htmlHasEmoji.length === 0, JSON.stringify(data.htmlHasEmoji));
        check('KONTEN: 0 string kota/wilayah terlarang',
            FORBIDDEN.every((w) => !data.text.toLowerCase().includes(w)), 'cek teks halaman');
        check('KONTEN: semua tautan tel: valid (+62/angka)',
            data.tel.every((h) => /^tel:\+?\d{9,15}$/.test(h)), JSON.stringify(data.tel));
        const badLocal = data.localhost.filter((u) => !u.startsWith(data.siteHost));
        check('KONTEN: 0 host localhost selain situs', badLocal.length === 0, JSON.stringify(data.localhost));
        check('STRUKTUR: tepat 1 H1', data.h1Count === 1, `h1=${data.h1Count}`);
        check('AKSESIBILITAS: semua <img> ber-alt deskriptif',
            data.imgCount > 0 && data.imgsNoAlt.length === 0, `${data.imgCount} img, tanpa alt=${data.imgsNoAlt.length}`);

        // forbidden strings perlu dicek di HTML juga (innerText bisa terpotong)
        const rawHtml = await page.content();
        const badWords = FORBIDDEN.filter((w) => rawHtml.toLowerCase().includes(w));
        check('KONTEN: 0 string kota terlarang di HTML', badWords.length === 0, JSON.stringify(badWords));

        // Anchor menuju tujuan nyata
        const anchorCheck = await page.evaluate((list) => list.filter((h) => !document.querySelector(h)), data.anchors);
        check('STRUKTUR: semua anchor menuju elemen nyata', anchorCheck.length === 0, JSON.stringify(anchorCheck));

        // Format angka Indonesia pada strip statistik hero
        const statsOk = data.stats.some((s) => s.includes('5.200+')) && data.stats.some((s) => s.includes('99,2%'));
        check('KONTEN: format angka Indonesia (5.200+ & 99,2%)', statsOk, JSON.stringify(data.stats));

        // Booking: bentuk URL WhatsApp tanpa mengirim
        const booking = await page.evaluate(() => {
            const form = document.getElementById('mt-booking-form');
            if (!form) return { ok: false, reason: 'form tidak ada' };
            const unit = document.getElementById('mt-booking-unit');
            const need = document.getElementById('mt-booking-need');
            const time = document.getElementById('mt-booking-time');
            unit.value = unit.options[1].value;
            need.value = need.options[2].value;
            time.value = time.options[1].value;
            const chosen = { unit: unit.value, need: need.value, time: time.value };
            const opened = [];
            const origOpen = window.open;
            window.open = function (u) { opened.push(u); return null; };
            form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
            window.open = origOpen;
            const btn = document.getElementById('mt-booking-wa');
            return {
                ok: true,
                opened,
                btnHref: btn.getAttribute('href'),
                aria: btn.getAttribute('aria-label'),
                wa: btn.getAttribute('data-wa'),
                labelForOk: Array.from(form.querySelectorAll('label')).every((l) => !!document.getElementById(l.getAttribute('for'))),
                defaultSelected: [unit, need, time].every((s) => s.selectedIndex >= 0),
                urlMT: window.MTBooking ? window.MTBooking.url() : null,
                chosen,
            };
        });
        check('BOOKING: form ada, label terhubung, opsi default valid',
            booking.ok && booking.labelForOk && booking.defaultSelected, JSON.stringify(booking));
        let waOk = false, waDetail = '';
        if (booking.opened && booking.opened.length) {
            const u = new URL(booking.opened[0]);
            const msg = u.searchParams.get('text') || '';
            waOk = u.hostname === 'wa.me' && /^62\d{8,}$/.test(u.pathname.slice(1)) &&
                msg.includes('Halo Master Truck') && msg.includes('Unit: ' + booking.chosen.unit) &&
                msg.includes('Kebutuhan: ' + booking.chosen.need) && msg.includes('Waktu: ' + booking.chosen.time);
            waDetail = booking.opened[0];
        } else if (booking.urlMT) {
            const u = new URL(booking.urlMT);
            const msg = u.searchParams.get('text') || '';
            waOk = u.hostname === 'wa.me' && msg.includes('Unit:') && msg.includes('Kebutuhan:') && msg.includes('Waktu:');
            waDetail = booking.urlMT;
        }
        check('BOOKING: membentuk URL WhatsApp benar (diuji tanpa mengirim)', waOk, decodeURIComponent(waDetail || ''));

        // Menu mobile & hamburger ada (meski diukur di desktop, elemennya harus ada)
        const navDom = await page.evaluate(() => ({
            burger: !!document.querySelector('.stitch-nav-burger'),
            panel: !!document.querySelector('.stitch-menu-panel'),
            login: (document.querySelector('.btn-nav-login a') || {}).href || '',
            register: (document.querySelector('.btn-nav-register a') || {}).href || '',
        }));
        check('NAV: hamburger & panel menu tersedia', navDom.burger && navDom.panel, JSON.stringify(navDom));
        check('NAV: link Masuk/Daftar bukan localhost:3000 (dari FLEET_URL)',
            !/localhost:3000/.test(navDom.login) && !/localhost:3000/.test(navDom.register), JSON.stringify(navDom));

        check('KUALITAS: 0 console/page error (desktop)', errors.length === 0, errors.slice(0, 3).join(' | '));
        await ctx.close();
    }

    // ---------- E. Overflow 320–1920 & responsif ----------
    {
        for (const w of [320, 360, 390, 414, 600, 768, 820, 1024, 1280, 1440, 1920]) {
            const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
            const page = await ctx.newPage();
            await page.goto(BASE_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
            await page.waitForTimeout(700);
            const ovf = await page.evaluate((vw) => ({
                scrollW: document.documentElement.scrollWidth,
                innerW: window.innerWidth,
                requested: vw,
            }), w);
            check(`OVERFLOW: 0 horizontal overflow @${w}`,
                ovf.scrollW <= ovf.innerW + 1, JSON.stringify(ovf));
            await ctx.close();
        }
    }

    // Mobile 390: hamburger berfungsi + hero rata tengah
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        const errors = [];
        page.on('pageerror', (e) => errors.push(String(e)));
        await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 60000 });
        await page.waitForTimeout(900);
        const before = await page.evaluate(() => {
            const panel = document.querySelector('.stitch-menu-panel');
            return { display: getComputedStyle(panel).display };
        });
        await page.click('.stitch-nav-burger');
        await page.waitForTimeout(300);
        const after = await page.evaluate(() => {
            const panel = document.querySelector('.stitch-menu-panel');
            const burger = document.querySelector('.stitch-nav-burger');
            const links = Array.from(panel.querySelectorAll('a')).map((a) => a.getAttribute('href'));
            const box = panel.getBoundingClientRect();
            return {
                display: getComputedStyle(panel).display,
                expanded: burger.getAttribute('aria-expanded'),
                links,
                insideViewport: box.left >= 0 && box.right <= window.innerWidth + 1,
            };
        });
        check('MOBILE 390: panel menu tertutup saat awal', before.display === 'none', `display=${before.display}`);
        check('MOBILE 390: hamburger membuka menu & aria-expanded benar',
            after.display === 'flex' && after.expanded === 'true', JSON.stringify(after));
        check('MOBILE 390: menu berisi semua tautan nav & di dalam layar',
            after.links.includes('#layanan') && after.links.includes('#fleet') &&
            after.links.includes('#fasilitas') && after.links.includes('#kontak') && after.insideViewport,
            JSON.stringify(after));

        // klik link menu: panel tertutup & berpindah ke tujuan
        await page.click('.stitch-menu-panel a[href="#fasilitas"]');
        await page.waitForTimeout(1200);
        const nav = await page.evaluate(() => ({
            display: getComputedStyle(document.querySelector('.stitch-menu-panel')).display,
            expanded: document.querySelector('.stitch-nav-burger').getAttribute('aria-expanded'),
            hash: location.hash,
        }));
        check('MOBILE 390: klik link menutup panel & mengubah hash',
            nav.display === 'none' && nav.expanded === 'false' && nav.hash === '#fasilitas', JSON.stringify(nav));

        // hero mobile rata tengah
        const centered = await page.evaluate(() => {
            const h1 = document.querySelector('h1.elementor-heading-title');
            const r = h1.getBoundingClientRect();
            const cx = window.innerWidth / 2;
            return Math.abs((r.left + r.right) / 2 - cx) < 40;
        });
        check('MOBILE 390: judul hero rata tengah', centered, `centered=${centered}`);
        check('KUALITAS: 0 console/page error (mobile)', errors.length === 0, errors.slice(0, 3).join(' | '));
        await ctx.close();
    }

    // Tablet 768: section utama 1 kolom (rata & tak tumpah)
    {
        const ctx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
        const page = await ctx.newPage();
        await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 60000 });
        await page.waitForTimeout(800);
        const t = await page.evaluate(() => {
            const feat = document.querySelector('.features-grid-row');
            const r = feat.getBoundingClientRect();
            return { w: Math.round(r.width), inner: window.innerWidth };
        });
        check('TABLET 768: grid fitur tidak tumpah layar', t.w <= t.inner + 1, JSON.stringify(t));
        await ctx.close();
    }

    // ---------- F. Editor Elementor sehat (login admin sementara) ----------
    {
        const testAdmin = 'tester_r21_' + Math.random().toString(36).substring(7);
        const testPass = 'AuditR21!#' + Math.random().toString(36).substring(7);
        execSync(`docker exec lpm-wp-app wp user create ${testAdmin} ${testAdmin}@example.com ` +
            `--role=administrator --user_pass="${testPass}" --allow-root`, { stdio: 'pipe' });
        try {
            const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
            const page = await ctx.newPage();
            const errors = [];
            page.on('pageerror', (e) => errors.push(String(e)));
            page.on('console', (msg) => {
                const t = msg.text();
                if (msg.type() === 'error' && !t.includes('favicon') && !t.includes('net::ERR_')) errors.push(t);
            });
            await page.goto(BASE_URL.replace(/\/$/, '') + '/wp-login.php', { waitUntil: 'domcontentloaded' });
            await page.fill('#user_login', testAdmin);
            await page.fill('#user_pass', testPass);
            await Promise.all([page.waitForNavigation({ waitUntil: 'domcontentloaded' }), page.click('#wp-submit')]);
            await page.goto(BASE_URL.replace(/\/$/, '') + '/wp-admin/post.php?post=59&action=elementor',
                { waitUntil: 'domcontentloaded', timeout: 90000 });
            await page.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 40000 });
            await page.waitForTimeout(6000);
            const info = await page.evaluate(() => {
                const el = window.elementor;
                const doc = el && el.documents ? el.documents.getCurrent() : null;
                return {
                    ready: !!(el && el.elements),
                    currentId: doc ? doc.id : (el && el.config ? el.config.document.id : null),
                    count: el && el.elements && el.elements.models ? el.elements.models.length : 0,
                };
            });
            check('EDITOR: Page 59 termuat & siap', info.ready && String(info.currentId) === '59', JSON.stringify(info));
            check('EDITOR: jumlah section di editor = hasil build', info.count === BUILD_SECTIONS,
                `editor=${info.count} build=${BUILD_SECTIONS}`);
            check('EDITOR: 0 console error', errors.length === 0, errors.slice(0, 3).join(' | '));
            await ctx.close();
        } catch (e) {
            check('EDITOR: Page 59 termuat & siap', false, e.message);
        } finally {
            try {
                execSync(`docker exec lpm-wp-app wp user delete ${testAdmin} --yes --allow-root`, { stdio: 'pipe' });
            } catch (e) { console.log('catatan: user uji gagal dihapus otomatis'); }
        }
    }

    await browser.close();
    console.log(`\nTOTAL: ${pass} PASS / ${fail} FAIL`);
    process.exit(fail ? 1 : 0);
})();
