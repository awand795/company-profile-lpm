const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp11');
fs.mkdirSync(OUT, { recursive: true });

async function verifyRonde19() {
    const browser = await chromium.launch({ headless: true });
    
    console.log('=== VERIFIKASI LENGKAP RONDE 19 (HERO LEBIH CANTIK & PREMIUM) ===\n');

    // 1. Desktop 1366x600 (Viewport utama pengukuran)
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
            const lead = document.querySelector('.hero-lead');
            const btns = document.querySelector('.hero-btns-row');
            const btnPrimary = document.querySelector('.btn-hero-primary .elementor-button');
            const btnSecondary = document.querySelector('.btn-hero-secondary .elementor-button');
            const brandLbl = document.querySelector('.brand-label');
            const brandChip = document.querySelector('.brand-chip');
            const photo = document.querySelector('.hero-truck-img img') || document.querySelector('.hero-truck-img');
            const card = document.querySelector('.hero-telematics-card');
            const teleTitle = document.querySelector('.telematics-title');
            const teleDesc = document.querySelector('.telematics-desc');
            const telePill = document.querySelector('.telematics-status-pill');
            const teleMetrics = document.querySelector('.telematics-metrics-block');

            const getRect = el => el ? el.getBoundingClientRect() : null;
            const bR = getRect(badge);
            const hR = getRect(h1);
            const lR = getRect(lead);
            const btR = getRect(btns);
            const pR = getRect(photo);
            const cR = getRect(card);
            const topbarR = getRect(topbar);
            const headerR = getRect(header);
            const heroR = getRect(hero);

            // Jarak atas foto vs badge
            const photoVsBadge = (pR && bR) ? Math.abs(Math.round(pR.top - bR.top)) : null;

            // Bawah tombol CTA
            const ctaBottom = btR ? Math.round(btR.bottom) : null;

            // Pengecekan teks kartu terpotong
            const isTruncated = el => {
                if (!el) return null;
                return el.scrollWidth > el.clientWidth + 1; // 1px threshold for subpixel
            };

            const titleTruncated = isTruncated(teleTitle);
            const descTruncated = isTruncated(teleDesc);

            // Periksa HScroll
            const hasHScroll = document.documentElement.scrollWidth > window.innerWidth;

            return {
                topbarHeight: topbarR ? topbarR.height : null,
                headerHeight: headerR ? headerR.height : null,
                heroHeight: heroR ? heroR.height : null,
                photoVsBadge,
                ctaBottom,
                cardWidth: cR ? Math.round(cR.width) : null,
                cardHeight: cR ? Math.round(cR.height) : null,
                teleTitleText: teleTitle ? teleTitle.innerText.trim() : null,
                titleTruncated,
                teleDescText: teleDesc ? teleDesc.innerText.trim() : null,
                descTruncated,
                hasHScroll
            };
        });

        console.log('--- Hasil Pengukuran Desktop 1366x600 ---');
        console.table(data);

        // Ambil screenshot viewport 1366x600
        await page.screenshot({ path: path.join(OUT, '1366x600.png'), fullPage: false });
        console.log('Saved: 1366x600.png');

        // Ambil crop kartu telematika membuktikan teks tidak terpotong
        const teleCard = await page.$('.hero-telematics-card');
        if (teleCard) {
            await teleCard.screenshot({ path: path.join(OUT, 'crop_kartu_telematika.png') });
            console.log('Saved: crop_kartu_telematika.png');
        }

        // Test hover CTA primary
        await page.hover('.btn-hero-primary .elementor-button');
        await page.waitForTimeout(250);
        await page.screenshot({ path: path.join(OUT, 'hover_cta_primary.png'), fullPage: false });
        console.log('Saved: hover_cta_primary.png');

        // Test sticky scrolled
        await page.evaluate(() => window.scrollTo(0, 300));
        await page.waitForTimeout(500);
        const stickyHeaderHeight = await page.evaluate(() => {
            const h = document.querySelector('.stitch-navbar');
            return h ? h.getBoundingClientRect().height : null;
        });
        console.log('Sticky Header Scrolled Height:', stickyHeaderHeight, '(Target <= 60px)');
        await page.screenshot({ path: path.join(OUT, 'sticky_scrolled.png'), fullPage: false });
        console.log('Saved: sticky_scrolled.png');

        await ctx.close();
    }

    // 2. Desktop 1440x900
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(OUT, '1440x900.png'), fullPage: false });
        console.log('Saved: 1440x900.png');
        await ctx.close();
    }

    // 3. Desktop 1920x1080
    {
        const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(OUT, '1920x1080.png'), fullPage: false });
        console.log('Saved: 1920x1080.png');
        await ctx.close();
    }

    // 4. Desktop 1024x768
    {
        const ctx = await browser.newContext({ viewport: { width: 1024, height: 768 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        const cardTrunc = await page.evaluate(() => {
            const t = document.querySelector('.telematics-title');
            const d = document.querySelector('.telematics-desc');
            return {
                titleTrunc: t ? t.scrollWidth > t.clientWidth + 1 : false,
                descTrunc: d ? d.scrollWidth > d.clientWidth + 1 : false,
                hScroll: document.documentElement.scrollWidth > window.innerWidth
            };
        });
        console.log('1024x768 card truncation check:', cardTrunc);
        await page.screenshot({ path: path.join(OUT, '1024x768.png'), fullPage: false });
        console.log('Saved: 1024x768.png');
        await ctx.close();
    }

    // 5. Tablet 768x1024
    {
        const ctx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(OUT, '768x1024.png'), fullPage: false });
        console.log('Saved: 768x1024.png');
        await ctx.close();
    }

    // 6. Mobile 390x844
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        const mobData = await page.evaluate(() => {
            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const card = document.querySelector('.hero-telematics-card');
            const hScroll = document.documentElement.scrollWidth > window.innerWidth;
            return {
                topbarHeight: topbar ? topbar.getBoundingClientRect().height : null,
                headerHeight: header ? header.getBoundingClientRect().height : null,
                hasHScroll: hScroll
            };
        });
        console.log('Mobile 390x844 data:', mobData);
        await page.screenshot({ path: path.join(OUT, '390x844.png'), fullPage: false });
        console.log('Saved: 390x844.png');
        await ctx.close();
    }

    await browser.close();
    console.log('\n=== VERIFIKASI SELESAI ===');
}

verifyRonde19().catch(err => {
    console.error('Error during verification:', err);
    process.exit(1);
});
