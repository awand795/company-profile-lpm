const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp9');
fs.mkdirSync(OUT, { recursive: true });

async function measure() {
    const browser = await chromium.launch({ headless: true });
    
    console.log('=== PENGUKURAN RONDE 17 (SESUDAH) ===\n');

    // 1. Desktop 1366x600 (View utama pengujian kerapatan)
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 600 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);

        const metrics = await page.evaluate(() => {
            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const hero = document.querySelector('.stitch-sec-hero');
            const badge = document.querySelector('.hero-authority-badge');
            const h1 = document.querySelector('.hero-title');
            const lead = document.querySelector('.hero-lead');
            const photo = document.querySelector('.hero-truck-img img') || document.querySelector('.hero-truck-img');
            const ctaBtns = document.querySelector('.hero-btns-row');
            const ctaPrimary = document.querySelector('.btn-hero-primary');
            const ctaSecondary = document.querySelector('.btn-hero-secondary');
            const telematics = document.querySelector('.hero-telematics-card');
            const stats = document.querySelector('.hero-stats-inner');

            const getRect = el => el ? el.getBoundingClientRect() : null;
            const topbarRect = getRect(topbar);
            const headerRect = getRect(header);
            const heroRect = getRect(hero);
            const badgeRect = getRect(badge);
            const h1Rect = getRect(h1);
            const photoRect = getRect(photo);
            const ctaRect = getRect(ctaBtns);
            const ctaPrimRect = getRect(ctaPrimary);
            const ctaSecRect = getRect(ctaSecondary);
            const teleRect = getRect(telematics);

            // Periksa baris H1
            let h1Lines = 0;
            if (h1) {
                const titleEl = h1.querySelector('.elementor-heading-title') || h1;
                const lh = parseFloat(getComputedStyle(titleEl).lineHeight) || (42 * 1.15);
                h1Lines = Math.round(titleEl.getBoundingClientRect().height / lh);
            }

            // Periksa teks wrap pada topbar
            const topbarTexts = Array.from(topbar ? topbar.querySelectorAll('div, span, a') : []);
            let topbarWrapped = 0;
            topbarTexts.forEach(el => {
                if (el.children.length === 0 && el.textContent.trim().length > 0) {
                    const cs = getComputedStyle(el);
                    if (cs.whiteSpace !== 'nowrap') {
                        // check if clientHeight > single line
                        const lh = parseFloat(cs.lineHeight) || 16;
                        if (el.clientHeight > lh * 1.5) topbarWrapped++;
                    }
                }
            });

            // Periksa selisih foto top vs badge top
            const photoVsBadgeTopDiff = (photoRect && badgeRect) ? Math.abs(photoRect.top - badgeRect.top) : null;

            // Bawah tombol CTA dari atas viewport
            const ctaBottomFromViewportTop = ctaRect ? ctaRect.bottom : (ctaPrimRect ? ctaPrimRect.bottom : null);

            // Jarak header -> hero (padding atas hero)
            const heroPaddingTop = hero ? parseFloat(getComputedStyle(hero.querySelector('.e-con-inner') || hero).paddingTop) : null;

            // Jarak foto -> telematika
            const distPhotoToTele = (photoRect && teleRect) ? Math.round(teleRect.top - photoRect.bottom) : null;

            // Horizontal scroll check
            const hasHScroll = document.documentElement.scrollWidth > window.innerWidth;

            return {
                topbarHeight: topbarRect ? topbarRect.height : null,
                headerHeight: headerRect ? headerRect.height : null,
                heroPaddingTop,
                photoVsBadgeTopDiff,
                h1Lines,
                h1Height: h1Rect ? h1Rect.height : null,
                ctaBottomFromViewportTop,
                distPhotoToTele,
                topbarWrapped,
                hasHScroll,
                scrollWidth: document.documentElement.scrollWidth,
                innerWidth: window.innerWidth
            };
        });

        console.log('--- Hasil Pengukuran 1366x600 ---');
        console.table(metrics);

        await page.screenshot({ path: path.join(OUT, '1366x600.png'), fullPage: false });
        console.log('Saved: 1366x600.png');
        await ctx.close();
    }

    // 2. Desktop 1440x900
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(500);
        await page.screenshot({ path: path.join(OUT, '1440x900.png'), fullPage: false });
        console.log('Saved: 1440x900.png');
        await ctx.close();
    }

    // 3. Tablet 1024x768
    {
        const ctx = await browser.newContext({ viewport: { width: 1024, height: 768 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(500);
        await page.screenshot({ path: path.join(OUT, '1024x768.png'), fullPage: false });
        console.log('Saved: 1024x768.png');
        await ctx.close();
    }

    // 4. Tablet 768x1024
    {
        const ctx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(500);
        await page.screenshot({ path: path.join(OUT, '768x1024.png'), fullPage: false });
        console.log('Saved: 768x1024.png');
        await ctx.close();
    }

    // 5. Mobile 390x844
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(500);
        const mobileMetrics = await page.evaluate(() => {
            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const cta = document.querySelector('.btn-hero-primary');
            return {
                topbarHeight: topbar ? topbar.getBoundingClientRect().height : 0,
                headerHeight: header ? header.getBoundingClientRect().height : 0,
                ctaVisibleInFirstScreen: cta ? cta.getBoundingClientRect().bottom <= 844 : false,
                ctaBottom: cta ? cta.getBoundingClientRect().bottom : null,
                hasHScroll: document.documentElement.scrollWidth > window.innerWidth
            };
        });
        console.log('--- Hasil Mobile 390x844 ---');
        console.table(mobileMetrics);

        await page.screenshot({ path: path.join(OUT, '390x844.png'), fullPage: false });
        console.log('Saved: 390x844.png');
        await ctx.close();
    }

    // 6. Sticky Header saat Scroll > 24px (1366x600)
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 600 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(500);

        // Scroll down 100px
        await page.evaluate(() => window.scrollTo(0, 100));
        await page.waitForTimeout(400); // Tunggu transisi 200ms

        const stickyMetrics = await page.evaluate(() => {
            const header = document.querySelector('.stitch-navbar');
            const rect = header ? header.getBoundingClientRect() : null;
            return {
                stickyHeaderHeight: rect ? rect.height : null,
                stickyHeaderTop: rect ? rect.top : null,
                isStickyScrolledClass: header ? header.classList.contains('sticky-scrolled') : false
            };
        });
        console.log('--- Hasil Sticky Header Scroll > 24px ---');
        console.table(stickyMetrics);

        await page.screenshot({ path: path.join(OUT, 'sticky_scrolled.png'), fullPage: false });
        console.log('Saved: sticky_scrolled.png');
        await ctx.close();
    }

    await browser.close();
    console.log('\nPengukuran selesai!');
}

measure().catch(err => {
    console.error('Error during measurement:', err);
    process.exit(1);
});
