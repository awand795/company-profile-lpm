const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp7b');
fs.mkdirSync(OUT, { recursive: true });

function getAuthCookies() {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    const cookies = [];
    for (const [name, value] of Object.entries(parsed)) {
        cookies.push({
            name,
            value,
            domain: 'localhost',
            path: '/',
            httpOnly: false,
            secure: false,
            sameSite: 'Lax'
        });
    }
    return cookies;
}

async function main() {
    const cookies = getAuthCookies();
    const browser = await chromium.launch({ headless: true });

    async function capture(name, url, w, h, actions = null) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h } });
        await ctx.addCookies(cookies);
        const page = await ctx.newPage();
        await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
        await page.waitForTimeout(1000);
        if (actions) {
            await actions(page);
        }
        await page.screenshot({ path: path.join(OUT, name), fullPage: false });
        console.log('Saved:', name);
        await ctx.close();
    }

    // SEBELUM Screenshots
    await capture('sebelum-dashboard-1366x640.png', 'http://localhost:5000/wp-admin/', 1366, 640);
    await capture('sebelum-dashboard-1440x900.png', 'http://localhost:5000/wp-admin/', 1440, 900);
    await capture('sebelum-dashboard-768.png', 'http://localhost:5000/wp-admin/', 768, 1024);
    await capture('sebelum-dashboard-390.png', 'http://localhost:5000/wp-admin/', 390, 844);

    await capture('sebelum-pages.png', 'http://localhost:5000/wp-admin/edit.php?post_type=page', 1366, 640);
    await capture('sebelum-media.png', 'http://localhost:5000/wp-admin/upload.php', 1366, 640);
    await capture('sebelum-users.png', 'http://localhost:5000/wp-admin/users.php', 1366, 640);
    await capture('sebelum-settings.png', 'http://localhost:5000/wp-admin/options-general.php', 1366, 640);

    // Sidebar hover on inactive item (e.g. Media or Pengaturan)
    await capture('sebelum-sidebar-hover.png', 'http://localhost:5000/wp-admin/', 1366, 640, async (page) => {
        const item = await page.$('#menu-media');
        if (item) {
            await item.hover();
            await page.waitForTimeout(500);
        }
    });

    // Editor Elementor Page 59
    await capture('sebelum-editor-page59.png', 'http://localhost:5000/wp-admin/post.php?post=59&action=elementor', 1366, 640, async (page) => {
        try {
            await page.waitForSelector('#elementor-panel, .elementor-panel', { timeout: 25000 });
            await page.waitForTimeout(3000);
        } catch (e) {
            console.log('editor wait timeout', e.message);
        }
    });

    await browser.close();
    console.log('SEBELUM captures complete.');
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
