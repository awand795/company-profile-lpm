const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp7b');
fs.mkdirSync(OUT, { recursive: true });

function getAuthCookies() {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({
        name,
        value,
        domain: 'localhost',
        path: '/',
        httpOnly: false,
        secure: false,
        sameSite: 'Lax'
    }));
}

function getRelativeLuminance(rgb) {
    const srgb = rgb.map(val => {
        val /= 255;
        return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2];
}

function getContrastRatio(fgRgb, bgRgb) {
    const l1 = getRelativeLuminance(fgRgb);
    const l2 = getRelativeLuminance(bgRgb);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}

async function main() {
    console.log('=== MEMULAI VERIFIKASI LENGKAP RONDE 16A ===\n');
    const cookies = getAuthCookies();
    const browser = await chromium.launch({ headless: true });

    const consoleErrors = [];

    async function newAdminPage(w, h, url = 'http://localhost:5000/wp-admin/', waitUntil = 'domcontentloaded') {
        const ctx = await browser.newContext({ viewport: { width: w, height: h } });
        await ctx.addCookies(cookies);
        const page = await ctx.newPage();
        page.on('console', msg => {
            if (msg.type() === 'error') {
                const text = msg.text();
                if (!text.includes('favicon') && !text.includes('net::ERR_')) {
                    consoleErrors.push({ url: page.url(), text });
                }
            }
        });
        await page.goto(url, { waitUntil, timeout: 45000 });
        await page.waitForTimeout(1500);
        return { ctx, page };
    }

    // 1. Screenshots SESUDAH
    console.log('--- 1. Pengambilan Screenshot SESUDAH ---');
    {
        const { ctx, page } = await newAdminPage(1366, 640);
        await page.screenshot({ path: path.join(OUT, 'sesudah-dashboard-1366x640.png') });
        console.log('Saved: sesudah-dashboard-1366x640.png');

        // Hover test on inactive item
        const mediaMenu = await page.$('#menu-media');
        if (mediaMenu) {
            await mediaMenu.hover();
            await page.waitForTimeout(500);
            await page.screenshot({ path: path.join(OUT, 'sesudah-sidebar-hover.png') });
            console.log('Saved: sesudah-sidebar-hover.png');
        }
        await ctx.close();
    }

    {
        const { ctx, page } = await newAdminPage(1440, 900);
        await page.screenshot({ path: path.join(OUT, 'sesudah-dashboard-1440x900.png') });
        console.log('Saved: sesudah-dashboard-1440x900.png');
        await ctx.close();
    }

    {
        const { ctx, page } = await newAdminPage(768, 1024);
        await page.screenshot({ path: path.join(OUT, 'sesudah-dashboard-768.png') });
        console.log('Saved: sesudah-dashboard-768.png');
        await ctx.close();
    }

    {
        const { ctx, page } = await newAdminPage(390, 844);
        await page.screenshot({ path: path.join(OUT, 'sesudah-dashboard-390.png') });
        console.log('Saved: sesudah-dashboard-390.png');
        await ctx.close();
    }

    // Admin pages
    for (const [name, url] of [
        ['sesudah-pages.png', 'http://localhost:5000/wp-admin/edit.php?post_type=page'],
        ['sesudah-media.png', 'http://localhost:5000/wp-admin/upload.php'],
        ['sesudah-users.png', 'http://localhost:5000/wp-admin/users.php'],
        ['sesudah-settings.png', 'http://localhost:5000/wp-admin/options-general.php'],
    ]) {
        const { ctx, page } = await newAdminPage(1366, 640, url);
        await page.screenshot({ path: path.join(OUT, name) });
        console.log('Saved:', name);
        await ctx.close();
    }

    // Mode lanjutan screenshot
    console.log('Mengaktifkan Mode Lanjutan sementara...');
    execSync('docker exec lpm-wp-app wp user meta set 1 mt_admin_advanced 1 --allow-root');
    {
        const { ctx, page } = await newAdminPage(1366, 640);
        await page.screenshot({ path: path.join(OUT, 'sesudah-dashboard-advanced.png') });
        console.log('Saved: sesudah-dashboard-advanced.png');
        await ctx.close();
    }
    execSync('docker exec lpm-wp-app wp user meta set 1 mt_admin_advanced 0 --allow-root');
    console.log('Mode Lanjutan dinonaktifkan kembali.');

    // Editor Elementor Page 59 screenshot
    {
        const { ctx, page } = await newAdminPage(1366, 640, 'http://localhost:5000/wp-admin/post.php?post=59&action=elementor');
        try {
            await page.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 35000 });
            await page.waitForTimeout(3000);
            await page.screenshot({ path: path.join(OUT, 'sesudah-editor-page59.png') });
            console.log('Saved: sesudah-editor-page59.png');
        } catch (e) {
            console.log('Editor load warning:', e.message);
        }
        await ctx.close();
    }

    // 2. Evaluasi Dasbor Otomatis
    console.log('\n--- 2. Evaluasi Otomatis Dasbor 1366x640 ---');
    const { ctx, page } = await newAdminPage(1366, 640);

    const audit = await page.evaluate(() => {
        function parseRgb(str) {
            if (!str) return null;
            const m = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
            if (!m) return null;
            return [parseInt(m[1]), parseInt(m[2]), parseInt(m[3]), m[4] !== undefined ? parseFloat(m[4]) : 1];
        }

        function getEffectiveBg(el) {
            let cur = el;
            while (cur && cur !== document.documentElement) {
                const bg = window.getComputedStyle(cur).backgroundColor;
                const parsed = parseRgb(bg);
                if (parsed && parsed[3] > 0.05) {
                    return [parsed[0], parsed[1], parsed[2]];
                }
                cur = cur.parentElement;
            }
            return [248, 250, 252]; // default body bg (#F8FAFC)
        }

        function getLum(rgb) {
            const s = rgb.map(v => {
                v /= 255;
                return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2];
        }

        function contrast(c1, c2) {
            const l1 = getLum(c1);
            const l2 = getLum(c2);
            return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
        }

        // (a) Kontras teks
        const contrastViolations = [];
        const checkedElements = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while ((node = walker.nextNode())) {
            const text = node.textContent.trim();
            if (!text || text.length === 0) continue;
            const el = node.parentElement;
            if (!el) continue;
            const cs = window.getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.1) continue;
            const r = el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0 || r.bottom < 0 || r.top > window.innerHeight) continue;

            const fg = parseRgb(cs.color);
            if (!fg) continue;
            const bg = getEffectiveBg(el);
            const cr = contrast([fg[0], fg[1], fg[2]], bg);
            checkedElements.push({ text: text.substring(0, 30), cr: Math.round(cr * 100) / 100 });
            if (cr < 4.5) {
                contrastViolations.push({
                    text: text.substring(0, 40),
                    tag: el.tagName + (el.id ? '#' + el.id : '') + (el.className ? '.' + el.className.split(' ').join('.') : ''),
                    fg: cs.color,
                    bg: `rgb(${bg.join(',')})`,
                    ratio: Math.round(cr * 100) / 100
                });
            }
        }

        // (b) Sidebar overlaps (bounding box)
        const sidebarItems = Array.from(document.querySelectorAll('#adminmenu > li')).map(li => {
            const r = li.getBoundingClientRect();
            return {
                id: li.id,
                className: li.className,
                text: li.innerText.replace(/\s+/g, ' ').trim(),
                rect: { top: Math.round(r.top), bottom: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right), h: Math.round(r.height) }
            };
        }).filter(it => it.rect.h > 0);

        const sidebarOverlaps = [];
        for (let i = 0; i < sidebarItems.length - 1; i++) {
            const curr = sidebarItems[i];
            const next = sidebarItems[i + 1];
            if (curr.rect.bottom > next.rect.top) {
                sidebarOverlaps.push({
                    curr: curr.id || curr.text,
                    next: next.id || next.text,
                    diff: curr.rect.bottom - next.rect.top
                });
            }
        }

        // (c) Elemen berlatar hitam/sangat gelap di dasbor
        const darkElements = [];
        document.querySelectorAll('#dashboard-widgets *').forEach(el => {
            const cs = window.getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden') return;
            const r = el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) return;
            const bg = parseRgb(cs.backgroundColor);
            if (bg && bg[3] > 0.5) {
                const lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2];
                if (lum < 40) {
                    darkElements.push({
                        el: el.tagName + (el.id ? '#' + el.id : ''),
                        bg: cs.backgroundColor,
                        lum
                    });
                }
            }
        });

        // (d) Kartu sambutan dan aksi cepat in view tanpa scroll
        const welcome = document.querySelector('#mt_admin_welcome');
        const quick = document.querySelector('#mt_admin_quick');
        const status = document.querySelector('#mt_admin_status');
        const inView = (el) => {
            if (!el) return false;
            const r = el.getBoundingClientRect();
            return r.top >= 0 && r.bottom <= window.innerHeight;
        };

        // (g) String Inggris tersisa di Dasbor
        const englishKeywords = [
            'welcome to wordpress',
            'quick draft',
            'wordpress events and news',
            'at a glance',
            'activity',
            'howdy',
            'screen options',
            'help'
        ];
        const pageText = document.body.innerText.toLowerCase();
        const foundEnglish = englishKeywords.filter(kw => pageText.includes(kw));

        return {
            checkedTextCount: checkedElements.length,
            contrastViolations,
            sidebarItemsCount: sidebarItems.length,
            sidebarOverlaps,
            darkElementsCount: darkElements.length,
            darkElements,
            welcomeInView: inView(welcome),
            quickInView: inView(quick),
            statusInView: inView(status),
            welcomeRect: welcome ? welcome.getBoundingClientRect() : null,
            quickRect: quick ? quick.getBoundingClientRect() : null,
            foundEnglish
        };
    });

    await ctx.close();

    console.log(`(a) Total teks diperiksa: ${audit.checkedTextCount}`);
    console.log(`    Pelanggaran kontras (< 4.5:1): ${audit.contrastViolations.length}`);
    if (audit.contrastViolations.length > 0) {
        console.log('    Daftar pelanggar:', JSON.stringify(audit.contrastViolations, null, 2));
    }

    console.log(`(b) Item sidebar diperiksa: ${audit.sidebarItemsCount}`);
    console.log(`    Tumpang tindih sidebar: ${audit.sidebarOverlaps.length}`);
    if (audit.sidebarOverlaps.length > 0) {
        console.log('    Overlap:', JSON.stringify(audit.sidebarOverlaps, null, 2));
    }

    console.log(`(c) Elemen berlatar hitam/sangat gelap di dasbor: ${audit.darkElementsCount}`);
    if (audit.darkElementsCount > 0) {
        console.log('    Daftar elemen gelap:', JSON.stringify(audit.darkElements, null, 2));
    }

    console.log(`(d) Kartu sambutan terlihat tanpa scroll di 1366x640: ${audit.welcomeInView}`);
    console.log(`    Aksi Cepat terlihat tanpa scroll di 1366x640: ${audit.quickInView}`);
    console.log(`    Status Situs terlihat tanpa scroll di 1366x640: ${audit.statusInView}`);

    // (e) PHP warnings di debug.log
    console.log('\n--- (e) Cek PHP warnings di debug.log ---');
    const debugLog = execSync('docker exec lpm-wp-app sh -c "cat /var/www/html/wp-content/debug.log 2>/dev/null || echo NO_LOG"', { encoding: 'utf-8' });
    const phpWarnings = debugLog === 'NO_LOG' ? [] : debugLog.split('\n').filter(line => line.includes('PHP Warning') || line.includes('PHP Notice') || line.includes('PHP Fatal'));
    console.log(`PHP warnings/errors: ${phpWarnings.length}`);

    // (f) Error konsol
    console.log('\n--- (f) Error konsol browser ---');
    console.log(`Error konsol: ${consoleErrors.length}`);
    if (consoleErrors.length > 0) {
        console.log('Daftar error konsol:', JSON.stringify(consoleErrors, null, 2));
    }

    // (g) String Inggris tersisa
    console.log('\n--- (g) String Inggris tersisa di Dasbor ---');
    console.log('String terdeteksi:', JSON.stringify(audit.foundEnglish));

    // 3. Fungsional
    console.log('\n--- 3. Uji Fungsional ---');
    // 3.1 Edit Beranda opens editor Page 59
    console.log('3.1 Edit Beranda link test:');
    const editUrl = execSync('docker exec lpm-wp-app wp eval "echo admin_url(MT_ADMIN_EDITOR_URL);" --allow-root', { encoding: 'utf-8' });
    console.log('  URL Edit Beranda:', editUrl.trim());

    // 3.2 Nonaktifkan mt-admin mengembalikan tampilan bawaan
    console.log('3.2 Nonaktifkan mt-admin...');
    execSync('docker exec lpm-wp-app wp plugin deactivate mt-admin --allow-root');
    const activePluginsAfterDeact = execSync('docker exec lpm-wp-app wp plugin list --status=active --field=name --allow-root', { encoding: 'utf-8' });
    console.log('  Plugin aktif saat dinonaktifkan:', activePluginsAfterDeact.trim().split('\n').join(', '));
    execSync('docker exec lpm-wp-app wp plugin activate mt-admin --allow-root');
    console.log('  mt-admin diaktifkan kembali.');

    await browser.close();
    console.log('\n=== VERIFIKASI SELESAI ===');
}

main().catch(err => {
    console.error('Verifikasi Gagal:', err);
    process.exit(1);
});
