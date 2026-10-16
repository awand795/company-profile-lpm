const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp10b');
fs.mkdirSync(OUT, { recursive: true });

async function verifyRonde18b() {
    const browser = await chromium.launch({ headless: true });
    
    console.log('=== VERIFIKASI LENGKAP RONDE 18b ===\n');

    // 1. Desktop 1366x600 (View utama pengujian)
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
            const lead = document.querySelector('.hero-lead');
            const btns = document.querySelector('.hero-btns-row');
            const brandLbl = document.querySelector('.brand-label');
            const brandChip = document.querySelector('.brand-chip');
            const photo = document.querySelector('.hero-truck-img img') || document.querySelector('.hero-truck-img');
            const card = document.querySelector('.hero-telematics-card');
            const pill = document.querySelector('.telematics-status-pill');
            const btnReg = document.querySelector('.btn-nav-register .elementor-button');
            const btnLog = document.querySelector('.btn-nav-login .elementor-button');

            const getRect = el => el ? el.getBoundingClientRect() : null;
            const bR = getRect(badge);
            const hR = getRect(h1);
            const lR = getRect(lead);
            const btR = getRect(btns);
            const blR = getRect(brandLbl);
            const bcR = getRect(brandChip);
            const pR = getRect(photo);
            const cR = getRect(card);
            const pillR = getRect(pill);
            const btnRegR = getRect(btnReg);
            const btnLogR = getRect(btnLog);
            const heroR = getRect(hero);
            const topbarR = getRect(topbar);
            const headerR = getRect(header);

            // Spacing
            const badgeToH1 = (bR && hR) ? Math.round(hR.top - bR.bottom) : null;
            const h1ToLead = (hR && lR) ? Math.round(lR.top - hR.bottom) : null;
            const leadToBtns = (lR && btR) ? Math.round(btR.top - lR.bottom) : null;
            const btnsToBrandLbl = (btR && blR) ? Math.round(blR.top - btR.bottom) : null;
            const brandLblToChip = (blR && bcR) ? Math.round(bcR.top - blR.bottom) : null;

            // Overlap percentage
            let overlapArea = 0;
            let photoArea = 0;
            let overlapPct = 0;
            if (pR && cR) {
                photoArea = pR.width * pR.height;
                const xOverlap = Math.max(0, Math.min(pR.right, cR.right) - Math.max(pR.left, cR.left));
                const yOverlap = Math.max(0, Math.min(pR.bottom, cR.bottom) - Math.max(pR.top, cR.top));
                overlapArea = xOverlap * yOverlap;
                overlapPct = (overlapArea / photoArea) * 100;
            }

            // Icons
            const icons = Array.from(document.querySelectorAll('.stitch-topbar i, .stitch-sec-hero i, .hero-authority-badge i')).map(el => {
                const before = getComputedStyle(el, '::before');
                return {
                    className: el.className,
                    content: before.content,
                    rendered: before.content !== 'none' && before.content !== 'normal' && before.content !== '',
                    width: el.getBoundingClientRect().width
                };
            });
            const failedIcons = icons.filter(i => !i.rendered).length;

            // Pill text lines
            const pillLines = pill ? Math.round(pillR.height / 24) : 0;

            // Topbar text lines
            const topbarItems = Array.from(document.querySelectorAll('.topbar-hotline-item, .topbar-location-item, .topbar-hours-item, .topbar-iso-item'));
            const topbarLines = topbarItems.map(el => ({
                text: el.innerText.trim(),
                height: el.getBoundingClientRect().height,
                singleLine: el.getBoundingClientRect().height <= 20
            }));

            // Horizontal scroll
            const hasHScroll = document.documentElement.scrollWidth > window.innerWidth;

            return {
                topbarHeight: topbarR ? topbarR.height : null,
                headerHeight: headerR ? headerR.height : null,
                heroHeight: heroR ? heroR.height : null,
                badgeToH1,
                h1ToLead,
                leadToBtns,
                btnsToBrandLbl,
                brandLblToChip,
                overlapPct: overlapPct.toFixed(2) + '%',
                cardHeight: cR ? cR.height : null,
                cardWidth: cR ? cR.width : null,
                pillHeight: pillR ? pillR.height : null,
                pillLines,
                btnRegHeight: btnRegR ? btnRegR.height : null,
                btnLogHeight: btnLogR ? btnLogR.height : null,
                btnRegBoxShadow: btnReg ? getComputedStyle(btnReg).boxShadow : null,
                ctaBottom: btR ? btR.bottom : null,
                failedIcons,
                icons,
                topbarLines,
                hasHScroll
            };
        });

        console.log('--- Hasil Pengukuran Desktop 1366x600 ---');
        console.table({
            topbarHeight: data.topbarHeight,
            headerHeight: data.headerHeight,
            heroHeight: data.heroHeight,
            badgeToH1: data.badgeToH1,
            h1ToLead: data.h1ToLead,
            leadToBtns: data.leadToBtns,
            btnsToBrandLbl: data.btnsToBrandLbl,
            brandLblToChip: data.brandLblToChip,
            overlapPct: data.overlapPct,
            cardHeight: data.cardHeight,
            cardWidth: data.cardWidth,
            pillHeight: data.pillHeight,
            btnRegHeight: data.btnRegHeight,
            ctaBottom: data.ctaBottom,
            failedIcons: data.failedIcons,
            hasHScroll: data.hasHScroll
        });

        console.log('\n--- Status Ikon Render ---');
        console.table(data.icons);

        await page.screenshot({ path: path.join(OUT, '1366x600.png'), fullPage: false });
        console.log('Saved: 1366x600.png');

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
        await page.screenshot({ path: path.join(OUT, '1024.png'), fullPage: false });
        console.log('Saved: 1024.png');
        await ctx.close();
    }

    // 4. Tablet 768x1024
    {
        const ctx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(600);
        await page.screenshot({ path: path.join(OUT, '768.png'), fullPage: false });
        console.log('Saved: 768.png');
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
        await page.screenshot({ path: path.join(OUT, '390.png'), fullPage: false });
        console.log('Saved: 390.png');
        await ctx.close();
    }

    await browser.close();
    console.log('\n=== VERIFIKASI SELESAI ===');
}

verifyRonde18b().catch(err => {
    console.error('Error during verification:', err);
    process.exit(1);
});
