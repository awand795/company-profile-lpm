const { chromium } = require('playwright');
const { execSync } = require('child_process');

function authCookies(userId) {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(${userId}, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(${userId}, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 768 } });
    await ctx.addCookies(authCookies(1));
    const p = await ctx.newPage();
    await p.goto('http://localhost:5000/wp-admin/post.php?post=59&action=elementor', { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForSelector('#elementor-editor-wrapper', { timeout: 60000 });
    await p.waitForTimeout(7000);

    const out = await p.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('#elementor-panel-footer button, #elementor-panel-footer [role="button"], #elementor-panel-footer .elementor-button, .elementor-panel-saver__row *'))
            .map(b => ({
                id: b.id,
                cls: (b.className || '').toString().slice(0, 90),
                text: (b.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60),
                aria: b.getAttribute('aria-label'),
            }))
            .filter(b => b.text || b.aria || b.id);
        return btns;
    });
    console.log(JSON.stringify(out, null, 1));
    await browser.close();
})();
