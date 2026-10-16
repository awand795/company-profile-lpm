const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp10');
fs.mkdirSync(OUT, { recursive: true });

async function verifyRonde18() {
    const browser = await chromium.launch({ headless: true });
    
    console.log('=== VERIFIKASI LENGKAP RONDE 18 (HERO LEBIH KEREN) ===\n');

    // 1. Desktop 1366x600 (View utama pengujian kerapatan & komposisi)
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 600 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);

        const data = await page.evaluate(() => {
            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const hero = document.querySelector('.stitch-sec-hero');
            const badge = document.querySelector('.hero-authority-badge');
            const h1 = document.querySelector('.hero-title');
            const highlight = document.querySelector('.hero-brand-highlight');
            const photo = document.querySelector('.hero-truck-img img') || document.querySelector('.hero-truck-img');
            const ctaRow = document.querySelector('.hero-btns-row');
            const ctaPrimary = document.querySelector('.btn-hero-primary');
            const ctaSecondary = document.querySelector('.btn-hero-secondary');
            const telematics = document.querySelector('.hero-telematics-card');
            const logoImg = document.querySelector('.brand-logo-img img');
            const liveDot = document.querySelector('.status-live-dot');

            const getRect = el => el ? el.getBoundingClientRect() : null;
            const topbarRect = getRect(topbar);
            const headerRect = getRect(header);
            const heroRect = getRect(hero);
            const badgeRect = getRect(badge);
            const h1Rect = getRect(h1);
            const photoRect = getRect(photo);
            const ctaRect = getRect(ctaRow);
            const teleRect = getRect(telematics);

            // Periksa apakah badge berbentuk pil
            const badgeCS = badge ? getComputedStyle(badge) : null;
            const badgeWidth = badgeRect ? badgeRect.width : 0;
            const badgeIsPill = badgeCS ? (parseFloat(badgeCS.borderRadius) >= 50 && badgeWidth < 650) : false;

            // Periksa H1 underline
            const h1Underline = h1 ? getComputedStyle(h1.querySelector('.elementor-heading-title') || h1).textDecorationLine : '';
            const highlightCS = highlight ? getComputedStyle(highlight) : null;

            // Periksa tombol CTA dalam satu row dan tinggi 52px
            const ctaPrimRect = getRect(ctaPrimary);
            const ctaSecRect = getRect(ctaSecondary);
            const ctaGap = (ctaPrimRect && ctaSecRect) ? Math.round(ctaSecRect.left - ctaPrimRect.right) : 0;
            const ctaSameRow = (ctaPrimRect && ctaSecRect) ? Math.abs(ctaPrimRect.top - ctaSecRect.top) < 4 : false;

            // Periksa emoji di teks
            const emojiRegex = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu;
            const topbarMatches = (document.querySelector('.stitch-topbar')?.innerText.match(emojiRegex) || []).length;
            const navbarMatches = (document.querySelector('.stitch-navbar')?.innerText.match(emojiRegex) || []).length;
            const heroMatches = (document.querySelector('.stitch-sec-hero')?.innerText.match(emojiRegex) || []).length;
            const emojiMatches = topbarMatches + navbarMatches + heroMatches;

            // Periksa H1 baris
            let h1Lines = 0;
            if (h1) {
                const titleEl = h1.querySelector('.elementor-heading-title') || h1;
                const lh = parseFloat(getComputedStyle(titleEl).lineHeight) || (42 * 1.15);
                h1Lines = Math.round(titleEl.getBoundingClientRect().height / lh);
            }

            // Periksa selisih foto top vs badge top
            const photoVsBadgeTopDiff = (photoRect && badgeRect) ? Math.abs(photoRect.top - badgeRect.top) : null;

            // Bawah tombol CTA dari atas viewport
            const ctaBottomFromViewportTop = ctaRect ? ctaRect.bottom : null;

            // Check logo transparent src
            const logoSrc = logoImg ? logoImg.src : '';

            // Check telematics position
            const telePosition = telematics ? getComputedStyle(telematics).position : '';

            return {
                topbarHeight: topbarRect ? topbarRect.height : null,
                headerHeight: headerRect ? headerRect.height : null,
                heroHeight: heroRect ? heroRect.height : null,
                photoVsBadgeTopDiff,
                h1Lines,
                ctaBottomFromViewportTop,
                badgeWidth,
                badgeIsPill,
                h1Underline,
                hasHighlight: !!highlight,
                ctaSameRow,
                ctaGap,
                primaryBtnHeight: ctaPrimRect ? ctaPrimRect.height : null,
                secondaryBtnHeight: ctaSecRect ? ctaSecRect.height : null,
                telePosition,
                logoSrc,
                emojiInHeroArea: emojiMatches,
                hasLiveDot: !!liveDot
            };
        });

        console.log('--- Metrik Desktop 1366x600 ---');
        console.table(data);

        await page.screenshot({ path: path.join(OUT, '1366x600.png'), fullPage: false });
        console.log('Saved: 1366x600.png');

        // Hover CTA Primary
        const primaryBtn = page.locator('.btn-hero-primary .elementor-button');
        if (await primaryBtn.count() > 0) {
            await primaryBtn.hover();
            await page.waitForTimeout(300);
            await page.screenshot({ path: path.join(OUT, 'hover_cta_primary.png'), fullPage: false });
            console.log('Saved: hover_cta_primary.png');
        }

        // Hover Nav Menu Link
        const navLink = page.locator('.stitch-menu-col a').first();
        if (await navLink.count() > 0) {
            await navLink.hover();
            await page.waitForTimeout(300);
            await page.screenshot({ path: path.join(OUT, 'hover_nav_menu.png'), fullPage: false });
            console.log('Saved: hover_nav_menu.png');
        }

        // Scrolled sticky navbar (> 100px)
        await page.evaluate(() => window.scrollTo(0, 150));
        await page.waitForTimeout(400);
        const stickyHeight = await page.evaluate(() => {
            const nb = document.querySelector('.stitch-navbar');
            return nb ? nb.getBoundingClientRect().height : null;
        });
        console.log(`Sticky Navbar Height: ${stickyHeight}px`);
        await page.screenshot({ path: path.join(OUT, 'sticky_scrolled.png'), fullPage: false });
        console.log('Saved: sticky_scrolled.png');

        await ctx.close();
    }

    // 2. Desktop 1440x900
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(600);
        await page.screenshot({ path: path.join(OUT, '1440x900.png'), fullPage: false });
        console.log('Saved: 1440x900.png');
        await ctx.close();
    }

    // 3. Tablet 1024x768
    {
        const ctx = await browser.newContext({ viewport: { width: 1024, height: 768 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(600);
        await page.screenshot({ path: path.join(OUT, '1024x768.png'), fullPage: false });
        console.log('Saved: 1024x768.png');
        await ctx.close();
    }

    // 4. Tablet Portrait 768x1024
    {
        const ctx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(600);
        await page.screenshot({ path: path.join(OUT, '768x1024.png'), fullPage: false });
        console.log('Saved: 768x1024.png');
        await ctx.close();
    }

    // 5. Mobile 390x844
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(600);
        const mobileMetrics = await page.evaluate(() => {
            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const tele = document.querySelector('.hero-telematics-card');
            return {
                topbarHeight: topbar ? topbar.getBoundingClientRect().height : null,
                headerHeight: header ? header.getBoundingClientRect().height : null,
                telePosition: tele ? getComputedStyle(tele).position : null,
                hasHScroll: document.documentElement.scrollWidth > window.innerWidth
            };
        });
        console.log('--- Metrik Mobile 390x844 ---');
        console.table(mobileMetrics);
        await page.screenshot({ path: path.join(OUT, '390x844.png'), fullPage: false });
        console.log('Saved: 390x844.png');
        await ctx.close();
    }

    // 6. Prefers Reduced Motion Test
    {
        const ctx = await browser.newContext({ 
            viewport: { width: 1366, height: 600 },
            reducedMotion: 'reduce'
        });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        const animCheck = await page.evaluate(() => {
            const badge = document.querySelector('.hero-authority-badge');
            const dot = document.querySelector('.status-live-dot');
            return {
                badgeAnimation: badge ? getComputedStyle(badge).animationName : '',
                dotAnimation: dot ? getComputedStyle(dot).animationName : ''
            };
        });
        console.log('--- Reduced Motion Check ---', animCheck);
        await ctx.close();
    }

    await browser.close();
    console.log('\n=== VERIFIKASI SELESAI ===');
}

verifyRonde18().catch(err => {
    console.error('Error during verification:', err);
    process.exit(1);
});
