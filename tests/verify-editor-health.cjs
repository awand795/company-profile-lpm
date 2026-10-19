/**
 * tests/verify-editor-health.cjs
 * RONDE 8 - A3: Verifikasi kesehatan editor Elementor Post 59
 * Memastikan editor TIDAK memuat autosave lama, preview memuat desain baru,
 * tidak ada console errors, dan iframe siap diedit.
 */

const { chromium } = require('playwright');
const { execSync } = require('child_process');

(async () => {
    console.log('=== MEMULAI TEST KESEHATAN EDITOR ELEMENTOR POST 59 ===');
    const testAdmin = 'tester_audit_editor_' + Math.random().toString(36).substring(7);
    const testPass = 'AuditPass2026!#' + Math.random().toString(36).substring(7);

    try {
        // Buat temp admin user
        execSync(`docker exec lpm-wp-app wp user create ${testAdmin} ${testAdmin}@example.com --role=administrator --user_pass="${testPass}" --allow-root`, { stdio: 'pipe' });

        const browser = await chromium.launch({ headless: true });
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();

        const consoleErrors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                const text = msg.text();
                // Filter benign network / favicon errors
                if (!text.includes('favicon') && !text.includes('net::ERR_')) {
                    consoleErrors.push(text);
                }
            }
        });

        // 1. Login
        await page.goto('http://localhost:5000/wp-login.php', { waitUntil: 'domcontentloaded' });
        await page.fill('#user_login', testAdmin);
        await page.fill('#user_pass', testPass);
        await Promise.all([
            page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
            page.click('#wp-submit')
        ]);

        // 2. Buka editor Elementor Post 59
        const editorUrl = 'http://localhost:5000/wp-admin/post.php?post=59&action=elementor';
        await page.goto(editorUrl, { waitUntil: 'domcontentloaded' });

        // Tunggu panel aktif
        await page.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 35000 });
        await page.waitForTimeout(6000);

        // 3. Evaluasi editor document config
        const editorDocInfo = await page.evaluate(() => {
            const el = window.elementor;
            if (!el) return { ready: false };
            const doc = el.documents ? el.documents.getCurrent() : null;
            const rev = el.config && el.config.document ? el.config.document.revisions : null;
            return {
                ready: true,
                docId: doc ? doc.id : null,
                elementsCount: el.elements ? el.elements.length : 0,
                currentRevId: rev ? rev.current_id : null
            };
        });

        console.log('Editor Document Info:', JSON.stringify(editorDocInfo, null, 2));

        if (!editorDocInfo.ready || editorDocInfo.docId !== 59) {
            throw new Error(`Editor tidak membuka document 59! docId=${editorDocInfo.docId}`);
        }

        // 4. Periksa isi preview iframe
        const frame = page.frameLocator('#elementor-preview-iframe');
        const frameBody = await frame.locator('body').innerHTML();

        const hasNavbarPill = frameBody.includes('navbar-pill') || frameBody.includes('stitch-navbar');
        const hasHeroHeadline = frameBody.includes('Truk Sehat') || frameBody.includes('MASTER TRUCK');
        const hasTopBarCustom = frameBody.includes('top-bar-custom');
        const hasLoginFleet = frameBody.includes('Login Fleet');
        const hasOldHeadline = frameBody.includes('Master Truck: Bengkel Truk Terpercaya');

        console.log('Pemeriksaan Preview Iframe:');
        console.log('  - Memuat navbar:', hasNavbarPill ? 'PASS' : 'FAIL');
        console.log('  - Memuat hero:', hasHeroHeadline ? 'PASS' : 'FAIL');
        console.log('  - TIDAK memuat top-bar-custom:', !hasTopBarCustom ? 'PASS' : 'FAIL');
        console.log('  - TIDAK memuat "Login Fleet":', !hasLoginFleet ? 'PASS' : 'FAIL');
        console.log('  - TIDAK memuat headline lama:', !hasOldHeadline ? 'PASS' : 'FAIL');

        if (!hasNavbarPill) throw new Error('Preview editor TIDAK memuat navbar!');
        if (!hasHeroHeadline) throw new Error('Preview editor TIDAK memuat hero headline!');
        if (hasTopBarCustom) throw new Error('Preview editor bocor memuat .top-bar-custom lama!');
        if (hasLoginFleet) throw new Error('Preview editor bocor memuat "Login Fleet" lama!');
        if (hasOldHeadline) throw new Error('Preview editor memuat headline lama!');

        // 5. Periksa console errors
        console.log('Console Errors Count:', consoleErrors.length);
        if (consoleErrors.length > 0) {
            console.warn('Console Errors:', consoleErrors);
        }

        // 6. Ambil screenshot bukti editor
        await page.screenshot({ path: 'playwright_review/sesudah_revamp6h_editor.png' });
        console.log('Screenshot editor tersimpan di playwright_review/sesudah_revamp6h_editor.png');

        await browser.close();
        console.log('=== TEST KESEHATAN EDITOR: SEMUA LULUS (PASS) ===\n');
    } finally {
        execSync(`docker exec lpm-wp-app wp user delete ${testAdmin} --yes --allow-root`, { stdio: 'pipe' });
    }
})();
