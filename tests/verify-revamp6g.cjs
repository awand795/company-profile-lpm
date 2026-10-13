/**
 * tests/verify-revamp6g.cjs
 * Verifikasi Mendalam RONDE 7:
 * - Hero desktop (tidak ada overlap foto & teks di 1024, 1280, 1366, 1440, 1920)
 * - Hero mobile 390 (rata tengah)
 * - Tombol melayang (back-to-top 48x48 + WA 48x48 tersusun vertikal, gap 12px)
 * - Admin bar WordPress utuh saat login (1440 & 390) tanpa bentrok navbar
 * - Elementor Editor post 59 termuat sehat (tanpa spinner abadi)
 */

const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:5000/';
const OUT_DIR = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp6g');

if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
}

(async () => {
    console.log('=== MEMULAI VERIFIKASI RONDE 7 ===\n');
    const browser = await chromium.launch();

    // -------------------------------------------------------------
    // 1. HERO DESKTOP: UJI BEBAS OVERLAP DI 1024, 1280, 1366, 1440, 1920
    // -------------------------------------------------------------
    console.log('--- 1. Uji Bebas Overlap Hero Desktop (1024, 1280, 1366, 1440, 1920) ---');
    const viewports = [
        { w: 1024, h: 768, name: 'hero-1024.png' },
        { w: 1280, h: 800, name: 'hero-1280.png' },
        { w: 1366, h: 640, name: 'hero-1366.png' },
        { w: 1440, h: 900, name: 'hero-1440.png' },
        { w: 1920, h: 1080, name: 'hero-1920.png' }
    ];

    for (const vp of viewports) {
        const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
        const p = await ctx.newPage();
        await p.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
        await p.waitForTimeout(1000);

        const heroMetrics = await p.evaluate(() => {
            const leftCol = document.querySelector('.hero-left-col');
            const rightCol = document.querySelector('.hero-right-col');
            const img = document.querySelector('.hero-truck-img img');
            const h1Tagline = document.querySelector('.hero-brand-tagline');
            const pillDerek = document.querySelector('.hero-card-live');

            const leftRect = leftCol ? leftCol.getBoundingClientRect() : null;
            const rightRect = rightCol ? rightCol.getBoundingClientRect() : null;
            const imgRect = img ? img.getBoundingClientRect() : null;
            const h1Rect = h1Tagline ? h1Tagline.getBoundingClientRect() : null;
            const derekRect = pillDerek ? pillDerek.getBoundingClientRect() : null;

            // Jarak horizontal antara tepi kanan teks dan tepi kiri foto
            let gap = null;
            if (h1Rect && imgRect) {
                gap = Math.round(imgRect.left - h1Rect.right);
            }

            return {
                h1Width: h1Rect ? Math.round(h1Rect.width) : null,
                imgWidth: imgRect ? Math.round(imgRect.width) : null,
                imgHeight: imgRect ? Math.round(imgRect.height) : null,
                gapTextToImg: gap,
                derekBottom: derekRect ? Math.round(derekRect.bottom) : null
            };
        });

        console.log(`Viewport ${vp.w}x${vp.h}:`, JSON.stringify(heroMetrics));
        await p.screenshot({ path: path.join(OUT_DIR, vp.name) });
        await ctx.close();
    }

    // -------------------------------------------------------------
    // 2. HERO MOBILE 390x844 (RATA TENGAH)
    // -------------------------------------------------------------
    console.log('\n--- 2. Hero Mobile 390x844 (Rata Tengah) ---');
    const ctx390 = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const p390 = await ctx390.newPage();
    await p390.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    await p390.waitForTimeout(1000);

    const mobHeroData = await p390.evaluate(() => {
        const leftCol = document.querySelector('.hero-left-col');
        const h1 = document.querySelector('.hero-title');
        const lead = document.querySelector('.hero-lead p');
        const btns = document.querySelector('.hero-btns-inner');
        const trustRow = document.querySelector('.hero-trust-row');
        const img = document.querySelector('.hero-truck-img img');
        const navPill = document.querySelector('.navbar-pill');

        const csLeft = leftCol ? window.getComputedStyle(leftCol) : {};
        const csH1 = h1 ? window.getComputedStyle(h1) : {};
        const csLead = lead ? window.getComputedStyle(lead) : {};
        const csBtns = btns ? window.getComputedStyle(btns) : {};
        const csTrust = trustRow ? window.getComputedStyle(trustRow) : {};

        return {
            leftAlign: csLeft.textAlign,
            leftAlignItems: csLeft.alignItems,
            leadAlign: csLead.textAlign,
            btnsDir: csBtns.flexDirection,
            btnsAlign: csBtns.alignItems,
            trustDir: csTrust.flexDirection,
            trustJustify: csTrust.justifyContent,
            imgH: img ? Math.round(img.getBoundingClientRect().height) : null,
            navPillH: navPill ? Math.round(navPill.getBoundingClientRect().height) : null
        };
    });
    console.log('Mobile Hero Data:', JSON.stringify(mobHeroData, null, 2));
    await p390.screenshot({ path: path.join(OUT_DIR, 'hero-mobile-390.png') });

    // Cek Tombol Melayang di Mobile
    await p390.evaluate(() => window.scrollTo(0, 600));
    await p390.waitForTimeout(500);
    const floatMob = await p390.evaluate(() => {
        const btt = document.querySelector('.mt-back-top');
        const wa = document.querySelector('.floating-wa-btn');
        const bttRect = btt ? btt.getBoundingClientRect() : null;
        const waRect = wa ? wa.getBoundingClientRect() : null;
        return {
            bttW: bttRect ? Math.round(bttRect.width) : null,
            bttH: bttRect ? Math.round(bttRect.height) : null,
            waW: waRect ? Math.round(waRect.width) : null,
            waH: waRect ? Math.round(waRect.height) : null,
            gapVertical: (bttRect && waRect) ? Math.round(waRect.top - bttRect.bottom) : null
        };
    });
    console.log('Mobile Floating Buttons:', JSON.stringify(floatMob, null, 2));
    await p390.screenshot({ path: path.join(OUT_DIR, 'floating-buttons-mobile.png') });
    await ctx390.close();

    // -------------------------------------------------------------
    // 3. TOMBOL MELAYANG DESKTOP 1440x900
    // -------------------------------------------------------------
    console.log('\n--- 3. Tombol Melayang Desktop 1440x900 ---');
    const ctx1440 = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p1440 = await ctx1440.newPage();
    await p1440.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
    await p1440.evaluate(() => window.scrollTo(0, 800));
    await p1440.waitForTimeout(500);

    const floatDesk = await p1440.evaluate(() => {
        const btt = document.querySelector('.mt-back-top');
        const wa = document.querySelector('.floating-wa-btn');
        const bttRect = btt ? btt.getBoundingClientRect() : null;
        const waRect = wa ? wa.getBoundingClientRect() : null;
        const bttCS = btt ? window.getComputedStyle(btt) : {};
        return {
            bttW: bttRect ? Math.round(bttRect.width) : null,
            bttH: bttRect ? Math.round(bttRect.height) : null,
            bttDisplay: bttCS.display,
            bttRadius: bttCS.borderRadius,
            waW: waRect ? Math.round(waRect.width) : null,
            waH: waRect ? Math.round(waRect.height) : null,
            gapVertical: (bttRect && waRect) ? Math.round(waRect.top - bttRect.bottom) : null
        };
    });
    console.log('Desktop Floating Buttons:', JSON.stringify(floatDesk, null, 2));
    await p1440.screenshot({ path: path.join(OUT_DIR, 'floating-buttons-desktop.png') });
    await ctx1440.close();

    // -------------------------------------------------------------
    // 4. ADMIN BAR SAAT LOGIN (1440 & 390)
    // -------------------------------------------------------------
    console.log('\n--- 4. Pengujian Admin Bar Saat Login ---');
    const testAdmin = 'tester_audit_7g';
    const testPass = 'AuditPass2026!#' + Math.random().toString(36).substring(7);

    try {
        execSync(`docker exec lpm-wp-app wp user create ${testAdmin} ${testAdmin}@example.com --role=administrator --user_pass="${testPass}" --allow-root`, { stdio: 'pipe' });

        // Login via browser context
        const authCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const pAuth = await authCtx.newPage();
        await pAuth.goto(BASE_URL + 'wp-login.php', { waitUntil: 'domcontentloaded' });
        await pAuth.fill('#user_login', testAdmin);
        await pAuth.fill('#user_pass', testPass);
        await Promise.all([
            pAuth.waitForNavigation({ waitUntil: 'domcontentloaded' }),
            pAuth.click('#wp-submit')
        ]);

        // Kunjungi homepage sebagai user login di 1440
        await pAuth.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
        await pAuth.waitForTimeout(1000);

        const adminBarDesk = await pAuth.evaluate(() => {
            const bar = document.querySelector('#wpadminbar');
            const nav = document.querySelector('.navbar.sticky-top');
            const barRect = bar ? bar.getBoundingClientRect() : null;
            const navRect = nav ? nav.getBoundingClientRect() : null;
            const dashicons = document.querySelector('#wpadminbar .dashicons, #wpadminbar .ab-icon');
            return {
                barExists: !!bar,
                barHeight: barRect ? Math.round(barRect.height) : null,
                navTop: navRect ? Math.round(navRect.top) : null,
                gapBarToNav: (barRect && navRect) ? Math.round(navRect.top - barRect.bottom) : null,
                hasIcons: !!dashicons
            };
        });
        console.log('Admin Bar Desktop (1440):', JSON.stringify(adminBarDesk, null, 2));
        await pAuth.screenshot({ path: path.join(OUT_DIR, 'beranda-loggedin-1440.png') });

        // Ubah viewport ke mobile 390 saat login
        await pAuth.setViewportSize({ width: 390, height: 844 });
        await pAuth.waitForTimeout(500);

        const adminBarMob = await pAuth.evaluate(() => {
            const bar = document.querySelector('#wpadminbar');
            const nav = document.querySelector('.navbar.sticky-top');
            const barRect = bar ? bar.getBoundingClientRect() : null;
            const navRect = nav ? nav.getBoundingClientRect() : null;
            return {
                barExists: !!bar,
                barHeight: barRect ? Math.round(barRect.height) : null,
                navTop: navRect ? Math.round(navRect.top) : null,
                gapBarToNav: (barRect && navRect) ? Math.round(navRect.top - barRect.bottom) : null
            };
        });
        console.log('Admin Bar Mobile (390):', JSON.stringify(adminBarMob, null, 2));
        await pAuth.screenshot({ path: path.join(OUT_DIR, 'beranda-loggedin-390.png') });

        // -------------------------------------------------------------
        // 5. PENGUJIAN EDITOR ELEMENTOR (POST 59)
        // -------------------------------------------------------------
        console.log('\n--- 5. Pengujian Editor Elementor Post 59 ---');
        await pAuth.setViewportSize({ width: 1440, height: 900 });
        const editorUrl = BASE_URL + 'wp-admin/post.php?post=59&action=elementor';
        
        const consoleErrors = [];
        pAuth.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
            }
        });

        await pAuth.goto(editorUrl, { waitUntil: 'domcontentloaded' });
        // Tunggu panel Elementor aktif
        await pAuth.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 30000 });
        await pAuth.waitForTimeout(3000);

        const editorStatus = await pAuth.evaluate(() => {
            const panel = document.querySelector('#elementor-panel');
            const previewIframe = document.querySelector('#elementor-preview-iframe');
            const loader = document.querySelector('.elementor-loader, .elementor-loading');
            let isLoaderVisible = false;
            if (loader) {
                const cs = window.getComputedStyle(loader);
                isLoaderVisible = cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0';
            }
            return {
                panelReady: !!panel,
                iframeReady: !!previewIframe,
                loaderVisible: isLoaderVisible
            };
        });
        console.log('Editor Elementor Status:', JSON.stringify(editorStatus, null, 2));
        console.log('Console Errors count:', consoleErrors.length);
        if (consoleErrors.length > 0) {
            console.log('Console Error samples:', consoleErrors.slice(0, 3));
        }

        await pAuth.screenshot({ path: path.join(OUT_DIR, 'elementor-editor-59.png') });
        await authCtx.close();
    } finally {
        try {
            execSync(`docker exec lpm-wp-app wp user delete ${testAdmin} --yes --allow-root`, { stdio: 'pipe' });
            console.log('User audit temporer berhasil dibersihkan.');
        } catch (e) {}
    }

    await browser.close();
    console.log('\n=== VERIFIKASI SELESAI ===');
})();
