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
    await p.screenshot({ path: 'playwright_review/sesudah_revamp7b/sebelum-dashboard-expanded.png' });

    const info = await p.evaluate(() => {
        const bodyClass = document.body.className;
        // Check "o." in admin bar
        const adminBarNodes = Array.from(document.querySelectorAll('#wpadminbar *')).map(el => ({
            tag: el.tagName,
            id: el.id,
            className: typeof el.className === 'string' ? el.className : (el.className && el.className.baseVal ? el.className.baseVal : ''),
            text: el.innerText ? el.innerText.trim() : '',
            rect: el.getBoundingClientRect()
        })).filter(x => x.text.includes('o') || x.text.includes('·') || x.id.includes('menu-toggle') || (typeof x.className === 'string' && x.className.includes('menu-toggle')));

        // Check MASTER TRUCK floating text
        const floatingMT = [];
        document.querySelectorAll('*').forEach(el => {
            const before = window.getComputedStyle(el, '::before');
            const after = window.getComputedStyle(el, '::after');
            if (before.content && before.content.includes('MASTER TRUCK')) {
                const r = el.getBoundingClientRect();
                floatingMT.push({ el: el.tagName + '#' + el.id + '.' + el.className, pseudo: '::before', rect: r });
            }
            if (after.content && after.content.includes('MASTER TRUCK')) {
                const r = el.getBoundingClientRect();
                floatingMT.push({ el: el.tagName + '#' + el.id + '.' + el.className, pseudo: '::after', rect: r });
            }
        });

        // Check submenu of Dasbor
        const dashSubmenu = document.querySelector('#menu-dashboard .wp-submenu');
        const dashSubStyle = dashSubmenu ? {
            position: window.getComputedStyle(dashSubmenu).position,
            boxShadow: window.getComputedStyle(dashSubmenu).boxShadow,
            rect: dashSubmenu.getBoundingClientRect()
        } : null;

        // Check menu items in sidebar
        const menuItems = Array.from(document.querySelectorAll('#adminmenu > li')).map(li => ({
            id: li.id,
            text: li.innerText.replace(/\s+/g, ' ').trim(),
            rect: li.getBoundingClientRect()
        }));

        // Check screen options and help buttons
        const screenOptions = document.querySelector('#screen-options-link-wrap');
        const help = document.querySelector('#contextual-help-link-wrap');

        return {
            bodyClass,
            floatingMT,
            adminBarNodes: adminBarNodes.slice(0, 10),
            dashSubStyle,
            menuItems,
            screenOptions: screenOptions ? screenOptions.getBoundingClientRect() : null,
            help: help ? help.getBoundingClientRect() : null
        };
    });

    console.log(JSON.stringify(info, null, 2));
    await browser.close();
})();
