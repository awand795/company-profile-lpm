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
    await p.screenshot({ path: 'playwright_review/sesudah_revamp7b/test-grupA-1366x640.png' });

    const checks = await p.evaluate(() => {
        const welcomePanel = document.querySelector('.welcome-panel, #welcome-panel');
        const welcomePanelVis = welcomePanel ? (window.getComputedStyle(welcomePanel).display !== 'none') : false;

        const w = document.querySelector('#mt_admin_welcome');
        const q = document.querySelector('#mt_admin_quick');
        const s = document.querySelector('#mt_admin_status');

        const inView = (el) => {
            if (!el) return false;
            const r = el.getBoundingClientRect();
            return r.top >= 0 && r.bottom <= window.innerHeight;
        };

        return {
            welcomePanelVis,
            wRect: w ? w.getBoundingClientRect() : null,
            qRect: q ? q.getBoundingClientRect() : null,
            sRect: s ? s.getBoundingClientRect() : null,
            wInView: inView(w),
            qInView: inView(q),
            sInView: inView(s),
            darkElements: Array.from(document.querySelectorAll('#dashboard-widgets *')).filter(el => {
                const bg = window.getComputedStyle(el).backgroundColor;
                if (!bg || bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') return false;
                const m = bg.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
                if (m) {
                    const lum = (0.299 * m[1] + 0.587 * m[2] + 0.114 * m[3]);
                    return lum < 40; // very dark/black
                }
                return false;
            }).map(el => el.tagName + '#' + el.id + '.' + el.className)
        };
    });

    console.log(JSON.stringify(checks, null, 2));
    await browser.close();
})();
