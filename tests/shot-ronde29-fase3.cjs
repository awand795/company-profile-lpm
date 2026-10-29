// tests/shot-ronde29-fase3.cjs
// Screenshot Fase 3 (8 viewport, view + full) dengan reveal/animasi stabil.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_ronde29_fase3');
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

(async () => {
    fs.mkdirSync(OUT, { recursive: true });
    const browser = await chromium.launch({ headless: true });
    for (const vp of VIEWPORTS) {
        const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, reducedMotion: 'no-preference' });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'load' });
        await page.evaluate(() => document.fonts.ready);
        await page.evaluate(async () => {
            const step = Math.round(window.innerHeight * 0.8);
            for (let y = 0; y < document.body.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise((r) => setTimeout(r, 40));
            }
            window.scrollTo(0, 0);
            await new Promise((r) => setTimeout(r, 300));
        });
        await page.addStyleTag({ content: `
            *, *::before, *::after { animation: none !important; transition: none !important; }
            .mt-reveal { opacity: 1 !important; transform: none !important; }
        ` });
        await page.evaluate(() => {
            document.querySelectorAll('.mt-reveal').forEach((el) => el.classList.add('is-inview'));
            document.querySelectorAll('.elementor-invisible').forEach((el) => el.classList.remove('elementor-invisible'));
            window.scrollTo(0, 0);
        });
        await page.waitForTimeout(300);
        await page.screenshot({ path: path.join(OUT, `fase3-${vp.name}-view.png`), animations: 'disabled' });
        await page.screenshot({ path: path.join(OUT, `fase3-${vp.name}-full.png`), fullPage: true, animations: 'disabled' });
        await ctx.close();
        console.log('OK', vp.name);
    }
    await browser.close();
})();
