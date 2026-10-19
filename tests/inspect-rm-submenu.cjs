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
    const submenu = await p.evaluate(() => {
        const li = document.getElementById('menu-rank-math');
        if (!li) return 'NO MENU';
        return Array.from(li.querySelectorAll('.wp-submenu a')).map(a => ({ text: a.innerText.trim(), href: a.getAttribute('href') }));
    });
    console.log(JSON.stringify(submenu, null, 1));
    await browser.close();
})();
