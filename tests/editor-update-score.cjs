const { chromium } = require('playwright');
const { execSync } = require('child_process');

function authCookies(userId) {
    const raw = execSync(`docker exec lpm-wp-app php -r "require '/var/www/html/wp-load.php'; echo json_encode([LOGGED_IN_COOKIE => wp_generate_auth_cookie(${userId}, time()+86400, 'logged_in'), AUTH_COOKIE => wp_generate_auth_cookie(${userId}, time()+86400, 'auth')]);"`, { encoding: 'utf-8' });
    const parsed = JSON.parse(raw.trim());
    return Object.entries(parsed).map(([name, value]) => ({ name, value, domain: 'localhost', path: '/' }));
}

function php(code) {
    return execSync(`docker exec lpm-wp-app php -r ${JSON.stringify(code)}`, { encoding: 'utf-8' }).trim();
}

(async () => {
    const mode = process.argv[2] || 'inspect';
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({ viewport: { width: 1366, height: 768 } });
    await ctx.addCookies(authCookies(1));
    const p = await ctx.newPage();
    const errors = [];
    p.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 250)); });
    p.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 250)));

    await p.goto('http://localhost:5000/wp-admin/post.php?post=59&action=elementor', { waitUntil: 'domcontentloaded', timeout: 90000 });
    await p.waitForSelector('#elementor-editor-wrapper', { timeout: 60000 });
    await p.waitForTimeout(6000);

    const tab = await p.$('[data-tab="rank-math"]');
    if (tab) { await tab.click().catch(() => {}); await p.waitForTimeout(3500); }

    // 1. Cari elemen promo "Upgrade today"
    const promo = await p.evaluate(() => {
        const all = Array.from(document.querySelectorAll('#elementor-panel *'));
        const hit = all.filter(el => /Upgrade today|PRO version/i.test(el.innerText || '') && el.innerText.length < 300);
        return hit.slice(0, 5).map(el => {
            const chain = [];
            let n = el;
            for (let i = 0; i < 4 && n && n !== document.body; i++) {
                chain.push(n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') + (typeof n.className === 'string' && n.className ? '.' + n.className.trim().split(/\s+/).slice(0, 3).join('.') : ''));
                n = n.parentElement;
            }
            return { text: el.innerText.replace(/\s+/g, ' ').slice(0, 160), chain };
        });
    });

    const before = php("require '/var/www/html/wp-load.php'; echo var_export(get_post_meta(59,'rank_math_seo_score',true),true);");

    let updateResult = null;
    if (mode === 'update') {
        // 2. Klik tombol Update/Perbarui Elementor (di mana pun)
        const clicked = await p.evaluate(() => {
            const cands = Array.from(document.querySelectorAll('button, .elementor-button, [role="button"], a'));
            const b = cands.find(x => /^(update|perbarui|save|simpan|terbitkan|publish)$/i.test((x.innerText || '').trim().replace(/\s+/g, ' ')));
            if (!b) return { found: false, samples: cands.map(c => (c.innerText || '').trim()).filter(Boolean).slice(0, 25) };
            b.scrollIntoView && b.scrollIntoView();
            b.click();
            return { found: true, id: b.id, cls: (b.className || '').toString().slice(0, 80), text: b.innerText.trim() };
        });
        await p.waitForTimeout(8000);

        // 3. Simpan skor persis seperti yang dilakukan aplikasi Rank Math (endpoint resmi)
        const scorePost = await p.evaluate(() => {
            const el = document.querySelector('#elementor-panel .score-text');
            const score = el ? parseInt((el.innerText || '').trim(), 10) : NaN;
            if (!el || isNaN(score) || typeof rankMath === 'undefined') {
                return { skipped: true, score: isNaN(score) ? null : score, hasRankMath: typeof rankMath !== 'undefined' };
            }
            return fetch(rankMath.api.root + 'rankmath/v1/updateSeoScore', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-WP-Nonce': rankMath.restNonce },
                body: JSON.stringify({ action: 'rank_math_update_seo_score', postScores: { 59: score } }),
            }).then(r => ({ status: r.status, score })).catch(e => ({ err: String(e).slice(0, 120), score }));
        });
        updateResult = { clicked, scorePost };
    }

    await p.waitForTimeout(2000);
    const after = php("require '/var/www/html/wp-load.php'; echo var_export(get_post_meta(59,'rank_math_seo_score',true),true);");
    const scoreInPanel = await p.evaluate(() => {
        const el = document.querySelector('#elementor-panel .score-text');
        return el ? el.innerText.trim() : null;
    });

    // Promo yang tersisa di panel editor
    const promoEditors = await p.evaluate(() => {
        const re = /Tingkatkan Sekarang|attain 100\/100|Upgrade today|Upgrade Now|Unlock PRO|GO RANK MATH PRO/i;
        const hits = Array.from(document.querySelectorAll('#elementor-panel *')).filter(el => re.test(el.innerText || '') && el.innerText.length < 200 && el.children.length <= 4);
        return hits.slice(0, 8).map(el => {
            const chain = [];
            let n = el;
            for (let i = 0; i < 3 && n && n !== document.body; i++) {
                chain.push(n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') + (typeof n.className === 'string' && n.className ? '.' + n.className.trim().split(/\s+/).slice(0, 3).join('.') : ''));
                n = n.parentElement;
            }
            return { text: el.innerText.replace(/\s+/g, ' ').slice(0, 110), chain };
        });
    });

    console.log(JSON.stringify({ promo, before, after, scoreInPanel, updateResult, promoEditors, errors }, null, 1));
    await browser.close();
})();
