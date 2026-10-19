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
    await p.goto('http://localhost:5000/wp-admin/index.php', { waitUntil: 'networkidle' });
    await p.waitForTimeout(1000);
    const out = await p.evaluate(() => {
        const grid = document.getElementById('dashboard-widgets');
        const cs = grid ? getComputedStyle(grid) : null;
        const boxes = Array.from(document.querySelectorAll('#dashboard-widgets .postbox')).map(b => {
            const s = getComputedStyle(b);
            const r = b.getBoundingClientRect();
            return { id: b.id || '(no id)', order: s.order, col: s.gridColumnStart + '/' + s.gridColumnEnd, top: Math.round(r.top), h: Math.round(r.height) };
        });
        return {
            gridDisplay: cs ? cs.display : null,
            gridCols: cs ? cs.gridTemplateColumns : null,
            boxes,
            contentTop: document.getElementById('wpbody-content').getBoundingClientRect().top,
            h1: (document.querySelector('#wpbody-content h1') || {}).getBoundingClientRect?.() || null,
            head: Array.from(document.getElementById('wpbody-content').children).slice(0, 8).map(c => {
                const r = c.getBoundingClientRect();
                const s = getComputedStyle(c);
                return { tag: c.tagName, id: c.id, cls: (c.className || '').toString().slice(0, 60), top: Math.round(r.top), h: Math.round(r.height), mt: s.marginTop, mb: s.marginBottom, pt: s.paddingTop };
            }),
            h1style: (() => { const h = document.querySelector('#wpbody-content h1'); if (!h) return null; const s = getComputedStyle(h); const r = h.getBoundingClientRect(); return { mt: s.marginTop, mb: s.marginBottom, pt: s.paddingTop, h: Math.round(r.height), top: Math.round(r.top) }; })(),
            welcomeInside: (() => { const w = document.getElementById('mt_admin_welcome'); if (!w) return null; const i = w.querySelector('.inside'); const s = i ? getComputedStyle(i) : null; return { insideH: i ? Math.round(i.getBoundingClientRect().height) : null, pad: s ? s.padding : null }; })(),
            seoSections: (() => {
                const c = document.getElementById('mt_admin_seo');
                if (!c) return null;
                const h = (sel) => { const e = c.querySelector(sel); if (!e) return null; const r = e.getBoundingClientRect(); return { top: Math.round(r.top), h: Math.round(r.height) }; };
                return {
                    header: h('.postbox-header'),
                    inside: h('.inside'),
                    top: h('.mt-seo-top'),
                    score: h('.mt-seo-score'),
                    meta: h('.mt-seo-score-meta'),
                    note: h('.mt-seo-note'),
                    hint: h('.mt-seo-hint'),
                    actions: h('.mt-seo-actions'),
                    stamp: h('.mt-seo-stamp'),
                    subtitle: h('.mt-seo-subtitle'),
                    list: h('.mt-seo-list'),
                    items: Array.from(c.querySelectorAll('.mt-seo-item')).map(i => Math.round(i.getBoundingClientRect().height)),
                    pages: h('.mt-seo-pages'),
                    disclaimer: h('.mt-seo-disclaimer'),
                };
            })(),
        };
    });
    console.log(JSON.stringify(out, null, 1));
    await browser.close();
})();
