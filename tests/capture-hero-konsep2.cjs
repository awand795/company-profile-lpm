const { chromium } = require('./node_modules/playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'hero_konsep2');
fs.mkdirSync(OUT, { recursive: true });

async function takeScreenshots(prefix) {
    const browser = await chromium.launch({ headless: true });
    
    // Desktop 1366x640
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 640 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(OUT, `${prefix}-1366x640.png`), fullPage: false });
        console.log(`Saved: ${prefix}-1366x640.png`);
        await ctx.close();
    }

    // Desktop 1440x900
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(OUT, `${prefix}-1440x900.png`), fullPage: false });
        console.log(`Saved: ${prefix}-1440x900.png`);
        await ctx.close();
    }

    // Mobile 390x844
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(OUT, `${prefix}-390x844.png`), fullPage: false });
        console.log(`Saved: ${prefix}-390x844.png`);
        await ctx.close();
    }

    await browser.close();
}

const prefix = process.argv[2] || 'sebelum';
takeScreenshots(prefix).catch(err => {
    console.error(err);
    process.exit(1);
});
