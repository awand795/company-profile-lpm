const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PHASE = process.argv[2] || 'sesudah';
const OUT = path.join(__dirname, '..', 'playwright_review', `ronde20b_${PHASE}`);
fs.mkdirSync(OUT, { recursive: true });

function getAuthCookies() {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(1, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const errors = [];

    // --- Desktop 1366x640 ---
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 640 } });
    await ctx.addCookies(getAuthCookies());
    const p = await ctx.newPage();
    p.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
    p.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 300)));
    await p.goto('http://localhost:5000/wp-admin/index.php', { waitUntil: 'networkidle' });
    await p.waitForTimeout(1500);

    const desk = await p.evaluate(() => {
        const card = document.getElementById('mt_admin_seo');
        const tips = document.getElementById('mt_admin_seo_tips');
        const rect = card ? card.getBoundingClientRect() : null;
        return {
            hasCard: !!card,
            cardTop: rect ? Math.round(rect.top) : null,
            cardBottom: rect ? Math.round(rect.bottom) : null,
            cardVisibleNoScroll: rect ? rect.top >= 0 && rect.bottom <= window.innerHeight : false,
            viewportH: window.innerHeight,
            scoreText: card ? (card.querySelector('.mt-seo-score-meta') || {}).innerText : null,
            ringLabel: card && card.querySelector('.mt-seo-ring') ? card.querySelector('.mt-seo-ring').getAttribute('aria-label') : null,
            checklist: card ? Array.from(card.querySelectorAll('.mt-seo-item')).map(li => ({
                cls: li.className.replace('mt-seo-item ', ''),
                title: (li.querySelector('strong') || {}).innerText || '',
                state: (li.querySelector('.mt-seo-pill') || {}).innerText || '',
                detail: (li.querySelector('p') || {}).innerText || '',
            })) : [],
            pages: card ? Array.from(card.querySelectorAll('.mt-seo-chip')).map(c => c.innerText.trim()) : [],
            disclaimer: card ? (card.querySelector('.mt-seo-disclaimer') || {}).innerText || '' : '',
            recheckHref: card ? ((Array.from(card.querySelectorAll('a')).find(a => a.innerText.includes('Periksa Ulang')) || {}).href || null) : null,
            editHref: card ? ((Array.from(card.querySelectorAll('a')).find(a => a.innerText.includes('Perbaiki di editor')) || {}).href || null) : null,
            tipsText: tips ? tips.innerText : null,
            hScroll: document.documentElement.scrollWidth > window.innerWidth + 1,
        };
    });
    await p.screenshot({ path: path.join(OUT, 'dasbor-1366.png') });

    // Klik "Periksa Ulang" (uji nonce berfungsi)
    let recheckResult = null;
    if (desk.recheckHref) {
        const p2 = await ctx.newPage();
        const p2err = [];
        p2.on('pageerror', e => p2err.push(String(e).slice(0, 200)));
        const resp = await p2.goto(desk.recheckHref, { waitUntil: 'domcontentloaded' });
        await p2.waitForTimeout(1500);
        recheckResult = {
            status: resp ? resp.status() : null,
            url: p2.url(),
            stillHasCard: !!(await p2.$('#mt_admin_seo')),
            errors: p2err,
        };
        await p2.close();
    }
    await p.close();
    await ctx.close();

    // --- Mobile 390x844 ---
    const mctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    await mctx.addCookies(getAuthCookies());
    const m = await mctx.newPage();
    await m.goto('http://localhost:5000/wp-admin/index.php', { waitUntil: 'networkidle' });
    await m.waitForTimeout(1200);
    const mob = await m.evaluate(() => ({
        hScroll: document.documentElement.scrollWidth > window.innerWidth + 1,
        scrollW: document.documentElement.scrollWidth,
        innerW: window.innerWidth,
        hasCard: !!document.getElementById('mt_admin_seo'),
        checklistCols: (() => {
            const ul = document.querySelector('.mt-seo-list');
            return ul ? getComputedStyle(ul).gridTemplateColumns : null;
        })(),
    }));
    await m.screenshot({ path: path.join(OUT, 'dasbor-390.png') });
    await mctx.close();

    console.log(JSON.stringify({ desk, recheckResult, mob, errors }, null, 1));
    await browser.close();
})();
