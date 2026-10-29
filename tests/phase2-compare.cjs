// tests/phase2-compare.cjs <before|after>
// Bukti NO-OP Fase 2: screenshot (viewport + full dengan reveal) & sidik jari computed style
// untuk seluruh elemen topbar/hero/strip pada 8 viewport.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = 'http://localhost:5000/';
const phase = process.argv[2] || 'before';
const OUT = path.join(__dirname, '..', 'playwright_review', phase === 'before' ? 'sebelum_ronde29' : 'sesudah_ronde29_fase2');
const VIEWPORTS = [
    { name: '360x740', w: 360, h: 740 },
    { name: '375x812', w: 375, h: 812 },
    { name: '390x844', w: 390, h: 844 },
    { name: '414x896', w: 414, h: 896 },
    { name: '768x1024', w: 768, h: 1024 },
    { name: '1366x600', w: 1366, h: 600 },
    { name: '1440x900', w: 1440, h: 900 },
    { name: '1920x1080', w: 1920, h: 1080 },
];
const PROPS = [
    'display', 'position', 'top', 'right', 'bottom', 'left', 'width', 'height', 'minWidth', 'minHeight', 'maxWidth', 'maxHeight',
    'marginTop', 'marginRight', 'marginBottom', 'marginLeft', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
    'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth', 'borderTopColor', 'borderTopStyle',
    'borderRadius', 'background', 'backgroundColor', 'backgroundImage', 'backgroundSize', 'backgroundPosition', 'backgroundRepeat',
    'color', 'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeight', 'letterSpacing', 'textAlign', 'textTransform',
    'textDecorationLine', 'whiteSpace', 'wordBreak', 'overflowWrap', 'textWrap', 'verticalAlign',
    'gap', 'rowGap', 'columnGap', 'flexDirection', 'flexWrap', 'flexGrow', 'flexShrink', 'flexBasis',
    'gridTemplateColumns', 'gridTemplateRows', 'alignItems', 'alignSelf', 'justifyContent', 'order',
    'overflow', 'overflowX', 'overflowY', 'boxShadow', 'transform', 'opacity', 'zIndex', 'isolation',
    'objectFit', 'objectPosition', 'aspectRatio', 'filter', 'backdropFilter', 'visibility', 'pointerEvents',
    'animationName', 'animationDuration', 'animationDelay', 'transitionProperty', 'cursor', 'content', 'maskImage', 'scrollSnapType',
];

(async () => {
    fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ headless: true });
    const fingerprints = {};

    for (const vp of VIEWPORTS) {
        const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, reducedMotion: 'no-preference' });
        const page = await ctx.newPage();
        await page.goto(BASE, { waitUntil: 'networkidle' });
        await page.evaluate(() => document.fonts.ready);
        await page.waitForTimeout(600);
        // trigger scroll reveal
        await page.evaluate(async () => {
            const step = Math.round(window.innerHeight * 0.8);
            for (let y = 0; y < document.body.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise((r) => setTimeout(r, 60));
            }
            window.scrollTo(0, 0);
            await new Promise((r) => setTimeout(r, 400));
        });
        await page.waitForTimeout(400);

        fingerprints[vp.name] = await page.evaluate((PROPS) => {
            const roots = [document.querySelector('.stitch-topbar'), document.querySelector('.stitch-sec-hero')].filter(Boolean);
            const els = [];
            for (const root of roots) {
                for (const el of [root, ...root.querySelectorAll('*')]) els.push(el);
            }
            const res = getComputedStyle(document.documentElement);
            const pick = (cs) => { const o = {}; for (const p of PROPS) o[p] = cs[p]; return o; };
            return {
                body: (() => { const cs = getComputedStyle(document.body); return { overflowX: cs.overflowX, pad: cs.padding }; })(),
                els: els.map((el, i) => ({
                    i,
                    tag: el.tagName,
                    cls: String(el.className || '').slice(0, 90),
                    rect: (() => { const r = el.getBoundingClientRect(); return [+r.left.toFixed(1), +r.top.toFixed(1), +r.width.toFixed(1), +r.height.toFixed(1)]; })(),
                    cs: pick(getComputedStyle(el)),
                    before: pick(getComputedStyle(el, '::before')),
                    after: pick(getComputedStyle(el, '::after')),
                })),
            };
        }, PROPS);

        await page.screenshot({ path: path.join(OUT, `${phase}-${vp.name}-view.png`) });
        await page.screenshot({ path: path.join(OUT, `${phase}-${vp.name}-full.png`), fullPage: true });
        await ctx.close();
        console.log('OK', vp.name);
    }
    await browser.close();
    fs.writeFileSync(path.join(OUT, `${phase}-fingerprint.json`), JSON.stringify(fingerprints), 'utf8');
    console.log('Fingerprint:', path.join(OUT, `${phase}-fingerprint.json`));
})();
