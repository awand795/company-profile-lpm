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
    await p.goto('http://localhost:5000/wp-admin/admin.php?page=rank-math', { waitUntil: 'networkidle' });
    await p.waitForTimeout(2000);

    // Inspect body class + promo box structure
    const info = await p.evaluate(() => {
        const out = {};
        out.bodyClass = document.body.className;
        const cta = document.querySelector('.rank-math-unlock-pro-box');
        out.ctaHtml = cta ? cta.outerHTML.slice(0, 600) : null;
        // find module boxes for ai-visibility, content-ai, link-genius
        const boxes = Array.from(document.querySelectorAll('.rank-math-box, .module, [class*="module"]'));
        out.boxSamples = boxes.slice(0, 8).map(b => ({ cls: b.className, id: b.id, text: (b.innerText || '').slice(0, 40).replace(/\n/g, '|') }));
        // find the specific cards by heading text
        const cards = Array.from(document.querySelectorAll('h3')).map(h => {
            const card = h.closest('div[class]');
            return { title: h.innerText.slice(0, 40).replace(/\n/g, '|'), cardClass: card ? card.className : '', cardId: card ? card.id : '' };
        }).slice(0, 30);
        out.cards = cards;
        // header bar / toolbar
        const header = document.querySelector('#wpadminbar, .rank-math-header, header');
        out.headerText = header ? header.innerText.slice(0, 200).replace(/\n/g, '|') : '';
        return out;
    });
    console.log(JSON.stringify(info, null, 1));
    await browser.close();
})();
