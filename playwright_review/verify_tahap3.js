const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, 'sesudah_tahap3');
if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
}

const viewports = [
    { name: '1440', width: 1440, height: 900 },
    { name: '1024', width: 1024, height: 768 },
    { name: '768', width: 768, height: 1024 },
    { name: '390', width: 390, height: 844, isMobile: true }
];

(async () => {
    const browser = await chromium.launch({ headless: true });
    let allPassed = true;

    for (const vp of viewports) {
        console.log(`\n========================================`);
        console.log(`Testing Viewport: ${vp.name} (${vp.width}x${vp.height})`);
        console.log(`========================================`);

        const context = await browser.newContext({
            viewport: { width: vp.width, height: vp.height },
            userAgent: vp.isMobile
                ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
                : undefined
        });
        const page = await context.newPage();

        const consoleErrors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
            }
        });
        page.on('pageerror', err => {
            consoleErrors.push(err.toString());
        });

        const resp = await page.goto('http://localhost:8080', { waitUntil: 'networkidle' });
        console.log(`Status Code: ${resp.status()}`);

        // Wait for fonts & styles
        await page.waitForTimeout(1000);

        // Smooth scroll to trigger scroll animations & reveal all sections
        await page.evaluate(async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 400;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if (totalHeight >= scrollHeight) {
                        clearInterval(timer);
                        window.scrollTo(0, 0);
                        resolve();
                    }
                }, 40);
            });
        });
        await page.waitForTimeout(800);

        // Check horizontal overflow
        const overflow = await page.evaluate(() => {
            return {
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
            };
        });

        console.log(`Horizontal Scroll: scrollWidth=${overflow.scrollWidth}, clientWidth=${overflow.clientWidth}`);
        if (overflow.hasOverflow) {
            console.error(`[ERROR] Horizontal overflow detected at viewport ${vp.name}!`);
            allPassed = false;
        } else {
            console.log(`[PASS] No horizontal overflow at viewport ${vp.name}.`);
        }

        // Topbar & Navbar screenshot
        const headerHandle = await page.$('.navbar');
        if (headerHandle) {
            await page.screenshot({
                path: path.join(outDir, `sesudah_${vp.name}_topbar_navbar.png`),
                clip: { x: 0, y: 0, width: vp.width, height: vp.width >= 992 ? 120 : 80 }
            });
        }

        // Full page screenshot
        await page.screenshot({
            path: path.join(outDir, `sesudah_${vp.name}_full.png`),
            fullPage: true
        });
        console.log(`Saved screenshots for ${vp.name}`);

        // Check Slide 2 copy intact
        const slide2Exists = await page.evaluate(() => {
            const h1s = Array.from(document.querySelectorAll('h1'));
            return h1s.some(h => h.textContent.includes('Pasokan Pelumas Resmi & Suku Cadang Asli'));
        });
        if (!slide2Exists) {
            console.error(`[ERROR] Slide 2 copy 'Pasokan Pelumas Resmi & Suku Cadang Asli' missing!`);
            allPassed = false;
        } else {
            console.log(`[PASS] Slide 2 copy verified intact.`);
        }

        if (consoleErrors.length > 0) {
            console.warn(`[CONSOLE WARNINGS/ERRORS] at ${vp.name}:`, consoleErrors);
        } else {
            console.log(`[PASS] Zero console errors at ${vp.name}.`);
        }

        await context.close();
    }

    // Scrollspy test on 1440
    console.log(`\n========================================`);
    console.log(`Testing Scrollspy / Active Links on Desktop 1440`);
    console.log(`========================================`);
    const scrollContext = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const scrollPage = await scrollContext.newPage();
    await scrollPage.goto('http://localhost:8080', { waitUntil: 'networkidle' });
    await scrollPage.waitForTimeout(500);

    // Scroll to #service and check active nav link
    await scrollPage.evaluate(() => {
        const el = document.getElementById('service');
        if (el) el.scrollIntoView({ behavior: 'instant' });
    });
    await scrollPage.waitForTimeout(400);

    const activeLink = await scrollPage.evaluate(() => {
        const active = document.querySelector('.navbar-nav .nav-link.active');
        return active ? active.textContent.trim() : null;
    });
    console.log(`Active Nav Link after scrolling to #service: "${activeLink}"`);

    await scrollContext.close();
    await browser.close();

    console.log(`\nAll tests completed. Overall success: ${allPassed}`);
})();
