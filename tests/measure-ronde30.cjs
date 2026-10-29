// tests/measure-ronde30.cjs <sebelum|sesudah>
// Ukur padding kartu + screenshot per section untuk Ronde 30.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const phase = process.argv[2] === 'sesudah' ? 'sesudah' : 'sebelum';
const OUT = path.join(__dirname, '..', 'playwright_review', `${phase}_ronde30`);
const SECTIONS = [
    ['strip', '.hero-stats-inner'],
    ['booking', '.stitch-sec-booking'],
    ['keunggulan', '.stitch-sec-features'],
    ['layanan', '.stitch-sec-services'],
    ['paket-fleet', '.stitch-sec-fleet'],
    ['cara-kerja', '.stitch-sec-workflow'],
    ['fasilitas', '.stitch-sec-facilities'],
    ['merek', '.stitch-sec-brands'],
    ['testimoni', '.stitch-sec-testimonials'],
    ['faq', '.stitch-sec-faq'],
    ['lokasi', '.stitch-sec-location'],
    ['footer', 'footer, .site-footer, .stitch-footer'],
];
const CARDS = [
    '.feat-bento-col', '.fleet-tier-col', '.svc-card-col', '.step-card',
    '.fac-card-col', '.testi-card-col', '.booking-card', '.hero-stats-inner',
    '.faq-accordion-box .elementor-accordion-item', '.location-info-col',
];

(async () => {
    fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ headless: true });
    const report = {};

    for (const [name, w, h] of [['360x740', 360, 740], ['390x844', 390, 844], ['480x800', 480, 800], ['768x1024', 768, 1024], ['1366x600', 1366, 600], ['1440x900', 1440, 900]]) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'load' });
        await page.evaluate(() => document.fonts.ready);
        await page.evaluate(async () => {
            const step = Math.round(innerHeight * 0.8);
            for (let y = 0; y < document.body.scrollHeight; y += step) {
                scrollTo(0, y);
                await new Promise((r) => setTimeout(r, 30));
            }
            scrollTo(0, 0);
            await new Promise((r) => setTimeout(r, 250));
        });
        await page.addStyleTag({ content: '*,*::before,*::after{animation:none!important;transition:none!important}.mt-reveal{opacity:1!important;transform:none!important}' });
        await page.evaluate(() => {
            document.querySelectorAll('.mt-reveal').forEach((e) => e.classList.add('is-inview'));
            document.querySelectorAll('.elementor-invisible').forEach((e) => e.classList.remove('elementor-invisible'));
            scrollTo(0, 0);
        });
        await page.waitForTimeout(250);

        report[name] = await page.evaluate(({ CARDS }) => {
            const rect = (e) => { const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height, r: r.right, b: r.bottom }; };
            const out = [];
            for (const sel of CARDS) {
                document.querySelectorAll(sel).forEach((card, idx) => {
                    const cr = rect(card);
                    if (cr.w < 70 || cr.h < 30) return;
                    const cs = getComputedStyle(card);
                    const pad = [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].map(parseFloat);
                    const leafSel = 'h1,h2,h3,h4,p,a,img,i,button,.elementor-button,.elementor-icon,.elementor-widget-container,.elementor-image-box-content';
                    const leaves = [...card.querySelectorAll(leafSel)].filter((e) => {
                        if (e.closest(sel) !== card) return false;
                        const r = e.getBoundingClientRect();
                        if (r.width < 2 || r.height < 2) return false;
                        if (e.children.length && !e.matches('a,button,.elementor-button')) return false;
                        return true;
                    });
                    let min = Infinity;
                    for (const e of leaves) {
                        const r = rect(e);
                        min = Math.min(min, r.x - cr.x, cr.r - r.r, r.y - cr.y, cr.b - r.b);
                    }
                    out.push({ sel, idx, pad, min: Number.isFinite(min) ? +min.toFixed(1) : null, w: +cr.w.toFixed(1), h: +cr.h.toFixed(1), bg: cs.backgroundColor, border: cs.borderTopWidth });
                });
            }
            return out;
        }, { CARDS });

        if (name === '390x844' || name === '360x740') {
            for (const [label, sel] of SECTIONS) {
                const el = await page.$(sel);
                if (!el) continue;
                try {
                    await el.scrollIntoViewIfNeeded();
                    await page.waitForTimeout(100);
                    await el.screenshot({ path: path.join(OUT, `${label}-${name}.png`), animations: 'disabled' });
                } catch (e) { console.log('SKIP', name, label, e.message); }
            }
            // Hero juga (view + full)
            await page.evaluate(() => scrollTo(0, 0));
            await page.waitForTimeout(100);
            await page.screenshot({ path: path.join(OUT, `hero-${name}-view.png`), animations: 'disabled' });
        }
        if (name === '1366x600' || name === '1440x900') {
            await page.screenshot({ path: path.join(OUT, `hero-${name}-view.png`), animations: 'disabled' });
        }
        await ctx.close();
        console.log('OK', name);
    }
    await browser.close();
    fs.writeFileSync(path.join(OUT, 'cards.json'), JSON.stringify(report, null, 2), 'utf8');
})();
