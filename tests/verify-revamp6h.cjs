/**
 * tests/verify-revamp6h.cjs
 * RONDE 8 Verifikasi Lengkap:
 * 1. Pengukuran jarak vertikal antar baris H1 (<= 8px)
 * 2. Pengukuran jarak vertikal tumpukan hero (eyebrow, H1, lead, btns, trust row)
 * 3. Hero ATF 1366x640 & mobile center 390x844
 * 4. Pengujian editor Elementor & screenshot
 * 5. Pengujian admin bar saat login (tidak ada shortcut "Edit Landing Page" yang mengganggu di beranda)
 */

const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:5000/';
const OUT_DIR = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp6h');

if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
}

(async () => {
    console.log('=== MEMULAI VERIFIKASI RONDE 8 (REVAMP6h) ===\n');

    const browser = await chromium.launch({ headless: true });

    // -----------------------------------------------------------------
    // 1. PENGUKURAN HERO DESKTOP (1366x640)
    // -----------------------------------------------------------------
    console.log('--- 1. Pengukuran Hero Desktop (1366x640) ---');
    const ctx1366 = await browser.newContext({ viewport: { width: 1366, height: 640 } });
    const p1366 = await ctx1366.newPage();
    await p1366.goto(BASE_URL, { waitUntil: 'networkidle' });
    await p1366.waitForTimeout(1000);

    const heroMetrics = await p1366.evaluate(() => {
        const eyebrow = document.querySelector('.hero-left-col .hero-brand-pill');
        const h1 = document.querySelector('.hero-left-col .hero-title');
        const h1Title = h1 ? h1.querySelector('.elementor-heading-title') : null;
        const h1Sub = h1 ? h1.querySelector('.hero-h1-sub') : null;
        const lead = document.querySelector('.hero-left-col .hero-lead');
        const btns = document.querySelector('.hero-left-col .hero-btns-inner');
        const trust = document.querySelector('.hero-left-col .hero-trust-row');
        const derekChip = document.querySelector('.hero-right-col .hero-card-live');

        // Bounding rect baris 1 H1 (teks Master Truck) vs baris 2 (span .hero-h1-sub)
        let h1Line1Bottom = null;
        if (h1Title) {
            const range = document.createRange();
            const firstTextNode = h1Title.firstChild;
            if (firstTextNode) {
                range.selectNodeContents(firstTextNode);
                const rect = range.getBoundingClientRect();
                h1Line1Bottom = Math.round(rect.bottom);
            }
        }
        const h1SubRect = h1Sub ? h1Sub.getBoundingClientRect() : null;
        const h1LineGap = (h1Line1Bottom !== null && h1SubRect) ? Math.round(h1SubRect.top - h1Line1Bottom) : null;

        const eyeRect = eyebrow ? eyebrow.getBoundingClientRect() : null;
        const h1Rect = h1 ? h1.getBoundingClientRect() : null;
        const leadRect = lead ? lead.getBoundingClientRect() : null;
        const btnsRect = btns ? btns.getBoundingClientRect() : null;
        const trustRect = trust ? trust.getBoundingClientRect() : null;
        const derekRect = derekChip ? derekChip.getBoundingClientRect() : null;

        return {
            h1LineGap, // Jarak vertikal baris 1 ke baris 2 H1 (<= 8px)
            gapEyebrowToH1: (eyeRect && h1Rect) ? Math.round(h1Rect.top - eyeRect.bottom) : null,
            gapH1ToLead: (h1Rect && leadRect) ? Math.round(leadRect.top - h1Rect.bottom) : null,
            gapLeadToBtns: (leadRect && btnsRect) ? Math.round(btnsRect.top - leadRect.bottom) : null,
            gapBtnsToTrust: (btnsRect && trustRect) ? Math.round(trustRect.top - btnsRect.bottom) : null,
            trustBottom: trustRect ? Math.round(trustRect.bottom) : null,
            derekBottom: derekRect ? Math.round(derekRect.bottom) : null
        };
    });

    console.log('Hero Metrics (1366x640):', JSON.stringify(heroMetrics, null, 2));

    await p1366.screenshot({ path: path.join(OUT_DIR, 'hero-desktop-1366x640.png') });
    await ctx1366.close();

    // -----------------------------------------------------------------
    // 2. HERO MOBILE (390x844) RATA TENGAH
    // -----------------------------------------------------------------
    console.log('\n--- 2. Hero Mobile (390x844) ---');
    const ctx390 = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const p390 = await ctx390.newPage();
    await p390.goto(BASE_URL, { waitUntil: 'networkidle' });
    await p390.waitForTimeout(1000);

    const mobMetrics = await p390.evaluate(() => {
        const leftCol = document.querySelector('.hero-left-col');
        const csLeft = leftCol ? getComputedStyle(leftCol) : {};
        const btns = document.querySelector('.hero-btns-inner');
        const csBtns = btns ? getComputedStyle(btns) : {};
        const trust = document.querySelector('.hero-trust-row');
        const csTrust = trust ? getComputedStyle(trust) : {};

        return {
            leftAlign: csLeft.textAlign,
            leftAlignItems: csLeft.alignItems,
            btnsDir: csBtns.flexDirection,
            btnsAlign: csBtns.alignItems,
            trustJustify: csTrust.justifyContent
        };
    });

    console.log('Mobile Hero Alignment:', JSON.stringify(mobMetrics, null, 2));
    await p390.screenshot({ path: path.join(OUT_DIR, 'hero-mobile-390.png') });
    await ctx390.close();

    // -----------------------------------------------------------------
    // 3. ADMIN BAR & SHORTCUT EDIT LANDING PAGE (SAAT LOGIN)
    // -----------------------------------------------------------------
    console.log('\n--- 3. Verifikasi Admin Bar Saat Login ---');
    const testAdmin = 'tester_audit_8h_' + Math.random().toString(36).substring(7);
    const testPass = 'AuditPass2026!#' + Math.random().toString(36).substring(7);

    try {
        execSync(`docker exec lpm-wp-app wp user create ${testAdmin} ${testAdmin}@example.com --role=administrator --user_pass="${testPass}" --allow-root`, { stdio: 'pipe' });

        const authCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const pAuth = await authCtx.newPage();

        await pAuth.goto(BASE_URL + 'wp-login.php', { waitUntil: 'domcontentloaded' });
        await pAuth.fill('#user_login', testAdmin);
        await pAuth.fill('#user_pass', testPass);
        await Promise.all([
            pAuth.waitForNavigation({ waitUntil: 'domcontentloaded' }),
            pAuth.click('#wp-submit')
        ]);

        // Kunjungi beranda
        await pAuth.goto(BASE_URL, { waitUntil: 'networkidle' });
        await pAuth.waitForTimeout(1000);

        const adminBarCheck = await pAuth.evaluate(() => {
            const bar = document.querySelector('#wpadminbar');
            const editLanding = document.querySelector('#wp-admin-bar-mt_edit_landing');
            const editWithElementor = document.querySelector('#wp-admin-bar-elementor_edit_page');
            return {
                barExists: !!bar,
                hasEditLandingShortcut: !!editLanding,
                hasEditWithElementor: !!editWithElementor
            };
        });

        console.log('Admin Bar Check:', JSON.stringify(adminBarCheck, null, 2));
        await pAuth.screenshot({ path: path.join(OUT_DIR, 'beranda-loggedin-adminbar.png') });

        // -----------------------------------------------------------------
        // 4. EDITOR ELEMENTOR POST 59
        // -----------------------------------------------------------------
        console.log('\n--- 4. Pengujian Editor Elementor Post 59 ---');
        const editorUrl = BASE_URL + 'wp-admin/post.php?post=59&action=elementor';
        await pAuth.goto(editorUrl, { waitUntil: 'domcontentloaded' });
        await pAuth.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 35000 });
        await pAuth.waitForTimeout(6000);

        const editorStatus = await pAuth.evaluate(() => {
            const el = window.elementor;
            const doc = el && el.documents ? el.documents.getCurrent() : null;
            const rev = el && el.config && el.config.document ? el.config.document.revisions : null;
            return {
                docId: doc ? doc.id : null,
                elementsCount: el && el.elements ? el.elements.length : 0,
                currentRevId: rev ? rev.current_id : null
            };
        });

        console.log('Editor Status:', JSON.stringify(editorStatus, null, 2));

        const frame = pAuth.frameLocator('#elementor-preview-iframe');
        const frameBody = await frame.locator('body').innerHTML();

        const hasNavbarPill = frameBody.includes('navbar-pill');
        const hasTrukSehat = frameBody.includes('Truk Sehat');
        const hasTopBarCustom = frameBody.includes('top-bar-custom');
        const hasLoginFleet = frameBody.includes('Login Fleet');

        console.log('Editor Iframe Content:');
        console.log('  - navbar-pill:', hasNavbarPill ? 'PASS' : 'FAIL');
        console.log('  - Truk Sehat:', hasTrukSehat ? 'PASS' : 'FAIL');
        console.log('  - TANPA top-bar-custom:', !hasTopBarCustom ? 'PASS' : 'FAIL');
        console.log('  - TANPA Login Fleet:', !hasLoginFleet ? 'PASS' : 'FAIL');

        await pAuth.screenshot({ path: path.join(OUT_DIR, 'editor-post59.png') });

        await authCtx.close();
    } finally {
        execSync(`docker exec lpm-wp-app wp user delete ${testAdmin} --yes --allow-root`, { stdio: 'pipe' });
    }

    await browser.close();
    console.log('\n=== VERIFIKASI RONDE 8 SELESAI ===');
})();
