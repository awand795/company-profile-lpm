const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PHASE = process.argv[2] || 'sebelum'; // sebelum | sesudah
const OUT = path.join(__dirname, '..', 'playwright_review', `ronde20b_${PHASE}`);
fs.mkdirSync(OUT, { recursive: true });

const PAGES = [
    { slug: 'dashboard', url: 'http://localhost:5000/wp-admin/admin.php?page=rank-math' },
    { slug: 'judul-meta', url: 'http://localhost:5000/wp-admin/admin.php?page=rank-math-options-titles' },
    { slug: 'sitemap', url: 'http://localhost:5000/wp-admin/admin.php?page=rank-math-options-sitemap' },
    { slug: 'umum', url: 'http://localhost:5000/wp-admin/admin.php?page=rank-math-options-general' },
    { slug: 'dasbor-wp', url: 'http://localhost:5000/wp-admin/index.php' },
];

const PROMO_RE = /BUY NOW|Buy Now|Unlock PRO|Take SEO to the Next Level|Take your SEO to the Next Level|Get Rank Math PRO|Free trial|Free 15-day|GO RANK MATH PRO|Upgrade to PRO|Upgrade Now|Rank Your Content With the Power of PRO/i;

function getAuthCookies() {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 640 } });
    await ctx.addCookies(getAuthCookies());
    const report = {};

    for (const p of PAGES) {
        const page = await ctx.newPage();
        const errors = [];
        page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
        page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 300)));
        try {
            await page.goto(p.url, { waitUntil: 'networkidle', timeout: 60000 });
        } catch (e) {
            errors.push('goto: ' + e.message.slice(0, 200));
        }
        await page.waitForTimeout(2500);

        const info = await page.evaluate((promoSrc) => {
            const promoRe = new RegExp(promoSrc, 'i');
            const promos = [];
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            let n;
            while ((n = walker.nextNode())) {
                const t = (n.nodeValue || '').trim();
                if (t && promoRe.test(t)) {
                    const el = n.parentElement;
                    if (!el) continue;
                    const r = el.getBoundingClientRect();
                    const style = getComputedStyle(el);
                    if (style.display === 'none' || style.visibility === 'hidden' || r.width === 0) continue;
                    let sel = el.tagName.toLowerCase();
                    if (el.id) sel += '#' + el.id;
                    if (el.className && typeof el.className === 'string') sel += '.' + el.className.trim().split(/\s+/).slice(0, 4).join('.');
                    promos.push({ text: t.slice(0, 90), sel, visible: true });
                }
            }
            // visible top-level labels in Rank Math nav/tabs/settings
            const labels = [];
            document.querySelectorAll('.rank-math-ui .tab, nav a, .rank-math-admin-header a, .rank-math-admin-header span, .cmb2-tab, h2, h3, .postbox-header h2, [role="tab"], .components-tabs__tabs-item, .components-tab-panel__tabs button, .rank-math-wrap .components-tab-panel__tab, .rank-math-options .cmb-nav-ul a').forEach(el => {
                const t = (el.innerText || '').trim().replace(/\s+/g, ' ');
                if (t && t.length < 70) labels.push(t);
            });
            const submenu = Array.from(document.querySelectorAll('#toplevel_page_rank-math .wp-submenu a')).map(a => a.innerText.trim());
            return {
                promos,
                labels: Array.from(new Set(labels)),
                submenu,
                hScroll: document.documentElement.scrollWidth > window.innerWidth + 1,
                scrollW: document.documentElement.scrollWidth,
                bodyClass: document.body.className,
                widgets: Array.from(document.querySelectorAll('#dashboard-widgets .postbox')).map(w => w.id).filter(Boolean),
            };
        }, PROMO_RE.source);

        await page.screenshot({ path: path.join(OUT, `${p.slug}.png`), fullPage: false });
        report[p.slug] = { ...info, errors };
        await page.close();
    }

    console.log(JSON.stringify(report, null, 1));
    await browser.close();
})();
