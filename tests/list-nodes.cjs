const { chromium } = require('playwright');
const { execSync } = require('child_process');

function getAuthCookies() {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 640 } });
    await ctx.addCookies(getAuthCookies());
    const p = await ctx.newPage();
    await p.goto('http://localhost:5000/wp-admin/', { waitUntil: 'networkidle' });

    const nodes = await p.evaluate(() => {
        return Array.from(document.querySelectorAll('#wpadminbar ul.ab-top-menu > li')).map(li => ({
            id: li.id,
            text: li.innerText.replace(/\s+/g, ' ').trim(),
            visible: window.getComputedStyle(li).display !== 'none',
            rect: li.getBoundingClientRect()
        }));
    });

    console.log(JSON.stringify(nodes, null, 2));
    await browser.close();
})();
