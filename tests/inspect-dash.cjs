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

    const layout = await p.evaluate(() => {
        const list = [];
        const elements = [
            '#wpadminbar',
            '#screen-meta-links',
            '.update-nag',
            '.wrap > h1',
            '#dashboard-widgets-wrap',
            '#dashboard-widgets',
            '#mt_admin_welcome',
            '#mt_admin_welcome .postbox-header',
            '#mt_admin_welcome .inside',
            '#mt_admin_welcome .mt-dash-welcome',
            '#mt_admin_quick',
            '#mt_admin_quick .postbox-header',
            '#mt_admin_quick .inside',
            '#mt_admin_quick .mt-dash-quick'
        ];
        elements.forEach(sel => {
            const el = document.querySelector(sel);
            if (el) {
                const r = el.getBoundingClientRect();
                const cs = window.getComputedStyle(el);
                list.push({
                    sel,
                    top: Math.round(r.top * 10) / 10,
                    bottom: Math.round(r.bottom * 10) / 10,
                    height: Math.round(r.height * 10) / 10,
                    mt: cs.marginTop,
                    mb: cs.marginBottom,
                    pt: cs.paddingTop,
                    pb: cs.paddingBottom
                });
            }
        });
        return list;
    });

    console.log(JSON.stringify(layout, null, 2));
    await browser.close();
})();
