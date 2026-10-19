const { chromium } = require('playwright');
const { execSync } = require('child_process');

function getAuthCookies() {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 900 } });
    await ctx.addCookies(getAuthCookies());
    const p = await ctx.newPage();
    await p.goto('http://localhost:5000/wp-admin/index.php', { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(1000);
    const menus = await p.evaluate(() => Array.from(document.querySelectorAll('#adminmenu > li')).map(li => ({
        id: li.id,
        first: (li.querySelector('.wp-menu-name') || {}).innerText || '',
        subs: Array.from(li.querySelectorAll('.wp-submenu a')).map(a => a.innerText.trim() + ' => ' + a.getAttribute('href'))
    })));
    menus.forEach(m => {
        console.log(`${m.id} [${m.first}]`);
        m.subs.forEach(s => console.log(`    ${s}`));
    });
    await browser.close();
})();
