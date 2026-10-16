const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp9');
fs.mkdirSync(OUT, { recursive: true });

(async () => {
    console.log('=== VERIFIKASI EDITOR ELEMENTOR PAGE 59 & HALAMAN LOGIN/ADMIN ===');
    const testAdmin = 'tester_ronde17_' + Math.random().toString(36).substring(7);
    const testPass = 'AdminPassRonde17!#' + Math.random().toString(36).substring(7);

    try {
        // Buat temp admin user
        execSync(`docker exec lpm-wp-app wp user create ${testAdmin} ${testAdmin}@example.com --role=administrator --user_pass="${testPass}" --allow-root`, { stdio: 'pipe' });

        const browser = await chromium.launch({ headless: true });
        const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
        const page = await ctx.newPage();

        // 1. Verifikasi Halaman Login
        console.log('1. Memeriksa halaman login...');
        await page.goto('http://localhost:5000/wp-login.php', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(1000);
        const loginFormExists = await page.$('#loginform') !== null;
        console.log('  Login form exists:', loginFormExists ? 'PASS' : 'FAIL');
        if (!loginFormExists) throw new Error('Halaman login rusak!');

        // Login
        await page.fill('#user_login', testAdmin);
        await page.fill('#user_pass', testPass);
        await Promise.all([
            page.waitForNavigation({ waitUntil: 'domcontentloaded' }),
            page.click('#wp-submit')
        ]);

        // 2. Verifikasi Dashboard Admin
        console.log('2. Memeriksa admin dashboard...');
        const inDashboard = page.url().includes('wp-admin');
        const adminBarExists = await page.$('#wpadminbar') !== null;
        console.log('  Admin bar exists:', adminBarExists ? 'PASS' : 'FAIL');
        if (!inDashboard || !adminBarExists) throw new Error('Dashboard admin rusak!');

        // 3. Verifikasi Editor Elementor Post 59
        console.log('3. Membuka Editor Elementor Post 59...');
        const editorUrl = 'http://localhost:5000/wp-admin/post.php?post=59&action=elementor';
        await page.goto(editorUrl, { waitUntil: 'domcontentloaded' });

        // Tunggu panel aktif
        await page.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 35000 });
        await page.waitForTimeout(6000);

        const editorDocInfo = await page.evaluate(() => {
            const el = window.elementor;
            if (!el) return { ready: false };
            const doc = el.documents ? el.documents.getCurrent() : null;
            return {
                ready: true,
                docId: doc ? doc.id : null,
                elementsCount: el.elements ? el.elements.length : 0
            };
        });

        console.log('  Editor Document Info:', JSON.stringify(editorDocInfo, null, 2));
        if (!editorDocInfo.ready || editorDocInfo.docId !== 59) {
            throw new Error(`Editor tidak membuka document 59! docId=${editorDocInfo.docId}`);
        }

        // Periksa frame
        const frame = page.frameLocator('#elementor-preview-iframe');
        const frameBody = await frame.locator('body').innerHTML();

        const hasStitchHero = frameBody.includes('stitch-sec-hero');
        const hasStitchNavbar = frameBody.includes('stitch-navbar');
        const hasStitchTopbar = frameBody.includes('stitch-topbar');
        const hasMedan = frameBody.includes('Medan');

        console.log('  Pemeriksaan Preview Iframe:');
        console.log('    - Memuat stitch-sec-hero:', hasStitchHero ? 'PASS' : 'FAIL');
        console.log('    - Memuat stitch-navbar:', hasStitchNavbar ? 'PASS' : 'FAIL');
        console.log('    - Memuat stitch-topbar:', hasStitchTopbar ? 'PASS' : 'FAIL');
        console.log('    - Lokasi "Medan" termuat:', hasMedan ? 'PASS' : 'FAIL');

        if (!hasStitchHero || !hasStitchNavbar || !hasStitchTopbar || !hasMedan) {
            throw new Error('Elemen Stitch tidak termuat lengkap di editor preview iframe!');
        }

        // Screenshot Editor Elementor
        await page.screenshot({ path: path.join(OUT, 'editor_elementor.png'), fullPage: false });
        console.log('Saved: editor_elementor.png');

        await browser.close();
        console.log('\nSEMUA PENGECEKAN EDITOR & ADMIN/LOGIN PASS!\n');
    } finally {
        // Hapus temp admin user
        try {
            execSync(`docker exec lpm-wp-app wp user delete ${testAdmin} --yes --allow-root`, { stdio: 'pipe' });
        } catch (e) {}
    }
})();
