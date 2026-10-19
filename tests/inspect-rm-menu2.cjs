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
    const errors = [];
    p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await p.goto('http://localhost:5000/wp-admin/index.php', { waitUntil: 'networkidle' });
    const out = await p.evaluate(() => {
        const menuIds = Array.from(document.querySelectorAll('#adminmenu > li')).map(li => li.id);
        const rm = document.getElementById('toplevel_page_rank-math') || document.getElementById('menu-rank-math');
        const sub = rm ? Array.from(rm.querySelectorAll('.wp-submenu a')).map(a => ({ t: a.innerText.trim(), h: a.getAttribute('href') })) : null;
        const widgets = Array.from(document.querySelectorAll('.postbox h2, .postbox h3')).map(h => h.innerText.trim());
        return { menuIds, sub, widgets, title: document.title };
    });
    console.log(JSON.stringify({ out, errors }, null, 1));
    await browser.close();
})();
