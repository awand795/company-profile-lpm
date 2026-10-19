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

    const consoleErrors = [];
    p.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text().slice(0, 200)); });

    // 1. Dashboard -> submenu Rank Math
    await p.goto('http://localhost:5000/wp-admin/', { waitUntil: 'networkidle' });
    const submenu = await p.evaluate(() => {
        const items = Array.from(document.querySelectorAll('#menu-rank-math .wp-submenu a'));
        return items.map(a => ({ text: a.innerText.trim(), href: a.getAttribute('href') }));
    });
    console.log('=== SUBMENU Pengaturan SEO ===');
    submenu.forEach(s => console.log(`  ${s.text} => ${s.href}`));

    // 2. Modules page
    await p.goto('http://localhost:5000/wp-admin/admin.php?page=rank-math', { waitUntil: 'networkidle' });
    await p.waitForTimeout(1500);
    const bodyText = await p.evaluate(() => document.body.innerText);
    const promos = ['Take SEO to the Next Level', 'Buy Now', 'Unlock PRO', 'AI Link Genius', 'Content AI', 'AI Visibility', 'Free trial', 'Start', 'Upgrade'];
    console.log('\n=== PROMO KEYWORDS DI HALAMAN MODULES ===');
    promos.forEach(k => {
        const count = bodyText.split(k).length - 1;
        if (count > 0) console.log(`  "${k}": ${count}x`);
    });

    // Module cards present
    const cards = await p.evaluate(() => Array.from(document.querySelectorAll('.rank-math-box h3, .module-listing h3')).map(h => h.innerText.trim()).slice(0, 40));
    console.log('\n=== MODULE CARDS (h3) ===');
    console.log(JSON.stringify(cards, null, 1));

    await p.screenshot({ path: 'playwright_review/inspect_rm_modules_before.png', fullPage: false });

    // 3. Titles page English strings audit
    await p.goto('http://localhost:5000/wp-admin/admin.php?page=rank-math-options-titles', { waitUntil: 'networkidle' });
    await p.waitForTimeout(1000);
    const titlesText = await p.evaluate(() => document.body.innerText);
    const englishWords = ['Save Changes', 'Modules', 'Help', 'Setup Wizard', 'Import & Export', 'Advanced', 'Easy Mode', 'Local SEO', 'Social Meta', 'Webmaster Tools', 'Search Console', 'Breadcrumbs', 'Noindex Empty', 'Attachment Pages', 'Strip Category', 'Google', 'Facebook', 'Twitter', 'Pinterest', 'Slack'];
    console.log('\n=== AUDIT STRING INGGRIS DI JUDUL & META ===');
    let total = 0;
    englishWords.forEach(k => {
        const c = titlesText.split(k).length - 1;
        if (c > 0) { console.log(`  "${k}": ${c}x`); total += c; }
    });
    console.log(`  TOTAL: ${total}`);

    console.log('\n=== CONSOLE ERRORS ===', consoleErrors.length, consoleErrors.slice(0, 5));
    await browser.close();
})();
