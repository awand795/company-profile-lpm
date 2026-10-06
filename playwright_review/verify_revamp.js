const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
    const browser = await chromium.launch({ headless: true });
    
    // 1. Desktop Test (1440x900)
    const contextDesk = await browser.newContext({
        viewport: { width: 1440, height: 900 }
    });
    const pageDesk = await contextDesk.newPage();
    
    const consoleLogs = [];
    pageDesk.on('console', msg => consoleLogs.push(`[${msg.type()}] ${msg.text()}`));
    pageDesk.on('pageerror', err => consoleLogs.push(`[PAGE_ERROR] ${err.toString()}`));

    console.log('Navigating to http://localhost:8080 (Desktop)...');
    const respDesk = await pageDesk.goto('http://localhost:8080', { waitUntil: 'networkidle' });
    console.log(`Desktop Status: ${respDesk.status()}`);

    // Wait for animations and smooth scroll to bottom then top
    await pageDesk.waitForTimeout(1000);
    await pageDesk.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 300;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;
                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    window.scrollTo(0, 0);
                    resolve();
                }
            }, 50);
        });
    });
    await pageDesk.waitForTimeout(1000);

    await pageDesk.screenshot({
        path: 'playwright_review/sesudah_desktop_1440.png',
        fullPage: true
    });
    console.log('Saved playwright_review/sesudah_desktop_1440.png');

    // 2. Mobile Test (390x844)
    const contextMob = await browser.newContext({
        viewport: { width: 390, height: 844 },
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
    });
    const pageMob = await contextMob.newPage();
    console.log('Navigating to http://localhost:8080 (Mobile)...');
    const respMob = await pageMob.goto('http://localhost:8080', { waitUntil: 'networkidle' });
    console.log(`Mobile Status: ${respMob.status()}`);

    await pageMob.waitForTimeout(1000);
    await pageMob.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 300;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;
                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    window.scrollTo(0, 0);
                    resolve();
                }
            }, 50);
        });
    });
    await pageMob.waitForTimeout(1000);

    await pageMob.screenshot({
        path: 'playwright_review/sesudah_mobile_390.png',
        fullPage: true
    });
    console.log('Saved playwright_review/sesudah_mobile_390.png');

    // 3. Inspect color & red violations on desktop page
    const redViolations = await pageDesk.evaluate(() => {
        const violations = [];
        const allElements = document.querySelectorAll('*');
        for (const el of allElements) {
            // Ignore script, style, noscript
            if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'HEAD', 'META', 'LINK'].includes(el.tagName)) continue;
            const style = window.getComputedStyle(el);
            const color = style.color;
            const bg = style.backgroundColor;
            const border = style.borderColor;

            // Check for pure red or carserv red: rgb(216, 19, 36) or pure red rgb(255, 0, 0)
            const isRed = (str) => {
                if (!str) return false;
                // check rgb(216, 19, 36) or rgb(220, 53, 69) or rgb(185, 15, 30)
                const match = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
                if (match) {
                    const r = parseInt(match[1], 10);
                    const g = parseInt(match[2], 10);
                    const b = parseInt(match[3], 10);
                    if (r > 180 && g < 70 && b < 70) return true;
                }
                return false;
            };

            if (isRed(color)) {
                violations.push({ tag: el.tagName, class: el.className, text: el.innerText ? el.innerText.slice(0, 30) : '', prop: 'color', val: color });
            }
            if (isRed(bg)) {
                violations.push({ tag: el.tagName, class: el.className, text: el.innerText ? el.innerText.slice(0, 30) : '', prop: 'background', val: bg });
            }
        }
        return violations;
    });

    console.log('Red color violations found:', redViolations.length);
    if (redViolations.length > 0) {
        console.log(JSON.stringify(redViolations.slice(0, 10), null, 2));
    }

    // 4. Verify Other Subpage Routes
    const routes = ['/profil/', '/produk/', '/wilayah/', '/kontak/', '/layanan-overhaul/'];
    console.log('\nTesting subpage routes:');
    for (const r of routes) {
        try {
            const res = await pageDesk.goto(`http://localhost:8080${r}`, { waitUntil: 'load', timeout: 5000 });
            console.log(`Route ${r}: HTTP ${res ? res.status() : 'null'}`);
        } catch (e) {
            console.log(`Route ${r}: Error ${e.message}`);
        }
    }

    // 5. Console logs check
    console.log('\nBrowser Console logs count:', consoleLogs.length);
    if (consoleLogs.length > 0) {
        console.log('Sample logs:', consoleLogs.slice(0, 10));
    }

    await browser.close();
})();
