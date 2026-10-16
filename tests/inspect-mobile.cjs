const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await ctx.newPage();
    await page.goto('http://localhost:5000/', { waitUntil: 'networkidle' });
    const res = await page.evaluate(() => {
        const topbar = document.querySelector('.stitch-topbar');
        const header = document.querySelector('.stitch-navbar');
        const navRow = document.querySelector('.stitch-nav-row');
        const brandCol = document.querySelector('.stitch-brand-col');
        const menuCol = document.querySelector('.stitch-menu-col');
        const ctaCol = document.querySelector('.stitch-cta-col');
        
        return {
            headerHeight: header ? header.getBoundingClientRect().height : 0,
            navRowHeight: navRow ? navRow.getBoundingClientRect().height : 0,
            brandCol: brandCol ? { h: brandCol.getBoundingClientRect().height, display: getComputedStyle(brandCol).display } : null,
            menuCol: menuCol ? { h: menuCol.getBoundingClientRect().height, display: getComputedStyle(menuCol).display } : null,
            ctaCol: ctaCol ? { h: ctaCol.getBoundingClientRect().height, display: getComputedStyle(ctaCol).display } : null,
            topbarHeight: topbar ? topbar.getBoundingClientRect().height : 0,
            topbarHTML: topbar ? topbar.innerHTML : ''
        };
    });
    console.log(JSON.stringify(res, null, 2));
    await browser.close();
})();
