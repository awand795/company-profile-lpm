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
    await p.screenshot({ path: 'playwright_review/sesudah_revamp7b/test-grupC-1366x640.png' });

    const results = await p.evaluate(() => {
        // 1. Admin bar nodes
        const nodes = Array.from(document.querySelectorAll('#wpadminbar ul.ab-top-menu > li')).map(li => ({
            id: li.id,
            text: li.innerText.replace(/\s+/g, ' ').trim(),
            visible: window.getComputedStyle(li).display !== 'none',
            color: window.getComputedStyle(li.querySelector('.ab-item') || li).color
        }));

        // Check if any unwanted nodes exist in DOM
        const wpLogo = document.querySelector('#wp-admin-bar-wp-logo');
        const comments = document.querySelector('#wp-admin-bar-comments');
        const newContent = document.querySelector('#wp-admin-bar-new-content');
        const mtLogo = document.querySelector('#wp-admin-bar-mt-logo');
        const menuToggle = document.querySelector('#wp-admin-bar-menu-toggle');

        // Check screen options and help buttons
        const screenMetaLinks = document.querySelector('#screen-meta-links');
        const h1 = document.querySelector('.wrap > h1');
        const nag = document.querySelector('.update-nag, #update-nag');

        const barRect = document.querySelector('#wpadminbar').getBoundingClientRect();
        const smlRect = screenMetaLinks ? screenMetaLinks.getBoundingClientRect() : null;
        const h1Rect = h1 ? h1.getBoundingClientRect() : null;
        const nagRect = nag ? nag.getBoundingClientRect() : null;

        return {
            adminBarNodes: nodes,
            unwantedInDOM: {
                wpLogo: !!wpLogo,
                comments: !!comments,
                newContent: !!newContent,
                mtLogo: !!mtLogo
            },
            menuToggleDisplay: menuToggle ? window.getComputedStyle(menuToggle).display : null,
            adminBarBottom: barRect.bottom,
            screenMetaTop: smlRect ? smlRect.top : null,
            screenMetaBottom: smlRect ? smlRect.bottom : null,
            distBarToMeta: smlRect ? smlRect.top - barRect.bottom : null,
            h1Top: h1Rect ? h1Rect.top : null,
            distMetaToH1: (smlRect && h1Rect) ? h1Rect.top - smlRect.bottom : null,
            nagTop: nagRect ? nagRect.top : null,
            nagBottom: nagRect ? nagRect.bottom : null,
            distNagToH1: (h1Rect && nagRect) ? h1Rect.top - nagRect.bottom : null
        };
    });

    console.log(JSON.stringify(results, null, 2));
    await browser.close();
})();
