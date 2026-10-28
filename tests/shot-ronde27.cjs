// tests/shot-ronde27.cjs
// Screenshot bukti visual Ronde 27 (sebelum / sesudah)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const fase = process.argv[2] || 'sebelum';
const outDir = path.resolve(__dirname, `../playwright_review/${fase}_ronde27`);
fs.mkdirSync(outDir, { recursive: true });

const BASE = 'http://localhost:5000/';

const VIEWPORTS = [
    { name: '390', w: 390, h: 844 },
    { name: '360', w: 360, h: 740 },
    { name: '768', w: 768, h: 1024 },
    { name: '1366x600', w: 1366, h: 600 },
    { name: '1440', w: 1440, h: 900 }
];

(async () => {
    const browser = await chromium.launch({ headless: true });
    
    // 1. Viewports full-page & ATF
    for (const vp of VIEWPORTS) {
        const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
        const page = await ctx.newPage();
        await page.goto(BASE, { waitUntil: 'networkidle' });
        await page.waitForTimeout(1000);
        
        // Viewport layar pertama (ATF)
        const pView = path.join(outDir, `ronde27-${vp.name}-view.png`);
        await page.screenshot({ path: pView, fullPage: false });
        console.log(`OK ${pView}`);

        // Full page
        const pFull = path.join(outDir, `ronde27-${vp.name}.png`);
        await page.screenshot({ path: pFull, fullPage: true });
        console.log(`OK ${pFull}`);

        await ctx.close();
    }

    // 2. Crop section penting di 1440
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto(BASE, { waitUntil: 'networkidle' });
        await page.waitForTimeout(1000);

        const sections = [
            { sel: '.stitch-topbar', name: 'sec-topbar' },
            { sel: '.stitch-navbar', name: 'sec-navbar' },
            { sel: '.stitch-sec-hero', name: 'sec-hero' },
            { sel: '.hero-stats-inner', name: 'sec-stats-strip' },
            { sel: '.hero-brands-block', name: 'hero-brands' },
            { sel: '.hero-visual-card-wrap', name: 'hero-visual' }
        ];

        for (const s of sections) {
            const el = await page.$(s.sel);
            if (el) {
                const p = path.join(outDir, `ronde27-${s.name}.png`);
                await el.screenshot({ path: p });
                console.log(`OK ${p}`);
            }
        }
        await ctx.close();
    }

    // 3. Mobile 390 detail
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto(BASE, { waitUntil: 'networkidle' });
        await page.waitForTimeout(1000);

        const elHero = await page.$('.stitch-sec-hero');
        if (elHero) {
            const p = path.join(outDir, `ronde27-m390-hero.png`);
            await elHero.screenshot({ path: p });
            console.log(`OK ${p}`);
        }

        const elStats = await page.$('.hero-stats-inner');
        if (elStats) {
            const p = path.join(outDir, `ronde27-m390-stats.png`);
            await elStats.screenshot({ path: p });
            console.log(`OK ${p}`);
        }
        await ctx.close();
    }

    await browser.close();
    console.log(`\nScreenshot ${fase} selesai di: ${outDir}`);
})();
