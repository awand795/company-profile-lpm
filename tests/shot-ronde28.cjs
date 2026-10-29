// tests/shot-ronde28.cjs
// Screenshot bukti visual Ronde 28 (sebelum / sesudah) — hero Beranda Page 59.
// Pakai: node tests/shot-ronde28.cjs sebelum|sesudah
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const fase = process.argv[2] || 'sebelum';
const outDir = path.resolve(__dirname, `../playwright_review/${fase}_ronde28`);
fs.mkdirSync(outDir, { recursive: true });

const BASE = 'http://localhost:5000/';

const VIEWPORTS = [
    { name: '1440', w: 1440, h: 900 },
    { name: '1366x600', w: 1366, h: 600 },
    { name: '1024', w: 1024, h: 768 },
    { name: '768', w: 768, h: 1024 },
    { name: '390x844', w: 390, h: 844 }
];

(async () => {
    const browser = await chromium.launch({ headless: true });

    for (const vp of VIEWPORTS) {
        const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
        const page = await ctx.newPage();
        await page.goto(BASE, { waitUntil: 'networkidle' });
        await page.waitForTimeout(1200);

        const pView = path.join(outDir, `ronde28-${vp.name}-view.png`);
        await page.screenshot({ path: pView, fullPage: false });
        console.log(`OK ${pView}`);

        const pFull = path.join(outDir, `ronde28-${vp.name}-full.png`);
        await page.screenshot({ path: pFull, fullPage: true });
        console.log(`OK ${pFull}`);

        await ctx.close();
    }

    // Crop detail hero di 1440
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto(BASE, { waitUntil: 'networkidle' });
        await page.waitForTimeout(1200);

        const sels = [
            { sel: '.stitch-sec-hero', name: 'hero' },
            { sel: '.hero-authority-badge', name: 'badge' },
            { sel: '.hero-visual-card-wrap', name: 'foto' },
            { sel: '.hero-telematics-card', name: 'kartu' },
            { sel: '.hero-brands-block', name: 'chip' }
        ];
        for (const s of sels) {
            const el = await page.$(s.sel);
            if (el) {
                const p = path.join(outDir, `ronde28-crop-${s.name}.png`);
                await el.screenshot({ path: p });
                console.log(`OK ${p}`);
            }
        }
        await ctx.close();
    }

    await browser.close();
    console.log(`\nScreenshot ${fase} selesai di: ${outDir}`);
})();
