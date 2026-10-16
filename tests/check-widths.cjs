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

    const widths = await p.evaluate(() => {
        const wrap = document.querySelector('#adminmenuwrap');
        const menu = document.querySelector('#adminmenu');
        const back = document.querySelector('#adminmenuback');
        const main = document.querySelector('#adminmenumain');
        const w = document.querySelector('#mt_admin_welcome');
        const q = document.querySelector('#mt_admin_quick');
        const s = document.querySelector('#mt_admin_status');
        const upd = document.querySelector('#wp-admin-bar-updates .ab-label');
        const kbd = document.querySelector('#wp-admin-bar-command-palette kbd');
        return {
            windowH: window.innerHeight,
            w: w ? { top: w.getBoundingClientRect().top, bottom: w.getBoundingClientRect().bottom, height: w.getBoundingClientRect().height } : null,
            q: q ? { top: q.getBoundingClientRect().top, bottom: q.getBoundingClientRect().bottom, height: q.getBoundingClientRect().height } : null,
            s: s ? { top: s.getBoundingClientRect().top, bottom: s.getBoundingClientRect().bottom, height: s.getBoundingClientRect().height } : null,
            updStyle: upd ? { fg: window.getComputedStyle(upd).color, bg: window.getComputedStyle(upd).backgroundColor, parentBg: window.getComputedStyle(upd.parentElement).backgroundColor } : null,
            kbdStyle: kbd ? { fg: window.getComputedStyle(kbd).color, bg: window.getComputedStyle(kbd).backgroundColor, parentBg: window.getComputedStyle(kbd.parentElement).backgroundColor } : null
        };
    });

    console.log(widths);
    await browser.close();
})();
