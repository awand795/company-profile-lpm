/**
 * tests/verify-revamp6i.cjs
 * RONDE 9 Verifikasi:
 * 1. Jarak dasar pill navbar -> eyebrow (target 64±4px desktop)
 * 2. Jarak dasar pill navbar -> tepi atas foto (selisih vs eyebrow <= 8px)
 * 3. Bawah baris keunggulan di 1366x640 (target <= 620px)
 * 4. Tiga angka statistik setelah animasi: "15", "120+", "2.500"
 * 5. Screenshot viewport 1366, 1024, 768, 390
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:5000/';
const OUT_DIR = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp6i');

if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
}

(async () => {
    console.log('=== MEMULAI VERIFIKASI RONDE 9 (REVAMP6i) ===\n');

    const browser = await chromium.launch({ headless: true });

    // -------------------------------------------------------------
    // 1. DESKTOP 1366x640
    // -------------------------------------------------------------
    console.log('--- 1. Desktop 1366x640 ---');
    const ctx1366 = await browser.newContext({ viewport: { width: 1366, height: 640 } });
    const p1366 = await ctx1366.newPage();
    await p1366.goto(BASE_URL, { waitUntil: 'networkidle' });
    await p1366.waitForTimeout(1000);

    const m1366 = await p1366.evaluate(() => {
        const pill = document.querySelector('.navbar-pill');
        const eyebrow = document.querySelector('.hero-left-col .hero-brand-pill');
        const img = document.querySelector('.hero-right-col .hero-truck-img img');
        const chipSLA = document.querySelector('.hero-right-col .hero-card-sla');
        const trust = document.querySelector('.hero-left-col .hero-trust-row');

        const pillRect = pill ? pill.getBoundingClientRect() : null;
        const eyeRect = eyebrow ? eyebrow.getBoundingClientRect() : null;
        const imgRect = img ? img.getBoundingClientRect() : null;
        const chipRect = chipSLA ? chipSLA.getBoundingClientRect() : null;
        const trustRect = trust ? trust.getBoundingClientRect() : null;

        const gapPillToEyebrow = (pillRect && eyeRect) ? Math.round(eyeRect.top - pillRect.bottom) : null;
        const gapPillToImgTop = (pillRect && imgRect) ? Math.round(imgRect.top - pillRect.bottom) : null;
        const gapPillToChip = (pillRect && chipRect) ? Math.round(chipRect.top - pillRect.bottom) : null;
        const diffEyeVsImg = (gapPillToEyebrow !== null && gapPillToImgTop !== null) ? Math.abs(gapPillToEyebrow - gapPillToImgTop) : null;

        return {
            gapPillToEyebrow,
            gapPillToImgTop,
            diffEyeVsImg,
            gapPillToChip,
            trustBottom: trustRect ? Math.round(trustRect.bottom) : null
        };
    });

    console.log('Metrik 1366x640:', JSON.stringify(m1366, null, 2));
    await p1366.screenshot({ path: path.join(OUT_DIR, 'hero-desktop-1366x640.png') });

    // Uji angka statistik di 1366 (scroll ke strip & tunggu animasi counter >= 3 detik)
    console.log('\nMenguji animasi counter statistik...');
    await p1366.evaluate(() => {
        const strip = document.querySelector('.hero-stats-strip');
        if (strip) strip.scrollIntoView();
    });
    await p1366.waitForTimeout(3500);

    const statsNumbers = await p1366.evaluate(() => {
        const items = Array.from(document.querySelectorAll('.hero-stats-strip .hero-counter-item'));
        return items.map(item => {
            const prefix = item.querySelector('.elementor-counter-number-prefix')?.textContent.trim() || '';
            const num = item.querySelector('.elementor-counter-number')?.textContent.trim() || '';
            const suffix = item.querySelector('.elementor-counter-number-suffix')?.textContent.trim() || '';
            const title = item.querySelector('.elementor-counter-title')?.textContent.trim() || '';
            return {
                fullText: prefix + num + suffix,
                number: num,
                title
            };
        });
    });

    console.log('Hasil Counter Statistik:', JSON.stringify(statsNumbers, null, 2));
    await ctx1366.close();

    // -------------------------------------------------------------
    // 2. DESKTOP 1024x768
    // -------------------------------------------------------------
    console.log('\n--- 2. Viewport 1024x768 ---');
    const ctx1024 = await browser.newContext({ viewport: { width: 1024, height: 768 } });
    const p1024 = await ctx1024.newPage();
    await p1024.goto(BASE_URL, { waitUntil: 'networkidle' });
    await p1024.waitForTimeout(1000);

    const m1024 = await p1024.evaluate(() => {
        const pill = document.querySelector('.navbar-pill');
        const eyebrow = document.querySelector('.hero-left-col .hero-brand-pill');
        const img = document.querySelector('.hero-right-col .hero-truck-img img');
        const pillRect = pill ? pill.getBoundingClientRect() : null;
        const eyeRect = eyebrow ? eyebrow.getBoundingClientRect() : null;
        const imgRect = img ? img.getBoundingClientRect() : null;
        return {
            gapPillToEyebrow: (pillRect && eyeRect) ? Math.round(eyeRect.top - pillRect.bottom) : null,
            gapPillToImgTop: (pillRect && imgRect) ? Math.round(imgRect.top - pillRect.bottom) : null
        };
    });
    console.log('Metrik 1024x768:', JSON.stringify(m1024, null, 2));
    await p1024.screenshot({ path: path.join(OUT_DIR, 'hero-1024x768.png') });
    await ctx1024.close();

    // -------------------------------------------------------------
    // 3. TABLET 768x1024
    // -------------------------------------------------------------
    console.log('\n--- 3. Tablet 768x1024 ---');
    const ctx768 = await browser.newContext({ viewport: { width: 768, height: 1024 } });
    const p768 = await ctx768.newPage();
    await p768.goto(BASE_URL, { waitUntil: 'networkidle' });
    await p768.waitForTimeout(1000);

    const m768 = await p768.evaluate(() => {
        const pill = document.querySelector('.navbar-pill');
        const eyebrow = document.querySelector('.hero-left-col .hero-brand-pill');
        const pillRect = pill ? pill.getBoundingClientRect() : null;
        const eyeRect = eyebrow ? eyebrow.getBoundingClientRect() : null;
        return {
            gapPillToEyebrow: (pillRect && eyeRect) ? Math.round(eyeRect.top - pillRect.bottom) : null
        };
    });
    console.log('Metrik 768x1024:', JSON.stringify(m768, null, 2));
    await p768.screenshot({ path: path.join(OUT_DIR, 'hero-tablet-768x1024.png') });
    await ctx768.close();

    // -------------------------------------------------------------
    // 4. MOBILE 390x844
    // -------------------------------------------------------------
    console.log('\n--- 4. Mobile 390x844 ---');
    const ctx390 = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const p390 = await ctx390.newPage();
    await p390.goto(BASE_URL, { waitUntil: 'networkidle' });
    await p390.waitForTimeout(1000);

    const m390 = await p390.evaluate(() => {
        const pill = document.querySelector('.navbar-pill');
        const eyebrow = document.querySelector('.hero-left-col .hero-brand-pill');
        const pillRect = pill ? pill.getBoundingClientRect() : null;
        const eyeRect = eyebrow ? eyebrow.getBoundingClientRect() : null;
        return {
            gapPillToEyebrow: (pillRect && eyeRect) ? Math.round(eyeRect.top - pillRect.bottom) : null
        };
    });
    console.log('Metrik 390x844:', JSON.stringify(m390, null, 2));
    await p390.screenshot({ path: path.join(OUT_DIR, 'hero-mobile-390x844.png') });
    await ctx390.close();

    await browser.close();
    console.log('\n=== VERIFIKASI RONDE 9 SELESAI ===');
})();
