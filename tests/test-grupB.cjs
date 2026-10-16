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
    await p.screenshot({ path: 'playwright_review/sesudah_revamp7b/test-grupB-1366x640.png' });

    const results = await p.evaluate(() => {
        // 1. Check brand header
        const brand = document.querySelector('#mt-sidebar-brand');
        const brandChip = brand ? brand.querySelector('.mt-sidebar-chip') : null;
        const brandName = brand ? brand.querySelector('.mt-brand-name') : null;
        const brandRole = brand ? brand.querySelector('.mt-brand-role') : null;

        // 2. Check floating MASTER TRUCK anywhere in content
        const floatingMT = [];
        document.querySelectorAll('body, #wpbody, #wpcontent, #wpbody-content, #adminmenumain').forEach(el => {
            const before = window.getComputedStyle(el, '::before');
            const after = window.getComputedStyle(el, '::after');
            if (before.content && before.content.includes('MASTER TRUCK')) {
                floatingMT.push({ el: el.tagName + '#' + el.id, pseudo: '::before' });
            }
            if (after.content && after.content.includes('MASTER TRUCK')) {
                floatingMT.push({ el: el.tagName + '#' + el.id, pseudo: '::after' });
            }
        });

        // 3. Check menu items list, text, and bounding boxes
        const items = Array.from(document.querySelectorAll('#adminmenu > li')).map(li => {
            const r = li.getBoundingClientRect();
            return {
                id: li.id,
                className: li.className,
                text: li.innerText.replace(/\s+/g, ' ').trim(),
                rect: { top: Math.round(r.top), bottom: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right), h: Math.round(r.height) }
            };
        }).filter(it => it.rect.h > 0);

        // Check overlaps between consecutive visible items
        const overlaps = [];
        for (let i = 0; i < items.length - 1; i++) {
            const curr = items[i];
            const next = items[i + 1];
            if (curr.rect.bottom > next.rect.top) {
                overlaps.push({
                    curr: curr.id || curr.text,
                    next: next.id || next.text,
                    overlap: curr.rect.bottom - next.rect.top
                });
            }
        }

        // 4. Check active submenu of Dasbor
        const dashSub = document.querySelector('#menu-dashboard .wp-submenu');
        const dashSubStyle = dashSub ? {
            position: window.getComputedStyle(dashSub).position,
            boxShadow: window.getComputedStyle(dashSub).boxShadow,
            border: window.getComputedStyle(dashSub).border,
            subItems: Array.from(dashSub.querySelectorAll('li')).map(li => {
                const a = li.querySelector('a');
                return {
                    text: li.innerText.trim(),
                    isCurrent: li.classList.contains('current'),
                    color: a ? window.getComputedStyle(a).color : null,
                    fontWeight: a ? window.getComputedStyle(a).fontWeight : null,
                    paddingLeft: a ? window.getComputedStyle(a).paddingLeft : null,
                    fontSize: a ? window.getComputedStyle(a).fontSize : null
                };
            })
        } : null;

        // 5. Check separator LANJUTAN
        const sep = document.querySelector('#adminmenu li.mt-sep-lanjutan');
        const sepBefore = sep ? window.getComputedStyle(sep, '::before').content : null;

        return {
            brandFound: !!brand,
            brandNameText: brandName ? brandName.innerText : null,
            brandRoleText: brandRole ? brandRole.innerText : null,
            floatingMT,
            itemsCount: items.length,
            items: items.map(it => `${it.id || it.className}: ${it.text} [y:${it.rect.top}..${it.rect.bottom}]`),
            overlaps,
            dashSubStyle,
            sepBefore
        };
    });

    console.log(JSON.stringify(results, null, 2));
    await browser.close();
})();
