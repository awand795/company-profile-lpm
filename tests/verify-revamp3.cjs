/**
 * verify-revamp3.cjs — Test suite Master Truck (homepage ID 59)
 * Assertion-style PASS/FAIL + exit code. Jalankan:
 *   node tests/verify-revamp3.cjs
 * Butuh: server http://localhost:5000 (docker lpm-wp-app).
 */
const PW = '/home/awanda/.gemini/antigravity-cli/brain/4a5c5b42-6ad5-4407-bfb4-71d03e96476c/scratch/node_modules/playwright';
const { chromium, devices } = require(PW);
const fs = require('fs');
const path = require('path');

const URL = 'http://localhost:5000/';
const OUT = path.join(__dirname, 'artifacts');

const results = [];
function check(name, ok, detail) {
    results.push({ name, ok: !!ok, detail: detail || '' });
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  [' + detail + ']' : ''}`);
}

async function scrollThrough(page) {
    await page.evaluate(async () => {
        await new Promise((res) => {
            let y = 0;
            const step = () => {
                y += 600;
                window.scrollTo(0, y);
                if (y < document.body.scrollHeight) { setTimeout(step, 80); } else { res(); }
            };
            step();
        });
    });
    await page.waitForTimeout(1200);
}

(async () => {
    if (!fs.existsSync(OUT)) { fs.mkdirSync(OUT, { recursive: true }); }
    const browser = await chromium.launch({ headless: true });

    // ================= MOBILE 390 (touch) =================
    const mob = await browser.newContext({ ...devices['iPhone 13'] });
    const m = await mob.newPage();
    const mobErrors = [];
    m.on('console', (msg) => { if (msg.type() === 'error') { mobErrors.push(msg.text()); } });
    m.on('pageerror', (e) => mobErrors.push(String(e)));

    const resp = await m.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await m.waitForTimeout(2000);
    check('MOBILE: HTTP 200', resp.status() === 200, 'status=' + resp.status());

    // Overflow di beberapa lebar
    let overflowOk = true;
    const overflowDetail = [];
    for (const w of [320, 360, 390, 414]) {
        await m.setViewportSize({ width: w, height: 800 });
        await m.waitForTimeout(350);
        const r = await m.evaluate(() => ({ doc: document.documentElement.scrollWidth, win: window.innerWidth }));
        const ok = r.doc <= r.win + 1;
        if (!ok) { overflowOk = false; overflowDetail.push(`${w}:${r.doc}>${r.win}`); }
    }
    check('MOBILE: tanpa overflow horizontal 320-414', overflowOk, overflowDetail.join(','));
    await m.setViewportSize({ width: 390, height: 844 });

    // Section utama ada
    const sections = await m.evaluate(() => {
        const ids = ['header-carousel', 'header-slide-2', 'about', 'service', 'principals', 'booking', 'team', 'testimonial', 'faq', 'contact'];
        return ids.filter((id) => !document.getElementById(id));
    });
    check('MOBILE: semua section utama ada', sections.length === 0, 'missing=' + sections.join(','));

    // Hero stats tampil
    const heroStats = await m.evaluate(() => {
        const el = document.querySelector('.hero-stats-inner');
        if (!el) { return null; }
        const cs = getComputedStyle(el);
        return { display: cs.display, visible: cs.display !== 'none' && el.getBoundingClientRect().width > 0 };
    });
    check('MOBILE: hero stats tampil', heroStats && heroStats.visible, JSON.stringify(heroStats));

    // Carousel scrollable
    const carousels = await m.evaluate(() => {
        const out = {};
        ['sec-services-cards', 'sec-team-cards', 'sec-testimonial-cards'].forEach((s) => {
            const sec = document.querySelector('.' + s);
            if (!sec) { out[s] = 'missing'; return; }
            const box = sec.querySelector(':scope > .elementor-container');
            const scrollable = box.scrollWidth > box.clientWidth;
            box.scrollLeft = 200;
            const moved = box.scrollLeft > 0;
            box.scrollLeft = 0;
            out[s] = scrollable && moved ? 'ok' : `scrollable=${scrollable} moved=${moved}`;
        });
        return out;
    });
    check('MOBILE: carousel service/team/testimonial scrollable',
        Object.values(carousels).every((v) => v === 'ok'), JSON.stringify(carousels));

    // Hamburger → X
    await m.evaluate(() => window.scrollTo(0, 0));
    await m.waitForTimeout(300);
    await m.click('.navbar .navbar-toggler');
    await m.waitForTimeout(450);
    const ham = await m.evaluate(() => {
        const t = document.querySelector('.navbar .navbar-toggler');
        const icon = t.querySelector('.elementor-button-icon');
        const svg = icon.querySelector('svg');
        const panel = document.querySelector('.navbar .navbar-menu-col');
        const before = getComputedStyle(icon, '::before');
        return {
            aria: t.getAttribute('aria-expanded'),
            panelShown: panel.classList.contains('show'),
            svgOpacity: getComputedStyle(svg).opacity,
            hasX: before.content !== 'none' && before.content !== 'normal',
        };
    });
    check('MOBILE: hamburger jadi X saat terbuka',
        ham.aria === 'true' && ham.panelShown && ham.svgOpacity === '0' && ham.hasX, JSON.stringify(ham));

    // Anchor FAQ presisi 118
    await m.click('.navbar-menu-col a[href="#faq"]');
    await m.waitForTimeout(3300);
    const faqTop = await m.evaluate(() => Math.round(document.querySelector('#faq').getBoundingClientRect().top));
    check('MOBILE: anchor #faq presisi 118px', Math.abs(faqTop - 118) <= 3, 'faqTop=' + faqTop);

    // Grayscale team off di touch
    const grayMob = await m.evaluate(() => {
        const img = document.querySelector('.sec-team-cards .team-enterprise-card .elementor-widget-image img');
        return img ? getComputedStyle(img).filter : null;
    });
    check('MOBILE: foto team warna penuh (tanpa grayscale)', grayMob === 'none', 'filter=' + grayMob);

    // Progress bar: lebar naik saat scroll
    await m.evaluate(() => window.scrollTo(0, 0));
    await m.waitForTimeout(400);
    const barTop = await m.evaluate(() => {
        const b = document.querySelector('.mt-scroll-progress');
        return b ? parseFloat(b.style.width || '0') : -1;
    });
    await m.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight / 2));
    await m.waitForTimeout(500);
    const barMid = await m.evaluate(() => {
        const b = document.querySelector('.mt-scroll-progress');
        return b ? parseFloat(b.style.width || '0') : -1;
    });
    check('MOBILE: progress bar lebar naik saat scroll',
        barTop >= 0 && barMid >= 0 && barMid > barTop + 10, `top=${barTop} mid=${barMid}`);

    // Reveal semua tampil setelah scroll-through (poll: transisi 0.55s bisa
    // masih berjalan saat pengukuran pertama)
    await scrollThrough(m);
    const reveal = await (async () => {
        for (let i = 0; i < 20; i++) {
            const r = await m.evaluate(() => {
                const all = document.querySelectorAll('.mt-reveal');
                const shown = document.querySelectorAll('.mt-reveal.is-inview');
                let opaque = true;
                all.forEach((el) => { if (getComputedStyle(el).opacity !== '1') { opaque = false; } });
                return { total: all.length, shown: shown.length, opaque };
            });
            if (r.opaque && r.total === r.shown) { return r; }
            await m.waitForTimeout(300);
        }
        return m.evaluate(() => {
            const all = document.querySelectorAll('.mt-reveal');
            const shown = document.querySelectorAll('.mt-reveal.is-inview');
            let opaque = true;
            all.forEach((el) => { if (getComputedStyle(el).opacity !== '1') { opaque = false; } });
            return { total: all.length, shown: shown.length, opaque };
        });
    })();
    check('MOBILE: reveal semua is-inview & opaque',
        reveal.total > 0 && reveal.total === reveal.shown && reveal.opaque, JSON.stringify(reveal));

    // Back-to-top
    const bt = await m.evaluate(() => {
        const b = document.querySelector('.mt-back-top');
        return b ? { exists: true, visible: b.classList.contains('is-visible') } : { exists: false };
    });
    let btOk = bt.exists && bt.visible;
    if (btOk) {
        await m.click('.mt-back-top');
        await m.waitForTimeout(3000);
        const y = await m.evaluate(() => window.scrollY);
        btOk = y < 5;
        bt.afterClickY = y;
    }
    check('MOBILE: back-to-top muncul & kembali ke atas', btOk, JSON.stringify(bt));

    check('MOBILE: 0 console/page error', mobErrors.length === 0, mobErrors.slice(0, 3).join(' | '));

    await m.evaluate(() => window.scrollTo(0, 0));
    await m.waitForTimeout(500);
    await m.screenshot({ path: path.join(OUT, 'm390-top.png') });
    await scrollThrough(m);
    await m.screenshot({ path: path.join(OUT, 'm390-full.png'), fullPage: true });

    // ================= TABLET 768 =================
    const tabCtx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
    const t = await tabCtx.newPage();
    const tabErrors = [];
    t.on('console', (msg) => { if (msg.type() === 'error') { tabErrors.push(msg.text()); } });
    t.on('pageerror', (e) => tabErrors.push(String(e)));
    await t.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await t.waitForTimeout(1500);
    const tOvf = await t.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
    check('TABLET: tanpa overflow 768', tOvf);
    const tGrid = await t.evaluate(() => {
        const box = document.querySelector('.sec-services-cards > .elementor-container');
        const cs = getComputedStyle(box);
        return { wrap: cs.flexWrap, overflow: cs.overflowX };
    });
    check('TABLET: service tetap grid (bukan carousel)',
        tGrid.wrap === 'wrap' && tGrid.overflow === 'visible', JSON.stringify(tGrid));
    check('TABLET: 0 console/page error', tabErrors.length === 0, tabErrors.slice(0, 3).join(' | '));
    await scrollThrough(t);
    await t.screenshot({ path: path.join(OUT, 't768-full.png'), fullPage: true });

    // ================= DESKTOP 1440 =================
    const deskCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const d = await deskCtx.newPage();
    const deskErrors = [];
    d.on('console', (msg) => { if (msg.type() === 'error') { deskErrors.push(msg.text()); } });
    d.on('pageerror', (e) => deskErrors.push(String(e)));
    await d.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await d.waitForTimeout(1500);

    const dOvf = await d.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
    check('DESKTOP: tanpa overflow 1440', dOvf);

    // Logo principals: grayscale → penuh saat hover
    // (hover dilakukan SETELAH transisi reveal selesai supaya :hover stabil)
    const logo = await d.evaluate(() => {
        const img = document.querySelector('.principal-wall-card .elementor-widget-image img');
        return img ? getComputedStyle(img).filter : null;
    });
    const logoHovered = await (async () => {
        const card = d.locator('.principal-wall-card').first();
        await card.scrollIntoViewIfNeeded();
        // tunggu section selesai reveal (opacity 1) — kalau belum, card bisa
        // bergeser 16px saat transisi dan hover jadi lepas
        for (let i = 0; i < 15; i++) {
            const done = await d.evaluate(() => {
                const sec = document.querySelector('.sec-principals');
                return !sec || getComputedStyle(sec).opacity === '1';
            });
            if (done) { break; }
            await d.waitForTimeout(300);
        }
        await card.hover();
        // poll sampai filter berubah (hover stabil)
        for (let i = 0; i < 10; i++) {
            const f = await d.evaluate(() => {
                const img = document.querySelector('.principal-wall-card .elementor-widget-image img');
                return img ? getComputedStyle(img).filter : null;
            });
            if (f && f.includes('grayscale(0)')) { return f; }
            await d.waitForTimeout(200);
        }
        return d.evaluate(() => {
            const img = document.querySelector('.principal-wall-card .elementor-widget-image img');
            return img ? getComputedStyle(img).filter : null;
        });
    })();
    check('DESKTOP: logo principals grayscale → penuh saat hover',
        logo && logo.includes('grayscale(1)') && logoHovered && logoHovered.includes('grayscale(0)'),
        `rest="${logo}" hover="${logoHovered}"`);

    // Pulse animasi tombol darurat
    const pulse = await d.evaluate(() => {
        const btn = document.querySelector('.btn-booking-call .elementor-button');
        if (!btn) { return null; }
        const ring = getComputedStyle(btn, '::after');
        return { anim: getComputedStyle(btn).animationName, ringAnim: ring.animationName };
    });
    check('DESKTOP: tombol darurat punya pulse + ring',
        pulse && pulse.anim.includes('mtCallPulse') && pulse.ringAnim.includes('mtCallRing'), JSON.stringify(pulse));

    // Scrollspy: nav aktif mengikuti section
    await d.evaluate(() => document.querySelector('#service').scrollIntoView());
    await d.waitForTimeout(900);
    const spy = await d.evaluate(() => {
        const active = document.querySelector('.navbar-right-inner .nav-link-active a');
        return active ? active.getAttribute('href') : null;
    });
    check('DESKTOP: scrollspy nav aktif = #service', spy === '#service', 'active=' + spy);

    // Hamburger desktop tersembunyi
    const dTog = await d.evaluate(() => {
        const el = document.querySelector('.navbar .navbar-toggler');
        return el ? getComputedStyle(el).display : null;
    });
    check('DESKTOP: hamburger tersembunyi', dTog === 'none', 'display=' + dTog);

    check('DESKTOP: 0 console/page error', deskErrors.length === 0, deskErrors.slice(0, 3).join(' | '));

    await d.evaluate(() => window.scrollTo(0, 0));
    await d.waitForTimeout(500);
    await d.screenshot({ path: path.join(OUT, 'd1440-top.png') });
    await scrollThrough(d);
    await d.screenshot({ path: path.join(OUT, 'd1440-full.png'), fullPage: true });

    // Hero tak tersentuh
    const hero = await d.evaluate(() => {
        const slides = document.querySelectorAll('.mt-hero-slide-item');
        const imgs = Array.from(document.querySelectorAll('.mt-hero-slide img')).map((i) => i.getAttribute('src'));
        return { slides: slides.length, imgs: imgs.length, first: imgs[0] };
    });
    check('DESKTOP: hero 2 slide utuh', hero.slides === 2 && hero.imgs >= 2, JSON.stringify(hero));

    // ================= RINGKASAN =================
    await browser.close();
    const failed = results.filter((r) => !r.ok);
    console.log('\n========================================');
    console.log(`TOTAL: ${results.length} | PASS: ${results.length - failed.length} | FAIL: ${failed.length}`);
    if (failed.length) {
        console.log('GAGAL:');
        failed.forEach((f) => console.log('  - ' + f.name + '  [' + f.detail + ']'));
    }
    console.log('Screenshot: ' + OUT);
    process.exit(failed.length ? 1 : 0);
})().catch((e) => { console.error('ERR', e); process.exit(1); });
