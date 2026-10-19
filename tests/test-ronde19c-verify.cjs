const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp11c');
fs.mkdirSync(OUT, { recursive: true });

// Copy baseline sebelum dari sesudah_revamp11b
const prevHero = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp11b', '1366x600.png');
if (fs.existsSync(prevHero)) {
    fs.copyFileSync(prevHero, path.join(OUT, 'sebelum_1366x600.png'));
}

async function verifyRonde19c() {
    const browser = await chromium.launch({ headless: true });
    
    console.log('=== VERIFIKASI LENGKAP RONDE 19c (JUDUL RINGKAS & HERO MUAT LAYAR PERTAMA) ===\n');

    // Helper to calculate line count of an element
    async function getLineCount(page, selector) {
        return await page.evaluate(sel => {
            const el = document.querySelector(sel);
            if (!el) return 0;
            const lh = parseFloat(window.getComputedStyle(el).lineHeight) || (parseFloat(window.getComputedStyle(el).fontSize) * 1.15);
            const h = el.clientHeight;
            return Math.round(h / lh);
        }, selector);
    }

    // 1. Desktop 1366x600 (Layar Pertama Utama)
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 600 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);

        const data = await page.evaluate(() => {
            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const hero = document.querySelector('.stitch-sec-hero');
            const btnLogin = document.querySelector('.btn-nav-login .elementor-button');
            const btnRegister = document.querySelector('.btn-nav-register .elementor-button');
            const badge = document.querySelector('.hero-authority-badge');
            const h1Title = document.querySelector('.hero-title .elementor-heading-title');
            const lead = document.querySelector('.hero-lead');
            const btns = document.querySelector('.hero-btns-row');
            const btnPrimary = document.querySelector('.btn-hero-primary .elementor-button');
            const brandBlock = document.querySelector('.hero-brands-block');
            const brandChipRow = document.querySelector('.brand-chips-row');
            const brandChips = Array.from(document.querySelectorAll('.brand-chip'));
            const photoWrap = document.querySelector('.hero-truck-img');
            const card = document.querySelector('.hero-telematics-card');
            const teleTitle = document.querySelector('.telematics-title');
            const telePill = document.querySelector('.telematics-status-pill');
            const teleMetrics = document.querySelector('.telematics-metrics-block');
            const waBtn = document.querySelector('.floating-wa-btn');

            const getRect = el => el ? el.getBoundingClientRect() : null;
            const bR = getRect(badge);
            const hR = getRect(h1Title);
            const lR = getRect(lead);
            const btR = getRect(btns);
            const pR = getRect(photoWrap);
            const cR = getRect(card);
            const topbarR = getRect(topbar);
            const headerR = getRect(header);
            const heroR = getRect(hero);
            const loginR = getRect(btnLogin);
            const regR = getRect(btnRegister);
            const waR = getRect(waBtn);
            const chipRowR = getRect(brandChipRow);

            // Jarak Masuk - Daftar
            const masukDaftarDistance = (loginR && regR) ? Math.round(regR.left - loginR.right) : null;

            // Jarak atas foto vs badge
            const photoVsBadge = (pR && bR) ? Math.abs(Math.round(pR.top - bR.top)) : null;

            // Bawah tombol CTA
            const ctaBottom = btR ? Math.round(btR.bottom) : null;

            // Overlap kartu ke foto
            const overlapPx = (pR && cR) ? Math.max(0, Math.round(pR.bottom - cR.top)) : 0;
            const overlapPct = pR ? ((overlapPx / pR.height) * 100).toFixed(2) : 0;

            // Bawah kartu dan bawah chip
            const cardBottom = cR ? Math.round(cR.bottom) : null;
            const chipBottom = chipRowR ? Math.round(chipRowR.bottom) : null;

            // Jarak kartu ke tombol WhatsApp
            let waCardDistance = null;
            if (cR && waR) {
                // Minimum distance between card bounding box and WhatsApp button
                const dx = Math.max(0, waR.left - cR.right, cR.left - waR.right);
                const dy = Math.max(0, waR.top - cR.bottom, cR.top - waR.bottom);
                waCardDistance = Math.round(Math.hypot(dx, dy));
            }

            // Hitung baris chip merek
            let chipRowTops = new Set();
            brandChips.forEach(c => {
                const r = c.getBoundingClientRect();
                chipRowTops.add(Math.round(r.top));
            });
            const chipLinesCount = chipRowTops.size;

            return {
                topbarHeight: topbarR ? Math.round(topbarR.height) : null,
                headerHeight: headerR ? Math.round(headerR.height) : null,
                masukDaftarDistance,
                photoVsBadge,
                photoHeight: pR ? Math.round(pR.height) : null,
                photoWidth: pR ? Math.round(pR.width) : null,
                ctaBottom,
                cardHeight: cR ? Math.round(cR.height) : null,
                cardBottom,
                cardOverlapPx: overlapPx,
                cardOverlapPct: parseFloat(overlapPct),
                chipLinesCount,
                chipBottom,
                waCardDistance,
                h1Text: h1Title ? h1Title.innerText.replace(/\n/g, ' ') : null,
                h1FontSize: h1Title ? window.getComputedStyle(h1Title).fontSize : null,
                hasHScroll: document.documentElement.scrollWidth > window.innerWidth
            };
        });

        const h1Lines1366 = await getLineCount(page, '.hero-title .elementor-heading-title');
        data.h1Lines = h1Lines1366;

        console.log('--- Hasil Pengukuran Desktop 1366x600 ---');
        console.table(data);

        // Assertions Desktop 1366x600
        if (data.ctaBottom > 460) {
            console.error(`FAIL: Bawah CTA (${data.ctaBottom}px) melebihi batas 460px!`);
        } else {
            console.log(`PASS: Bawah CTA = ${data.ctaBottom}px (Target <= 460px)`);
        }

        if (data.cardOverlapPct > 6.0) {
            console.error(`FAIL: Overlap kartu (${data.cardOverlapPct}%) melebihi 6%!`);
        } else {
            console.log(`PASS: Overlap kartu = ${data.cardOverlapPct}% (Target <= 6%)`);
        }

        if (data.cardBottom >= 600) {
            console.error(`FAIL: Bawah kartu (${data.cardBottom}px) terpotong lipatan 600px!`);
        } else {
            console.log(`PASS: Bawah kartu = ${data.cardBottom}px (Muat layar pertama < 600px)`);
        }

        if (data.chipBottom >= 600) {
            console.error(`FAIL: Bawah chip (${data.chipBottom}px) terpotong lipatan 600px!`);
        } else {
            console.log(`PASS: Bawah chip = ${data.chipBottom}px (Muat layar pertama < 600px)`);
        }

        if (data.h1Lines > 2) {
            console.error(`FAIL: H1 memiliki ${data.h1Lines} baris (Maksimal 2 baris)!`);
        } else {
            console.log(`PASS: H1 memiliki ${data.h1Lines} baris di 1366px`);
        }

        if (data.masukDaftarDistance > 12) {
            console.error(`FAIL: Jarak Masuk-Daftar (${data.masukDaftarDistance}px) > 12px!`);
        } else {
            console.log(`PASS: Jarak Masuk-Daftar = ${data.masukDaftarDistance}px (Target <= 12px)`);
        }

        if (data.waCardDistance !== null && data.waCardDistance < 16) {
            console.error(`FAIL: Jarak kartu ke WA (${data.waCardDistance}px) < 16px!`);
        } else {
            console.log(`PASS: Jarak kartu ke WA = ${data.waCardDistance}px (Target >= 16px)`);
        }

        if (data.photoVsBadge > 8) {
            console.error(`FAIL: Selisih foto vs badge (${data.photoVsBadge}px) > 8px!`);
        } else {
            console.log(`PASS: Selisih foto vs badge = ${data.photoVsBadge}px (Target <= 8px)`);
        }

        await page.screenshot({ path: path.join(OUT, '1366x600.png'), fullPage: false });
        console.log('Saved: 1366x600.png');

        // Crop Header Nav Actions (Masuk - Daftar)
        const headerEl = await page.$('.stitch-navbar');
        if (headerEl) {
            await headerEl.screenshot({ path: path.join(OUT, 'crop_header_nav_actions.png') });
            console.log('Saved: crop_header_nav_actions.png');
        }

        // Crop Kartu Telematika
        const cardEl = await page.$('.hero-telematics-card');
        if (cardEl) {
            await cardEl.screenshot({ path: path.join(OUT, 'crop_hero_telematics.png') });
            console.log('Saved: crop_hero_telematics.png');
        }

        // Hover Tombol Utama
        const btn = await page.$('.btn-hero-primary .elementor-button');
        if (btn) {
            await btn.hover();
            await page.waitForTimeout(300);
            await page.screenshot({ path: path.join(OUT, 'hover_cta_primary.png'), fullPage: false });
            console.log('Saved: hover_cta_primary.png');
        }

        // Sticky Scrolled Header
        await page.evaluate(() => window.scrollTo(0, 300));
        await page.waitForTimeout(600);
        const stickyH = await page.evaluate(() => {
            const h = document.querySelector('.stitch-navbar');
            return h ? Math.round(h.getBoundingClientRect().height) : null;
        });
        console.log(`Sticky Header Scrolled Height: ${stickyH}px (Target <= 60px)`);
        await page.screenshot({ path: path.join(OUT, 'sticky_scrolled.png'), fullPage: false });
        console.log('Saved: sticky_scrolled.png');

        await ctx.close();
    }

    // 2. Desktop 1366x768
    {
        const ctx = await browser.newContext({ viewport: { width: 1366, height: 768 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(OUT, '1366x768.png'), fullPage: false });
        console.log('Saved: 1366x768.png');
        await ctx.close();
    }

    // 3. Desktop 1440x900
    {
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        const h1Lines1440 = await getLineCount(page, '.hero-title .elementor-heading-title');
        console.log(`1440x900 H1 Lines: ${h1Lines1440} (Target <= 2)`);
        await page.screenshot({ path: path.join(OUT, '1440x900.png'), fullPage: false });
        console.log('Saved: 1440x900.png');
        await ctx.close();
    }

    // 4. Desktop 1920x1080
    {
        const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        const h1Lines1920 = await getLineCount(page, '.hero-title .elementor-heading-title');
        console.log(`1920x1080 H1 Lines: ${h1Lines1920} (Target <= 2)`);
        await page.screenshot({ path: path.join(OUT, '1920x1080.png'), fullPage: false });
        console.log('Saved: 1920x1080.png');
        await ctx.close();
    }

    // 5. Desktop 1024x768
    {
        const ctx = await browser.newContext({ viewport: { width: 1024, height: 768 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        const h1Lines1024 = await getLineCount(page, '.hero-title .elementor-heading-title');
        console.log(`1024x768 H1 Lines: ${h1Lines1024} (Target <= 2)`);
        await page.screenshot({ path: path.join(OUT, '1024x768.png'), fullPage: false });
        console.log('Saved: 1024x768.png');
        await ctx.close();
    }

    // 6. Tablet 768x1024
    {
        const ctx = await browser.newContext({ viewport: { width: 768, height: 1024 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        const h1Lines768 = await getLineCount(page, '.hero-title .elementor-heading-title');
        console.log(`768x1024 H1 Lines: ${h1Lines768} (Target <= 2)`);
        await page.screenshot({ path: path.join(OUT, '768x1024.png'), fullPage: false });
        console.log('Saved: 768x1024.png');
        await ctx.close();
    }

    // 7. Mobile 390x844
    {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        await page.goto('http://localhost:5000/', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
        const mobData = await page.evaluate(() => {
            const topbar = document.querySelector('.stitch-topbar');
            const header = document.querySelector('.stitch-navbar');
            const hScroll = document.documentElement.scrollWidth > window.innerWidth;
            return {
                topbarHeight: topbar ? Math.round(topbar.getBoundingClientRect().height) : null,
                headerHeight: header ? Math.round(header.getBoundingClientRect().height) : null,
                hasHScroll: hScroll
            };
        });
        const h1Lines390 = await getLineCount(page, '.hero-title .elementor-heading-title');
        console.log(`390x844 H1 Lines: ${h1Lines390} (Target <= 3)`);
        console.log('Mobile 390x844 data:', mobData);
        await page.screenshot({ path: path.join(OUT, '390x844.png'), fullPage: false });
        console.log('Saved: 390x844.png');
        await ctx.close();
    }

    // 8. Horizontal Overflow Check across 320 to 1920
    {
        const viewports = [320, 360, 390, 414, 768, 1024, 1280, 1366, 1440, 1920];
        let overflowFail = 0;
        for (const w of viewports) {
            const ctx = await browser.newContext({ viewport: { width: w, height: 800 } });
            const page = await ctx.newPage();
            await page.goto('http://localhost:5000/', { waitUntil: 'domcontentloaded' });
            const hasHScroll = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
            if (hasHScroll) {
                console.error(`FAIL: Horizontal scroll detected on width ${w}px!`);
                overflowFail++;
            }
            await ctx.close();
        }
        if (overflowFail === 0) {
            console.log('PASS: 0 horizontal overflow across 320px - 1920px');
        }
    }

    await browser.close();
    console.log('\n=== VERIFIKASI RONDE 19c SELESAI ===');
}

verifyRonde19c().catch(err => {
    console.error('Error during verification:', err);
    process.exit(1);
});
