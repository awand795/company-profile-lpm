const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, '..', 'playwright_review', 'sesudah_revamp12b');
fs.mkdirSync(OUT, { recursive: true });

function authCookies(userId) {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(${userId}, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(${userId}, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

(async () => {
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 768 } });
    await ctx.addCookies(authCookies(1));
    const p = await ctx.newPage();
    const errors = [];
    p.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
    p.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 300)));

    await p.goto('http://localhost:5000/wp-admin/post.php?post=59&action=elementor', { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForSelector('#elementor-editor-wrapper', { timeout: 60000 });
    await p.waitForTimeout(6000);

    // Klik tab SEO Rank Math di panel kiri Elementor
    let tabFound = false;
    for (const sel of ['[data-tab="rank-math"]', '.elementor-component-tab[data-tab="rank-math"]']) {
        const el = await p.$(sel);
        if (el) {
            await el.click().catch(() => {});
            tabFound = true;
            break;
        }
    }
    await p.waitForTimeout(4000);

    const info = await p.evaluate(() => {
        const side = document.querySelector('#elementor-panel-inner, .elementor-panel-siderbar, #elementor-panel-content-wrapper');
        const panel = side ? side.innerText.replace(/\n{2,}/g, '\n').slice(0, 2500) : null;
        const scoreCandidates = Array.from(document.querySelectorAll('#elementor-panel *'))
            .filter(el => el.children.length === 0 && /(^|\s)(8[0-9]|9[0-9]|100|7[0-9]|6[0-9]|5[0-9]|4[0-9]|3[0-9]|2[0-9]|1[0-9]|[0-9])\s*%?$/.test((el.innerText || '').trim()))
            .slice(0, 12)
            .map(el => ({ cls: (el.className || '').toString().slice(0, 60), text: (el.innerText || '').trim().slice(0, 40) }));
        const bodyClass = document.body.className;
        const hasRM = !!document.querySelector('[data-tab="rank-math"]');
        const rmPanelText = (() => {
            const nodes = Array.from(document.querySelectorAll('#elementor-panel *')).filter(el => /seo|google|score|skor/i.test(el.innerText || '') && el.children.length <= 3 && el.innerText.length < 400);
            return nodes.slice(0, 6).map(el => ({ cls: (el.className || '').toString().slice(0, 60), text: el.innerText.replace(/\s+/g, ' ').slice(0, 200) }));
        })();
        return { hasRM, panel, scoreCandidates, rmPanelText, bodyClass: bodyClass.slice(0, 200) };
    });

    await p.screenshot({ path: path.join(OUT, 'editor-seo-panel.png') });
    console.log(JSON.stringify({ tabFound, info, errors }, null, 1));
    await browser.close();
})();
